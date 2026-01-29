r'''
# `aws_sns_platform_application`

Refer to the Terraform Registry for docs: [`aws_sns_platform_application`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application).
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


class SnsPlatformApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.snsPlatformApplication.SnsPlatformApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application aws_sns_platform_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        platform: builtins.str,
        platform_credential: builtins.str,
        apple_platform_bundle_id: typing.Optional[builtins.str] = None,
        apple_platform_team_id: typing.Optional[builtins.str] = None,
        event_delivery_failure_topic_arn: typing.Optional[builtins.str] = None,
        event_endpoint_created_topic_arn: typing.Optional[builtins.str] = None,
        event_endpoint_deleted_topic_arn: typing.Optional[builtins.str] = None,
        event_endpoint_updated_topic_arn: typing.Optional[builtins.str] = None,
        failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        platform_principal: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        success_feedback_role_arn: typing.Optional[builtins.str] = None,
        success_feedback_sample_rate: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application aws_sns_platform_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#name SnsPlatformApplication#name}.
        :param platform: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#platform SnsPlatformApplication#platform}.
        :param platform_credential: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#platform_credential SnsPlatformApplication#platform_credential}.
        :param apple_platform_bundle_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#apple_platform_bundle_id SnsPlatformApplication#apple_platform_bundle_id}.
        :param apple_platform_team_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#apple_platform_team_id SnsPlatformApplication#apple_platform_team_id}.
        :param event_delivery_failure_topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_delivery_failure_topic_arn SnsPlatformApplication#event_delivery_failure_topic_arn}.
        :param event_endpoint_created_topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_endpoint_created_topic_arn SnsPlatformApplication#event_endpoint_created_topic_arn}.
        :param event_endpoint_deleted_topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_endpoint_deleted_topic_arn SnsPlatformApplication#event_endpoint_deleted_topic_arn}.
        :param event_endpoint_updated_topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_endpoint_updated_topic_arn SnsPlatformApplication#event_endpoint_updated_topic_arn}.
        :param failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#failure_feedback_role_arn SnsPlatformApplication#failure_feedback_role_arn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#id SnsPlatformApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param platform_principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#platform_principal SnsPlatformApplication#platform_principal}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#region SnsPlatformApplication#region}
        :param success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#success_feedback_role_arn SnsPlatformApplication#success_feedback_role_arn}.
        :param success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#success_feedback_sample_rate SnsPlatformApplication#success_feedback_sample_rate}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9bf9d1b2bd82d4d30ab7ef75c72cc6e04d3cbe0e124f8d99d8f145e2304b27)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SnsPlatformApplicationConfig(
            name=name,
            platform=platform,
            platform_credential=platform_credential,
            apple_platform_bundle_id=apple_platform_bundle_id,
            apple_platform_team_id=apple_platform_team_id,
            event_delivery_failure_topic_arn=event_delivery_failure_topic_arn,
            event_endpoint_created_topic_arn=event_endpoint_created_topic_arn,
            event_endpoint_deleted_topic_arn=event_endpoint_deleted_topic_arn,
            event_endpoint_updated_topic_arn=event_endpoint_updated_topic_arn,
            failure_feedback_role_arn=failure_feedback_role_arn,
            id=id,
            platform_principal=platform_principal,
            region=region,
            success_feedback_role_arn=success_feedback_role_arn,
            success_feedback_sample_rate=success_feedback_sample_rate,
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
        '''Generates CDKTF code for importing a SnsPlatformApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SnsPlatformApplication to import.
        :param import_from_id: The id of the existing SnsPlatformApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SnsPlatformApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a920861a50ac9a20a524a57bd8d942837ad4bd16c26c71a00d70f05be898df)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetApplePlatformBundleId")
    def reset_apple_platform_bundle_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplePlatformBundleId", []))

    @jsii.member(jsii_name="resetApplePlatformTeamId")
    def reset_apple_platform_team_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplePlatformTeamId", []))

    @jsii.member(jsii_name="resetEventDeliveryFailureTopicArn")
    def reset_event_delivery_failure_topic_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventDeliveryFailureTopicArn", []))

    @jsii.member(jsii_name="resetEventEndpointCreatedTopicArn")
    def reset_event_endpoint_created_topic_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventEndpointCreatedTopicArn", []))

    @jsii.member(jsii_name="resetEventEndpointDeletedTopicArn")
    def reset_event_endpoint_deleted_topic_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventEndpointDeletedTopicArn", []))

    @jsii.member(jsii_name="resetEventEndpointUpdatedTopicArn")
    def reset_event_endpoint_updated_topic_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventEndpointUpdatedTopicArn", []))

    @jsii.member(jsii_name="resetFailureFeedbackRoleArn")
    def reset_failure_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPlatformPrincipal")
    def reset_platform_principal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformPrincipal", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSuccessFeedbackRoleArn")
    def reset_success_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetSuccessFeedbackSampleRate")
    def reset_success_feedback_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessFeedbackSampleRate", []))

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
    @jsii.member(jsii_name="applePlatformBundleIdInput")
    def apple_platform_bundle_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applePlatformBundleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="applePlatformTeamIdInput")
    def apple_platform_team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applePlatformTeamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eventDeliveryFailureTopicArnInput")
    def event_delivery_failure_topic_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventDeliveryFailureTopicArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventEndpointCreatedTopicArnInput")
    def event_endpoint_created_topic_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventEndpointCreatedTopicArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventEndpointDeletedTopicArnInput")
    def event_endpoint_deleted_topic_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventEndpointDeletedTopicArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventEndpointUpdatedTopicArnInput")
    def event_endpoint_updated_topic_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventEndpointUpdatedTopicArnInput"))

    @builtins.property
    @jsii.member(jsii_name="failureFeedbackRoleArnInput")
    def failure_feedback_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failureFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="platformCredentialInput")
    def platform_credential_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="platformPrincipalInput")
    def platform_principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformPrincipalInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="successFeedbackRoleArnInput")
    def success_feedback_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="successFeedbackSampleRateInput")
    def success_feedback_sample_rate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successFeedbackSampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="applePlatformBundleId")
    def apple_platform_bundle_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applePlatformBundleId"))

    @apple_platform_bundle_id.setter
    def apple_platform_bundle_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e64da65bdf8a2d9349b8a01bba9749badf8965bf717a1a6a52756f2501abd08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applePlatformBundleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applePlatformTeamId")
    def apple_platform_team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applePlatformTeamId"))

    @apple_platform_team_id.setter
    def apple_platform_team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42eb4bda50f30c6556f710da608328e4a573c5342c64905118b4111dda4f8ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applePlatformTeamId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventDeliveryFailureTopicArn")
    def event_delivery_failure_topic_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventDeliveryFailureTopicArn"))

    @event_delivery_failure_topic_arn.setter
    def event_delivery_failure_topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf0b5ef3e62a266aa20edacb9867dfe7a4055dcbe216eaeb5970fcd5360e86d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventDeliveryFailureTopicArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventEndpointCreatedTopicArn")
    def event_endpoint_created_topic_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventEndpointCreatedTopicArn"))

    @event_endpoint_created_topic_arn.setter
    def event_endpoint_created_topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b53325831894a899c305c660b02b4a0fdab85a5a9949da5e40f27176476bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventEndpointCreatedTopicArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventEndpointDeletedTopicArn")
    def event_endpoint_deleted_topic_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventEndpointDeletedTopicArn"))

    @event_endpoint_deleted_topic_arn.setter
    def event_endpoint_deleted_topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04974972e012629d3262e745e9b87f356345f6d67d6cf4fe34d0c5f9e5002f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventEndpointDeletedTopicArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventEndpointUpdatedTopicArn")
    def event_endpoint_updated_topic_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventEndpointUpdatedTopicArn"))

    @event_endpoint_updated_topic_arn.setter
    def event_endpoint_updated_topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f7fe40155c3fe9c164e117a5e1c69152792aa77b7ecc980a471a0dca9b171a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventEndpointUpdatedTopicArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureFeedbackRoleArn")
    def failure_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failureFeedbackRoleArn"))

    @failure_feedback_role_arn.setter
    def failure_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a839683592769817f68e22f14453889e0727c574486ba88e284fa03fa78a8ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389b75eca8cdfbb83042b36ab5cedcc7a8e8f8e8b867ca478fe93384590e4f9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97041e9b0a626cab43c506dee95ab267ede467c098e765c11df7e76c9edd6d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ade2e318981cdfde695cf6b83c458e8ff89c7215472bc122500e919a64e6a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platformCredential")
    def platform_credential(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformCredential"))

    @platform_credential.setter
    def platform_credential(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17a9c3c38c617677329b5d8c8665906d17cf58e0c064a117ab610b002029d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformCredential", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platformPrincipal")
    def platform_principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformPrincipal"))

    @platform_principal.setter
    def platform_principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b0f3ea69f4b40256c31d43c6e5cae0d957e8d7d29e3383f5bd3750572f115c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformPrincipal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383fc0cdc86a2017cf8e0adf2abbe2e5fea6c798921f78da921e1afb25009f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successFeedbackRoleArn")
    def success_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "successFeedbackRoleArn"))

    @success_feedback_role_arn.setter
    def success_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4176c563f2e14caf897e5a2a568e8235ef6109f8b61d0a4a4c82b97f8f76743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successFeedbackSampleRate")
    def success_feedback_sample_rate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "successFeedbackSampleRate"))

    @success_feedback_sample_rate.setter
    def success_feedback_sample_rate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7e97548687b05af03fcd6722e603d4d0cd15bbf376afdde30b8a30fbb8b9b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successFeedbackSampleRate", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.snsPlatformApplication.SnsPlatformApplicationConfig",
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
        "platform": "platform",
        "platform_credential": "platformCredential",
        "apple_platform_bundle_id": "applePlatformBundleId",
        "apple_platform_team_id": "applePlatformTeamId",
        "event_delivery_failure_topic_arn": "eventDeliveryFailureTopicArn",
        "event_endpoint_created_topic_arn": "eventEndpointCreatedTopicArn",
        "event_endpoint_deleted_topic_arn": "eventEndpointDeletedTopicArn",
        "event_endpoint_updated_topic_arn": "eventEndpointUpdatedTopicArn",
        "failure_feedback_role_arn": "failureFeedbackRoleArn",
        "id": "id",
        "platform_principal": "platformPrincipal",
        "region": "region",
        "success_feedback_role_arn": "successFeedbackRoleArn",
        "success_feedback_sample_rate": "successFeedbackSampleRate",
    },
)
class SnsPlatformApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        platform: builtins.str,
        platform_credential: builtins.str,
        apple_platform_bundle_id: typing.Optional[builtins.str] = None,
        apple_platform_team_id: typing.Optional[builtins.str] = None,
        event_delivery_failure_topic_arn: typing.Optional[builtins.str] = None,
        event_endpoint_created_topic_arn: typing.Optional[builtins.str] = None,
        event_endpoint_deleted_topic_arn: typing.Optional[builtins.str] = None,
        event_endpoint_updated_topic_arn: typing.Optional[builtins.str] = None,
        failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        platform_principal: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        success_feedback_role_arn: typing.Optional[builtins.str] = None,
        success_feedback_sample_rate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#name SnsPlatformApplication#name}.
        :param platform: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#platform SnsPlatformApplication#platform}.
        :param platform_credential: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#platform_credential SnsPlatformApplication#platform_credential}.
        :param apple_platform_bundle_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#apple_platform_bundle_id SnsPlatformApplication#apple_platform_bundle_id}.
        :param apple_platform_team_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#apple_platform_team_id SnsPlatformApplication#apple_platform_team_id}.
        :param event_delivery_failure_topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_delivery_failure_topic_arn SnsPlatformApplication#event_delivery_failure_topic_arn}.
        :param event_endpoint_created_topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_endpoint_created_topic_arn SnsPlatformApplication#event_endpoint_created_topic_arn}.
        :param event_endpoint_deleted_topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_endpoint_deleted_topic_arn SnsPlatformApplication#event_endpoint_deleted_topic_arn}.
        :param event_endpoint_updated_topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_endpoint_updated_topic_arn SnsPlatformApplication#event_endpoint_updated_topic_arn}.
        :param failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#failure_feedback_role_arn SnsPlatformApplication#failure_feedback_role_arn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#id SnsPlatformApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param platform_principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#platform_principal SnsPlatformApplication#platform_principal}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#region SnsPlatformApplication#region}
        :param success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#success_feedback_role_arn SnsPlatformApplication#success_feedback_role_arn}.
        :param success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#success_feedback_sample_rate SnsPlatformApplication#success_feedback_sample_rate}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca30996fecfee4355e3df7fa6430e96ec4d378abd3638814cd883e2d0f09a714)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument platform_credential", value=platform_credential, expected_type=type_hints["platform_credential"])
            check_type(argname="argument apple_platform_bundle_id", value=apple_platform_bundle_id, expected_type=type_hints["apple_platform_bundle_id"])
            check_type(argname="argument apple_platform_team_id", value=apple_platform_team_id, expected_type=type_hints["apple_platform_team_id"])
            check_type(argname="argument event_delivery_failure_topic_arn", value=event_delivery_failure_topic_arn, expected_type=type_hints["event_delivery_failure_topic_arn"])
            check_type(argname="argument event_endpoint_created_topic_arn", value=event_endpoint_created_topic_arn, expected_type=type_hints["event_endpoint_created_topic_arn"])
            check_type(argname="argument event_endpoint_deleted_topic_arn", value=event_endpoint_deleted_topic_arn, expected_type=type_hints["event_endpoint_deleted_topic_arn"])
            check_type(argname="argument event_endpoint_updated_topic_arn", value=event_endpoint_updated_topic_arn, expected_type=type_hints["event_endpoint_updated_topic_arn"])
            check_type(argname="argument failure_feedback_role_arn", value=failure_feedback_role_arn, expected_type=type_hints["failure_feedback_role_arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument platform_principal", value=platform_principal, expected_type=type_hints["platform_principal"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument success_feedback_role_arn", value=success_feedback_role_arn, expected_type=type_hints["success_feedback_role_arn"])
            check_type(argname="argument success_feedback_sample_rate", value=success_feedback_sample_rate, expected_type=type_hints["success_feedback_sample_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "platform": platform,
            "platform_credential": platform_credential,
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
        if apple_platform_bundle_id is not None:
            self._values["apple_platform_bundle_id"] = apple_platform_bundle_id
        if apple_platform_team_id is not None:
            self._values["apple_platform_team_id"] = apple_platform_team_id
        if event_delivery_failure_topic_arn is not None:
            self._values["event_delivery_failure_topic_arn"] = event_delivery_failure_topic_arn
        if event_endpoint_created_topic_arn is not None:
            self._values["event_endpoint_created_topic_arn"] = event_endpoint_created_topic_arn
        if event_endpoint_deleted_topic_arn is not None:
            self._values["event_endpoint_deleted_topic_arn"] = event_endpoint_deleted_topic_arn
        if event_endpoint_updated_topic_arn is not None:
            self._values["event_endpoint_updated_topic_arn"] = event_endpoint_updated_topic_arn
        if failure_feedback_role_arn is not None:
            self._values["failure_feedback_role_arn"] = failure_feedback_role_arn
        if id is not None:
            self._values["id"] = id
        if platform_principal is not None:
            self._values["platform_principal"] = platform_principal
        if region is not None:
            self._values["region"] = region
        if success_feedback_role_arn is not None:
            self._values["success_feedback_role_arn"] = success_feedback_role_arn
        if success_feedback_sample_rate is not None:
            self._values["success_feedback_sample_rate"] = success_feedback_sample_rate

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#name SnsPlatformApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platform(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#platform SnsPlatformApplication#platform}.'''
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platform_credential(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#platform_credential SnsPlatformApplication#platform_credential}.'''
        result = self._values.get("platform_credential")
        assert result is not None, "Required property 'platform_credential' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def apple_platform_bundle_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#apple_platform_bundle_id SnsPlatformApplication#apple_platform_bundle_id}.'''
        result = self._values.get("apple_platform_bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apple_platform_team_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#apple_platform_team_id SnsPlatformApplication#apple_platform_team_id}.'''
        result = self._values.get("apple_platform_team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_delivery_failure_topic_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_delivery_failure_topic_arn SnsPlatformApplication#event_delivery_failure_topic_arn}.'''
        result = self._values.get("event_delivery_failure_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_endpoint_created_topic_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_endpoint_created_topic_arn SnsPlatformApplication#event_endpoint_created_topic_arn}.'''
        result = self._values.get("event_endpoint_created_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_endpoint_deleted_topic_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_endpoint_deleted_topic_arn SnsPlatformApplication#event_endpoint_deleted_topic_arn}.'''
        result = self._values.get("event_endpoint_deleted_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_endpoint_updated_topic_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#event_endpoint_updated_topic_arn SnsPlatformApplication#event_endpoint_updated_topic_arn}.'''
        result = self._values.get("event_endpoint_updated_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#failure_feedback_role_arn SnsPlatformApplication#failure_feedback_role_arn}.'''
        result = self._values.get("failure_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#id SnsPlatformApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform_principal(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#platform_principal SnsPlatformApplication#platform_principal}.'''
        result = self._values.get("platform_principal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#region SnsPlatformApplication#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#success_feedback_role_arn SnsPlatformApplication#success_feedback_role_arn}.'''
        result = self._values.get("success_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_feedback_sample_rate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sns_platform_application#success_feedback_sample_rate SnsPlatformApplication#success_feedback_sample_rate}.'''
        result = self._values.get("success_feedback_sample_rate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsPlatformApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SnsPlatformApplication",
    "SnsPlatformApplicationConfig",
]

publication.publish()

def _typecheckingstub__ff9bf9d1b2bd82d4d30ab7ef75c72cc6e04d3cbe0e124f8d99d8f145e2304b27(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    platform: builtins.str,
    platform_credential: builtins.str,
    apple_platform_bundle_id: typing.Optional[builtins.str] = None,
    apple_platform_team_id: typing.Optional[builtins.str] = None,
    event_delivery_failure_topic_arn: typing.Optional[builtins.str] = None,
    event_endpoint_created_topic_arn: typing.Optional[builtins.str] = None,
    event_endpoint_deleted_topic_arn: typing.Optional[builtins.str] = None,
    event_endpoint_updated_topic_arn: typing.Optional[builtins.str] = None,
    failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    platform_principal: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    success_feedback_role_arn: typing.Optional[builtins.str] = None,
    success_feedback_sample_rate: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a8a920861a50ac9a20a524a57bd8d942837ad4bd16c26c71a00d70f05be898df(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e64da65bdf8a2d9349b8a01bba9749badf8965bf717a1a6a52756f2501abd08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42eb4bda50f30c6556f710da608328e4a573c5342c64905118b4111dda4f8ef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf0b5ef3e62a266aa20edacb9867dfe7a4055dcbe216eaeb5970fcd5360e86d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b53325831894a899c305c660b02b4a0fdab85a5a9949da5e40f27176476bd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04974972e012629d3262e745e9b87f356345f6d67d6cf4fe34d0c5f9e5002f8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f7fe40155c3fe9c164e117a5e1c69152792aa77b7ecc980a471a0dca9b171a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a839683592769817f68e22f14453889e0727c574486ba88e284fa03fa78a8ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389b75eca8cdfbb83042b36ab5cedcc7a8e8f8e8b867ca478fe93384590e4f9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97041e9b0a626cab43c506dee95ab267ede467c098e765c11df7e76c9edd6d18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ade2e318981cdfde695cf6b83c458e8ff89c7215472bc122500e919a64e6a4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17a9c3c38c617677329b5d8c8665906d17cf58e0c064a117ab610b002029d41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b0f3ea69f4b40256c31d43c6e5cae0d957e8d7d29e3383f5bd3750572f115c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383fc0cdc86a2017cf8e0adf2abbe2e5fea6c798921f78da921e1afb25009f50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4176c563f2e14caf897e5a2a568e8235ef6109f8b61d0a4a4c82b97f8f76743(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e97548687b05af03fcd6722e603d4d0cd15bbf376afdde30b8a30fbb8b9b5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca30996fecfee4355e3df7fa6430e96ec4d378abd3638814cd883e2d0f09a714(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    platform: builtins.str,
    platform_credential: builtins.str,
    apple_platform_bundle_id: typing.Optional[builtins.str] = None,
    apple_platform_team_id: typing.Optional[builtins.str] = None,
    event_delivery_failure_topic_arn: typing.Optional[builtins.str] = None,
    event_endpoint_created_topic_arn: typing.Optional[builtins.str] = None,
    event_endpoint_deleted_topic_arn: typing.Optional[builtins.str] = None,
    event_endpoint_updated_topic_arn: typing.Optional[builtins.str] = None,
    failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    platform_principal: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    success_feedback_role_arn: typing.Optional[builtins.str] = None,
    success_feedback_sample_rate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
