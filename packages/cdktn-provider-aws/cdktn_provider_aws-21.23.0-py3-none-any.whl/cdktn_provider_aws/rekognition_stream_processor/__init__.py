r'''
# `aws_rekognition_stream_processor`

Refer to the Terraform Registry for docs: [`aws_rekognition_stream_processor`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor).
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


class RekognitionStreamProcessor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessor",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor aws_rekognition_stream_processor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        role_arn: builtins.str,
        data_sharing_preference: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorDataSharingPreference", typing.Dict[builtins.str, typing.Any]]]]] = None,
        input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorInput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        notification_channel: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorNotificationChannel", typing.Dict[builtins.str, typing.Any]]]]] = None,
        output: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorOutput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        regions_of_interest: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorRegionsOfInterest", typing.Dict[builtins.str, typing.Any]]]]] = None,
        settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RekognitionStreamProcessorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor aws_rekognition_stream_processor} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: An identifier you assign to the stream processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#name RekognitionStreamProcessor#name}
        :param role_arn: The Amazon Resource Number (ARN) of the IAM role that allows access to the stream processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#role_arn RekognitionStreamProcessor#role_arn}
        :param data_sharing_preference: data_sharing_preference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#data_sharing_preference RekognitionStreamProcessor#data_sharing_preference}
        :param input: input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#input RekognitionStreamProcessor#input}
        :param kms_key_id: The identifier for your AWS Key Management Service key (AWS KMS key). You can supply the Amazon Resource Name (ARN) of your KMS key, the ID of your KMS key, an alias for your KMS key, or an alias ARN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#kms_key_id RekognitionStreamProcessor#kms_key_id}
        :param notification_channel: notification_channel block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#notification_channel RekognitionStreamProcessor#notification_channel}
        :param output: output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#output RekognitionStreamProcessor#output}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#region RekognitionStreamProcessor#region}
        :param regions_of_interest: regions_of_interest block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#regions_of_interest RekognitionStreamProcessor#regions_of_interest}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#settings RekognitionStreamProcessor#settings}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#tags RekognitionStreamProcessor#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#timeouts RekognitionStreamProcessor#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690faf2084a4187ba423d9851ce6c5762f44bff2362c1dbce3c04eaff3339788)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = RekognitionStreamProcessorConfig(
            name=name,
            role_arn=role_arn,
            data_sharing_preference=data_sharing_preference,
            input=input,
            kms_key_id=kms_key_id,
            notification_channel=notification_channel,
            output=output,
            region=region,
            regions_of_interest=regions_of_interest,
            settings=settings,
            tags=tags,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a RekognitionStreamProcessor resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RekognitionStreamProcessor to import.
        :param import_from_id: The id of the existing RekognitionStreamProcessor that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RekognitionStreamProcessor to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed5927856c228091b2ae3ace94d33e32f706f86927a45543d4c4c405f8d8ea7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataSharingPreference")
    def put_data_sharing_preference(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorDataSharingPreference", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a278d794b5e885a14113f52194701040dd577370e3df7023bdd9bcc856c923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataSharingPreference", [value]))

    @jsii.member(jsii_name="putInput")
    def put_input(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorInput", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59906d49a4e38ed405063b499aace6b1c7a6261425840274c3a0519cb245b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInput", [value]))

    @jsii.member(jsii_name="putNotificationChannel")
    def put_notification_channel(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorNotificationChannel", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f30dfd1183ab9b930618711e4881f96af0bc88ebe6ea611ab2baf2e8a7ee074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotificationChannel", [value]))

    @jsii.member(jsii_name="putOutput")
    def put_output(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorOutput", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a374ab6d87b3613f19e25cf8fb831bc8354a8cbb2795d48eb45fb556eb296aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOutput", [value]))

    @jsii.member(jsii_name="putRegionsOfInterest")
    def put_regions_of_interest(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorRegionsOfInterest", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b6631cd319d90499adad4a76afc2ac43ec922968144e97f237dc040293c33b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegionsOfInterest", [value]))

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorSettings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce46377ec37515789ad58443b1daf14f3cbf8a5e12d70620729c85ebb01317d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#create RekognitionStreamProcessor#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#delete RekognitionStreamProcessor#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#update RekognitionStreamProcessor#update}
        '''
        value = RekognitionStreamProcessorTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataSharingPreference")
    def reset_data_sharing_preference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSharingPreference", []))

    @jsii.member(jsii_name="resetInput")
    def reset_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInput", []))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetNotificationChannel")
    def reset_notification_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationChannel", []))

    @jsii.member(jsii_name="resetOutput")
    def reset_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutput", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRegionsOfInterest")
    def reset_regions_of_interest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionsOfInterest", []))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="dataSharingPreference")
    def data_sharing_preference(
        self,
    ) -> "RekognitionStreamProcessorDataSharingPreferenceList":
        return typing.cast("RekognitionStreamProcessorDataSharingPreferenceList", jsii.get(self, "dataSharingPreference"))

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(self) -> "RekognitionStreamProcessorInputList":
        return typing.cast("RekognitionStreamProcessorInputList", jsii.get(self, "input"))

    @builtins.property
    @jsii.member(jsii_name="notificationChannel")
    def notification_channel(
        self,
    ) -> "RekognitionStreamProcessorNotificationChannelList":
        return typing.cast("RekognitionStreamProcessorNotificationChannelList", jsii.get(self, "notificationChannel"))

    @builtins.property
    @jsii.member(jsii_name="output")
    def output(self) -> "RekognitionStreamProcessorOutputList":
        return typing.cast("RekognitionStreamProcessorOutputList", jsii.get(self, "output"))

    @builtins.property
    @jsii.member(jsii_name="regionsOfInterest")
    def regions_of_interest(self) -> "RekognitionStreamProcessorRegionsOfInterestList":
        return typing.cast("RekognitionStreamProcessorRegionsOfInterestList", jsii.get(self, "regionsOfInterest"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "RekognitionStreamProcessorSettingsList":
        return typing.cast("RekognitionStreamProcessorSettingsList", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="streamProcessorArn")
    def stream_processor_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamProcessorArn"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RekognitionStreamProcessorTimeoutsOutputReference":
        return typing.cast("RekognitionStreamProcessorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataSharingPreferenceInput")
    def data_sharing_preference_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorDataSharingPreference"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorDataSharingPreference"]]], jsii.get(self, "dataSharingPreferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="inputInput")
    def input_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorInput"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorInput"]]], jsii.get(self, "inputInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationChannelInput")
    def notification_channel_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorNotificationChannel"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorNotificationChannel"]]], jsii.get(self, "notificationChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="outputInput")
    def output_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorOutput"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorOutput"]]], jsii.get(self, "outputInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="regionsOfInterestInput")
    def regions_of_interest_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorRegionsOfInterest"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorRegionsOfInterest"]]], jsii.get(self, "regionsOfInterestInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorSettings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorSettings"]]], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RekognitionStreamProcessorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RekognitionStreamProcessorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b5a43e178d3b3e423855ff26ede7ac26f3ee2ed89198e24ac4cce246779ff0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04fa4da728b1419df03462546d970b7f7cd33b2e34f6155ff73ff538e3e56e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a413111236ce8a92a058ad75149b30bc2e834e7e2e4f8c2c2713df3b15424c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83eaf56027f68fac88ec1a239cde3852c14b022f5c58cb3329a909d7712dae57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb21783025351be4aa2ccef7bb3fdc246fce36482cf526f331f5ef1cc1f7b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorConfig",
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
        "role_arn": "roleArn",
        "data_sharing_preference": "dataSharingPreference",
        "input": "input",
        "kms_key_id": "kmsKeyId",
        "notification_channel": "notificationChannel",
        "output": "output",
        "region": "region",
        "regions_of_interest": "regionsOfInterest",
        "settings": "settings",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class RekognitionStreamProcessorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        role_arn: builtins.str,
        data_sharing_preference: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorDataSharingPreference", typing.Dict[builtins.str, typing.Any]]]]] = None,
        input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorInput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        notification_channel: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorNotificationChannel", typing.Dict[builtins.str, typing.Any]]]]] = None,
        output: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorOutput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        regions_of_interest: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorRegionsOfInterest", typing.Dict[builtins.str, typing.Any]]]]] = None,
        settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RekognitionStreamProcessorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: An identifier you assign to the stream processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#name RekognitionStreamProcessor#name}
        :param role_arn: The Amazon Resource Number (ARN) of the IAM role that allows access to the stream processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#role_arn RekognitionStreamProcessor#role_arn}
        :param data_sharing_preference: data_sharing_preference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#data_sharing_preference RekognitionStreamProcessor#data_sharing_preference}
        :param input: input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#input RekognitionStreamProcessor#input}
        :param kms_key_id: The identifier for your AWS Key Management Service key (AWS KMS key). You can supply the Amazon Resource Name (ARN) of your KMS key, the ID of your KMS key, an alias for your KMS key, or an alias ARN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#kms_key_id RekognitionStreamProcessor#kms_key_id}
        :param notification_channel: notification_channel block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#notification_channel RekognitionStreamProcessor#notification_channel}
        :param output: output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#output RekognitionStreamProcessor#output}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#region RekognitionStreamProcessor#region}
        :param regions_of_interest: regions_of_interest block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#regions_of_interest RekognitionStreamProcessor#regions_of_interest}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#settings RekognitionStreamProcessor#settings}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#tags RekognitionStreamProcessor#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#timeouts RekognitionStreamProcessor#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = RekognitionStreamProcessorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f20a55d0c76692298f1777a4fa2fa3c5b8143675ef34fca018711665378f71e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument data_sharing_preference", value=data_sharing_preference, expected_type=type_hints["data_sharing_preference"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument notification_channel", value=notification_channel, expected_type=type_hints["notification_channel"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument regions_of_interest", value=regions_of_interest, expected_type=type_hints["regions_of_interest"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "role_arn": role_arn,
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
        if data_sharing_preference is not None:
            self._values["data_sharing_preference"] = data_sharing_preference
        if input is not None:
            self._values["input"] = input
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if notification_channel is not None:
            self._values["notification_channel"] = notification_channel
        if output is not None:
            self._values["output"] = output
        if region is not None:
            self._values["region"] = region
        if regions_of_interest is not None:
            self._values["regions_of_interest"] = regions_of_interest
        if settings is not None:
            self._values["settings"] = settings
        if tags is not None:
            self._values["tags"] = tags
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
    def name(self) -> builtins.str:
        '''An identifier you assign to the stream processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#name RekognitionStreamProcessor#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) of the IAM role that allows access to the stream processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#role_arn RekognitionStreamProcessor#role_arn}
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_sharing_preference(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorDataSharingPreference"]]]:
        '''data_sharing_preference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#data_sharing_preference RekognitionStreamProcessor#data_sharing_preference}
        '''
        result = self._values.get("data_sharing_preference")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorDataSharingPreference"]]], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorInput"]]]:
        '''input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#input RekognitionStreamProcessor#input}
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorInput"]]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for your AWS Key Management Service key (AWS KMS key).

        You can supply the Amazon Resource Name (ARN) of your KMS key, the ID of your KMS key, an alias for your KMS key, or an alias ARN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#kms_key_id RekognitionStreamProcessor#kms_key_id}
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_channel(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorNotificationChannel"]]]:
        '''notification_channel block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#notification_channel RekognitionStreamProcessor#notification_channel}
        '''
        result = self._values.get("notification_channel")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorNotificationChannel"]]], result)

    @builtins.property
    def output(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorOutput"]]]:
        '''output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#output RekognitionStreamProcessor#output}
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorOutput"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#region RekognitionStreamProcessor#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regions_of_interest(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorRegionsOfInterest"]]]:
        '''regions_of_interest block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#regions_of_interest RekognitionStreamProcessor#regions_of_interest}
        '''
        result = self._values.get("regions_of_interest")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorRegionsOfInterest"]]], result)

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorSettings"]]]:
        '''settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#settings RekognitionStreamProcessor#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorSettings"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#tags RekognitionStreamProcessor#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RekognitionStreamProcessorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#timeouts RekognitionStreamProcessor#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RekognitionStreamProcessorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorDataSharingPreference",
    jsii_struct_bases=[],
    name_mapping={"opt_in": "optIn"},
)
class RekognitionStreamProcessorDataSharingPreference:
    def __init__(
        self,
        *,
        opt_in: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param opt_in: Do you want to share data with Rekognition to improve model performance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#opt_in RekognitionStreamProcessor#opt_in}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a34a939ca677c21621ac6c0704080939eeb76d9607dddcfe8d731a10c87b376)
            check_type(argname="argument opt_in", value=opt_in, expected_type=type_hints["opt_in"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "opt_in": opt_in,
        }

    @builtins.property
    def opt_in(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Do you want to share data with Rekognition to improve model performance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#opt_in RekognitionStreamProcessor#opt_in}
        '''
        result = self._values.get("opt_in")
        assert result is not None, "Required property 'opt_in' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorDataSharingPreference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RekognitionStreamProcessorDataSharingPreferenceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorDataSharingPreferenceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__230db5099c754e39d54e6f7a44babb21a806af5afbc5f47ae99b1056b5b8ac59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorDataSharingPreferenceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc8da9fa291d3e3a3afc85af000cc0081a822d9984e3e0656689ee9ef58f7a9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorDataSharingPreferenceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fadf13f033114cc47fc1b962fff786ad6e8fa921ba3995e3f411f2ccac55160)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e586d68b9fc6a0e6f2dba939a14176f44f7023d158039154674f41fdbc5ce1d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__049af734818486a09b934312aa9e84e66d0adc7529e45d42995817b320c0273d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorDataSharingPreference]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorDataSharingPreference]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorDataSharingPreference]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e298b8cdee02b1ed88c429e2687cc5b39a50d6fae3a92ea30477f57d499d5bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorDataSharingPreferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorDataSharingPreferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b253fdb212836eea6c2c22f4a0ca761ca513b971a784cb1e0a0ec9a6bd54eac0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="optInInput")
    def opt_in_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optInInput"))

    @builtins.property
    @jsii.member(jsii_name="optIn")
    def opt_in(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optIn"))

    @opt_in.setter
    def opt_in(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cde652245407ea4ed4d4818e719cef2c85a847f490c0525f577662824814777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorDataSharingPreference]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorDataSharingPreference]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorDataSharingPreference]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f7a8975cf08b17c8a24cd8507996f1ae9a95c211290251a548df013af2546b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorInput",
    jsii_struct_bases=[],
    name_mapping={"kinesis_video_stream": "kinesisVideoStream"},
)
class RekognitionStreamProcessorInput:
    def __init__(
        self,
        *,
        kinesis_video_stream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorInputKinesisVideoStream", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param kinesis_video_stream: kinesis_video_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#kinesis_video_stream RekognitionStreamProcessor#kinesis_video_stream}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b739c8a693758390c11548245b826bee091459aa57f4802b5f7542767a3b77)
            check_type(argname="argument kinesis_video_stream", value=kinesis_video_stream, expected_type=type_hints["kinesis_video_stream"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kinesis_video_stream is not None:
            self._values["kinesis_video_stream"] = kinesis_video_stream

    @builtins.property
    def kinesis_video_stream(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorInputKinesisVideoStream"]]]:
        '''kinesis_video_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#kinesis_video_stream RekognitionStreamProcessor#kinesis_video_stream}
        '''
        result = self._values.get("kinesis_video_stream")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorInputKinesisVideoStream"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorInputKinesisVideoStream",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn"},
)
class RekognitionStreamProcessorInputKinesisVideoStream:
    def __init__(self, *, arn: builtins.str) -> None:
        '''
        :param arn: ARN of the Kinesis video stream stream that streams the source video. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#arn RekognitionStreamProcessor#arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd60f0ef08d34ce135d1539fc3ffa93d14638d8019ec7633e822ad15aebd4932)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
        }

    @builtins.property
    def arn(self) -> builtins.str:
        '''ARN of the Kinesis video stream stream that streams the source video.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#arn RekognitionStreamProcessor#arn}
        '''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorInputKinesisVideoStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RekognitionStreamProcessorInputKinesisVideoStreamList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorInputKinesisVideoStreamList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50a005594825fe7c93678b24db1609530a71dfafc3790f271e305f1c3014047c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorInputKinesisVideoStreamOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27955339e9cbf1efa288b3e4d66d216d15486f4297a904b27722edd2cc4c94ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorInputKinesisVideoStreamOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594fed579af69a938e6f05b71c2d8aedae8f319f20119cdbcaf3fcf910c2d1a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7afeefaf0972be2174b2b6ca602772cd75a654af60ac1f57eb3550feb9167ab0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__162080d2039656a4fbf5569a193476c148d227fc343a9a02ab3b1d7b237a535b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorInputKinesisVideoStream]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorInputKinesisVideoStream]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorInputKinesisVideoStream]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d6b583d94e432911ce0411041cb187c106257f48600e3db0161621c65d4ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorInputKinesisVideoStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorInputKinesisVideoStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a73f32ca7bdfced1a132bce82d1702346267d18f23f59464fc11fd62f4781acb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61376e7c2fd80b13bf79d523b7ee7723a76af8df138f4613015cf6d73f94faec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorInputKinesisVideoStream]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorInputKinesisVideoStream]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorInputKinesisVideoStream]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77bd1a44ecaa1abdfdb30098100e1a1544e21c3b50db82c804f130b1d44d5326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorInputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorInputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27382efa75280ae0067bdeed20f385751a2d3205e2dad0d3c76f433a62aabace)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorInputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0fa22ce7897bee4426bbaa81f732758d2c0fcb2d2306bdd81bdecac461e1a5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorInputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467ab808590092a7e710d1aa0c4e2e75d0af7bc6ab457517a14883790d0535b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__388da6c004af5a6066ee694dce3ecfd4edde2db3be8f8a78106c6fcad7a8ee2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c58e60d0885b49b63e827a392baad15d8a79dcb74cf6e3530257c14b510b3ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorInput]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorInput]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorInput]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef3ee1208c8978add1314498555db652fa9cd9d59e480deb9b0313fc60707e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3b7b46273e2bd6b25667a8b41bc67d19ec909b90ac0be776134277550e6d6a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putKinesisVideoStream")
    def put_kinesis_video_stream(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorInputKinesisVideoStream, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1dc41de59cd8cb6c745a0b70b09a7718dd5fc3deb69f783cb28facc0601ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKinesisVideoStream", [value]))

    @jsii.member(jsii_name="resetKinesisVideoStream")
    def reset_kinesis_video_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisVideoStream", []))

    @builtins.property
    @jsii.member(jsii_name="kinesisVideoStream")
    def kinesis_video_stream(
        self,
    ) -> RekognitionStreamProcessorInputKinesisVideoStreamList:
        return typing.cast(RekognitionStreamProcessorInputKinesisVideoStreamList, jsii.get(self, "kinesisVideoStream"))

    @builtins.property
    @jsii.member(jsii_name="kinesisVideoStreamInput")
    def kinesis_video_stream_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorInputKinesisVideoStream]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorInputKinesisVideoStream]]], jsii.get(self, "kinesisVideoStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorInput]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorInput]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorInput]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9759251ce16951f04cb85c2a450bc661ecd898656d25b875f5de8423027cdd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorNotificationChannel",
    jsii_struct_bases=[],
    name_mapping={"sns_topic_arn": "snsTopicArn"},
)
class RekognitionStreamProcessorNotificationChannel:
    def __init__(self, *, sns_topic_arn: typing.Optional[builtins.str] = None) -> None:
        '''
        :param sns_topic_arn: The Amazon Resource Number (ARN) of the Amazon Amazon Simple Notification Service topic to which Amazon Rekognition posts the completion status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#sns_topic_arn RekognitionStreamProcessor#sns_topic_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68314adccf9adadb971ca7eb958a61c27dc98489daefbcc462aeaa99a9c75f1b)
            check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sns_topic_arn is not None:
            self._values["sns_topic_arn"] = sns_topic_arn

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the Amazon Amazon Simple Notification Service topic to which Amazon Rekognition posts the completion status.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#sns_topic_arn RekognitionStreamProcessor#sns_topic_arn}
        '''
        result = self._values.get("sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorNotificationChannel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RekognitionStreamProcessorNotificationChannelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorNotificationChannelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__678dc0b68f68909c7159e5400622fd9c1af6b3845d1965e539743afc85779b45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorNotificationChannelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58fd2b7a5dd0e46e338e87284c232ffc3ce36596143d3b12b69c2d3efed78fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorNotificationChannelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a4aa0b26fd5c959c448d999ff4f8ef0477f2ac65a0bc13b4ebdae4281320cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__676f608ded7e6cec17beb16a1bdc6fc696eb76741493e57dc621039868a9450b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64465f35f4975741b79134f2c7d4c95dc800274f31dcc9767a40848cbf721140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorNotificationChannel]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorNotificationChannel]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorNotificationChannel]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6f92d5bbe551dbe5df3800b09ea1751c0c9c7b23ce8b8ec3eccb56538cb236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorNotificationChannelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorNotificationChannelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74563b708c4ecb9baa9fcde682d686af3e0f0bc175a0936fd01016e9d324e7d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSnsTopicArn")
    def reset_sns_topic_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnsTopicArn", []))

    @builtins.property
    @jsii.member(jsii_name="snsTopicArnInput")
    def sns_topic_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snsTopicArnInput"))

    @builtins.property
    @jsii.member(jsii_name="snsTopicArn")
    def sns_topic_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snsTopicArn"))

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da0ae2e52b59a80e7b46a515f0b86e8db8dd6e63db8b5164fbd387c33c7e4ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsTopicArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorNotificationChannel]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorNotificationChannel]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorNotificationChannel]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035dac467e865b139173c59fa685341f211f6e4e59cb616061d8b5759c489baa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorOutput",
    jsii_struct_bases=[],
    name_mapping={
        "kinesis_data_stream": "kinesisDataStream",
        "s3_destination": "s3Destination",
    },
)
class RekognitionStreamProcessorOutput:
    def __init__(
        self,
        *,
        kinesis_data_stream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorOutputKinesisDataStream", typing.Dict[builtins.str, typing.Any]]]]] = None,
        s3_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorOutputS3Destination", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param kinesis_data_stream: kinesis_data_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#kinesis_data_stream RekognitionStreamProcessor#kinesis_data_stream}
        :param s3_destination: s3_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#s3_destination RekognitionStreamProcessor#s3_destination}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e8e9407ce568bb19679a5fa736764c60589f91633428024571d5deea381940)
            check_type(argname="argument kinesis_data_stream", value=kinesis_data_stream, expected_type=type_hints["kinesis_data_stream"])
            check_type(argname="argument s3_destination", value=s3_destination, expected_type=type_hints["s3_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kinesis_data_stream is not None:
            self._values["kinesis_data_stream"] = kinesis_data_stream
        if s3_destination is not None:
            self._values["s3_destination"] = s3_destination

    @builtins.property
    def kinesis_data_stream(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorOutputKinesisDataStream"]]]:
        '''kinesis_data_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#kinesis_data_stream RekognitionStreamProcessor#kinesis_data_stream}
        '''
        result = self._values.get("kinesis_data_stream")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorOutputKinesisDataStream"]]], result)

    @builtins.property
    def s3_destination(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorOutputS3Destination"]]]:
        '''s3_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#s3_destination RekognitionStreamProcessor#s3_destination}
        '''
        result = self._values.get("s3_destination")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorOutputS3Destination"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorOutputKinesisDataStream",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn"},
)
class RekognitionStreamProcessorOutputKinesisDataStream:
    def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
        '''
        :param arn: ARN of the output Amazon Kinesis Data Streams stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#arn RekognitionStreamProcessor#arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b8c8a79417e926f1933b838151d9bc05bc58d3e5ca023e4d263809801b2d21)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''ARN of the output Amazon Kinesis Data Streams stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#arn RekognitionStreamProcessor#arn}
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorOutputKinesisDataStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RekognitionStreamProcessorOutputKinesisDataStreamList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorOutputKinesisDataStreamList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dd0c856161f1f24ea71905b8b97c14cb9f64aa2d3f4b44b3f8f1d31f8034c44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorOutputKinesisDataStreamOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6dd0e78fb719a14388f2cbed1086d53baff843c4349a9ce1b89582a08b9efbd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorOutputKinesisDataStreamOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44544b25e04def564a772dd385772cc4d8c7b012adef7f2d7b70cfd5d150aff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24177a59308f6dde66ff875323a477c18794827451dea53632f01b3d4c303818)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c3331511841debdc8c5488cee1d8be53e83c742bdc22647c298663774b6c0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutputKinesisDataStream]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutputKinesisDataStream]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutputKinesisDataStream]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9476ece587f337b0a3291676760974481d5eff1f8e945ce51404c3db3b6886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorOutputKinesisDataStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorOutputKinesisDataStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99efc993a355cee0ce68bbf61d23f5acea66f099007d8f3b6a549f52eda41fa8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetArn")
    def reset_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArn", []))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2671e59054aac278d60444ab6967bbac92c6699c7db65a146165982a7c37e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutputKinesisDataStream]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutputKinesisDataStream]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutputKinesisDataStream]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__110f6d1ac74646d20c555e8eaaa6099e334a36831c353f97a7258a703fd1e059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cc5139c7b2a55a023a281672c2d0246cd541ddd9ab35b3d903be2918ea5e028)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e02e07ff08e7cb554411e86f1da5df6615c4879629454a5e7a28167437c5088)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a264090856237890d28afbfa7f17b898c7d5fc9fa6ba61ca57b57016897f796b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4eaa28cf61ea75184f3bd1588d596aa4b7b29da66cb9b7e3efec237bd7fdea41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fe5f9e18c954f540af06d321783235eba49af606a31b4fcbaccfb4cc6693cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutput]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutput]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutput]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcac1e8c01dbf873106fbcce8780dd7673822b5418683df06cd176e0f82cedbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a7a370a1fdaed30495bbc17474aac90a41f0dae730d23e52490c3ae1a1ac23c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putKinesisDataStream")
    def put_kinesis_data_stream(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorOutputKinesisDataStream, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9dc17b12d3174f81bc7f0a5639eaf5cc129faed1fd07c0e4c4c3798fc3c38e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKinesisDataStream", [value]))

    @jsii.member(jsii_name="putS3Destination")
    def put_s3_destination(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorOutputS3Destination", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5243d00506c0c62d8047a0c7826cdb42770aa8e08ad075882fac622085bd41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3Destination", [value]))

    @jsii.member(jsii_name="resetKinesisDataStream")
    def reset_kinesis_data_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisDataStream", []))

    @jsii.member(jsii_name="resetS3Destination")
    def reset_s3_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Destination", []))

    @builtins.property
    @jsii.member(jsii_name="kinesisDataStream")
    def kinesis_data_stream(
        self,
    ) -> RekognitionStreamProcessorOutputKinesisDataStreamList:
        return typing.cast(RekognitionStreamProcessorOutputKinesisDataStreamList, jsii.get(self, "kinesisDataStream"))

    @builtins.property
    @jsii.member(jsii_name="s3Destination")
    def s3_destination(self) -> "RekognitionStreamProcessorOutputS3DestinationList":
        return typing.cast("RekognitionStreamProcessorOutputS3DestinationList", jsii.get(self, "s3Destination"))

    @builtins.property
    @jsii.member(jsii_name="kinesisDataStreamInput")
    def kinesis_data_stream_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutputKinesisDataStream]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutputKinesisDataStream]]], jsii.get(self, "kinesisDataStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DestinationInput")
    def s3_destination_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorOutputS3Destination"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorOutputS3Destination"]]], jsii.get(self, "s3DestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutput]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutput]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutput]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395ed565ac1bbbe67ac939b19da1c279c1c4514af3be5ac4a0076bd43b5d524e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorOutputS3Destination",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "key_prefix": "keyPrefix"},
)
class RekognitionStreamProcessorOutputS3Destination:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        key_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The name of the Amazon S3 bucket you want to associate with the streaming video project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#bucket RekognitionStreamProcessor#bucket}
        :param key_prefix: The prefix value of the location within the bucket that you want the information to be published to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#key_prefix RekognitionStreamProcessor#key_prefix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad119faf600f8bd8920b3c80e73de930e4de14e9fc04bb228c8386c34512069a)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if key_prefix is not None:
            self._values["key_prefix"] = key_prefix

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon S3 bucket you want to associate with the streaming video project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#bucket RekognitionStreamProcessor#bucket}
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix value of the location within the bucket that you want the information to be published to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#key_prefix RekognitionStreamProcessor#key_prefix}
        '''
        result = self._values.get("key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorOutputS3Destination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RekognitionStreamProcessorOutputS3DestinationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorOutputS3DestinationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a354564e0776d30a03d3f3464f17f8b9874716af9b5c6aafa39737681429b6ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorOutputS3DestinationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6690b6c94db56d77080d1c6bdeb369dce750a7fd076b3d8538d1a6bac2488370)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorOutputS3DestinationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4578c68c9c57e987c572ef05179608a5ef14ea85f8ed4d41d78d7c0402124c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94d7cd2f3935984fcaa6bf903eb98f0f1d28ac9de8182b6c62eb9fcc237fe985)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ace606b54cce7a6120accd3456d3217349a0bf5b32a80e5be739ebea853350b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutputS3Destination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutputS3Destination]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutputS3Destination]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63fac29fbc802f981bf8ebac8cb84fdca9b6e23f8a42fc729c245f8af298bf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorOutputS3DestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorOutputS3DestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb0a8d24c8cdf1c6649b689dacb731cc964c0c169619e1661f7f3d4e525878a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetKeyPrefix")
    def reset_key_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPrefixInput")
    def key_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c47dc26c4432572195cc2c02729235d01787bb6590f7afcce77bd98b19c936f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPrefix")
    def key_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPrefix"))

    @key_prefix.setter
    def key_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb047f07ed8f403036d260d37b4c638990a0443c1b6e967f56b6b7b1783cc374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutputS3Destination]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutputS3Destination]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutputS3Destination]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e9b037f5f966dbaf046734c96eefb700169ee287b7fbba1c2786375e5f630e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorRegionsOfInterest",
    jsii_struct_bases=[],
    name_mapping={"bounding_box": "boundingBox", "polygon": "polygon"},
)
class RekognitionStreamProcessorRegionsOfInterest:
    def __init__(
        self,
        *,
        bounding_box: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorRegionsOfInterestBoundingBox", typing.Dict[builtins.str, typing.Any]]]]] = None,
        polygon: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorRegionsOfInterestPolygon", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param bounding_box: bounding_box block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#bounding_box RekognitionStreamProcessor#bounding_box}
        :param polygon: polygon block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#polygon RekognitionStreamProcessor#polygon}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e385b4cc2e8cbafc4f6146ad675fa2d30b98ea41edd56392f1707c53bb0d1a8)
            check_type(argname="argument bounding_box", value=bounding_box, expected_type=type_hints["bounding_box"])
            check_type(argname="argument polygon", value=polygon, expected_type=type_hints["polygon"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bounding_box is not None:
            self._values["bounding_box"] = bounding_box
        if polygon is not None:
            self._values["polygon"] = polygon

    @builtins.property
    def bounding_box(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorRegionsOfInterestBoundingBox"]]]:
        '''bounding_box block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#bounding_box RekognitionStreamProcessor#bounding_box}
        '''
        result = self._values.get("bounding_box")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorRegionsOfInterestBoundingBox"]]], result)

    @builtins.property
    def polygon(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorRegionsOfInterestPolygon"]]]:
        '''polygon block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#polygon RekognitionStreamProcessor#polygon}
        '''
        result = self._values.get("polygon")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorRegionsOfInterestPolygon"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorRegionsOfInterest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorRegionsOfInterestBoundingBox",
    jsii_struct_bases=[],
    name_mapping={"height": "height", "left": "left", "top": "top", "width": "width"},
)
class RekognitionStreamProcessorRegionsOfInterestBoundingBox:
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        left: typing.Optional[jsii.Number] = None,
        top: typing.Optional[jsii.Number] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param height: Height of the bounding box as a ratio of the overall image height. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#height RekognitionStreamProcessor#height}
        :param left: Left coordinate of the bounding box as a ratio of overall image width. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#left RekognitionStreamProcessor#left}
        :param top: Top coordinate of the bounding box as a ratio of overall image height. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#top RekognitionStreamProcessor#top}
        :param width: Width of the bounding box as a ratio of the overall image width. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#width RekognitionStreamProcessor#width}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77897fc2f4e670cb2be589a99c67a8f1eeb04025966b8f29ebe834ee8677e136)
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument top", value=top, expected_type=type_hints["top"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if height is not None:
            self._values["height"] = height
        if left is not None:
            self._values["left"] = left
        if top is not None:
            self._values["top"] = top
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Height of the bounding box as a ratio of the overall image height.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#height RekognitionStreamProcessor#height}
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def left(self) -> typing.Optional[jsii.Number]:
        '''Left coordinate of the bounding box as a ratio of overall image width.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#left RekognitionStreamProcessor#left}
        '''
        result = self._values.get("left")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def top(self) -> typing.Optional[jsii.Number]:
        '''Top coordinate of the bounding box as a ratio of overall image height.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#top RekognitionStreamProcessor#top}
        '''
        result = self._values.get("top")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Width of the bounding box as a ratio of the overall image width.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#width RekognitionStreamProcessor#width}
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorRegionsOfInterestBoundingBox(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RekognitionStreamProcessorRegionsOfInterestBoundingBoxList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorRegionsOfInterestBoundingBoxList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb1986a15d9f7abdcd2a17dd1d5b2773d7e36badc85fb2ac5038e1d2c9ace416)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorRegionsOfInterestBoundingBoxOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668149f6897b61556f0fdcf0e4ed92cf797ce706125d463abe691e01067d2aff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorRegionsOfInterestBoundingBoxOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70abb16364efbd229f4993c173820b6fba214d3682899ab039ff9456890aa14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71e164b208d1621dc9a1bba52fd45425be857451449b11426f287ada133d0c07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6090e5d396175d46e30528afde1a42e5443ba6516948e223507e57a8c938f2f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterestBoundingBox]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterestBoundingBox]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterestBoundingBox]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1419bb191f7ca404bc3aada0dea0aefdd3332ea48f7df44a51470b6c989fe49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorRegionsOfInterestBoundingBoxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorRegionsOfInterestBoundingBoxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bca7de675eefdf94bd3d536432cd53c4f2e68bd7a1fb98b08df94ab62e4a530)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetLeft")
    def reset_left(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLeft", []))

    @jsii.member(jsii_name="resetTop")
    def reset_top(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTop", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="leftInput")
    def left_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "leftInput"))

    @builtins.property
    @jsii.member(jsii_name="topInput")
    def top_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "topInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad6a4a93da5cac7f77ecd0e63d36e63555ef3358541d06c74a00743c1ddb145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="left")
    def left(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "left"))

    @left.setter
    def left(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd809b563767cf1fc8dd843b01a5042d15a8b014f6ce6a83dc838861ea90e295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "left", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="top")
    def top(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "top"))

    @top.setter
    def top(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea32246ba055ad506d2f86638ad6a51e57a873d3a4f831ffbb659cf968a2e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "top", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ab9b0e196950c5cbde3f24b3178352708683475a208e15485f3b235ed1478e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterestBoundingBox]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterestBoundingBox]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterestBoundingBox]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc02e79aca2fe733e3167e12744016451e02797bbd8ec936b5113666814b32cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorRegionsOfInterestList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorRegionsOfInterestList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ad07383c55871ec6a241ec3a16d2066a7bc54fdf08a720d8e7f00fe873b3ffa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorRegionsOfInterestOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ebfda8caee9dc34e8c7d42653abef255e30e9ebe3d9b7b8f8cfa24bce50037c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorRegionsOfInterestOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3081ca4b4ee3b61dc47acfbfcc717198f0d7db7975d283433517480227379e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20b38bc772168556302c902c5403c2707c441f58b14530d0157cd67d6f30391b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb0721e13b773df103435b20bf5fa14b1ab2a616d78303bc07ae581a283dd74f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterest]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterest]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterest]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c4bdd1d923ce40ebd4212f30e409e7536e82e42abcbc3d4662540ec55c8bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorRegionsOfInterestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorRegionsOfInterestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__726409854e8cf9c162d41a7e34952a9c2d631010ce35f1c311b9df4729519167)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBoundingBox")
    def put_bounding_box(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorRegionsOfInterestBoundingBox, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3a6b127256121b0cea3fb3b7c4144f1da86dea8c2c624c5c2fd7ab822c118d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBoundingBox", [value]))

    @jsii.member(jsii_name="putPolygon")
    def put_polygon(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorRegionsOfInterestPolygon", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e95185ac0e021cf45b6d10d4e50e4dc5b156063b8d114b9dea216937d81c6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolygon", [value]))

    @jsii.member(jsii_name="resetBoundingBox")
    def reset_bounding_box(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBoundingBox", []))

    @jsii.member(jsii_name="resetPolygon")
    def reset_polygon(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolygon", []))

    @builtins.property
    @jsii.member(jsii_name="boundingBox")
    def bounding_box(
        self,
    ) -> RekognitionStreamProcessorRegionsOfInterestBoundingBoxList:
        return typing.cast(RekognitionStreamProcessorRegionsOfInterestBoundingBoxList, jsii.get(self, "boundingBox"))

    @builtins.property
    @jsii.member(jsii_name="polygon")
    def polygon(self) -> "RekognitionStreamProcessorRegionsOfInterestPolygonList":
        return typing.cast("RekognitionStreamProcessorRegionsOfInterestPolygonList", jsii.get(self, "polygon"))

    @builtins.property
    @jsii.member(jsii_name="boundingBoxInput")
    def bounding_box_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterestBoundingBox]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterestBoundingBox]]], jsii.get(self, "boundingBoxInput"))

    @builtins.property
    @jsii.member(jsii_name="polygonInput")
    def polygon_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorRegionsOfInterestPolygon"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorRegionsOfInterestPolygon"]]], jsii.get(self, "polygonInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterest]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterest]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterest]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd5f3f98f82e7123b1567d47e05fa3d02822a09c54551b8221e1ee66c2e0d6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorRegionsOfInterestPolygon",
    jsii_struct_bases=[],
    name_mapping={"x": "x", "y": "y"},
)
class RekognitionStreamProcessorRegionsOfInterestPolygon:
    def __init__(
        self,
        *,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param x: The value of the X coordinate for a point on a Polygon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#x RekognitionStreamProcessor#x}
        :param y: The value of the Y coordinate for a point on a Polygon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#y RekognitionStreamProcessor#y}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf1b67c98c77096d82ddff2bcb106afe7479925a817ee1447f6935082ad920a)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        '''The value of the X coordinate for a point on a Polygon.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#x RekognitionStreamProcessor#x}
        '''
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        '''The value of the Y coordinate for a point on a Polygon.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#y RekognitionStreamProcessor#y}
        '''
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorRegionsOfInterestPolygon(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RekognitionStreamProcessorRegionsOfInterestPolygonList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorRegionsOfInterestPolygonList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ea9e9a928c9a5d98a7f7130d70feaa7e2dd90533cc41bcad270ec7154d655e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorRegionsOfInterestPolygonOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a1e3c5818cbf550a924ae4b29498f116ade98dcf23e0e6a153982f4334a540)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorRegionsOfInterestPolygonOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313608c276be63f2ad2f1de2aac4de6da51447929d39b94b45c74ab690e356de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e9582804f8c5fb8539d92820cf9447fa0eed9290b9a2cd11b80ce88e5caaa04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea54a285cf1997bcccc61e6155726674191e8a655dcfe2499fa0358de5fdacdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterestPolygon]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterestPolygon]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterestPolygon]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0ffa490ba091eff8a913e0c18df87f124878dc15a60a90da7811078e42294d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorRegionsOfInterestPolygonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorRegionsOfInterestPolygonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3f42179f257be4c8cf68f6dd6793db769069711c21b683bcabc42f510c06f74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetX")
    def reset_x(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetX", []))

    @jsii.member(jsii_name="resetY")
    def reset_y(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetY", []))

    @builtins.property
    @jsii.member(jsii_name="xInput")
    def x_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "xInput"))

    @builtins.property
    @jsii.member(jsii_name="yInput")
    def y_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yInput"))

    @builtins.property
    @jsii.member(jsii_name="x")
    def x(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "x"))

    @x.setter
    def x(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10eda08b85d44d9124b57191384d4a2be4e5a161e546d329965d4a8efafa11f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="y")
    def y(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "y"))

    @y.setter
    def y(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5586006567815ab0448df36b44c80c3ab10470f85a71157fc722a8e1414131d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "y", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterestPolygon]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterestPolygon]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterestPolygon]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c0086fa56b2a4bf3dedd3fa20f5ebf05474bd618f6ea7cac52ea9ef5ce9476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorSettings",
    jsii_struct_bases=[],
    name_mapping={"connected_home": "connectedHome", "face_search": "faceSearch"},
)
class RekognitionStreamProcessorSettings:
    def __init__(
        self,
        *,
        connected_home: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorSettingsConnectedHome", typing.Dict[builtins.str, typing.Any]]]]] = None,
        face_search: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RekognitionStreamProcessorSettingsFaceSearch", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connected_home: connected_home block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#connected_home RekognitionStreamProcessor#connected_home}
        :param face_search: face_search block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#face_search RekognitionStreamProcessor#face_search}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da8e65310d6891664a5f26f0561aeb7dfc4ed03613214e8b5e95ff6b468d69e)
            check_type(argname="argument connected_home", value=connected_home, expected_type=type_hints["connected_home"])
            check_type(argname="argument face_search", value=face_search, expected_type=type_hints["face_search"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connected_home is not None:
            self._values["connected_home"] = connected_home
        if face_search is not None:
            self._values["face_search"] = face_search

    @builtins.property
    def connected_home(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorSettingsConnectedHome"]]]:
        '''connected_home block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#connected_home RekognitionStreamProcessor#connected_home}
        '''
        result = self._values.get("connected_home")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorSettingsConnectedHome"]]], result)

    @builtins.property
    def face_search(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorSettingsFaceSearch"]]]:
        '''face_search block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#face_search RekognitionStreamProcessor#face_search}
        '''
        result = self._values.get("face_search")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RekognitionStreamProcessorSettingsFaceSearch"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorSettingsConnectedHome",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "min_confidence": "minConfidence"},
)
class RekognitionStreamProcessorSettingsConnectedHome:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        min_confidence: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param labels: Specifies what you want to detect in the video, such as people, packages, or pets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#labels RekognitionStreamProcessor#labels}
        :param min_confidence: The minimum confidence required to label an object in the video. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#min_confidence RekognitionStreamProcessor#min_confidence}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f1e5cd9239e9711ffc6699b82866fa4fe5fcd017d5c4b96f0fc111910577f4)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument min_confidence", value=min_confidence, expected_type=type_hints["min_confidence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if min_confidence is not None:
            self._values["min_confidence"] = min_confidence

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies what you want to detect in the video, such as people, packages, or pets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#labels RekognitionStreamProcessor#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def min_confidence(self) -> typing.Optional[jsii.Number]:
        '''The minimum confidence required to label an object in the video.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#min_confidence RekognitionStreamProcessor#min_confidence}
        '''
        result = self._values.get("min_confidence")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorSettingsConnectedHome(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RekognitionStreamProcessorSettingsConnectedHomeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorSettingsConnectedHomeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a9cb8de1af9a39744bb4249d8bbb601a0cc86bf48ffa317942c3ac6c11d374)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorSettingsConnectedHomeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5f0bfbba481f17b74a98ba25f87be54f7f0010fdce37efc3332211ad59dac2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorSettingsConnectedHomeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a64fd4fff2a51787040160b959974a38eb0eda77b2ec915ebccf7b98fb2927c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e3dde511ce1e9c200b8b5bca70d89504800e9eeea3bd5bc29d97c1e7f88fd95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb1c0b122c50c2f45a80372374f89b1d60020bd33c52b4e00895f6df27feb508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsConnectedHome]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsConnectedHome]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsConnectedHome]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13995f04042d693b1c75142617023c616b2e024ebe5ac69b2b874ba672935cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorSettingsConnectedHomeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorSettingsConnectedHomeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de92cc875cb48502c0a66bc8321bbd32c5d9675317e298387cc0706a3befd44b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMinConfidence")
    def reset_min_confidence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinConfidence", []))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="minConfidenceInput")
    def min_confidence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minConfidenceInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af01c58a9d35561a740da674ba0bde44075deab0cf7c0f9c86e280d870666cd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minConfidence")
    def min_confidence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minConfidence"))

    @min_confidence.setter
    def min_confidence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b839e4cb95917f3c74a861f2343c2909340ca54603aacb8e104bb39448c3f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minConfidence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettingsConnectedHome]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettingsConnectedHome]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettingsConnectedHome]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9243bc5f6bdf04ae87285cef0051c15794421382a42cc0eac8ba745e139a2dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorSettingsFaceSearch",
    jsii_struct_bases=[],
    name_mapping={
        "collection_id": "collectionId",
        "face_match_threshold": "faceMatchThreshold",
    },
)
class RekognitionStreamProcessorSettingsFaceSearch:
    def __init__(
        self,
        *,
        collection_id: builtins.str,
        face_match_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param collection_id: The ID of a collection that contains faces that you want to search for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#collection_id RekognitionStreamProcessor#collection_id}
        :param face_match_threshold: Minimum face match confidence score that must be met to return a result for a recognized face. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#face_match_threshold RekognitionStreamProcessor#face_match_threshold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7956871de591361d63499b096b35229b768999e5fd1fdc88da6186fdd67c46a)
            check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
            check_type(argname="argument face_match_threshold", value=face_match_threshold, expected_type=type_hints["face_match_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "collection_id": collection_id,
        }
        if face_match_threshold is not None:
            self._values["face_match_threshold"] = face_match_threshold

    @builtins.property
    def collection_id(self) -> builtins.str:
        '''The ID of a collection that contains faces that you want to search for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#collection_id RekognitionStreamProcessor#collection_id}
        '''
        result = self._values.get("collection_id")
        assert result is not None, "Required property 'collection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def face_match_threshold(self) -> typing.Optional[jsii.Number]:
        '''Minimum face match confidence score that must be met to return a result for a recognized face.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#face_match_threshold RekognitionStreamProcessor#face_match_threshold}
        '''
        result = self._values.get("face_match_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorSettingsFaceSearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RekognitionStreamProcessorSettingsFaceSearchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorSettingsFaceSearchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11169c5e6b7dd80962954fd2709690ebdf171d8fd6ab8df097836063498de885)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorSettingsFaceSearchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43fc16e82ede8cb33cfcc2423a0fed3efd51d68c365e266c99a10920c2ff500)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorSettingsFaceSearchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d380a961ed37a3630dd7cce18ed2c8c9ae2508186a7394d5e50111a86e0ea4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__060dbf4b338a0a0f79c336b5f2f4fe4e24ae5e518721fb7efd13fadee317dba4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21bf8cc5e49bcea23ac67fc40ad7245a6201651661723c024eec5dd21fd1404b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsFaceSearch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsFaceSearch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsFaceSearch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67892946326f1a7723d80ee5bd6f7f316d86ad8f7f3d1de5602ce40c2abd592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorSettingsFaceSearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorSettingsFaceSearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13503d9a8c41bc95ccf108e17dddfaf1a6895b24f4982b0044f312eed719ff23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFaceMatchThreshold")
    def reset_face_match_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFaceMatchThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="collectionIdInput")
    def collection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="faceMatchThresholdInput")
    def face_match_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "faceMatchThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionId")
    def collection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionId"))

    @collection_id.setter
    def collection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47085a9c7e1ad5951029a547e974bd1fa0dc118586d4d33b85611c40181c148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="faceMatchThreshold")
    def face_match_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "faceMatchThreshold"))

    @face_match_threshold.setter
    def face_match_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb1d3fb43f64a06219d574bd99fc7332a2b790cc09e95bfc55006e3f8ff4e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "faceMatchThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettingsFaceSearch]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettingsFaceSearch]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettingsFaceSearch]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871c8e691d5f3743e114a3ab705c8cbe1ca32e8307d77b093937e7bf1bce1de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c7e1d392e6710d75e755062adc6856484a4e77bc681e5da3754c9236bf75218)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RekognitionStreamProcessorSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4766277b26fde598d0e57adf85522535a10f959d60b46601c3c5e46d4c28b6a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RekognitionStreamProcessorSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b3b741b7f9aaf79acd39c5257abbf81a38f76663bd5cc0ee6ff85b64689bbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0047c14d93c81a2845e540ffcac0e45c17d18f5e90fbe71726e26d33e2e85a0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72e7e6e78d4ceb88d4dcaa7ae3c36b7308666d460b5b483113d562aa0b50014a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b168dc18f8480cb13cfb73fe68d9ddd986a4fb33adba000743350da2228b0d32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RekognitionStreamProcessorSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc41bcc25d3086d462baf52603ce78cbefdb5bd3e9bcead86d794824c60e7d4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConnectedHome")
    def put_connected_home(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorSettingsConnectedHome, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee86e37aabc2a71fe902021615d63c27a6fb52caa9393378ba693da53e66761d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnectedHome", [value]))

    @jsii.member(jsii_name="putFaceSearch")
    def put_face_search(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorSettingsFaceSearch, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7976d5d03a5cf0161db0bf97dc2e745771b8109597e34117152efcc6b5d41bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFaceSearch", [value]))

    @jsii.member(jsii_name="resetConnectedHome")
    def reset_connected_home(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectedHome", []))

    @jsii.member(jsii_name="resetFaceSearch")
    def reset_face_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFaceSearch", []))

    @builtins.property
    @jsii.member(jsii_name="connectedHome")
    def connected_home(self) -> RekognitionStreamProcessorSettingsConnectedHomeList:
        return typing.cast(RekognitionStreamProcessorSettingsConnectedHomeList, jsii.get(self, "connectedHome"))

    @builtins.property
    @jsii.member(jsii_name="faceSearch")
    def face_search(self) -> RekognitionStreamProcessorSettingsFaceSearchList:
        return typing.cast(RekognitionStreamProcessorSettingsFaceSearchList, jsii.get(self, "faceSearch"))

    @builtins.property
    @jsii.member(jsii_name="connectedHomeInput")
    def connected_home_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsConnectedHome]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsConnectedHome]]], jsii.get(self, "connectedHomeInput"))

    @builtins.property
    @jsii.member(jsii_name="faceSearchInput")
    def face_search_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsFaceSearch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsFaceSearch]]], jsii.get(self, "faceSearchInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34731115b70a0ebd3dd663c592a05ece6b661ca265bde96cbdf499e46b62f9a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class RekognitionStreamProcessorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#create RekognitionStreamProcessor#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#delete RekognitionStreamProcessor#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#update RekognitionStreamProcessor#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d8eaf88cf5aba70601abb0fbb513d5465d687800fd86db3e03b19df91b75c4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#create RekognitionStreamProcessor#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#delete RekognitionStreamProcessor#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rekognition_stream_processor#update RekognitionStreamProcessor#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RekognitionStreamProcessorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RekognitionStreamProcessorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rekognitionStreamProcessor.RekognitionStreamProcessorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4e4a911038158d2252bd09944c9f20f778ab3e9ba5488bb585c80153a7385a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__016ccb04c34bd3226782f6caf233178c56cd23e319667976dc107cb4ae56db10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509b30e1da0539972483c9f00206fb29b44e1bd4ab6ef2b574fb403fd9a2141a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e4175c1fe80b399813c0f5a07eeedf314de9555715cc01c24c412004d3e0b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52904d5f536ece80f295d440d28f8a2b72a66741b1056fafaa0bf1ee789b7c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RekognitionStreamProcessor",
    "RekognitionStreamProcessorConfig",
    "RekognitionStreamProcessorDataSharingPreference",
    "RekognitionStreamProcessorDataSharingPreferenceList",
    "RekognitionStreamProcessorDataSharingPreferenceOutputReference",
    "RekognitionStreamProcessorInput",
    "RekognitionStreamProcessorInputKinesisVideoStream",
    "RekognitionStreamProcessorInputKinesisVideoStreamList",
    "RekognitionStreamProcessorInputKinesisVideoStreamOutputReference",
    "RekognitionStreamProcessorInputList",
    "RekognitionStreamProcessorInputOutputReference",
    "RekognitionStreamProcessorNotificationChannel",
    "RekognitionStreamProcessorNotificationChannelList",
    "RekognitionStreamProcessorNotificationChannelOutputReference",
    "RekognitionStreamProcessorOutput",
    "RekognitionStreamProcessorOutputKinesisDataStream",
    "RekognitionStreamProcessorOutputKinesisDataStreamList",
    "RekognitionStreamProcessorOutputKinesisDataStreamOutputReference",
    "RekognitionStreamProcessorOutputList",
    "RekognitionStreamProcessorOutputOutputReference",
    "RekognitionStreamProcessorOutputS3Destination",
    "RekognitionStreamProcessorOutputS3DestinationList",
    "RekognitionStreamProcessorOutputS3DestinationOutputReference",
    "RekognitionStreamProcessorRegionsOfInterest",
    "RekognitionStreamProcessorRegionsOfInterestBoundingBox",
    "RekognitionStreamProcessorRegionsOfInterestBoundingBoxList",
    "RekognitionStreamProcessorRegionsOfInterestBoundingBoxOutputReference",
    "RekognitionStreamProcessorRegionsOfInterestList",
    "RekognitionStreamProcessorRegionsOfInterestOutputReference",
    "RekognitionStreamProcessorRegionsOfInterestPolygon",
    "RekognitionStreamProcessorRegionsOfInterestPolygonList",
    "RekognitionStreamProcessorRegionsOfInterestPolygonOutputReference",
    "RekognitionStreamProcessorSettings",
    "RekognitionStreamProcessorSettingsConnectedHome",
    "RekognitionStreamProcessorSettingsConnectedHomeList",
    "RekognitionStreamProcessorSettingsConnectedHomeOutputReference",
    "RekognitionStreamProcessorSettingsFaceSearch",
    "RekognitionStreamProcessorSettingsFaceSearchList",
    "RekognitionStreamProcessorSettingsFaceSearchOutputReference",
    "RekognitionStreamProcessorSettingsList",
    "RekognitionStreamProcessorSettingsOutputReference",
    "RekognitionStreamProcessorTimeouts",
    "RekognitionStreamProcessorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__690faf2084a4187ba423d9851ce6c5762f44bff2362c1dbce3c04eaff3339788(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    role_arn: builtins.str,
    data_sharing_preference: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorDataSharingPreference, typing.Dict[builtins.str, typing.Any]]]]] = None,
    input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorInput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    notification_channel: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorNotificationChannel, typing.Dict[builtins.str, typing.Any]]]]] = None,
    output: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorOutput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    regions_of_interest: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorRegionsOfInterest, typing.Dict[builtins.str, typing.Any]]]]] = None,
    settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RekognitionStreamProcessorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__eed5927856c228091b2ae3ace94d33e32f706f86927a45543d4c4c405f8d8ea7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a278d794b5e885a14113f52194701040dd577370e3df7023bdd9bcc856c923(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorDataSharingPreference, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59906d49a4e38ed405063b499aace6b1c7a6261425840274c3a0519cb245b33(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorInput, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f30dfd1183ab9b930618711e4881f96af0bc88ebe6ea611ab2baf2e8a7ee074(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorNotificationChannel, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a374ab6d87b3613f19e25cf8fb831bc8354a8cbb2795d48eb45fb556eb296aa6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorOutput, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b6631cd319d90499adad4a76afc2ac43ec922968144e97f237dc040293c33b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorRegionsOfInterest, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce46377ec37515789ad58443b1daf14f3cbf8a5e12d70620729c85ebb01317d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b5a43e178d3b3e423855ff26ede7ac26f3ee2ed89198e24ac4cce246779ff0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04fa4da728b1419df03462546d970b7f7cd33b2e34f6155ff73ff538e3e56e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a413111236ce8a92a058ad75149b30bc2e834e7e2e4f8c2c2713df3b15424c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83eaf56027f68fac88ec1a239cde3852c14b022f5c58cb3329a909d7712dae57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb21783025351be4aa2ccef7bb3fdc246fce36482cf526f331f5ef1cc1f7b3f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f20a55d0c76692298f1777a4fa2fa3c5b8143675ef34fca018711665378f71e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    role_arn: builtins.str,
    data_sharing_preference: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorDataSharingPreference, typing.Dict[builtins.str, typing.Any]]]]] = None,
    input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorInput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    notification_channel: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorNotificationChannel, typing.Dict[builtins.str, typing.Any]]]]] = None,
    output: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorOutput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    regions_of_interest: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorRegionsOfInterest, typing.Dict[builtins.str, typing.Any]]]]] = None,
    settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RekognitionStreamProcessorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a34a939ca677c21621ac6c0704080939eeb76d9607dddcfe8d731a10c87b376(
    *,
    opt_in: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230db5099c754e39d54e6f7a44babb21a806af5afbc5f47ae99b1056b5b8ac59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc8da9fa291d3e3a3afc85af000cc0081a822d9984e3e0656689ee9ef58f7a9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fadf13f033114cc47fc1b962fff786ad6e8fa921ba3995e3f411f2ccac55160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e586d68b9fc6a0e6f2dba939a14176f44f7023d158039154674f41fdbc5ce1d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049af734818486a09b934312aa9e84e66d0adc7529e45d42995817b320c0273d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e298b8cdee02b1ed88c429e2687cc5b39a50d6fae3a92ea30477f57d499d5bfd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorDataSharingPreference]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b253fdb212836eea6c2c22f4a0ca761ca513b971a784cb1e0a0ec9a6bd54eac0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cde652245407ea4ed4d4818e719cef2c85a847f490c0525f577662824814777(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f7a8975cf08b17c8a24cd8507996f1ae9a95c211290251a548df013af2546b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorDataSharingPreference]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b739c8a693758390c11548245b826bee091459aa57f4802b5f7542767a3b77(
    *,
    kinesis_video_stream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorInputKinesisVideoStream, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd60f0ef08d34ce135d1539fc3ffa93d14638d8019ec7633e822ad15aebd4932(
    *,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a005594825fe7c93678b24db1609530a71dfafc3790f271e305f1c3014047c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27955339e9cbf1efa288b3e4d66d216d15486f4297a904b27722edd2cc4c94ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594fed579af69a938e6f05b71c2d8aedae8f319f20119cdbcaf3fcf910c2d1a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afeefaf0972be2174b2b6ca602772cd75a654af60ac1f57eb3550feb9167ab0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162080d2039656a4fbf5569a193476c148d227fc343a9a02ab3b1d7b237a535b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d6b583d94e432911ce0411041cb187c106257f48600e3db0161621c65d4ff0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorInputKinesisVideoStream]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73f32ca7bdfced1a132bce82d1702346267d18f23f59464fc11fd62f4781acb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61376e7c2fd80b13bf79d523b7ee7723a76af8df138f4613015cf6d73f94faec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bd1a44ecaa1abdfdb30098100e1a1544e21c3b50db82c804f130b1d44d5326(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorInputKinesisVideoStream]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27382efa75280ae0067bdeed20f385751a2d3205e2dad0d3c76f433a62aabace(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0fa22ce7897bee4426bbaa81f732758d2c0fcb2d2306bdd81bdecac461e1a5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467ab808590092a7e710d1aa0c4e2e75d0af7bc6ab457517a14883790d0535b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388da6c004af5a6066ee694dce3ecfd4edde2db3be8f8a78106c6fcad7a8ee2d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58e60d0885b49b63e827a392baad15d8a79dcb74cf6e3530257c14b510b3ce9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef3ee1208c8978add1314498555db652fa9cd9d59e480deb9b0313fc60707e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorInput]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b7b46273e2bd6b25667a8b41bc67d19ec909b90ac0be776134277550e6d6a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1dc41de59cd8cb6c745a0b70b09a7718dd5fc3deb69f783cb28facc0601ddc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorInputKinesisVideoStream, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9759251ce16951f04cb85c2a450bc661ecd898656d25b875f5de8423027cdd2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorInput]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68314adccf9adadb971ca7eb958a61c27dc98489daefbcc462aeaa99a9c75f1b(
    *,
    sns_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678dc0b68f68909c7159e5400622fd9c1af6b3845d1965e539743afc85779b45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58fd2b7a5dd0e46e338e87284c232ffc3ce36596143d3b12b69c2d3efed78fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a4aa0b26fd5c959c448d999ff4f8ef0477f2ac65a0bc13b4ebdae4281320cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676f608ded7e6cec17beb16a1bdc6fc696eb76741493e57dc621039868a9450b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64465f35f4975741b79134f2c7d4c95dc800274f31dcc9767a40848cbf721140(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6f92d5bbe551dbe5df3800b09ea1751c0c9c7b23ce8b8ec3eccb56538cb236(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorNotificationChannel]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74563b708c4ecb9baa9fcde682d686af3e0f0bc175a0936fd01016e9d324e7d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da0ae2e52b59a80e7b46a515f0b86e8db8dd6e63db8b5164fbd387c33c7e4ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035dac467e865b139173c59fa685341f211f6e4e59cb616061d8b5759c489baa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorNotificationChannel]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e8e9407ce568bb19679a5fa736764c60589f91633428024571d5deea381940(
    *,
    kinesis_data_stream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorOutputKinesisDataStream, typing.Dict[builtins.str, typing.Any]]]]] = None,
    s3_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorOutputS3Destination, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b8c8a79417e926f1933b838151d9bc05bc58d3e5ca023e4d263809801b2d21(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd0c856161f1f24ea71905b8b97c14cb9f64aa2d3f4b44b3f8f1d31f8034c44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6dd0e78fb719a14388f2cbed1086d53baff843c4349a9ce1b89582a08b9efbd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44544b25e04def564a772dd385772cc4d8c7b012adef7f2d7b70cfd5d150aff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24177a59308f6dde66ff875323a477c18794827451dea53632f01b3d4c303818(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3331511841debdc8c5488cee1d8be53e83c742bdc22647c298663774b6c0de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9476ece587f337b0a3291676760974481d5eff1f8e945ce51404c3db3b6886(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutputKinesisDataStream]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99efc993a355cee0ce68bbf61d23f5acea66f099007d8f3b6a549f52eda41fa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2671e59054aac278d60444ab6967bbac92c6699c7db65a146165982a7c37e5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110f6d1ac74646d20c555e8eaaa6099e334a36831c353f97a7258a703fd1e059(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutputKinesisDataStream]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc5139c7b2a55a023a281672c2d0246cd541ddd9ab35b3d903be2918ea5e028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e02e07ff08e7cb554411e86f1da5df6615c4879629454a5e7a28167437c5088(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a264090856237890d28afbfa7f17b898c7d5fc9fa6ba61ca57b57016897f796b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eaa28cf61ea75184f3bd1588d596aa4b7b29da66cb9b7e3efec237bd7fdea41(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe5f9e18c954f540af06d321783235eba49af606a31b4fcbaccfb4cc6693cd8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcac1e8c01dbf873106fbcce8780dd7673822b5418683df06cd176e0f82cedbf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutput]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7a370a1fdaed30495bbc17474aac90a41f0dae730d23e52490c3ae1a1ac23c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dc17b12d3174f81bc7f0a5639eaf5cc129faed1fd07c0e4c4c3798fc3c38e2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorOutputKinesisDataStream, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5243d00506c0c62d8047a0c7826cdb42770aa8e08ad075882fac622085bd41(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorOutputS3Destination, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395ed565ac1bbbe67ac939b19da1c279c1c4514af3be5ac4a0076bd43b5d524e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutput]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad119faf600f8bd8920b3c80e73de930e4de14e9fc04bb228c8386c34512069a(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a354564e0776d30a03d3f3464f17f8b9874716af9b5c6aafa39737681429b6ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6690b6c94db56d77080d1c6bdeb369dce750a7fd076b3d8538d1a6bac2488370(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4578c68c9c57e987c572ef05179608a5ef14ea85f8ed4d41d78d7c0402124c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d7cd2f3935984fcaa6bf903eb98f0f1d28ac9de8182b6c62eb9fcc237fe985(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ace606b54cce7a6120accd3456d3217349a0bf5b32a80e5be739ebea853350b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63fac29fbc802f981bf8ebac8cb84fdca9b6e23f8a42fc729c245f8af298bf4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorOutputS3Destination]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0a8d24c8cdf1c6649b689dacb731cc964c0c169619e1661f7f3d4e525878a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c47dc26c4432572195cc2c02729235d01787bb6590f7afcce77bd98b19c936f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb047f07ed8f403036d260d37b4c638990a0443c1b6e967f56b6b7b1783cc374(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e9b037f5f966dbaf046734c96eefb700169ee287b7fbba1c2786375e5f630e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorOutputS3Destination]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e385b4cc2e8cbafc4f6146ad675fa2d30b98ea41edd56392f1707c53bb0d1a8(
    *,
    bounding_box: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorRegionsOfInterestBoundingBox, typing.Dict[builtins.str, typing.Any]]]]] = None,
    polygon: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorRegionsOfInterestPolygon, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77897fc2f4e670cb2be589a99c67a8f1eeb04025966b8f29ebe834ee8677e136(
    *,
    height: typing.Optional[jsii.Number] = None,
    left: typing.Optional[jsii.Number] = None,
    top: typing.Optional[jsii.Number] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1986a15d9f7abdcd2a17dd1d5b2773d7e36badc85fb2ac5038e1d2c9ace416(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668149f6897b61556f0fdcf0e4ed92cf797ce706125d463abe691e01067d2aff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70abb16364efbd229f4993c173820b6fba214d3682899ab039ff9456890aa14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e164b208d1621dc9a1bba52fd45425be857451449b11426f287ada133d0c07(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6090e5d396175d46e30528afde1a42e5443ba6516948e223507e57a8c938f2f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1419bb191f7ca404bc3aada0dea0aefdd3332ea48f7df44a51470b6c989fe49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterestBoundingBox]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bca7de675eefdf94bd3d536432cd53c4f2e68bd7a1fb98b08df94ab62e4a530(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad6a4a93da5cac7f77ecd0e63d36e63555ef3358541d06c74a00743c1ddb145(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd809b563767cf1fc8dd843b01a5042d15a8b014f6ce6a83dc838861ea90e295(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea32246ba055ad506d2f86638ad6a51e57a873d3a4f831ffbb659cf968a2e85(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ab9b0e196950c5cbde3f24b3178352708683475a208e15485f3b235ed1478e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc02e79aca2fe733e3167e12744016451e02797bbd8ec936b5113666814b32cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterestBoundingBox]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad07383c55871ec6a241ec3a16d2066a7bc54fdf08a720d8e7f00fe873b3ffa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebfda8caee9dc34e8c7d42653abef255e30e9ebe3d9b7b8f8cfa24bce50037c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3081ca4b4ee3b61dc47acfbfcc717198f0d7db7975d283433517480227379e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b38bc772168556302c902c5403c2707c441f58b14530d0157cd67d6f30391b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0721e13b773df103435b20bf5fa14b1ab2a616d78303bc07ae581a283dd74f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c4bdd1d923ce40ebd4212f30e409e7536e82e42abcbc3d4662540ec55c8bd4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterest]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726409854e8cf9c162d41a7e34952a9c2d631010ce35f1c311b9df4729519167(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3a6b127256121b0cea3fb3b7c4144f1da86dea8c2c624c5c2fd7ab822c118d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorRegionsOfInterestBoundingBox, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e95185ac0e021cf45b6d10d4e50e4dc5b156063b8d114b9dea216937d81c6b5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorRegionsOfInterestPolygon, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5f3f98f82e7123b1567d47e05fa3d02822a09c54551b8221e1ee66c2e0d6c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterest]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf1b67c98c77096d82ddff2bcb106afe7479925a817ee1447f6935082ad920a(
    *,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea9e9a928c9a5d98a7f7130d70feaa7e2dd90533cc41bcad270ec7154d655e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a1e3c5818cbf550a924ae4b29498f116ade98dcf23e0e6a153982f4334a540(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313608c276be63f2ad2f1de2aac4de6da51447929d39b94b45c74ab690e356de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9582804f8c5fb8539d92820cf9447fa0eed9290b9a2cd11b80ce88e5caaa04(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea54a285cf1997bcccc61e6155726674191e8a655dcfe2499fa0358de5fdacdb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0ffa490ba091eff8a913e0c18df87f124878dc15a60a90da7811078e42294d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorRegionsOfInterestPolygon]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f42179f257be4c8cf68f6dd6793db769069711c21b683bcabc42f510c06f74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10eda08b85d44d9124b57191384d4a2be4e5a161e546d329965d4a8efafa11f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5586006567815ab0448df36b44c80c3ab10470f85a71157fc722a8e1414131d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c0086fa56b2a4bf3dedd3fa20f5ebf05474bd618f6ea7cac52ea9ef5ce9476(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorRegionsOfInterestPolygon]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da8e65310d6891664a5f26f0561aeb7dfc4ed03613214e8b5e95ff6b468d69e(
    *,
    connected_home: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorSettingsConnectedHome, typing.Dict[builtins.str, typing.Any]]]]] = None,
    face_search: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorSettingsFaceSearch, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f1e5cd9239e9711ffc6699b82866fa4fe5fcd017d5c4b96f0fc111910577f4(
    *,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    min_confidence: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a9cb8de1af9a39744bb4249d8bbb601a0cc86bf48ffa317942c3ac6c11d374(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5f0bfbba481f17b74a98ba25f87be54f7f0010fdce37efc3332211ad59dac2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a64fd4fff2a51787040160b959974a38eb0eda77b2ec915ebccf7b98fb2927c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3dde511ce1e9c200b8b5bca70d89504800e9eeea3bd5bc29d97c1e7f88fd95(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1c0b122c50c2f45a80372374f89b1d60020bd33c52b4e00895f6df27feb508(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13995f04042d693b1c75142617023c616b2e024ebe5ac69b2b874ba672935cfa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsConnectedHome]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de92cc875cb48502c0a66bc8321bbd32c5d9675317e298387cc0706a3befd44b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af01c58a9d35561a740da674ba0bde44075deab0cf7c0f9c86e280d870666cd7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b839e4cb95917f3c74a861f2343c2909340ca54603aacb8e104bb39448c3f7f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9243bc5f6bdf04ae87285cef0051c15794421382a42cc0eac8ba745e139a2dc8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettingsConnectedHome]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7956871de591361d63499b096b35229b768999e5fd1fdc88da6186fdd67c46a(
    *,
    collection_id: builtins.str,
    face_match_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11169c5e6b7dd80962954fd2709690ebdf171d8fd6ab8df097836063498de885(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43fc16e82ede8cb33cfcc2423a0fed3efd51d68c365e266c99a10920c2ff500(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d380a961ed37a3630dd7cce18ed2c8c9ae2508186a7394d5e50111a86e0ea4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060dbf4b338a0a0f79c336b5f2f4fe4e24ae5e518721fb7efd13fadee317dba4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21bf8cc5e49bcea23ac67fc40ad7245a6201651661723c024eec5dd21fd1404b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67892946326f1a7723d80ee5bd6f7f316d86ad8f7f3d1de5602ce40c2abd592(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettingsFaceSearch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13503d9a8c41bc95ccf108e17dddfaf1a6895b24f4982b0044f312eed719ff23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47085a9c7e1ad5951029a547e974bd1fa0dc118586d4d33b85611c40181c148(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb1d3fb43f64a06219d574bd99fc7332a2b790cc09e95bfc55006e3f8ff4e61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871c8e691d5f3743e114a3ab705c8cbe1ca32e8307d77b093937e7bf1bce1de9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettingsFaceSearch]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7e1d392e6710d75e755062adc6856484a4e77bc681e5da3754c9236bf75218(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4766277b26fde598d0e57adf85522535a10f959d60b46601c3c5e46d4c28b6a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b3b741b7f9aaf79acd39c5257abbf81a38f76663bd5cc0ee6ff85b64689bbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0047c14d93c81a2845e540ffcac0e45c17d18f5e90fbe71726e26d33e2e85a0e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e7e6e78d4ceb88d4dcaa7ae3c36b7308666d460b5b483113d562aa0b50014a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b168dc18f8480cb13cfb73fe68d9ddd986a4fb33adba000743350da2228b0d32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RekognitionStreamProcessorSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc41bcc25d3086d462baf52603ce78cbefdb5bd3e9bcead86d794824c60e7d4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee86e37aabc2a71fe902021615d63c27a6fb52caa9393378ba693da53e66761d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorSettingsConnectedHome, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7976d5d03a5cf0161db0bf97dc2e745771b8109597e34117152efcc6b5d41bb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RekognitionStreamProcessorSettingsFaceSearch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34731115b70a0ebd3dd663c592a05ece6b661ca265bde96cbdf499e46b62f9a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d8eaf88cf5aba70601abb0fbb513d5465d687800fd86db3e03b19df91b75c4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e4a911038158d2252bd09944c9f20f778ab3e9ba5488bb585c80153a7385a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016ccb04c34bd3226782f6caf233178c56cd23e319667976dc107cb4ae56db10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509b30e1da0539972483c9f00206fb29b44e1bd4ab6ef2b574fb403fd9a2141a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e4175c1fe80b399813c0f5a07eeedf314de9555715cc01c24c412004d3e0b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52904d5f536ece80f295d440d28f8a2b72a66741b1056fafaa0bf1ee789b7c22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RekognitionStreamProcessorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
