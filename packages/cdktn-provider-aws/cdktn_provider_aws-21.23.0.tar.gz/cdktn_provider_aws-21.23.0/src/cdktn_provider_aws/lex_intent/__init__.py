r'''
# `aws_lex_intent`

Refer to the Terraform Registry for docs: [`aws_lex_intent`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent).
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


class LexIntent(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntent",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent aws_lex_intent}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        fulfillment_activity: typing.Union["LexIntentFulfillmentActivity", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        conclusion_statement: typing.Optional[typing.Union["LexIntentConclusionStatement", typing.Dict[builtins.str, typing.Any]]] = None,
        confirmation_prompt: typing.Optional[typing.Union["LexIntentConfirmationPrompt", typing.Dict[builtins.str, typing.Any]]] = None,
        create_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        dialog_code_hook: typing.Optional[typing.Union["LexIntentDialogCodeHook", typing.Dict[builtins.str, typing.Any]]] = None,
        follow_up_prompt: typing.Optional[typing.Union["LexIntentFollowUpPrompt", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        parent_intent_signature: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rejection_statement: typing.Optional[typing.Union["LexIntentRejectionStatement", typing.Dict[builtins.str, typing.Any]]] = None,
        sample_utterances: typing.Optional[typing.Sequence[builtins.str]] = None,
        slot: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentSlot", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["LexIntentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent aws_lex_intent} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param fulfillment_activity: fulfillment_activity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#fulfillment_activity LexIntent#fulfillment_activity}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#name LexIntent#name}.
        :param conclusion_statement: conclusion_statement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#conclusion_statement LexIntent#conclusion_statement}
        :param confirmation_prompt: confirmation_prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#confirmation_prompt LexIntent#confirmation_prompt}
        :param create_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#create_version LexIntent#create_version}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#description LexIntent#description}.
        :param dialog_code_hook: dialog_code_hook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#dialog_code_hook LexIntent#dialog_code_hook}
        :param follow_up_prompt: follow_up_prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#follow_up_prompt LexIntent#follow_up_prompt}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#id LexIntent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parent_intent_signature: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#parent_intent_signature LexIntent#parent_intent_signature}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#region LexIntent#region}
        :param rejection_statement: rejection_statement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#rejection_statement LexIntent#rejection_statement}
        :param sample_utterances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#sample_utterances LexIntent#sample_utterances}.
        :param slot: slot block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#slot LexIntent#slot}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#timeouts LexIntent#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2144e0e09490de9a676ffc57b21e43232707acb66154ced92eacd3f20f0237)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LexIntentConfig(
            fulfillment_activity=fulfillment_activity,
            name=name,
            conclusion_statement=conclusion_statement,
            confirmation_prompt=confirmation_prompt,
            create_version=create_version,
            description=description,
            dialog_code_hook=dialog_code_hook,
            follow_up_prompt=follow_up_prompt,
            id=id,
            parent_intent_signature=parent_intent_signature,
            region=region,
            rejection_statement=rejection_statement,
            sample_utterances=sample_utterances,
            slot=slot,
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
        '''Generates CDKTF code for importing a LexIntent resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LexIntent to import.
        :param import_from_id: The id of the existing LexIntent that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LexIntent to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63bb3ceb111cff1eb709151e522f76f3947f3dfbc02ca57103d20860b24f5fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConclusionStatement")
    def put_conclusion_statement(
        self,
        *,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentConclusionStatementMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        value = LexIntentConclusionStatement(
            message=message, response_card=response_card
        )

        return typing.cast(None, jsii.invoke(self, "putConclusionStatement", [value]))

    @jsii.member(jsii_name="putConfirmationPrompt")
    def put_confirmation_prompt(
        self,
        *,
        max_attempts: jsii.Number,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentConfirmationPromptMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#max_attempts LexIntent#max_attempts}.
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        value = LexIntentConfirmationPrompt(
            max_attempts=max_attempts, message=message, response_card=response_card
        )

        return typing.cast(None, jsii.invoke(self, "putConfirmationPrompt", [value]))

    @jsii.member(jsii_name="putDialogCodeHook")
    def put_dialog_code_hook(
        self,
        *,
        message_version: builtins.str,
        uri: builtins.str,
    ) -> None:
        '''
        :param message_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message_version LexIntent#message_version}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#uri LexIntent#uri}.
        '''
        value = LexIntentDialogCodeHook(message_version=message_version, uri=uri)

        return typing.cast(None, jsii.invoke(self, "putDialogCodeHook", [value]))

    @jsii.member(jsii_name="putFollowUpPrompt")
    def put_follow_up_prompt(
        self,
        *,
        prompt: typing.Union["LexIntentFollowUpPromptPrompt", typing.Dict[builtins.str, typing.Any]],
        rejection_statement: typing.Union["LexIntentFollowUpPromptRejectionStatement", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param prompt: prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#prompt LexIntent#prompt}
        :param rejection_statement: rejection_statement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#rejection_statement LexIntent#rejection_statement}
        '''
        value = LexIntentFollowUpPrompt(
            prompt=prompt, rejection_statement=rejection_statement
        )

        return typing.cast(None, jsii.invoke(self, "putFollowUpPrompt", [value]))

    @jsii.member(jsii_name="putFulfillmentActivity")
    def put_fulfillment_activity(
        self,
        *,
        type: builtins.str,
        code_hook: typing.Optional[typing.Union["LexIntentFulfillmentActivityCodeHook", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#type LexIntent#type}.
        :param code_hook: code_hook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#code_hook LexIntent#code_hook}
        '''
        value = LexIntentFulfillmentActivity(type=type, code_hook=code_hook)

        return typing.cast(None, jsii.invoke(self, "putFulfillmentActivity", [value]))

    @jsii.member(jsii_name="putRejectionStatement")
    def put_rejection_statement(
        self,
        *,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentRejectionStatementMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        value = LexIntentRejectionStatement(
            message=message, response_card=response_card
        )

        return typing.cast(None, jsii.invoke(self, "putRejectionStatement", [value]))

    @jsii.member(jsii_name="putSlot")
    def put_slot(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentSlot", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea235c48aab0c745330246afe4205aa0afeb4a73aea350c2298639b6085c829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSlot", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#create LexIntent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#delete LexIntent#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#update LexIntent#update}.
        '''
        value = LexIntentTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConclusionStatement")
    def reset_conclusion_statement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConclusionStatement", []))

    @jsii.member(jsii_name="resetConfirmationPrompt")
    def reset_confirmation_prompt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfirmationPrompt", []))

    @jsii.member(jsii_name="resetCreateVersion")
    def reset_create_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateVersion", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDialogCodeHook")
    def reset_dialog_code_hook(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDialogCodeHook", []))

    @jsii.member(jsii_name="resetFollowUpPrompt")
    def reset_follow_up_prompt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFollowUpPrompt", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetParentIntentSignature")
    def reset_parent_intent_signature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentIntentSignature", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRejectionStatement")
    def reset_rejection_statement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRejectionStatement", []))

    @jsii.member(jsii_name="resetSampleUtterances")
    def reset_sample_utterances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleUtterances", []))

    @jsii.member(jsii_name="resetSlot")
    def reset_slot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlot", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="checksum")
    def checksum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checksum"))

    @builtins.property
    @jsii.member(jsii_name="conclusionStatement")
    def conclusion_statement(self) -> "LexIntentConclusionStatementOutputReference":
        return typing.cast("LexIntentConclusionStatementOutputReference", jsii.get(self, "conclusionStatement"))

    @builtins.property
    @jsii.member(jsii_name="confirmationPrompt")
    def confirmation_prompt(self) -> "LexIntentConfirmationPromptOutputReference":
        return typing.cast("LexIntentConfirmationPromptOutputReference", jsii.get(self, "confirmationPrompt"))

    @builtins.property
    @jsii.member(jsii_name="createdDate")
    def created_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdDate"))

    @builtins.property
    @jsii.member(jsii_name="dialogCodeHook")
    def dialog_code_hook(self) -> "LexIntentDialogCodeHookOutputReference":
        return typing.cast("LexIntentDialogCodeHookOutputReference", jsii.get(self, "dialogCodeHook"))

    @builtins.property
    @jsii.member(jsii_name="followUpPrompt")
    def follow_up_prompt(self) -> "LexIntentFollowUpPromptOutputReference":
        return typing.cast("LexIntentFollowUpPromptOutputReference", jsii.get(self, "followUpPrompt"))

    @builtins.property
    @jsii.member(jsii_name="fulfillmentActivity")
    def fulfillment_activity(self) -> "LexIntentFulfillmentActivityOutputReference":
        return typing.cast("LexIntentFulfillmentActivityOutputReference", jsii.get(self, "fulfillmentActivity"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedDate")
    def last_updated_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedDate"))

    @builtins.property
    @jsii.member(jsii_name="rejectionStatement")
    def rejection_statement(self) -> "LexIntentRejectionStatementOutputReference":
        return typing.cast("LexIntentRejectionStatementOutputReference", jsii.get(self, "rejectionStatement"))

    @builtins.property
    @jsii.member(jsii_name="slot")
    def slot(self) -> "LexIntentSlotList":
        return typing.cast("LexIntentSlotList", jsii.get(self, "slot"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LexIntentTimeoutsOutputReference":
        return typing.cast("LexIntentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="conclusionStatementInput")
    def conclusion_statement_input(
        self,
    ) -> typing.Optional["LexIntentConclusionStatement"]:
        return typing.cast(typing.Optional["LexIntentConclusionStatement"], jsii.get(self, "conclusionStatementInput"))

    @builtins.property
    @jsii.member(jsii_name="confirmationPromptInput")
    def confirmation_prompt_input(
        self,
    ) -> typing.Optional["LexIntentConfirmationPrompt"]:
        return typing.cast(typing.Optional["LexIntentConfirmationPrompt"], jsii.get(self, "confirmationPromptInput"))

    @builtins.property
    @jsii.member(jsii_name="createVersionInput")
    def create_version_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dialogCodeHookInput")
    def dialog_code_hook_input(self) -> typing.Optional["LexIntentDialogCodeHook"]:
        return typing.cast(typing.Optional["LexIntentDialogCodeHook"], jsii.get(self, "dialogCodeHookInput"))

    @builtins.property
    @jsii.member(jsii_name="followUpPromptInput")
    def follow_up_prompt_input(self) -> typing.Optional["LexIntentFollowUpPrompt"]:
        return typing.cast(typing.Optional["LexIntentFollowUpPrompt"], jsii.get(self, "followUpPromptInput"))

    @builtins.property
    @jsii.member(jsii_name="fulfillmentActivityInput")
    def fulfillment_activity_input(
        self,
    ) -> typing.Optional["LexIntentFulfillmentActivity"]:
        return typing.cast(typing.Optional["LexIntentFulfillmentActivity"], jsii.get(self, "fulfillmentActivityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentIntentSignatureInput")
    def parent_intent_signature_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentIntentSignatureInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="rejectionStatementInput")
    def rejection_statement_input(
        self,
    ) -> typing.Optional["LexIntentRejectionStatement"]:
        return typing.cast(typing.Optional["LexIntentRejectionStatement"], jsii.get(self, "rejectionStatementInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleUtterancesInput")
    def sample_utterances_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sampleUtterancesInput"))

    @builtins.property
    @jsii.member(jsii_name="slotInput")
    def slot_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentSlot"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentSlot"]]], jsii.get(self, "slotInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LexIntentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LexIntentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="createVersion")
    def create_version(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createVersion"))

    @create_version.setter
    def create_version(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8615ebd157e9ec139384b61242f12df771ebd2b627a8154f44b37d327767ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d03ff5c81a62623dae2e19be40c12ccdb179fd4f38d5109ea30607849b45fd1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea30864d9c7ef8085ae304d5dd34419ed98c76028dc97e6fc256eaa3ec40b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfaf6d63ed2a9d536009198f2266c1f7d6afee7d72e1d55ecfc486b7dbc42a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentIntentSignature")
    def parent_intent_signature(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentIntentSignature"))

    @parent_intent_signature.setter
    def parent_intent_signature(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cbb539e656e451aacbd84534dfcabed44a13449cf3171aca5fade09485311f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentIntentSignature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad7f4aa450473f557b2da3cb3146de7c72e13b2c6ef7445df03ba39dfc56946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleUtterances")
    def sample_utterances(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sampleUtterances"))

    @sample_utterances.setter
    def sample_utterances(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8278c58dab150a9c8c16f2aff6d9e2525d8416c4cfa74fe81f81955ab0f6abc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleUtterances", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConclusionStatement",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "response_card": "responseCard"},
)
class LexIntentConclusionStatement:
    def __init__(
        self,
        *,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentConclusionStatementMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3499f83ea5c616290b8d6966c74dd90e9dffb4a2da0c5260e730ae2cd75fcd5)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument response_card", value=response_card, expected_type=type_hints["response_card"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message": message,
        }
        if response_card is not None:
            self._values["response_card"] = response_card

    @builtins.property
    def message(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentConclusionStatementMessage"]]:
        '''message block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentConclusionStatementMessage"]], result)

    @builtins.property
    def response_card(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.'''
        result = self._values.get("response_card")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentConclusionStatement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConclusionStatementMessage",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "content_type": "contentType",
        "group_number": "groupNumber",
    },
)
class LexIntentConclusionStatementMessage:
    def __init__(
        self,
        *,
        content: builtins.str,
        content_type: builtins.str,
        group_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.
        :param group_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e454ec4eeaed80f69ef62bd7ea498ba6d9ed31b8bf53fe43c239cf766cc0f2d)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument group_number", value=group_number, expected_type=type_hints["group_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "content_type": content_type,
        }
        if group_number is not None:
            self._values["group_number"] = group_number

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.'''
        result = self._values.get("group_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentConclusionStatementMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentConclusionStatementMessageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConclusionStatementMessageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af24de87ba3be73b62d554fb40877a29d93fad64481ca2bf31469cbe41da87e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LexIntentConclusionStatementMessageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a8bcc0239ee01c49c1a6761cd848855e760aeed388aa0fc1f56224f91c771e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LexIntentConclusionStatementMessageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9435a56c40aeb1a001f12258924c81b556358647c708992d4584c9845515835c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb19113e3e05b5bb94cb2a0509c0d0d740c7171ef897c13b4fe1323d954d9b3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de20b0a82534e4fa6c6f99520fb3a6173ee142d4a47d5814f5b951d9b97aba7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConclusionStatementMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConclusionStatementMessage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConclusionStatementMessage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b815d01ce84dc8ffebfb4c490ad41019a7dab1eb10181c9a541f9483293db37d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentConclusionStatementMessageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConclusionStatementMessageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd2f05d082f49c25dbf6a8f33edb24d17b5131c5b47a80a8215a8d9cead85dbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGroupNumber")
    def reset_group_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupNumber", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupNumberInput")
    def group_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf30ea567a4a5db2a19687908736a767fedfbe71061d029a9fd536a50dc4229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__674632209759468bbf94fee41f83544f8f9cb41430929403cc2dbe455eed1390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupNumber")
    def group_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupNumber"))

    @group_number.setter
    def group_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be49adf19cd0c68deac1f1ab5d2809f66c63d45a340e06f9360f2e0167dff0a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentConclusionStatementMessage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentConclusionStatementMessage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentConclusionStatementMessage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b6c724a39d698ffdf00808df83cf6bb33ca72eb31d01802a978bd4405badc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentConclusionStatementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConclusionStatementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3c02a7a806ddc9646c40be5bcacdc3b4dd272637908f8355e0c36e80f8b22cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMessage")
    def put_message(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentConclusionStatementMessage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356909beb91b0c7099d1ef279746b3cd3a9d9de1ca49f6405247d1f89dcfa3f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessage", [value]))

    @jsii.member(jsii_name="resetResponseCard")
    def reset_response_card(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCard", []))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> LexIntentConclusionStatementMessageList:
        return typing.cast(LexIntentConclusionStatementMessageList, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConclusionStatementMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConclusionStatementMessage]]], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCardInput")
    def response_card_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseCardInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCard")
    def response_card(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseCard"))

    @response_card.setter
    def response_card(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c253a7a9f7a45d245df38bdeff191615ae4fc6164013f58f38cabed3fdcce8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LexIntentConclusionStatement]:
        return typing.cast(typing.Optional[LexIntentConclusionStatement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LexIntentConclusionStatement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e39b45072252dbc827d3d155cb1110a8934430fdd3fe2e005b4d68f2b63cd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "fulfillment_activity": "fulfillmentActivity",
        "name": "name",
        "conclusion_statement": "conclusionStatement",
        "confirmation_prompt": "confirmationPrompt",
        "create_version": "createVersion",
        "description": "description",
        "dialog_code_hook": "dialogCodeHook",
        "follow_up_prompt": "followUpPrompt",
        "id": "id",
        "parent_intent_signature": "parentIntentSignature",
        "region": "region",
        "rejection_statement": "rejectionStatement",
        "sample_utterances": "sampleUtterances",
        "slot": "slot",
        "timeouts": "timeouts",
    },
)
class LexIntentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        fulfillment_activity: typing.Union["LexIntentFulfillmentActivity", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        conclusion_statement: typing.Optional[typing.Union[LexIntentConclusionStatement, typing.Dict[builtins.str, typing.Any]]] = None,
        confirmation_prompt: typing.Optional[typing.Union["LexIntentConfirmationPrompt", typing.Dict[builtins.str, typing.Any]]] = None,
        create_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        dialog_code_hook: typing.Optional[typing.Union["LexIntentDialogCodeHook", typing.Dict[builtins.str, typing.Any]]] = None,
        follow_up_prompt: typing.Optional[typing.Union["LexIntentFollowUpPrompt", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        parent_intent_signature: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rejection_statement: typing.Optional[typing.Union["LexIntentRejectionStatement", typing.Dict[builtins.str, typing.Any]]] = None,
        sample_utterances: typing.Optional[typing.Sequence[builtins.str]] = None,
        slot: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentSlot", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["LexIntentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param fulfillment_activity: fulfillment_activity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#fulfillment_activity LexIntent#fulfillment_activity}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#name LexIntent#name}.
        :param conclusion_statement: conclusion_statement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#conclusion_statement LexIntent#conclusion_statement}
        :param confirmation_prompt: confirmation_prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#confirmation_prompt LexIntent#confirmation_prompt}
        :param create_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#create_version LexIntent#create_version}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#description LexIntent#description}.
        :param dialog_code_hook: dialog_code_hook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#dialog_code_hook LexIntent#dialog_code_hook}
        :param follow_up_prompt: follow_up_prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#follow_up_prompt LexIntent#follow_up_prompt}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#id LexIntent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parent_intent_signature: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#parent_intent_signature LexIntent#parent_intent_signature}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#region LexIntent#region}
        :param rejection_statement: rejection_statement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#rejection_statement LexIntent#rejection_statement}
        :param sample_utterances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#sample_utterances LexIntent#sample_utterances}.
        :param slot: slot block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#slot LexIntent#slot}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#timeouts LexIntent#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fulfillment_activity, dict):
            fulfillment_activity = LexIntentFulfillmentActivity(**fulfillment_activity)
        if isinstance(conclusion_statement, dict):
            conclusion_statement = LexIntentConclusionStatement(**conclusion_statement)
        if isinstance(confirmation_prompt, dict):
            confirmation_prompt = LexIntentConfirmationPrompt(**confirmation_prompt)
        if isinstance(dialog_code_hook, dict):
            dialog_code_hook = LexIntentDialogCodeHook(**dialog_code_hook)
        if isinstance(follow_up_prompt, dict):
            follow_up_prompt = LexIntentFollowUpPrompt(**follow_up_prompt)
        if isinstance(rejection_statement, dict):
            rejection_statement = LexIntentRejectionStatement(**rejection_statement)
        if isinstance(timeouts, dict):
            timeouts = LexIntentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b7e143f443badd936eecae335f13df0d9822538d812e848838dce575938bc0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument fulfillment_activity", value=fulfillment_activity, expected_type=type_hints["fulfillment_activity"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument conclusion_statement", value=conclusion_statement, expected_type=type_hints["conclusion_statement"])
            check_type(argname="argument confirmation_prompt", value=confirmation_prompt, expected_type=type_hints["confirmation_prompt"])
            check_type(argname="argument create_version", value=create_version, expected_type=type_hints["create_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dialog_code_hook", value=dialog_code_hook, expected_type=type_hints["dialog_code_hook"])
            check_type(argname="argument follow_up_prompt", value=follow_up_prompt, expected_type=type_hints["follow_up_prompt"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parent_intent_signature", value=parent_intent_signature, expected_type=type_hints["parent_intent_signature"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rejection_statement", value=rejection_statement, expected_type=type_hints["rejection_statement"])
            check_type(argname="argument sample_utterances", value=sample_utterances, expected_type=type_hints["sample_utterances"])
            check_type(argname="argument slot", value=slot, expected_type=type_hints["slot"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fulfillment_activity": fulfillment_activity,
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
        if conclusion_statement is not None:
            self._values["conclusion_statement"] = conclusion_statement
        if confirmation_prompt is not None:
            self._values["confirmation_prompt"] = confirmation_prompt
        if create_version is not None:
            self._values["create_version"] = create_version
        if description is not None:
            self._values["description"] = description
        if dialog_code_hook is not None:
            self._values["dialog_code_hook"] = dialog_code_hook
        if follow_up_prompt is not None:
            self._values["follow_up_prompt"] = follow_up_prompt
        if id is not None:
            self._values["id"] = id
        if parent_intent_signature is not None:
            self._values["parent_intent_signature"] = parent_intent_signature
        if region is not None:
            self._values["region"] = region
        if rejection_statement is not None:
            self._values["rejection_statement"] = rejection_statement
        if sample_utterances is not None:
            self._values["sample_utterances"] = sample_utterances
        if slot is not None:
            self._values["slot"] = slot
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
    def fulfillment_activity(self) -> "LexIntentFulfillmentActivity":
        '''fulfillment_activity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#fulfillment_activity LexIntent#fulfillment_activity}
        '''
        result = self._values.get("fulfillment_activity")
        assert result is not None, "Required property 'fulfillment_activity' is missing"
        return typing.cast("LexIntentFulfillmentActivity", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#name LexIntent#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def conclusion_statement(self) -> typing.Optional[LexIntentConclusionStatement]:
        '''conclusion_statement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#conclusion_statement LexIntent#conclusion_statement}
        '''
        result = self._values.get("conclusion_statement")
        return typing.cast(typing.Optional[LexIntentConclusionStatement], result)

    @builtins.property
    def confirmation_prompt(self) -> typing.Optional["LexIntentConfirmationPrompt"]:
        '''confirmation_prompt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#confirmation_prompt LexIntent#confirmation_prompt}
        '''
        result = self._values.get("confirmation_prompt")
        return typing.cast(typing.Optional["LexIntentConfirmationPrompt"], result)

    @builtins.property
    def create_version(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#create_version LexIntent#create_version}.'''
        result = self._values.get("create_version")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#description LexIntent#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dialog_code_hook(self) -> typing.Optional["LexIntentDialogCodeHook"]:
        '''dialog_code_hook block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#dialog_code_hook LexIntent#dialog_code_hook}
        '''
        result = self._values.get("dialog_code_hook")
        return typing.cast(typing.Optional["LexIntentDialogCodeHook"], result)

    @builtins.property
    def follow_up_prompt(self) -> typing.Optional["LexIntentFollowUpPrompt"]:
        '''follow_up_prompt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#follow_up_prompt LexIntent#follow_up_prompt}
        '''
        result = self._values.get("follow_up_prompt")
        return typing.cast(typing.Optional["LexIntentFollowUpPrompt"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#id LexIntent#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_intent_signature(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#parent_intent_signature LexIntent#parent_intent_signature}.'''
        result = self._values.get("parent_intent_signature")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#region LexIntent#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rejection_statement(self) -> typing.Optional["LexIntentRejectionStatement"]:
        '''rejection_statement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#rejection_statement LexIntent#rejection_statement}
        '''
        result = self._values.get("rejection_statement")
        return typing.cast(typing.Optional["LexIntentRejectionStatement"], result)

    @builtins.property
    def sample_utterances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#sample_utterances LexIntent#sample_utterances}.'''
        result = self._values.get("sample_utterances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def slot(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentSlot"]]]:
        '''slot block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#slot LexIntent#slot}
        '''
        result = self._values.get("slot")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentSlot"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LexIntentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#timeouts LexIntent#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LexIntentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConfirmationPrompt",
    jsii_struct_bases=[],
    name_mapping={
        "max_attempts": "maxAttempts",
        "message": "message",
        "response_card": "responseCard",
    },
)
class LexIntentConfirmationPrompt:
    def __init__(
        self,
        *,
        max_attempts: jsii.Number,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentConfirmationPromptMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#max_attempts LexIntent#max_attempts}.
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069b083d5851c6d8af449ba59329e5f19a26aa341d44a1e87bf87b60ed98bec0)
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument response_card", value=response_card, expected_type=type_hints["response_card"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_attempts": max_attempts,
            "message": message,
        }
        if response_card is not None:
            self._values["response_card"] = response_card

    @builtins.property
    def max_attempts(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#max_attempts LexIntent#max_attempts}.'''
        result = self._values.get("max_attempts")
        assert result is not None, "Required property 'max_attempts' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def message(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentConfirmationPromptMessage"]]:
        '''message block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentConfirmationPromptMessage"]], result)

    @builtins.property
    def response_card(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.'''
        result = self._values.get("response_card")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentConfirmationPrompt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConfirmationPromptMessage",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "content_type": "contentType",
        "group_number": "groupNumber",
    },
)
class LexIntentConfirmationPromptMessage:
    def __init__(
        self,
        *,
        content: builtins.str,
        content_type: builtins.str,
        group_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.
        :param group_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df59af37a3ed9eef06c13187efb053178d19e9022f385284636324fa4211e5a3)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument group_number", value=group_number, expected_type=type_hints["group_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "content_type": content_type,
        }
        if group_number is not None:
            self._values["group_number"] = group_number

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.'''
        result = self._values.get("group_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentConfirmationPromptMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentConfirmationPromptMessageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConfirmationPromptMessageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2dd91db1c9ca75f32eeafb8dba84346645e3047f561ec4e8780821fa16a139f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LexIntentConfirmationPromptMessageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1050410aca609aa9ea193c0330375aaa1a82d22c28ba7a10de17e072aca94928)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LexIntentConfirmationPromptMessageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825d635394b6a4a504c7a70366aea7f196456b8846c30ec43b19002417f9636d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__664a51020afb6d1450709181067a1203aba113a5672c84153304f9dbf8d0b837)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc88430dabb5107ea81f3d09d0dd3c828fea614896b1d678af2509eb2fe7e4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConfirmationPromptMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConfirmationPromptMessage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConfirmationPromptMessage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80fa711ffcb61c3ebee311efaacff010e38618f939d547f735fbf80405cadd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentConfirmationPromptMessageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConfirmationPromptMessageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c301ac9e1f2c02f1404b59dc8741d667ffe90ec24a0a0f2b0a3839ad2e0b9b22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGroupNumber")
    def reset_group_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupNumber", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupNumberInput")
    def group_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d05e3ea71aac4752ecc16448d96eb1ce95d7dbda865588b12d2e9b8b5e5171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d462bd726e802b2916ac246242471caf94c3d361b18a50194ffdfaaa74dbf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupNumber")
    def group_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupNumber"))

    @group_number.setter
    def group_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb641c4465164e1f17704634d1c53093839adc68102327f1abefac5bdee7e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentConfirmationPromptMessage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentConfirmationPromptMessage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentConfirmationPromptMessage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873125d7b2844d07fcdee080a00bc63245220a93892336ca68f12f7d612bf094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentConfirmationPromptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentConfirmationPromptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__377f0d741ad767e309ddf4458bf8eb27a69718c756915a9c0d0ce4b30f02c1c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMessage")
    def put_message(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentConfirmationPromptMessage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d344a910a5daf24b0fbfa2fcd946c83511ab2afd7476a6e50036d9b3df3df4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessage", [value]))

    @jsii.member(jsii_name="resetResponseCard")
    def reset_response_card(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCard", []))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> LexIntentConfirmationPromptMessageList:
        return typing.cast(LexIntentConfirmationPromptMessageList, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsInput")
    def max_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConfirmationPromptMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConfirmationPromptMessage]]], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCardInput")
    def response_card_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseCardInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAttempts")
    def max_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttempts"))

    @max_attempts.setter
    def max_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39839d5c30ac26fbddc031844b341175ea9042fc64f6b03db76f25c05ab52a2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCard")
    def response_card(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseCard"))

    @response_card.setter
    def response_card(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cb769d74750a99fbb91c097b66fd76fa96827ce5c40fda629785d4604217b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LexIntentConfirmationPrompt]:
        return typing.cast(typing.Optional[LexIntentConfirmationPrompt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LexIntentConfirmationPrompt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19615d85a2ec1f9af8c9cc803e13c6b78119b3d3d963868e5402a2b7c2324b04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentDialogCodeHook",
    jsii_struct_bases=[],
    name_mapping={"message_version": "messageVersion", "uri": "uri"},
)
class LexIntentDialogCodeHook:
    def __init__(self, *, message_version: builtins.str, uri: builtins.str) -> None:
        '''
        :param message_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message_version LexIntent#message_version}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#uri LexIntent#uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abaf6712bc968dcb04290fa0a0c6a02bae7bc2a4d818f3835cbf7200d4e2c533)
            check_type(argname="argument message_version", value=message_version, expected_type=type_hints["message_version"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message_version": message_version,
            "uri": uri,
        }

    @builtins.property
    def message_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message_version LexIntent#message_version}.'''
        result = self._values.get("message_version")
        assert result is not None, "Required property 'message_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#uri LexIntent#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentDialogCodeHook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentDialogCodeHookOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentDialogCodeHookOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__888d3a3f60639a2d87e96208c7d7fd076034b7bfd0ce50c223af0d4a874b2a45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="messageVersionInput")
    def message_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="messageVersion")
    def message_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageVersion"))

    @message_version.setter
    def message_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b7db0652b8678ffca78ee0ce0f175bf7e6ac749cc2855b1e145d8c24f2dc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead7d665896ea12b4ff814bf4399c6a9182e5984d7e044dfcf183e8083780504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LexIntentDialogCodeHook]:
        return typing.cast(typing.Optional[LexIntentDialogCodeHook], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LexIntentDialogCodeHook]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ad388869e40ce648f1d614b28f0592d3a3de7a1e10758b8268660c5c8de1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPrompt",
    jsii_struct_bases=[],
    name_mapping={"prompt": "prompt", "rejection_statement": "rejectionStatement"},
)
class LexIntentFollowUpPrompt:
    def __init__(
        self,
        *,
        prompt: typing.Union["LexIntentFollowUpPromptPrompt", typing.Dict[builtins.str, typing.Any]],
        rejection_statement: typing.Union["LexIntentFollowUpPromptRejectionStatement", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param prompt: prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#prompt LexIntent#prompt}
        :param rejection_statement: rejection_statement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#rejection_statement LexIntent#rejection_statement}
        '''
        if isinstance(prompt, dict):
            prompt = LexIntentFollowUpPromptPrompt(**prompt)
        if isinstance(rejection_statement, dict):
            rejection_statement = LexIntentFollowUpPromptRejectionStatement(**rejection_statement)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536259bd872a796d73a805c5dc8b64d6727a3277a9b3e1cbaf8d83df80341a58)
            check_type(argname="argument prompt", value=prompt, expected_type=type_hints["prompt"])
            check_type(argname="argument rejection_statement", value=rejection_statement, expected_type=type_hints["rejection_statement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prompt": prompt,
            "rejection_statement": rejection_statement,
        }

    @builtins.property
    def prompt(self) -> "LexIntentFollowUpPromptPrompt":
        '''prompt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#prompt LexIntent#prompt}
        '''
        result = self._values.get("prompt")
        assert result is not None, "Required property 'prompt' is missing"
        return typing.cast("LexIntentFollowUpPromptPrompt", result)

    @builtins.property
    def rejection_statement(self) -> "LexIntentFollowUpPromptRejectionStatement":
        '''rejection_statement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#rejection_statement LexIntent#rejection_statement}
        '''
        result = self._values.get("rejection_statement")
        assert result is not None, "Required property 'rejection_statement' is missing"
        return typing.cast("LexIntentFollowUpPromptRejectionStatement", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentFollowUpPrompt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentFollowUpPromptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce9d1acfd29284f208b4a5c9cc85696898637b4b91cdfa3f4651d55e1b1dadd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrompt")
    def put_prompt(
        self,
        *,
        max_attempts: jsii.Number,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentFollowUpPromptPromptMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#max_attempts LexIntent#max_attempts}.
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        value = LexIntentFollowUpPromptPrompt(
            max_attempts=max_attempts, message=message, response_card=response_card
        )

        return typing.cast(None, jsii.invoke(self, "putPrompt", [value]))

    @jsii.member(jsii_name="putRejectionStatement")
    def put_rejection_statement(
        self,
        *,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentFollowUpPromptRejectionStatementMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        value = LexIntentFollowUpPromptRejectionStatement(
            message=message, response_card=response_card
        )

        return typing.cast(None, jsii.invoke(self, "putRejectionStatement", [value]))

    @builtins.property
    @jsii.member(jsii_name="prompt")
    def prompt(self) -> "LexIntentFollowUpPromptPromptOutputReference":
        return typing.cast("LexIntentFollowUpPromptPromptOutputReference", jsii.get(self, "prompt"))

    @builtins.property
    @jsii.member(jsii_name="rejectionStatement")
    def rejection_statement(
        self,
    ) -> "LexIntentFollowUpPromptRejectionStatementOutputReference":
        return typing.cast("LexIntentFollowUpPromptRejectionStatementOutputReference", jsii.get(self, "rejectionStatement"))

    @builtins.property
    @jsii.member(jsii_name="promptInput")
    def prompt_input(self) -> typing.Optional["LexIntentFollowUpPromptPrompt"]:
        return typing.cast(typing.Optional["LexIntentFollowUpPromptPrompt"], jsii.get(self, "promptInput"))

    @builtins.property
    @jsii.member(jsii_name="rejectionStatementInput")
    def rejection_statement_input(
        self,
    ) -> typing.Optional["LexIntentFollowUpPromptRejectionStatement"]:
        return typing.cast(typing.Optional["LexIntentFollowUpPromptRejectionStatement"], jsii.get(self, "rejectionStatementInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LexIntentFollowUpPrompt]:
        return typing.cast(typing.Optional[LexIntentFollowUpPrompt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LexIntentFollowUpPrompt]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__005004290a1cb20ad270c9830631acbd5703d06e511f30c46bb286c7786324c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptPrompt",
    jsii_struct_bases=[],
    name_mapping={
        "max_attempts": "maxAttempts",
        "message": "message",
        "response_card": "responseCard",
    },
)
class LexIntentFollowUpPromptPrompt:
    def __init__(
        self,
        *,
        max_attempts: jsii.Number,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentFollowUpPromptPromptMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#max_attempts LexIntent#max_attempts}.
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6953579615d403cc6ee6c7e62f75a5103c4abcc8a3dadfb3f46ff6ccb6c173)
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument response_card", value=response_card, expected_type=type_hints["response_card"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_attempts": max_attempts,
            "message": message,
        }
        if response_card is not None:
            self._values["response_card"] = response_card

    @builtins.property
    def max_attempts(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#max_attempts LexIntent#max_attempts}.'''
        result = self._values.get("max_attempts")
        assert result is not None, "Required property 'max_attempts' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def message(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentFollowUpPromptPromptMessage"]]:
        '''message block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentFollowUpPromptPromptMessage"]], result)

    @builtins.property
    def response_card(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.'''
        result = self._values.get("response_card")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentFollowUpPromptPrompt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptPromptMessage",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "content_type": "contentType",
        "group_number": "groupNumber",
    },
)
class LexIntentFollowUpPromptPromptMessage:
    def __init__(
        self,
        *,
        content: builtins.str,
        content_type: builtins.str,
        group_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.
        :param group_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6b879b20672f9bcbec5ea577b0f96ec0179ac994a2ca5540f1bbb379c4adf3)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument group_number", value=group_number, expected_type=type_hints["group_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "content_type": content_type,
        }
        if group_number is not None:
            self._values["group_number"] = group_number

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.'''
        result = self._values.get("group_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentFollowUpPromptPromptMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentFollowUpPromptPromptMessageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptPromptMessageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a06c0980f82c28d28732d8f57634f4a60fb9cfd94a9c548b29e7606179ff3a35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LexIntentFollowUpPromptPromptMessageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b091dfa8eac8015fcdac65fc59d7b45eefa07e6f412e437209338a299298ad4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LexIntentFollowUpPromptPromptMessageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc6cfe3b77821f5de3331cbe7233033636761d7048d24b84ca0245d6bc4f532)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4925ace3501f6e9d0a808946b36810c1163c1efc8d9c42200d997cc55c6fd22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40548335c4a0a77046b04aa940758b670aa81ab73e3adb6c13be9d56dbbbdafc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptPromptMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptPromptMessage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptPromptMessage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed61d3b025f81aa1672bf94fca7592c469cb0651da8b6115d979919ced7ff11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentFollowUpPromptPromptMessageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptPromptMessageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43b6d3fbd6a01cde526dddc4eea84bf38706be87d0f9d5a09f7f84e20daba6b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGroupNumber")
    def reset_group_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupNumber", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupNumberInput")
    def group_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e58cc1627b6781c2e80f25999b441c33ce6fd6da722c01676c6c8ff8e9c4653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555e41232eadf51e3a0d11187093917d7549fca01d2efe5c48532ef1be30df5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupNumber")
    def group_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupNumber"))

    @group_number.setter
    def group_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dfbdf45e46af0916e3e2bd943cd86c84e5ecfe1cf328b089a2f59472c6ecb6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentFollowUpPromptPromptMessage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentFollowUpPromptPromptMessage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentFollowUpPromptPromptMessage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed2cbbe3999e318d61824dfac82497744d18037ba985fb38ddcbecd5a115b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentFollowUpPromptPromptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptPromptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ed903d25fec93da994690bd5b831bf55cd7fd4ba7055f2d865e19e500d8e80c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMessage")
    def put_message(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentFollowUpPromptPromptMessage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f223cac5ac5b04a1ad9f653c2f2063c660ffbc4b2d1d1febbc7389dd720e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessage", [value]))

    @jsii.member(jsii_name="resetResponseCard")
    def reset_response_card(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCard", []))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> LexIntentFollowUpPromptPromptMessageList:
        return typing.cast(LexIntentFollowUpPromptPromptMessageList, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsInput")
    def max_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptPromptMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptPromptMessage]]], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCardInput")
    def response_card_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseCardInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAttempts")
    def max_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttempts"))

    @max_attempts.setter
    def max_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267f79aa1e754f7e408ccb8f9560bc083e3e93a44fd88313adbdce24ff32f8bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCard")
    def response_card(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseCard"))

    @response_card.setter
    def response_card(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6dc4c7e21413c2151b782213a14a0485b52111b4f98478550c6d9e91d02eb7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LexIntentFollowUpPromptPrompt]:
        return typing.cast(typing.Optional[LexIntentFollowUpPromptPrompt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LexIntentFollowUpPromptPrompt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87360d1fd197a69d7722007901009375aacf1cf526e828409eaa4595ebe814ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptRejectionStatement",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "response_card": "responseCard"},
)
class LexIntentFollowUpPromptRejectionStatement:
    def __init__(
        self,
        *,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentFollowUpPromptRejectionStatementMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d700d1e64714b35f6483cbe17dd38c369c9f6a01dd45a50d0f747debdc7a7c4c)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument response_card", value=response_card, expected_type=type_hints["response_card"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message": message,
        }
        if response_card is not None:
            self._values["response_card"] = response_card

    @builtins.property
    def message(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentFollowUpPromptRejectionStatementMessage"]]:
        '''message block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentFollowUpPromptRejectionStatementMessage"]], result)

    @builtins.property
    def response_card(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.'''
        result = self._values.get("response_card")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentFollowUpPromptRejectionStatement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptRejectionStatementMessage",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "content_type": "contentType",
        "group_number": "groupNumber",
    },
)
class LexIntentFollowUpPromptRejectionStatementMessage:
    def __init__(
        self,
        *,
        content: builtins.str,
        content_type: builtins.str,
        group_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.
        :param group_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bddc3db4c6d0f36c1040005784e7037bec891a7a0723663e9a3135d27549ab83)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument group_number", value=group_number, expected_type=type_hints["group_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "content_type": content_type,
        }
        if group_number is not None:
            self._values["group_number"] = group_number

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.'''
        result = self._values.get("group_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentFollowUpPromptRejectionStatementMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentFollowUpPromptRejectionStatementMessageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptRejectionStatementMessageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc4cfd77de05610235c8a4a7b9bba8640f4b5b978e8a6e884d7735a6336160d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LexIntentFollowUpPromptRejectionStatementMessageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6443e2810bd33db9901c28219b0d50b136b5817521c73c615b739cd62557d226)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LexIntentFollowUpPromptRejectionStatementMessageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02d73da939ec85d0176c28ef1386f9b98c9e5121f3e3a5631ad067ec9a2357c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efd26d5d1e65f3176266d0d4a5b98ee8b724972f57cc5a590e554543fb56740d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6fc16425b1ad451d7b98fed1dd8c8348ef77fe28447c6be547ae22cc61364ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptRejectionStatementMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptRejectionStatementMessage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptRejectionStatementMessage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61b068cb94884ef3c1e7a8e76e036422919bbf229cabc21681ad609289e585e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentFollowUpPromptRejectionStatementMessageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptRejectionStatementMessageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aff029365fa5e6a5e4e4da79217cbe78a871ae3724216bbf99c64b414f3a1e3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGroupNumber")
    def reset_group_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupNumber", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupNumberInput")
    def group_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0283293e53a2a02dc2c1588ad1495579d04a92674ff1a9a8f7f2c919a11df3e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f4f507ac0d1762506cab975ae14084b0bfe5605c24ed9912faacdf91c563ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupNumber")
    def group_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupNumber"))

    @group_number.setter
    def group_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77abb3ca729cdb3b59ad766cbc2a1a8bd41622a996b52e9ac82f61a139db4ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentFollowUpPromptRejectionStatementMessage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentFollowUpPromptRejectionStatementMessage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentFollowUpPromptRejectionStatementMessage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997965c8c0248334ace5f210e83e2e38584834987b6dc6e50b89af0c63ad0782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentFollowUpPromptRejectionStatementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFollowUpPromptRejectionStatementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf31fddb585476d4e7645cf5ed33a6d186eb875a6e946facb98410dc5a12b252)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMessage")
    def put_message(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentFollowUpPromptRejectionStatementMessage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4700a496342f681423a1742af628f9a5e6999e268a8a12b58ef1745583725fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessage", [value]))

    @jsii.member(jsii_name="resetResponseCard")
    def reset_response_card(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCard", []))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> LexIntentFollowUpPromptRejectionStatementMessageList:
        return typing.cast(LexIntentFollowUpPromptRejectionStatementMessageList, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptRejectionStatementMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptRejectionStatementMessage]]], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCardInput")
    def response_card_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseCardInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCard")
    def response_card(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseCard"))

    @response_card.setter
    def response_card(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1392c3f462f83ebdbac48587db747fbb62408823f5536bb9e7ec57f9c7c19f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LexIntentFollowUpPromptRejectionStatement]:
        return typing.cast(typing.Optional[LexIntentFollowUpPromptRejectionStatement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LexIntentFollowUpPromptRejectionStatement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c69260760d7ab8da522c09e172c0496ab118acd2b6b71c349e5dedfadb12c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFulfillmentActivity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "code_hook": "codeHook"},
)
class LexIntentFulfillmentActivity:
    def __init__(
        self,
        *,
        type: builtins.str,
        code_hook: typing.Optional[typing.Union["LexIntentFulfillmentActivityCodeHook", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#type LexIntent#type}.
        :param code_hook: code_hook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#code_hook LexIntent#code_hook}
        '''
        if isinstance(code_hook, dict):
            code_hook = LexIntentFulfillmentActivityCodeHook(**code_hook)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3348b73a2f18871dce9468c07bfd8c904ba3c3c6a223690e0f75d8e9094478dc)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument code_hook", value=code_hook, expected_type=type_hints["code_hook"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if code_hook is not None:
            self._values["code_hook"] = code_hook

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#type LexIntent#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code_hook(self) -> typing.Optional["LexIntentFulfillmentActivityCodeHook"]:
        '''code_hook block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#code_hook LexIntent#code_hook}
        '''
        result = self._values.get("code_hook")
        return typing.cast(typing.Optional["LexIntentFulfillmentActivityCodeHook"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentFulfillmentActivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFulfillmentActivityCodeHook",
    jsii_struct_bases=[],
    name_mapping={"message_version": "messageVersion", "uri": "uri"},
)
class LexIntentFulfillmentActivityCodeHook:
    def __init__(self, *, message_version: builtins.str, uri: builtins.str) -> None:
        '''
        :param message_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message_version LexIntent#message_version}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#uri LexIntent#uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873e1310a6ec5a47f4fc998632d903852514a7b38f60f97b8a033d55995a1087)
            check_type(argname="argument message_version", value=message_version, expected_type=type_hints["message_version"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message_version": message_version,
            "uri": uri,
        }

    @builtins.property
    def message_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message_version LexIntent#message_version}.'''
        result = self._values.get("message_version")
        assert result is not None, "Required property 'message_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#uri LexIntent#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentFulfillmentActivityCodeHook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentFulfillmentActivityCodeHookOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFulfillmentActivityCodeHookOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e1a861fb9a0257d42db59b5727da2ece3b870c30ab798a6b2d8b4f7d4cd77b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="messageVersionInput")
    def message_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="messageVersion")
    def message_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageVersion"))

    @message_version.setter
    def message_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de4e09d9c90fd8e572bbc6ccc30b69de5778e91dcfda383e9686473e023f26e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab1ac4a3c5787a2c419364dacfa9102902f6f70128e667c9fe18dcec3cac0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LexIntentFulfillmentActivityCodeHook]:
        return typing.cast(typing.Optional[LexIntentFulfillmentActivityCodeHook], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LexIntentFulfillmentActivityCodeHook],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f843236ea1be990c89638500db577ed5b035868c5a4762149d2a30b9eb5ad6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentFulfillmentActivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentFulfillmentActivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__151cb373be413617374e2f1f450f8c0ce383a195bfc78aacfd03b8191e34ad59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCodeHook")
    def put_code_hook(
        self,
        *,
        message_version: builtins.str,
        uri: builtins.str,
    ) -> None:
        '''
        :param message_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message_version LexIntent#message_version}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#uri LexIntent#uri}.
        '''
        value = LexIntentFulfillmentActivityCodeHook(
            message_version=message_version, uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putCodeHook", [value]))

    @jsii.member(jsii_name="resetCodeHook")
    def reset_code_hook(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeHook", []))

    @builtins.property
    @jsii.member(jsii_name="codeHook")
    def code_hook(self) -> LexIntentFulfillmentActivityCodeHookOutputReference:
        return typing.cast(LexIntentFulfillmentActivityCodeHookOutputReference, jsii.get(self, "codeHook"))

    @builtins.property
    @jsii.member(jsii_name="codeHookInput")
    def code_hook_input(self) -> typing.Optional[LexIntentFulfillmentActivityCodeHook]:
        return typing.cast(typing.Optional[LexIntentFulfillmentActivityCodeHook], jsii.get(self, "codeHookInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1ddb4e47ee81d6b8fd15891f62fe536226c66a0b3cc43cba459f35ecf19e8db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LexIntentFulfillmentActivity]:
        return typing.cast(typing.Optional[LexIntentFulfillmentActivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LexIntentFulfillmentActivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73954779cb7c1b960c3fa9966b273edf6e49fe31b87ec63a10dc00e8e980b755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentRejectionStatement",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "response_card": "responseCard"},
)
class LexIntentRejectionStatement:
    def __init__(
        self,
        *,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentRejectionStatementMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58aa22fbf0dd907c468b165f4c719e089e46f0df1141337491a50b937bc66bf4)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument response_card", value=response_card, expected_type=type_hints["response_card"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message": message,
        }
        if response_card is not None:
            self._values["response_card"] = response_card

    @builtins.property
    def message(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentRejectionStatementMessage"]]:
        '''message block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentRejectionStatementMessage"]], result)

    @builtins.property
    def response_card(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.'''
        result = self._values.get("response_card")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentRejectionStatement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentRejectionStatementMessage",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "content_type": "contentType",
        "group_number": "groupNumber",
    },
)
class LexIntentRejectionStatementMessage:
    def __init__(
        self,
        *,
        content: builtins.str,
        content_type: builtins.str,
        group_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.
        :param group_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90ffe216ca89019b5256c40e7a4e9eec4d0820a0270ccfbada4ac1fe9245024)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument group_number", value=group_number, expected_type=type_hints["group_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "content_type": content_type,
        }
        if group_number is not None:
            self._values["group_number"] = group_number

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.'''
        result = self._values.get("group_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentRejectionStatementMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentRejectionStatementMessageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentRejectionStatementMessageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d7122b803cec0e41d4bfec802e0e166cec7ee986b92da1958a7d1fed2f8bee0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LexIntentRejectionStatementMessageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247176ab6d03a21c07372eb31107f6ed6f7f5fc548017888e3f00c690e267a24)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LexIntentRejectionStatementMessageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94de943428617484412e5167f750b0ab6de42bc9ea85e2be5583c3767c296f03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__032bbf3ed64d9df3fc466ef73545b52726c3b8efaaaa26d8bfab734608379075)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddd151dd11246db66aef30df0da0c035c573de4f56261b4b7bf14004e42b84fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentRejectionStatementMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentRejectionStatementMessage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentRejectionStatementMessage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b4ad91e961afd0740061b17ae5961df2f0f2b30fab4a85184f842c001d294c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentRejectionStatementMessageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentRejectionStatementMessageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cb8e3f1e50ec5d7acb22765343b76e60800472d2fdb16e38fdb914b9ba2e84c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGroupNumber")
    def reset_group_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupNumber", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupNumberInput")
    def group_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3520dae501e847d1d0cc9994fd80979aed1249848f39abc4aa901637a96e135c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26a2ebf07b1cb677d8ef89247c9e4873058ac0c655c01c1cbd9056eb26a745b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupNumber")
    def group_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupNumber"))

    @group_number.setter
    def group_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204cbe23124636bc6bc3e078f98ade2ba14027668eebc78e56dc84dff6d6aa91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentRejectionStatementMessage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentRejectionStatementMessage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentRejectionStatementMessage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cdef1b1a8222951791530c8f8a8b0eebe397a49695411f340cb3984884e3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentRejectionStatementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentRejectionStatementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6019609113eba373fb6766aa2544db194af32230081d0e1e24eeabb18ba7937a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMessage")
    def put_message(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentRejectionStatementMessage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e75492a161a06c98b7fd4b7c9f7ef5727ab5a5db32686b9ecf132d041aa143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessage", [value]))

    @jsii.member(jsii_name="resetResponseCard")
    def reset_response_card(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCard", []))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> LexIntentRejectionStatementMessageList:
        return typing.cast(LexIntentRejectionStatementMessageList, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentRejectionStatementMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentRejectionStatementMessage]]], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCardInput")
    def response_card_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseCardInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCard")
    def response_card(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseCard"))

    @response_card.setter
    def response_card(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9fc70429fbe97024b7f22d56a9be9f945b994321d2603ff908ec8bb9a803da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LexIntentRejectionStatement]:
        return typing.cast(typing.Optional[LexIntentRejectionStatement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LexIntentRejectionStatement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd5566d68837563b43b0d556d692f5e467cc2afba7c050ec80d5ae21c2fcf5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentSlot",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "slot_constraint": "slotConstraint",
        "slot_type": "slotType",
        "description": "description",
        "priority": "priority",
        "response_card": "responseCard",
        "sample_utterances": "sampleUtterances",
        "slot_type_version": "slotTypeVersion",
        "value_elicitation_prompt": "valueElicitationPrompt",
    },
)
class LexIntentSlot:
    def __init__(
        self,
        *,
        name: builtins.str,
        slot_constraint: builtins.str,
        slot_type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        response_card: typing.Optional[builtins.str] = None,
        sample_utterances: typing.Optional[typing.Sequence[builtins.str]] = None,
        slot_type_version: typing.Optional[builtins.str] = None,
        value_elicitation_prompt: typing.Optional[typing.Union["LexIntentSlotValueElicitationPrompt", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#name LexIntent#name}.
        :param slot_constraint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#slot_constraint LexIntent#slot_constraint}.
        :param slot_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#slot_type LexIntent#slot_type}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#description LexIntent#description}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#priority LexIntent#priority}.
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        :param sample_utterances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#sample_utterances LexIntent#sample_utterances}.
        :param slot_type_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#slot_type_version LexIntent#slot_type_version}.
        :param value_elicitation_prompt: value_elicitation_prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#value_elicitation_prompt LexIntent#value_elicitation_prompt}
        '''
        if isinstance(value_elicitation_prompt, dict):
            value_elicitation_prompt = LexIntentSlotValueElicitationPrompt(**value_elicitation_prompt)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b54f757b8cec25dca59cb4546a6a9d612ae1f6171ef9ee2df7db8a630582a2f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument slot_constraint", value=slot_constraint, expected_type=type_hints["slot_constraint"])
            check_type(argname="argument slot_type", value=slot_type, expected_type=type_hints["slot_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument response_card", value=response_card, expected_type=type_hints["response_card"])
            check_type(argname="argument sample_utterances", value=sample_utterances, expected_type=type_hints["sample_utterances"])
            check_type(argname="argument slot_type_version", value=slot_type_version, expected_type=type_hints["slot_type_version"])
            check_type(argname="argument value_elicitation_prompt", value=value_elicitation_prompt, expected_type=type_hints["value_elicitation_prompt"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "slot_constraint": slot_constraint,
            "slot_type": slot_type,
        }
        if description is not None:
            self._values["description"] = description
        if priority is not None:
            self._values["priority"] = priority
        if response_card is not None:
            self._values["response_card"] = response_card
        if sample_utterances is not None:
            self._values["sample_utterances"] = sample_utterances
        if slot_type_version is not None:
            self._values["slot_type_version"] = slot_type_version
        if value_elicitation_prompt is not None:
            self._values["value_elicitation_prompt"] = value_elicitation_prompt

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#name LexIntent#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slot_constraint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#slot_constraint LexIntent#slot_constraint}.'''
        result = self._values.get("slot_constraint")
        assert result is not None, "Required property 'slot_constraint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slot_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#slot_type LexIntent#slot_type}.'''
        result = self._values.get("slot_type")
        assert result is not None, "Required property 'slot_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#description LexIntent#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#priority LexIntent#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def response_card(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.'''
        result = self._values.get("response_card")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_utterances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#sample_utterances LexIntent#sample_utterances}.'''
        result = self._values.get("sample_utterances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def slot_type_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#slot_type_version LexIntent#slot_type_version}.'''
        result = self._values.get("slot_type_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_elicitation_prompt(
        self,
    ) -> typing.Optional["LexIntentSlotValueElicitationPrompt"]:
        '''value_elicitation_prompt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#value_elicitation_prompt LexIntent#value_elicitation_prompt}
        '''
        result = self._values.get("value_elicitation_prompt")
        return typing.cast(typing.Optional["LexIntentSlotValueElicitationPrompt"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentSlot(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentSlotList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentSlotList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79d3cfd2d4f412716d8f2128b45d2daef6d8c56f71dc3e970e8fa7680c9e983f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LexIntentSlotOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c05e779a013dcdac3b75b3e1c6f86fd5d8e5cab328880765ee9372f367a8ad2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LexIntentSlotOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4556b3b3320ecdba9088ebb0a9d478c99f3e86777f1bf1b5b6b2fad1bb506339)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d65bae7b352832b3ca87649f7bd76c31afd3cccfa8cc07bd1117f33d2a69f618)
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
            type_hints = typing.get_type_hints(_typecheckingstub__972ccdccb8a678fcde3096b9e66c49a26ea4a7bdd0570b6b0473ed97a57f01b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentSlot]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentSlot]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentSlot]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ddb612b789f22341efb2e4d06b71ea82b1b9643711244f7f053e5914626a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentSlotOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentSlotOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a48122a7e64f468c16e5a5d73eeca25c0c69f3f3cc988ca5b2bb6b13f8d2ce4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueElicitationPrompt")
    def put_value_elicitation_prompt(
        self,
        *,
        max_attempts: jsii.Number,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentSlotValueElicitationPromptMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#max_attempts LexIntent#max_attempts}.
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        value = LexIntentSlotValueElicitationPrompt(
            max_attempts=max_attempts, message=message, response_card=response_card
        )

        return typing.cast(None, jsii.invoke(self, "putValueElicitationPrompt", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetResponseCard")
    def reset_response_card(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCard", []))

    @jsii.member(jsii_name="resetSampleUtterances")
    def reset_sample_utterances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleUtterances", []))

    @jsii.member(jsii_name="resetSlotTypeVersion")
    def reset_slot_type_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlotTypeVersion", []))

    @jsii.member(jsii_name="resetValueElicitationPrompt")
    def reset_value_elicitation_prompt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueElicitationPrompt", []))

    @builtins.property
    @jsii.member(jsii_name="valueElicitationPrompt")
    def value_elicitation_prompt(
        self,
    ) -> "LexIntentSlotValueElicitationPromptOutputReference":
        return typing.cast("LexIntentSlotValueElicitationPromptOutputReference", jsii.get(self, "valueElicitationPrompt"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCardInput")
    def response_card_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseCardInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleUtterancesInput")
    def sample_utterances_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sampleUtterancesInput"))

    @builtins.property
    @jsii.member(jsii_name="slotConstraintInput")
    def slot_constraint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slotConstraintInput"))

    @builtins.property
    @jsii.member(jsii_name="slotTypeInput")
    def slot_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slotTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="slotTypeVersionInput")
    def slot_type_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slotTypeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="valueElicitationPromptInput")
    def value_elicitation_prompt_input(
        self,
    ) -> typing.Optional["LexIntentSlotValueElicitationPrompt"]:
        return typing.cast(typing.Optional["LexIntentSlotValueElicitationPrompt"], jsii.get(self, "valueElicitationPromptInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d0d5bed461a1701fa040d20edff53a7303cd0b5b733ab4488b3a59a8b395b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066add88675f0c8ba941c5fab4d004223ca2369f7cbd0e93e7eca02b058f38c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d297d3d59fa0edfe32af70ad275f9bddbcb702d2d5b6da81b91fd9da2224a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCard")
    def response_card(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseCard"))

    @response_card.setter
    def response_card(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc55c9586ac1b6dd8d12c8506371118648df2953254d8fd0348cbfbd5aef169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleUtterances")
    def sample_utterances(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sampleUtterances"))

    @sample_utterances.setter
    def sample_utterances(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd6e7d78a6a85ea46c1eb12a7ecd2e1bf4f1502c249842bf6de3611b9df617c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleUtterances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slotConstraint")
    def slot_constraint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slotConstraint"))

    @slot_constraint.setter
    def slot_constraint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e2950eb935d50dccef45d76d5972395e404ff1a10dc373c42a0847a203bdd13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slotConstraint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slotType")
    def slot_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slotType"))

    @slot_type.setter
    def slot_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f222f76deb888cac2b1bf86e396873e67dca09b38ca72f037c5369f06bcd2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slotType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slotTypeVersion")
    def slot_type_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slotTypeVersion"))

    @slot_type_version.setter
    def slot_type_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3719dcdad7da7d737cf83c198dd6c026fd9131c50e55eb93f9df0daa0cf464ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slotTypeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentSlot]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentSlot]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentSlot]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efb0021c4c7d439c4f0df5488a59e2dd2b7c151574749062d73423f2f275a43b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentSlotValueElicitationPrompt",
    jsii_struct_bases=[],
    name_mapping={
        "max_attempts": "maxAttempts",
        "message": "message",
        "response_card": "responseCard",
    },
)
class LexIntentSlotValueElicitationPrompt:
    def __init__(
        self,
        *,
        max_attempts: jsii.Number,
        message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LexIntentSlotValueElicitationPromptMessage", typing.Dict[builtins.str, typing.Any]]]],
        response_card: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#max_attempts LexIntent#max_attempts}.
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        :param response_card: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ba8392a646e7747d5cd8a2746abc1950d5304b3dd8742dbea8551c64ae7131)
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument response_card", value=response_card, expected_type=type_hints["response_card"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_attempts": max_attempts,
            "message": message,
        }
        if response_card is not None:
            self._values["response_card"] = response_card

    @builtins.property
    def max_attempts(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#max_attempts LexIntent#max_attempts}.'''
        result = self._values.get("max_attempts")
        assert result is not None, "Required property 'max_attempts' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def message(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentSlotValueElicitationPromptMessage"]]:
        '''message block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#message LexIntent#message}
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LexIntentSlotValueElicitationPromptMessage"]], result)

    @builtins.property
    def response_card(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#response_card LexIntent#response_card}.'''
        result = self._values.get("response_card")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentSlotValueElicitationPrompt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentSlotValueElicitationPromptMessage",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "content_type": "contentType",
        "group_number": "groupNumber",
    },
)
class LexIntentSlotValueElicitationPromptMessage:
    def __init__(
        self,
        *,
        content: builtins.str,
        content_type: builtins.str,
        group_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.
        :param group_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3560bf6576230500a6e2e679222a7269be4bee9f85470fd149d65890a5abbf29)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument group_number", value=group_number, expected_type=type_hints["group_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "content_type": content_type,
        }
        if group_number is not None:
            self._values["group_number"] = group_number

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content LexIntent#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#content_type LexIntent#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#group_number LexIntent#group_number}.'''
        result = self._values.get("group_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentSlotValueElicitationPromptMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentSlotValueElicitationPromptMessageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentSlotValueElicitationPromptMessageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6da25f769a9a25cdc9c185774759ff0def1978b4674ee84f35a9b01b29dea7ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LexIntentSlotValueElicitationPromptMessageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378353b0fda5f9179d3cc6af7ecabebd4ece7a71bb4a32663e21e6f088b8b388)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LexIntentSlotValueElicitationPromptMessageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43ec747b07744cdc0565c60c80482d718ae801a3a91f3c811ddba91df46d7ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb0aec23a0a19b5bb6fb26be67407d1101978e9ebe32e56e9e815d41f40c4219)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbe35898a47e282c32f25ed4e7a12a9a3678c2be0f61ad5af8fb922fbd6c8636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentSlotValueElicitationPromptMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentSlotValueElicitationPromptMessage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentSlotValueElicitationPromptMessage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0575f2390df0718841c72c7ced1affa64068ea91156adf2fa1c380491e9ce5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentSlotValueElicitationPromptMessageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentSlotValueElicitationPromptMessageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af9cba1ba7f95026a70572de71b733dd46d27a88a13e2137093a66636b18bcbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGroupNumber")
    def reset_group_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupNumber", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupNumberInput")
    def group_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__473eef64edafbfe37e99be74c86465cabbcd05d1fcffe928446ccb39f4e54731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d254b04c9964960a3e75ae5e4200f36358af44efd449b3af5276fe9bd70ae41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupNumber")
    def group_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupNumber"))

    @group_number.setter
    def group_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3638f60257cf57d2f9631139e5128f9f2692ff409d7290ee6a268c20ea83342d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentSlotValueElicitationPromptMessage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentSlotValueElicitationPromptMessage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentSlotValueElicitationPromptMessage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c2092bfd8212932195abde78aff12e82d0dd85ddae72ae7fc80a6ed047871d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LexIntentSlotValueElicitationPromptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentSlotValueElicitationPromptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a67122596febaad59038559f754dc5b1a8be1366149f0de47e83877a715ea2fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMessage")
    def put_message(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentSlotValueElicitationPromptMessage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aca8a48ea2eeded9fb359530b6c567da73c01d87d6edeaa15e5538f2519f7aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessage", [value]))

    @jsii.member(jsii_name="resetResponseCard")
    def reset_response_card(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCard", []))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> LexIntentSlotValueElicitationPromptMessageList:
        return typing.cast(LexIntentSlotValueElicitationPromptMessageList, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsInput")
    def max_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentSlotValueElicitationPromptMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentSlotValueElicitationPromptMessage]]], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCardInput")
    def response_card_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseCardInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAttempts")
    def max_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttempts"))

    @max_attempts.setter
    def max_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74bd0133c35e3594d9ee5d8a6f4c3254658f94208a875a0cb07f7a9f214c9d71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCard")
    def response_card(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseCard"))

    @response_card.setter
    def response_card(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9ba1b88cd0f9195910bc9de8c549e21b1d5ff16d992ce03fbda65e61f6ea19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LexIntentSlotValueElicitationPrompt]:
        return typing.cast(typing.Optional[LexIntentSlotValueElicitationPrompt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LexIntentSlotValueElicitationPrompt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b558f8fbc113a52d9f8c465e1ba8156daebaed01b1962008399b701c3e1b9129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class LexIntentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#create LexIntent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#delete LexIntent#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#update LexIntent#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300a5b95d9ec6d53edebaaa97caca9e1d84fae5d2b369eecb5f393f1a04c58f2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#create LexIntent#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#delete LexIntent#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lex_intent#update LexIntent#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexIntentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LexIntentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexIntent.LexIntentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0817fff424a3e6e60cabf50c5a724dd32d3da19928bb703cc5a89e737c967113)
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
            type_hints = typing.get_type_hints(_typecheckingstub__387beacd4a01b33505bfc6a3d1ffdd620197562d74f64251e9c371fe796362a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__745cb8e914549f14581f831d758260b418b228cad5d41f344825f64af51d8e9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c394e086b834ce0c9c2eda3a8af9acf5413054901f0db6a30fe81522160eb2c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb26b33d74446e79481246f29aa0feeddf5dae850340b0c8900a033ed41649aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LexIntent",
    "LexIntentConclusionStatement",
    "LexIntentConclusionStatementMessage",
    "LexIntentConclusionStatementMessageList",
    "LexIntentConclusionStatementMessageOutputReference",
    "LexIntentConclusionStatementOutputReference",
    "LexIntentConfig",
    "LexIntentConfirmationPrompt",
    "LexIntentConfirmationPromptMessage",
    "LexIntentConfirmationPromptMessageList",
    "LexIntentConfirmationPromptMessageOutputReference",
    "LexIntentConfirmationPromptOutputReference",
    "LexIntentDialogCodeHook",
    "LexIntentDialogCodeHookOutputReference",
    "LexIntentFollowUpPrompt",
    "LexIntentFollowUpPromptOutputReference",
    "LexIntentFollowUpPromptPrompt",
    "LexIntentFollowUpPromptPromptMessage",
    "LexIntentFollowUpPromptPromptMessageList",
    "LexIntentFollowUpPromptPromptMessageOutputReference",
    "LexIntentFollowUpPromptPromptOutputReference",
    "LexIntentFollowUpPromptRejectionStatement",
    "LexIntentFollowUpPromptRejectionStatementMessage",
    "LexIntentFollowUpPromptRejectionStatementMessageList",
    "LexIntentFollowUpPromptRejectionStatementMessageOutputReference",
    "LexIntentFollowUpPromptRejectionStatementOutputReference",
    "LexIntentFulfillmentActivity",
    "LexIntentFulfillmentActivityCodeHook",
    "LexIntentFulfillmentActivityCodeHookOutputReference",
    "LexIntentFulfillmentActivityOutputReference",
    "LexIntentRejectionStatement",
    "LexIntentRejectionStatementMessage",
    "LexIntentRejectionStatementMessageList",
    "LexIntentRejectionStatementMessageOutputReference",
    "LexIntentRejectionStatementOutputReference",
    "LexIntentSlot",
    "LexIntentSlotList",
    "LexIntentSlotOutputReference",
    "LexIntentSlotValueElicitationPrompt",
    "LexIntentSlotValueElicitationPromptMessage",
    "LexIntentSlotValueElicitationPromptMessageList",
    "LexIntentSlotValueElicitationPromptMessageOutputReference",
    "LexIntentSlotValueElicitationPromptOutputReference",
    "LexIntentTimeouts",
    "LexIntentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9c2144e0e09490de9a676ffc57b21e43232707acb66154ced92eacd3f20f0237(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    fulfillment_activity: typing.Union[LexIntentFulfillmentActivity, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    conclusion_statement: typing.Optional[typing.Union[LexIntentConclusionStatement, typing.Dict[builtins.str, typing.Any]]] = None,
    confirmation_prompt: typing.Optional[typing.Union[LexIntentConfirmationPrompt, typing.Dict[builtins.str, typing.Any]]] = None,
    create_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    dialog_code_hook: typing.Optional[typing.Union[LexIntentDialogCodeHook, typing.Dict[builtins.str, typing.Any]]] = None,
    follow_up_prompt: typing.Optional[typing.Union[LexIntentFollowUpPrompt, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    parent_intent_signature: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rejection_statement: typing.Optional[typing.Union[LexIntentRejectionStatement, typing.Dict[builtins.str, typing.Any]]] = None,
    sample_utterances: typing.Optional[typing.Sequence[builtins.str]] = None,
    slot: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentSlot, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[LexIntentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e63bb3ceb111cff1eb709151e522f76f3947f3dfbc02ca57103d20860b24f5fa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea235c48aab0c745330246afe4205aa0afeb4a73aea350c2298639b6085c829(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentSlot, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8615ebd157e9ec139384b61242f12df771ebd2b627a8154f44b37d327767ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03ff5c81a62623dae2e19be40c12ccdb179fd4f38d5109ea30607849b45fd1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea30864d9c7ef8085ae304d5dd34419ed98c76028dc97e6fc256eaa3ec40b37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfaf6d63ed2a9d536009198f2266c1f7d6afee7d72e1d55ecfc486b7dbc42a2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cbb539e656e451aacbd84534dfcabed44a13449cf3171aca5fade09485311f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad7f4aa450473f557b2da3cb3146de7c72e13b2c6ef7445df03ba39dfc56946(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8278c58dab150a9c8c16f2aff6d9e2525d8416c4cfa74fe81f81955ab0f6abc9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3499f83ea5c616290b8d6966c74dd90e9dffb4a2da0c5260e730ae2cd75fcd5(
    *,
    message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentConclusionStatementMessage, typing.Dict[builtins.str, typing.Any]]]],
    response_card: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e454ec4eeaed80f69ef62bd7ea498ba6d9ed31b8bf53fe43c239cf766cc0f2d(
    *,
    content: builtins.str,
    content_type: builtins.str,
    group_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af24de87ba3be73b62d554fb40877a29d93fad64481ca2bf31469cbe41da87e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a8bcc0239ee01c49c1a6761cd848855e760aeed388aa0fc1f56224f91c771e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9435a56c40aeb1a001f12258924c81b556358647c708992d4584c9845515835c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb19113e3e05b5bb94cb2a0509c0d0d740c7171ef897c13b4fe1323d954d9b3e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de20b0a82534e4fa6c6f99520fb3a6173ee142d4a47d5814f5b951d9b97aba7a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b815d01ce84dc8ffebfb4c490ad41019a7dab1eb10181c9a541f9483293db37d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConclusionStatementMessage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2f05d082f49c25dbf6a8f33edb24d17b5131c5b47a80a8215a8d9cead85dbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf30ea567a4a5db2a19687908736a767fedfbe71061d029a9fd536a50dc4229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674632209759468bbf94fee41f83544f8f9cb41430929403cc2dbe455eed1390(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be49adf19cd0c68deac1f1ab5d2809f66c63d45a340e06f9360f2e0167dff0a5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b6c724a39d698ffdf00808df83cf6bb33ca72eb31d01802a978bd4405badc7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentConclusionStatementMessage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c02a7a806ddc9646c40be5bcacdc3b4dd272637908f8355e0c36e80f8b22cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356909beb91b0c7099d1ef279746b3cd3a9d9de1ca49f6405247d1f89dcfa3f7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentConclusionStatementMessage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c253a7a9f7a45d245df38bdeff191615ae4fc6164013f58f38cabed3fdcce8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e39b45072252dbc827d3d155cb1110a8934430fdd3fe2e005b4d68f2b63cd4(
    value: typing.Optional[LexIntentConclusionStatement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b7e143f443badd936eecae335f13df0d9822538d812e848838dce575938bc0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    fulfillment_activity: typing.Union[LexIntentFulfillmentActivity, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    conclusion_statement: typing.Optional[typing.Union[LexIntentConclusionStatement, typing.Dict[builtins.str, typing.Any]]] = None,
    confirmation_prompt: typing.Optional[typing.Union[LexIntentConfirmationPrompt, typing.Dict[builtins.str, typing.Any]]] = None,
    create_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    dialog_code_hook: typing.Optional[typing.Union[LexIntentDialogCodeHook, typing.Dict[builtins.str, typing.Any]]] = None,
    follow_up_prompt: typing.Optional[typing.Union[LexIntentFollowUpPrompt, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    parent_intent_signature: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rejection_statement: typing.Optional[typing.Union[LexIntentRejectionStatement, typing.Dict[builtins.str, typing.Any]]] = None,
    sample_utterances: typing.Optional[typing.Sequence[builtins.str]] = None,
    slot: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentSlot, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[LexIntentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069b083d5851c6d8af449ba59329e5f19a26aa341d44a1e87bf87b60ed98bec0(
    *,
    max_attempts: jsii.Number,
    message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentConfirmationPromptMessage, typing.Dict[builtins.str, typing.Any]]]],
    response_card: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df59af37a3ed9eef06c13187efb053178d19e9022f385284636324fa4211e5a3(
    *,
    content: builtins.str,
    content_type: builtins.str,
    group_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2dd91db1c9ca75f32eeafb8dba84346645e3047f561ec4e8780821fa16a139f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1050410aca609aa9ea193c0330375aaa1a82d22c28ba7a10de17e072aca94928(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825d635394b6a4a504c7a70366aea7f196456b8846c30ec43b19002417f9636d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664a51020afb6d1450709181067a1203aba113a5672c84153304f9dbf8d0b837(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc88430dabb5107ea81f3d09d0dd3c828fea614896b1d678af2509eb2fe7e4c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fa711ffcb61c3ebee311efaacff010e38618f939d547f735fbf80405cadd0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentConfirmationPromptMessage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c301ac9e1f2c02f1404b59dc8741d667ffe90ec24a0a0f2b0a3839ad2e0b9b22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d05e3ea71aac4752ecc16448d96eb1ce95d7dbda865588b12d2e9b8b5e5171(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d462bd726e802b2916ac246242471caf94c3d361b18a50194ffdfaaa74dbf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb641c4465164e1f17704634d1c53093839adc68102327f1abefac5bdee7e18(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873125d7b2844d07fcdee080a00bc63245220a93892336ca68f12f7d612bf094(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentConfirmationPromptMessage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377f0d741ad767e309ddf4458bf8eb27a69718c756915a9c0d0ce4b30f02c1c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d344a910a5daf24b0fbfa2fcd946c83511ab2afd7476a6e50036d9b3df3df4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentConfirmationPromptMessage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39839d5c30ac26fbddc031844b341175ea9042fc64f6b03db76f25c05ab52a2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cb769d74750a99fbb91c097b66fd76fa96827ce5c40fda629785d4604217b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19615d85a2ec1f9af8c9cc803e13c6b78119b3d3d963868e5402a2b7c2324b04(
    value: typing.Optional[LexIntentConfirmationPrompt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abaf6712bc968dcb04290fa0a0c6a02bae7bc2a4d818f3835cbf7200d4e2c533(
    *,
    message_version: builtins.str,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888d3a3f60639a2d87e96208c7d7fd076034b7bfd0ce50c223af0d4a874b2a45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b7db0652b8678ffca78ee0ce0f175bf7e6ac749cc2855b1e145d8c24f2dc86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead7d665896ea12b4ff814bf4399c6a9182e5984d7e044dfcf183e8083780504(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ad388869e40ce648f1d614b28f0592d3a3de7a1e10758b8268660c5c8de1a8(
    value: typing.Optional[LexIntentDialogCodeHook],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536259bd872a796d73a805c5dc8b64d6727a3277a9b3e1cbaf8d83df80341a58(
    *,
    prompt: typing.Union[LexIntentFollowUpPromptPrompt, typing.Dict[builtins.str, typing.Any]],
    rejection_statement: typing.Union[LexIntentFollowUpPromptRejectionStatement, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9d1acfd29284f208b4a5c9cc85696898637b4b91cdfa3f4651d55e1b1dadd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005004290a1cb20ad270c9830631acbd5703d06e511f30c46bb286c7786324c9(
    value: typing.Optional[LexIntentFollowUpPrompt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6953579615d403cc6ee6c7e62f75a5103c4abcc8a3dadfb3f46ff6ccb6c173(
    *,
    max_attempts: jsii.Number,
    message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentFollowUpPromptPromptMessage, typing.Dict[builtins.str, typing.Any]]]],
    response_card: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6b879b20672f9bcbec5ea577b0f96ec0179ac994a2ca5540f1bbb379c4adf3(
    *,
    content: builtins.str,
    content_type: builtins.str,
    group_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06c0980f82c28d28732d8f57634f4a60fb9cfd94a9c548b29e7606179ff3a35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b091dfa8eac8015fcdac65fc59d7b45eefa07e6f412e437209338a299298ad4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc6cfe3b77821f5de3331cbe7233033636761d7048d24b84ca0245d6bc4f532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4925ace3501f6e9d0a808946b36810c1163c1efc8d9c42200d997cc55c6fd22(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40548335c4a0a77046b04aa940758b670aa81ab73e3adb6c13be9d56dbbbdafc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed61d3b025f81aa1672bf94fca7592c469cb0651da8b6115d979919ced7ff11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptPromptMessage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b6d3fbd6a01cde526dddc4eea84bf38706be87d0f9d5a09f7f84e20daba6b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e58cc1627b6781c2e80f25999b441c33ce6fd6da722c01676c6c8ff8e9c4653(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555e41232eadf51e3a0d11187093917d7549fca01d2efe5c48532ef1be30df5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dfbdf45e46af0916e3e2bd943cd86c84e5ecfe1cf328b089a2f59472c6ecb6b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed2cbbe3999e318d61824dfac82497744d18037ba985fb38ddcbecd5a115b7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentFollowUpPromptPromptMessage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed903d25fec93da994690bd5b831bf55cd7fd4ba7055f2d865e19e500d8e80c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f223cac5ac5b04a1ad9f653c2f2063c660ffbc4b2d1d1febbc7389dd720e7d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentFollowUpPromptPromptMessage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267f79aa1e754f7e408ccb8f9560bc083e3e93a44fd88313adbdce24ff32f8bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6dc4c7e21413c2151b782213a14a0485b52111b4f98478550c6d9e91d02eb7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87360d1fd197a69d7722007901009375aacf1cf526e828409eaa4595ebe814ea(
    value: typing.Optional[LexIntentFollowUpPromptPrompt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d700d1e64714b35f6483cbe17dd38c369c9f6a01dd45a50d0f747debdc7a7c4c(
    *,
    message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentFollowUpPromptRejectionStatementMessage, typing.Dict[builtins.str, typing.Any]]]],
    response_card: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddc3db4c6d0f36c1040005784e7037bec891a7a0723663e9a3135d27549ab83(
    *,
    content: builtins.str,
    content_type: builtins.str,
    group_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4cfd77de05610235c8a4a7b9bba8640f4b5b978e8a6e884d7735a6336160d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6443e2810bd33db9901c28219b0d50b136b5817521c73c615b739cd62557d226(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02d73da939ec85d0176c28ef1386f9b98c9e5121f3e3a5631ad067ec9a2357c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd26d5d1e65f3176266d0d4a5b98ee8b724972f57cc5a590e554543fb56740d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fc16425b1ad451d7b98fed1dd8c8348ef77fe28447c6be547ae22cc61364ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61b068cb94884ef3c1e7a8e76e036422919bbf229cabc21681ad609289e585e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentFollowUpPromptRejectionStatementMessage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff029365fa5e6a5e4e4da79217cbe78a871ae3724216bbf99c64b414f3a1e3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0283293e53a2a02dc2c1588ad1495579d04a92674ff1a9a8f7f2c919a11df3e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f4f507ac0d1762506cab975ae14084b0bfe5605c24ed9912faacdf91c563ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77abb3ca729cdb3b59ad766cbc2a1a8bd41622a996b52e9ac82f61a139db4ca3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997965c8c0248334ace5f210e83e2e38584834987b6dc6e50b89af0c63ad0782(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentFollowUpPromptRejectionStatementMessage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf31fddb585476d4e7645cf5ed33a6d186eb875a6e946facb98410dc5a12b252(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4700a496342f681423a1742af628f9a5e6999e268a8a12b58ef1745583725fb3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentFollowUpPromptRejectionStatementMessage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1392c3f462f83ebdbac48587db747fbb62408823f5536bb9e7ec57f9c7c19f9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c69260760d7ab8da522c09e172c0496ab118acd2b6b71c349e5dedfadb12c9(
    value: typing.Optional[LexIntentFollowUpPromptRejectionStatement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3348b73a2f18871dce9468c07bfd8c904ba3c3c6a223690e0f75d8e9094478dc(
    *,
    type: builtins.str,
    code_hook: typing.Optional[typing.Union[LexIntentFulfillmentActivityCodeHook, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873e1310a6ec5a47f4fc998632d903852514a7b38f60f97b8a033d55995a1087(
    *,
    message_version: builtins.str,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1a861fb9a0257d42db59b5727da2ece3b870c30ab798a6b2d8b4f7d4cd77b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de4e09d9c90fd8e572bbc6ccc30b69de5778e91dcfda383e9686473e023f26e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab1ac4a3c5787a2c419364dacfa9102902f6f70128e667c9fe18dcec3cac0de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f843236ea1be990c89638500db577ed5b035868c5a4762149d2a30b9eb5ad6c(
    value: typing.Optional[LexIntentFulfillmentActivityCodeHook],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151cb373be413617374e2f1f450f8c0ce383a195bfc78aacfd03b8191e34ad59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ddb4e47ee81d6b8fd15891f62fe536226c66a0b3cc43cba459f35ecf19e8db1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73954779cb7c1b960c3fa9966b273edf6e49fe31b87ec63a10dc00e8e980b755(
    value: typing.Optional[LexIntentFulfillmentActivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58aa22fbf0dd907c468b165f4c719e089e46f0df1141337491a50b937bc66bf4(
    *,
    message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentRejectionStatementMessage, typing.Dict[builtins.str, typing.Any]]]],
    response_card: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90ffe216ca89019b5256c40e7a4e9eec4d0820a0270ccfbada4ac1fe9245024(
    *,
    content: builtins.str,
    content_type: builtins.str,
    group_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7122b803cec0e41d4bfec802e0e166cec7ee986b92da1958a7d1fed2f8bee0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247176ab6d03a21c07372eb31107f6ed6f7f5fc548017888e3f00c690e267a24(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94de943428617484412e5167f750b0ab6de42bc9ea85e2be5583c3767c296f03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032bbf3ed64d9df3fc466ef73545b52726c3b8efaaaa26d8bfab734608379075(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd151dd11246db66aef30df0da0c035c573de4f56261b4b7bf14004e42b84fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b4ad91e961afd0740061b17ae5961df2f0f2b30fab4a85184f842c001d294c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentRejectionStatementMessage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cb8e3f1e50ec5d7acb22765343b76e60800472d2fdb16e38fdb914b9ba2e84c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3520dae501e847d1d0cc9994fd80979aed1249848f39abc4aa901637a96e135c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26a2ebf07b1cb677d8ef89247c9e4873058ac0c655c01c1cbd9056eb26a745b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204cbe23124636bc6bc3e078f98ade2ba14027668eebc78e56dc84dff6d6aa91(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cdef1b1a8222951791530c8f8a8b0eebe397a49695411f340cb3984884e3a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentRejectionStatementMessage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6019609113eba373fb6766aa2544db194af32230081d0e1e24eeabb18ba7937a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e75492a161a06c98b7fd4b7c9f7ef5727ab5a5db32686b9ecf132d041aa143(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentRejectionStatementMessage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9fc70429fbe97024b7f22d56a9be9f945b994321d2603ff908ec8bb9a803da5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd5566d68837563b43b0d556d692f5e467cc2afba7c050ec80d5ae21c2fcf5a(
    value: typing.Optional[LexIntentRejectionStatement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b54f757b8cec25dca59cb4546a6a9d612ae1f6171ef9ee2df7db8a630582a2f(
    *,
    name: builtins.str,
    slot_constraint: builtins.str,
    slot_type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    response_card: typing.Optional[builtins.str] = None,
    sample_utterances: typing.Optional[typing.Sequence[builtins.str]] = None,
    slot_type_version: typing.Optional[builtins.str] = None,
    value_elicitation_prompt: typing.Optional[typing.Union[LexIntentSlotValueElicitationPrompt, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d3cfd2d4f412716d8f2128b45d2daef6d8c56f71dc3e970e8fa7680c9e983f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c05e779a013dcdac3b75b3e1c6f86fd5d8e5cab328880765ee9372f367a8ad2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4556b3b3320ecdba9088ebb0a9d478c99f3e86777f1bf1b5b6b2fad1bb506339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65bae7b352832b3ca87649f7bd76c31afd3cccfa8cc07bd1117f33d2a69f618(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972ccdccb8a678fcde3096b9e66c49a26ea4a7bdd0570b6b0473ed97a57f01b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ddb612b789f22341efb2e4d06b71ea82b1b9643711244f7f053e5914626a87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentSlot]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a48122a7e64f468c16e5a5d73eeca25c0c69f3f3cc988ca5b2bb6b13f8d2ce4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d0d5bed461a1701fa040d20edff53a7303cd0b5b733ab4488b3a59a8b395b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066add88675f0c8ba941c5fab4d004223ca2369f7cbd0e93e7eca02b058f38c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d297d3d59fa0edfe32af70ad275f9bddbcb702d2d5b6da81b91fd9da2224a7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc55c9586ac1b6dd8d12c8506371118648df2953254d8fd0348cbfbd5aef169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd6e7d78a6a85ea46c1eb12a7ecd2e1bf4f1502c249842bf6de3611b9df617c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2950eb935d50dccef45d76d5972395e404ff1a10dc373c42a0847a203bdd13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f222f76deb888cac2b1bf86e396873e67dca09b38ca72f037c5369f06bcd2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3719dcdad7da7d737cf83c198dd6c026fd9131c50e55eb93f9df0daa0cf464ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb0021c4c7d439c4f0df5488a59e2dd2b7c151574749062d73423f2f275a43b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentSlot]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ba8392a646e7747d5cd8a2746abc1950d5304b3dd8742dbea8551c64ae7131(
    *,
    max_attempts: jsii.Number,
    message: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentSlotValueElicitationPromptMessage, typing.Dict[builtins.str, typing.Any]]]],
    response_card: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3560bf6576230500a6e2e679222a7269be4bee9f85470fd149d65890a5abbf29(
    *,
    content: builtins.str,
    content_type: builtins.str,
    group_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da25f769a9a25cdc9c185774759ff0def1978b4674ee84f35a9b01b29dea7ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378353b0fda5f9179d3cc6af7ecabebd4ece7a71bb4a32663e21e6f088b8b388(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43ec747b07744cdc0565c60c80482d718ae801a3a91f3c811ddba91df46d7ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0aec23a0a19b5bb6fb26be67407d1101978e9ebe32e56e9e815d41f40c4219(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe35898a47e282c32f25ed4e7a12a9a3678c2be0f61ad5af8fb922fbd6c8636(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0575f2390df0718841c72c7ced1affa64068ea91156adf2fa1c380491e9ce5c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LexIntentSlotValueElicitationPromptMessage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9cba1ba7f95026a70572de71b733dd46d27a88a13e2137093a66636b18bcbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473eef64edafbfe37e99be74c86465cabbcd05d1fcffe928446ccb39f4e54731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d254b04c9964960a3e75ae5e4200f36358af44efd449b3af5276fe9bd70ae41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3638f60257cf57d2f9631139e5128f9f2692ff409d7290ee6a268c20ea83342d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c2092bfd8212932195abde78aff12e82d0dd85ddae72ae7fc80a6ed047871d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentSlotValueElicitationPromptMessage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67122596febaad59038559f754dc5b1a8be1366149f0de47e83877a715ea2fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aca8a48ea2eeded9fb359530b6c567da73c01d87d6edeaa15e5538f2519f7aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LexIntentSlotValueElicitationPromptMessage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74bd0133c35e3594d9ee5d8a6f4c3254658f94208a875a0cb07f7a9f214c9d71(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9ba1b88cd0f9195910bc9de8c549e21b1d5ff16d992ce03fbda65e61f6ea19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b558f8fbc113a52d9f8c465e1ba8156daebaed01b1962008399b701c3e1b9129(
    value: typing.Optional[LexIntentSlotValueElicitationPrompt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300a5b95d9ec6d53edebaaa97caca9e1d84fae5d2b369eecb5f393f1a04c58f2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0817fff424a3e6e60cabf50c5a724dd32d3da19928bb703cc5a89e737c967113(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387beacd4a01b33505bfc6a3d1ffdd620197562d74f64251e9c371fe796362a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745cb8e914549f14581f831d758260b418b228cad5d41f344825f64af51d8e9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c394e086b834ce0c9c2eda3a8af9acf5413054901f0db6a30fe81522160eb2c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb26b33d74446e79481246f29aa0feeddf5dae850340b0c8900a033ed41649aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LexIntentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
