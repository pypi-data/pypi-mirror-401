r'''
# `aws_elastictranscoder_preset`

Refer to the Terraform Registry for docs: [`aws_elastictranscoder_preset`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset).
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


class ElastictranscoderPreset(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPreset",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset aws_elastictranscoder_preset}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        container: builtins.str,
        audio: typing.Optional[typing.Union["ElastictranscoderPresetAudio", typing.Dict[builtins.str, typing.Any]]] = None,
        audio_codec_options: typing.Optional[typing.Union["ElastictranscoderPresetAudioCodecOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        thumbnails: typing.Optional[typing.Union["ElastictranscoderPresetThumbnails", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        video: typing.Optional[typing.Union["ElastictranscoderPresetVideo", typing.Dict[builtins.str, typing.Any]]] = None,
        video_codec_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        video_watermarks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastictranscoderPresetVideoWatermarks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset aws_elastictranscoder_preset} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param container: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#container ElastictranscoderPreset#container}.
        :param audio: audio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#audio ElastictranscoderPreset#audio}
        :param audio_codec_options: audio_codec_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#audio_codec_options ElastictranscoderPreset#audio_codec_options}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#description ElastictranscoderPreset#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#id ElastictranscoderPreset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#name ElastictranscoderPreset#name}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#region ElastictranscoderPreset#region}
        :param thumbnails: thumbnails block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#thumbnails ElastictranscoderPreset#thumbnails}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#type ElastictranscoderPreset#type}.
        :param video: video block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#video ElastictranscoderPreset#video}
        :param video_codec_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#video_codec_options ElastictranscoderPreset#video_codec_options}.
        :param video_watermarks: video_watermarks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#video_watermarks ElastictranscoderPreset#video_watermarks}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d50a118f3b1d9ddba04be25eeeb8552bd4ee623fc8c9fff8703f56c41f5981d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ElastictranscoderPresetConfig(
            container=container,
            audio=audio,
            audio_codec_options=audio_codec_options,
            description=description,
            id=id,
            name=name,
            region=region,
            thumbnails=thumbnails,
            type=type,
            video=video,
            video_codec_options=video_codec_options,
            video_watermarks=video_watermarks,
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
        '''Generates CDKTF code for importing a ElastictranscoderPreset resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ElastictranscoderPreset to import.
        :param import_from_id: The id of the existing ElastictranscoderPreset that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ElastictranscoderPreset to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f1c0eee7e0e1c1c8270df0abb850f4ce0becb11f036e7d2905930d020620db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAudio")
    def put_audio(
        self,
        *,
        audio_packing_mode: typing.Optional[builtins.str] = None,
        bit_rate: typing.Optional[builtins.str] = None,
        channels: typing.Optional[builtins.str] = None,
        codec: typing.Optional[builtins.str] = None,
        sample_rate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audio_packing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#audio_packing_mode ElastictranscoderPreset#audio_packing_mode}.
        :param bit_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_rate ElastictranscoderPreset#bit_rate}.
        :param channels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#channels ElastictranscoderPreset#channels}.
        :param codec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#codec ElastictranscoderPreset#codec}.
        :param sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sample_rate ElastictranscoderPreset#sample_rate}.
        '''
        value = ElastictranscoderPresetAudio(
            audio_packing_mode=audio_packing_mode,
            bit_rate=bit_rate,
            channels=channels,
            codec=codec,
            sample_rate=sample_rate,
        )

        return typing.cast(None, jsii.invoke(self, "putAudio", [value]))

    @jsii.member(jsii_name="putAudioCodecOptions")
    def put_audio_codec_options(
        self,
        *,
        bit_depth: typing.Optional[builtins.str] = None,
        bit_order: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        signed: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bit_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_depth ElastictranscoderPreset#bit_depth}.
        :param bit_order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_order ElastictranscoderPreset#bit_order}.
        :param profile: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#profile ElastictranscoderPreset#profile}.
        :param signed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#signed ElastictranscoderPreset#signed}.
        '''
        value = ElastictranscoderPresetAudioCodecOptions(
            bit_depth=bit_depth, bit_order=bit_order, profile=profile, signed=signed
        )

        return typing.cast(None, jsii.invoke(self, "putAudioCodecOptions", [value]))

    @jsii.member(jsii_name="putThumbnails")
    def put_thumbnails(
        self,
        *,
        aspect_ratio: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        interval: typing.Optional[builtins.str] = None,
        max_height: typing.Optional[builtins.str] = None,
        max_width: typing.Optional[builtins.str] = None,
        padding_policy: typing.Optional[builtins.str] = None,
        resolution: typing.Optional[builtins.str] = None,
        sizing_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aspect_ratio: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#aspect_ratio ElastictranscoderPreset#aspect_ratio}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#format ElastictranscoderPreset#format}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#interval ElastictranscoderPreset#interval}.
        :param max_height: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_height ElastictranscoderPreset#max_height}.
        :param max_width: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_width ElastictranscoderPreset#max_width}.
        :param padding_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#padding_policy ElastictranscoderPreset#padding_policy}.
        :param resolution: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#resolution ElastictranscoderPreset#resolution}.
        :param sizing_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sizing_policy ElastictranscoderPreset#sizing_policy}.
        '''
        value = ElastictranscoderPresetThumbnails(
            aspect_ratio=aspect_ratio,
            format=format,
            interval=interval,
            max_height=max_height,
            max_width=max_width,
            padding_policy=padding_policy,
            resolution=resolution,
            sizing_policy=sizing_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putThumbnails", [value]))

    @jsii.member(jsii_name="putVideo")
    def put_video(
        self,
        *,
        aspect_ratio: typing.Optional[builtins.str] = None,
        bit_rate: typing.Optional[builtins.str] = None,
        codec: typing.Optional[builtins.str] = None,
        display_aspect_ratio: typing.Optional[builtins.str] = None,
        fixed_gop: typing.Optional[builtins.str] = None,
        frame_rate: typing.Optional[builtins.str] = None,
        keyframes_max_dist: typing.Optional[builtins.str] = None,
        max_frame_rate: typing.Optional[builtins.str] = None,
        max_height: typing.Optional[builtins.str] = None,
        max_width: typing.Optional[builtins.str] = None,
        padding_policy: typing.Optional[builtins.str] = None,
        resolution: typing.Optional[builtins.str] = None,
        sizing_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aspect_ratio: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#aspect_ratio ElastictranscoderPreset#aspect_ratio}.
        :param bit_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_rate ElastictranscoderPreset#bit_rate}.
        :param codec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#codec ElastictranscoderPreset#codec}.
        :param display_aspect_ratio: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#display_aspect_ratio ElastictranscoderPreset#display_aspect_ratio}.
        :param fixed_gop: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#fixed_gop ElastictranscoderPreset#fixed_gop}.
        :param frame_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#frame_rate ElastictranscoderPreset#frame_rate}.
        :param keyframes_max_dist: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#keyframes_max_dist ElastictranscoderPreset#keyframes_max_dist}.
        :param max_frame_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_frame_rate ElastictranscoderPreset#max_frame_rate}.
        :param max_height: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_height ElastictranscoderPreset#max_height}.
        :param max_width: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_width ElastictranscoderPreset#max_width}.
        :param padding_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#padding_policy ElastictranscoderPreset#padding_policy}.
        :param resolution: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#resolution ElastictranscoderPreset#resolution}.
        :param sizing_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sizing_policy ElastictranscoderPreset#sizing_policy}.
        '''
        value = ElastictranscoderPresetVideo(
            aspect_ratio=aspect_ratio,
            bit_rate=bit_rate,
            codec=codec,
            display_aspect_ratio=display_aspect_ratio,
            fixed_gop=fixed_gop,
            frame_rate=frame_rate,
            keyframes_max_dist=keyframes_max_dist,
            max_frame_rate=max_frame_rate,
            max_height=max_height,
            max_width=max_width,
            padding_policy=padding_policy,
            resolution=resolution,
            sizing_policy=sizing_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putVideo", [value]))

    @jsii.member(jsii_name="putVideoWatermarks")
    def put_video_watermarks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastictranscoderPresetVideoWatermarks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23a8fa356a9ead71e171bd1bbce60b883698c239c396124b95582ab5cb17084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVideoWatermarks", [value]))

    @jsii.member(jsii_name="resetAudio")
    def reset_audio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudio", []))

    @jsii.member(jsii_name="resetAudioCodecOptions")
    def reset_audio_codec_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioCodecOptions", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetThumbnails")
    def reset_thumbnails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThumbnails", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetVideo")
    def reset_video(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVideo", []))

    @jsii.member(jsii_name="resetVideoCodecOptions")
    def reset_video_codec_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVideoCodecOptions", []))

    @jsii.member(jsii_name="resetVideoWatermarks")
    def reset_video_watermarks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVideoWatermarks", []))

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
    @jsii.member(jsii_name="audio")
    def audio(self) -> "ElastictranscoderPresetAudioOutputReference":
        return typing.cast("ElastictranscoderPresetAudioOutputReference", jsii.get(self, "audio"))

    @builtins.property
    @jsii.member(jsii_name="audioCodecOptions")
    def audio_codec_options(
        self,
    ) -> "ElastictranscoderPresetAudioCodecOptionsOutputReference":
        return typing.cast("ElastictranscoderPresetAudioCodecOptionsOutputReference", jsii.get(self, "audioCodecOptions"))

    @builtins.property
    @jsii.member(jsii_name="thumbnails")
    def thumbnails(self) -> "ElastictranscoderPresetThumbnailsOutputReference":
        return typing.cast("ElastictranscoderPresetThumbnailsOutputReference", jsii.get(self, "thumbnails"))

    @builtins.property
    @jsii.member(jsii_name="video")
    def video(self) -> "ElastictranscoderPresetVideoOutputReference":
        return typing.cast("ElastictranscoderPresetVideoOutputReference", jsii.get(self, "video"))

    @builtins.property
    @jsii.member(jsii_name="videoWatermarks")
    def video_watermarks(self) -> "ElastictranscoderPresetVideoWatermarksList":
        return typing.cast("ElastictranscoderPresetVideoWatermarksList", jsii.get(self, "videoWatermarks"))

    @builtins.property
    @jsii.member(jsii_name="audioCodecOptionsInput")
    def audio_codec_options_input(
        self,
    ) -> typing.Optional["ElastictranscoderPresetAudioCodecOptions"]:
        return typing.cast(typing.Optional["ElastictranscoderPresetAudioCodecOptions"], jsii.get(self, "audioCodecOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="audioInput")
    def audio_input(self) -> typing.Optional["ElastictranscoderPresetAudio"]:
        return typing.cast(typing.Optional["ElastictranscoderPresetAudio"], jsii.get(self, "audioInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerInput"))

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
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbnailsInput")
    def thumbnails_input(self) -> typing.Optional["ElastictranscoderPresetThumbnails"]:
        return typing.cast(typing.Optional["ElastictranscoderPresetThumbnails"], jsii.get(self, "thumbnailsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="videoCodecOptionsInput")
    def video_codec_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "videoCodecOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="videoInput")
    def video_input(self) -> typing.Optional["ElastictranscoderPresetVideo"]:
        return typing.cast(typing.Optional["ElastictranscoderPresetVideo"], jsii.get(self, "videoInput"))

    @builtins.property
    @jsii.member(jsii_name="videoWatermarksInput")
    def video_watermarks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPresetVideoWatermarks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPresetVideoWatermarks"]]], jsii.get(self, "videoWatermarksInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42889b966c0a571fbeefaf50f046e29e81b51bf35b46bf4f6b28e7e269820369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6406d802fdd1344875f4f7cc77672fea7469a243381027ad41bab45271a22b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13920b8064443704857c8e0b11a58d9d411daedbe754bda7ce7a5b5a583cdf4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38ce4638031beffd1f98d2ec24ebd887348049ccd43fc5170bc5e32e1b16e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1952f546c01156c3c15855ce391048caafda0477f90525800f186917b80ea7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445e7310128b1d747b95cacc758c75f85a72bb372baa0eef44a22b040df3df71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="videoCodecOptions")
    def video_codec_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "videoCodecOptions"))

    @video_codec_options.setter
    def video_codec_options(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf0bba8542bd29b78a2ce4d1071ef69ed985cf4c589a7b3cdb2824460d75621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "videoCodecOptions", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetAudio",
    jsii_struct_bases=[],
    name_mapping={
        "audio_packing_mode": "audioPackingMode",
        "bit_rate": "bitRate",
        "channels": "channels",
        "codec": "codec",
        "sample_rate": "sampleRate",
    },
)
class ElastictranscoderPresetAudio:
    def __init__(
        self,
        *,
        audio_packing_mode: typing.Optional[builtins.str] = None,
        bit_rate: typing.Optional[builtins.str] = None,
        channels: typing.Optional[builtins.str] = None,
        codec: typing.Optional[builtins.str] = None,
        sample_rate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audio_packing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#audio_packing_mode ElastictranscoderPreset#audio_packing_mode}.
        :param bit_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_rate ElastictranscoderPreset#bit_rate}.
        :param channels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#channels ElastictranscoderPreset#channels}.
        :param codec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#codec ElastictranscoderPreset#codec}.
        :param sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sample_rate ElastictranscoderPreset#sample_rate}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa54a95d777a8efa116c5004553a12a3fb790cb5f400606821f5cb52b6a3f66e)
            check_type(argname="argument audio_packing_mode", value=audio_packing_mode, expected_type=type_hints["audio_packing_mode"])
            check_type(argname="argument bit_rate", value=bit_rate, expected_type=type_hints["bit_rate"])
            check_type(argname="argument channels", value=channels, expected_type=type_hints["channels"])
            check_type(argname="argument codec", value=codec, expected_type=type_hints["codec"])
            check_type(argname="argument sample_rate", value=sample_rate, expected_type=type_hints["sample_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audio_packing_mode is not None:
            self._values["audio_packing_mode"] = audio_packing_mode
        if bit_rate is not None:
            self._values["bit_rate"] = bit_rate
        if channels is not None:
            self._values["channels"] = channels
        if codec is not None:
            self._values["codec"] = codec
        if sample_rate is not None:
            self._values["sample_rate"] = sample_rate

    @builtins.property
    def audio_packing_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#audio_packing_mode ElastictranscoderPreset#audio_packing_mode}.'''
        result = self._values.get("audio_packing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bit_rate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_rate ElastictranscoderPreset#bit_rate}.'''
        result = self._values.get("bit_rate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channels(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#channels ElastictranscoderPreset#channels}.'''
        result = self._values.get("channels")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codec(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#codec ElastictranscoderPreset#codec}.'''
        result = self._values.get("codec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_rate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sample_rate ElastictranscoderPreset#sample_rate}.'''
        result = self._values.get("sample_rate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPresetAudio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetAudioCodecOptions",
    jsii_struct_bases=[],
    name_mapping={
        "bit_depth": "bitDepth",
        "bit_order": "bitOrder",
        "profile": "profile",
        "signed": "signed",
    },
)
class ElastictranscoderPresetAudioCodecOptions:
    def __init__(
        self,
        *,
        bit_depth: typing.Optional[builtins.str] = None,
        bit_order: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        signed: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bit_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_depth ElastictranscoderPreset#bit_depth}.
        :param bit_order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_order ElastictranscoderPreset#bit_order}.
        :param profile: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#profile ElastictranscoderPreset#profile}.
        :param signed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#signed ElastictranscoderPreset#signed}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424593bb86ea17a56111457e6785079b8be35426cc607f00ddc3651231fbe7d8)
            check_type(argname="argument bit_depth", value=bit_depth, expected_type=type_hints["bit_depth"])
            check_type(argname="argument bit_order", value=bit_order, expected_type=type_hints["bit_order"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument signed", value=signed, expected_type=type_hints["signed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bit_depth is not None:
            self._values["bit_depth"] = bit_depth
        if bit_order is not None:
            self._values["bit_order"] = bit_order
        if profile is not None:
            self._values["profile"] = profile
        if signed is not None:
            self._values["signed"] = signed

    @builtins.property
    def bit_depth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_depth ElastictranscoderPreset#bit_depth}.'''
        result = self._values.get("bit_depth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bit_order(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_order ElastictranscoderPreset#bit_order}.'''
        result = self._values.get("bit_order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#profile ElastictranscoderPreset#profile}.'''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signed(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#signed ElastictranscoderPreset#signed}.'''
        result = self._values.get("signed")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPresetAudioCodecOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastictranscoderPresetAudioCodecOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetAudioCodecOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d50e25ff6a09ef3a08d8f2d7da8b984dbebe9496a73c412861b2cd5218701b24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBitDepth")
    def reset_bit_depth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitDepth", []))

    @jsii.member(jsii_name="resetBitOrder")
    def reset_bit_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitOrder", []))

    @jsii.member(jsii_name="resetProfile")
    def reset_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfile", []))

    @jsii.member(jsii_name="resetSigned")
    def reset_signed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSigned", []))

    @builtins.property
    @jsii.member(jsii_name="bitDepthInput")
    def bit_depth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bitDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="bitOrderInput")
    def bit_order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bitOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="profileInput")
    def profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileInput"))

    @builtins.property
    @jsii.member(jsii_name="signedInput")
    def signed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signedInput"))

    @builtins.property
    @jsii.member(jsii_name="bitDepth")
    def bit_depth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bitDepth"))

    @bit_depth.setter
    def bit_depth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c074b3513f4d926929146565eedbb8076d9c6f8c64b70c160f0b94999863b93c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bitOrder")
    def bit_order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bitOrder"))

    @bit_order.setter
    def bit_order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb5086d54e590da34f040ed32071c9414095acc49f64c7cfcdebef2923afb86c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitOrder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profile")
    def profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profile"))

    @profile.setter
    def profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3cf09e80395d9bff13b7257c3b01f403f4c6a009491d7637db4e704d253baf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signed")
    def signed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signed"))

    @signed.setter
    def signed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27adac483b357caf6977c921d371d28c2a97bfdb7fb5460542dc1d412f52d3cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ElastictranscoderPresetAudioCodecOptions]:
        return typing.cast(typing.Optional[ElastictranscoderPresetAudioCodecOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElastictranscoderPresetAudioCodecOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60ae960250b44938ee79e7548451a2b9c397249362201c45fd236d56d151376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ElastictranscoderPresetAudioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetAudioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f8c35670fa2d1ba6d587d97ae63c153605503a73791424e4a2345fb6be38181)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudioPackingMode")
    def reset_audio_packing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioPackingMode", []))

    @jsii.member(jsii_name="resetBitRate")
    def reset_bit_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitRate", []))

    @jsii.member(jsii_name="resetChannels")
    def reset_channels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannels", []))

    @jsii.member(jsii_name="resetCodec")
    def reset_codec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodec", []))

    @jsii.member(jsii_name="resetSampleRate")
    def reset_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleRate", []))

    @builtins.property
    @jsii.member(jsii_name="audioPackingModeInput")
    def audio_packing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioPackingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bitRateInput")
    def bit_rate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bitRateInput"))

    @builtins.property
    @jsii.member(jsii_name="channelsInput")
    def channels_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelsInput"))

    @builtins.property
    @jsii.member(jsii_name="codecInput")
    def codec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codecInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleRateInput")
    def sample_rate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="audioPackingMode")
    def audio_packing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioPackingMode"))

    @audio_packing_mode.setter
    def audio_packing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b665e62b7d7f51b37c7cc09cc7f12f217cf941ad0a643fa305424d25d07bf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioPackingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bitRate")
    def bit_rate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bitRate"))

    @bit_rate.setter
    def bit_rate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee8cacaf49b630221ff7a184aca810080905162f694682b4d8622531735905f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channels")
    def channels(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channels"))

    @channels.setter
    def channels(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54479fd4ead551477b484f1f027e6e9fd4f534d05f5e263cc4168cea1f80f533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codec")
    def codec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codec"))

    @codec.setter
    def codec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28df4833114a65cee854539b59d2b780f7c01a287d237c13adb4695ccdc92ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRate")
    def sample_rate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sampleRate"))

    @sample_rate.setter
    def sample_rate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65c3c175d430586e381a66d97be29a921b44eeec76a62080d9701f9ee842577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElastictranscoderPresetAudio]:
        return typing.cast(typing.Optional[ElastictranscoderPresetAudio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElastictranscoderPresetAudio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c901ef9dbf4924e7552105b65d631971507ad601b271c2e4d7ad48170decc578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "container": "container",
        "audio": "audio",
        "audio_codec_options": "audioCodecOptions",
        "description": "description",
        "id": "id",
        "name": "name",
        "region": "region",
        "thumbnails": "thumbnails",
        "type": "type",
        "video": "video",
        "video_codec_options": "videoCodecOptions",
        "video_watermarks": "videoWatermarks",
    },
)
class ElastictranscoderPresetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        container: builtins.str,
        audio: typing.Optional[typing.Union[ElastictranscoderPresetAudio, typing.Dict[builtins.str, typing.Any]]] = None,
        audio_codec_options: typing.Optional[typing.Union[ElastictranscoderPresetAudioCodecOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        thumbnails: typing.Optional[typing.Union["ElastictranscoderPresetThumbnails", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        video: typing.Optional[typing.Union["ElastictranscoderPresetVideo", typing.Dict[builtins.str, typing.Any]]] = None,
        video_codec_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        video_watermarks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastictranscoderPresetVideoWatermarks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param container: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#container ElastictranscoderPreset#container}.
        :param audio: audio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#audio ElastictranscoderPreset#audio}
        :param audio_codec_options: audio_codec_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#audio_codec_options ElastictranscoderPreset#audio_codec_options}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#description ElastictranscoderPreset#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#id ElastictranscoderPreset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#name ElastictranscoderPreset#name}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#region ElastictranscoderPreset#region}
        :param thumbnails: thumbnails block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#thumbnails ElastictranscoderPreset#thumbnails}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#type ElastictranscoderPreset#type}.
        :param video: video block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#video ElastictranscoderPreset#video}
        :param video_codec_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#video_codec_options ElastictranscoderPreset#video_codec_options}.
        :param video_watermarks: video_watermarks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#video_watermarks ElastictranscoderPreset#video_watermarks}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(audio, dict):
            audio = ElastictranscoderPresetAudio(**audio)
        if isinstance(audio_codec_options, dict):
            audio_codec_options = ElastictranscoderPresetAudioCodecOptions(**audio_codec_options)
        if isinstance(thumbnails, dict):
            thumbnails = ElastictranscoderPresetThumbnails(**thumbnails)
        if isinstance(video, dict):
            video = ElastictranscoderPresetVideo(**video)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2165084cf446e180755a5a9359de1df7623c26dd4a8b59a4bd2a1cd77438d8a7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument audio", value=audio, expected_type=type_hints["audio"])
            check_type(argname="argument audio_codec_options", value=audio_codec_options, expected_type=type_hints["audio_codec_options"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument thumbnails", value=thumbnails, expected_type=type_hints["thumbnails"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument video", value=video, expected_type=type_hints["video"])
            check_type(argname="argument video_codec_options", value=video_codec_options, expected_type=type_hints["video_codec_options"])
            check_type(argname="argument video_watermarks", value=video_watermarks, expected_type=type_hints["video_watermarks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
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
        if audio is not None:
            self._values["audio"] = audio
        if audio_codec_options is not None:
            self._values["audio_codec_options"] = audio_codec_options
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region
        if thumbnails is not None:
            self._values["thumbnails"] = thumbnails
        if type is not None:
            self._values["type"] = type
        if video is not None:
            self._values["video"] = video
        if video_codec_options is not None:
            self._values["video_codec_options"] = video_codec_options
        if video_watermarks is not None:
            self._values["video_watermarks"] = video_watermarks

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
    def container(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#container ElastictranscoderPreset#container}.'''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audio(self) -> typing.Optional[ElastictranscoderPresetAudio]:
        '''audio block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#audio ElastictranscoderPreset#audio}
        '''
        result = self._values.get("audio")
        return typing.cast(typing.Optional[ElastictranscoderPresetAudio], result)

    @builtins.property
    def audio_codec_options(
        self,
    ) -> typing.Optional[ElastictranscoderPresetAudioCodecOptions]:
        '''audio_codec_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#audio_codec_options ElastictranscoderPreset#audio_codec_options}
        '''
        result = self._values.get("audio_codec_options")
        return typing.cast(typing.Optional[ElastictranscoderPresetAudioCodecOptions], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#description ElastictranscoderPreset#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#id ElastictranscoderPreset#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#name ElastictranscoderPreset#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#region ElastictranscoderPreset#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thumbnails(self) -> typing.Optional["ElastictranscoderPresetThumbnails"]:
        '''thumbnails block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#thumbnails ElastictranscoderPreset#thumbnails}
        '''
        result = self._values.get("thumbnails")
        return typing.cast(typing.Optional["ElastictranscoderPresetThumbnails"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#type ElastictranscoderPreset#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def video(self) -> typing.Optional["ElastictranscoderPresetVideo"]:
        '''video block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#video ElastictranscoderPreset#video}
        '''
        result = self._values.get("video")
        return typing.cast(typing.Optional["ElastictranscoderPresetVideo"], result)

    @builtins.property
    def video_codec_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#video_codec_options ElastictranscoderPreset#video_codec_options}.'''
        result = self._values.get("video_codec_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def video_watermarks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPresetVideoWatermarks"]]]:
        '''video_watermarks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#video_watermarks ElastictranscoderPreset#video_watermarks}
        '''
        result = self._values.get("video_watermarks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPresetVideoWatermarks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPresetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetThumbnails",
    jsii_struct_bases=[],
    name_mapping={
        "aspect_ratio": "aspectRatio",
        "format": "format",
        "interval": "interval",
        "max_height": "maxHeight",
        "max_width": "maxWidth",
        "padding_policy": "paddingPolicy",
        "resolution": "resolution",
        "sizing_policy": "sizingPolicy",
    },
)
class ElastictranscoderPresetThumbnails:
    def __init__(
        self,
        *,
        aspect_ratio: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        interval: typing.Optional[builtins.str] = None,
        max_height: typing.Optional[builtins.str] = None,
        max_width: typing.Optional[builtins.str] = None,
        padding_policy: typing.Optional[builtins.str] = None,
        resolution: typing.Optional[builtins.str] = None,
        sizing_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aspect_ratio: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#aspect_ratio ElastictranscoderPreset#aspect_ratio}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#format ElastictranscoderPreset#format}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#interval ElastictranscoderPreset#interval}.
        :param max_height: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_height ElastictranscoderPreset#max_height}.
        :param max_width: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_width ElastictranscoderPreset#max_width}.
        :param padding_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#padding_policy ElastictranscoderPreset#padding_policy}.
        :param resolution: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#resolution ElastictranscoderPreset#resolution}.
        :param sizing_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sizing_policy ElastictranscoderPreset#sizing_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b7c140d96559acb09639831d7302ace24089b4446f96b689e3dfd27c63618d)
            check_type(argname="argument aspect_ratio", value=aspect_ratio, expected_type=type_hints["aspect_ratio"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument max_height", value=max_height, expected_type=type_hints["max_height"])
            check_type(argname="argument max_width", value=max_width, expected_type=type_hints["max_width"])
            check_type(argname="argument padding_policy", value=padding_policy, expected_type=type_hints["padding_policy"])
            check_type(argname="argument resolution", value=resolution, expected_type=type_hints["resolution"])
            check_type(argname="argument sizing_policy", value=sizing_policy, expected_type=type_hints["sizing_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aspect_ratio is not None:
            self._values["aspect_ratio"] = aspect_ratio
        if format is not None:
            self._values["format"] = format
        if interval is not None:
            self._values["interval"] = interval
        if max_height is not None:
            self._values["max_height"] = max_height
        if max_width is not None:
            self._values["max_width"] = max_width
        if padding_policy is not None:
            self._values["padding_policy"] = padding_policy
        if resolution is not None:
            self._values["resolution"] = resolution
        if sizing_policy is not None:
            self._values["sizing_policy"] = sizing_policy

    @builtins.property
    def aspect_ratio(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#aspect_ratio ElastictranscoderPreset#aspect_ratio}.'''
        result = self._values.get("aspect_ratio")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#format ElastictranscoderPreset#format}.'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#interval ElastictranscoderPreset#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_height(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_height ElastictranscoderPreset#max_height}.'''
        result = self._values.get("max_height")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_width(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_width ElastictranscoderPreset#max_width}.'''
        result = self._values.get("max_width")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def padding_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#padding_policy ElastictranscoderPreset#padding_policy}.'''
        result = self._values.get("padding_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolution(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#resolution ElastictranscoderPreset#resolution}.'''
        result = self._values.get("resolution")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sizing_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sizing_policy ElastictranscoderPreset#sizing_policy}.'''
        result = self._values.get("sizing_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPresetThumbnails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastictranscoderPresetThumbnailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetThumbnailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__723778c9715854eb2fd7ba28f1b5fc8c40c23f5c80f63da7e5b1074a5ed6083e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAspectRatio")
    def reset_aspect_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAspectRatio", []))

    @jsii.member(jsii_name="resetFormat")
    def reset_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFormat", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetMaxHeight")
    def reset_max_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxHeight", []))

    @jsii.member(jsii_name="resetMaxWidth")
    def reset_max_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxWidth", []))

    @jsii.member(jsii_name="resetPaddingPolicy")
    def reset_padding_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaddingPolicy", []))

    @jsii.member(jsii_name="resetResolution")
    def reset_resolution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResolution", []))

    @jsii.member(jsii_name="resetSizingPolicy")
    def reset_sizing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizingPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="aspectRatioInput")
    def aspect_ratio_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aspectRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="maxHeightInput")
    def max_height_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxHeightInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWidthInput")
    def max_width_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxWidthInput"))

    @builtins.property
    @jsii.member(jsii_name="paddingPolicyInput")
    def padding_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "paddingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="resolutionInput")
    def resolution_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resolutionInput"))

    @builtins.property
    @jsii.member(jsii_name="sizingPolicyInput")
    def sizing_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="aspectRatio")
    def aspect_ratio(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aspectRatio"))

    @aspect_ratio.setter
    def aspect_ratio(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4673f0cdbd7c3fc7fa533aead64a103c9442fc763324f215b6bf32afd2df0957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aspectRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047559658ec7d7d1132fc8013ffb9d44d09a07510b850b7c58e0501944309669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4299a0c51e6c7494d7356ad1bcd23fe7555ce8c8de61d7e1f1b1839c2eab139c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxHeight")
    def max_height(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxHeight"))

    @max_height.setter
    def max_height(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901b3fdbe282c3372935bf06ae0392edf162c11f83ff22c4e04e90d249fd24b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxHeight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWidth")
    def max_width(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxWidth"))

    @max_width.setter
    def max_width(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac621cbeca8efb53dae0e797bdfaf1bd42ad24f44a12972f4f0465b93e1f8453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paddingPolicy")
    def padding_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "paddingPolicy"))

    @padding_policy.setter
    def padding_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4311a66040d81e530b7944cf5e961574e98885900202fe4a32989c60886bce61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paddingPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resolution")
    def resolution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resolution"))

    @resolution.setter
    def resolution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52db27f9ade1555f3b4b5a5e89d9f5feb75a3e9ace08a24dbb64916a13d4f9cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizingPolicy")
    def sizing_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizingPolicy"))

    @sizing_policy.setter
    def sizing_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b61a38610e0d6bdba569f6814a79080223bd9382a022507a68ab5e4f572425c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizingPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElastictranscoderPresetThumbnails]:
        return typing.cast(typing.Optional[ElastictranscoderPresetThumbnails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElastictranscoderPresetThumbnails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7049a06eb46ad18e2e8d475bc2bbb8b2b07e9cae02f450a06c53a04b7d2d193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetVideo",
    jsii_struct_bases=[],
    name_mapping={
        "aspect_ratio": "aspectRatio",
        "bit_rate": "bitRate",
        "codec": "codec",
        "display_aspect_ratio": "displayAspectRatio",
        "fixed_gop": "fixedGop",
        "frame_rate": "frameRate",
        "keyframes_max_dist": "keyframesMaxDist",
        "max_frame_rate": "maxFrameRate",
        "max_height": "maxHeight",
        "max_width": "maxWidth",
        "padding_policy": "paddingPolicy",
        "resolution": "resolution",
        "sizing_policy": "sizingPolicy",
    },
)
class ElastictranscoderPresetVideo:
    def __init__(
        self,
        *,
        aspect_ratio: typing.Optional[builtins.str] = None,
        bit_rate: typing.Optional[builtins.str] = None,
        codec: typing.Optional[builtins.str] = None,
        display_aspect_ratio: typing.Optional[builtins.str] = None,
        fixed_gop: typing.Optional[builtins.str] = None,
        frame_rate: typing.Optional[builtins.str] = None,
        keyframes_max_dist: typing.Optional[builtins.str] = None,
        max_frame_rate: typing.Optional[builtins.str] = None,
        max_height: typing.Optional[builtins.str] = None,
        max_width: typing.Optional[builtins.str] = None,
        padding_policy: typing.Optional[builtins.str] = None,
        resolution: typing.Optional[builtins.str] = None,
        sizing_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aspect_ratio: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#aspect_ratio ElastictranscoderPreset#aspect_ratio}.
        :param bit_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_rate ElastictranscoderPreset#bit_rate}.
        :param codec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#codec ElastictranscoderPreset#codec}.
        :param display_aspect_ratio: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#display_aspect_ratio ElastictranscoderPreset#display_aspect_ratio}.
        :param fixed_gop: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#fixed_gop ElastictranscoderPreset#fixed_gop}.
        :param frame_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#frame_rate ElastictranscoderPreset#frame_rate}.
        :param keyframes_max_dist: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#keyframes_max_dist ElastictranscoderPreset#keyframes_max_dist}.
        :param max_frame_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_frame_rate ElastictranscoderPreset#max_frame_rate}.
        :param max_height: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_height ElastictranscoderPreset#max_height}.
        :param max_width: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_width ElastictranscoderPreset#max_width}.
        :param padding_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#padding_policy ElastictranscoderPreset#padding_policy}.
        :param resolution: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#resolution ElastictranscoderPreset#resolution}.
        :param sizing_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sizing_policy ElastictranscoderPreset#sizing_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045da46a0caa4dfc1f124fe8b53e3a7d69003d57f347a3c9ee855a87999a4d7d)
            check_type(argname="argument aspect_ratio", value=aspect_ratio, expected_type=type_hints["aspect_ratio"])
            check_type(argname="argument bit_rate", value=bit_rate, expected_type=type_hints["bit_rate"])
            check_type(argname="argument codec", value=codec, expected_type=type_hints["codec"])
            check_type(argname="argument display_aspect_ratio", value=display_aspect_ratio, expected_type=type_hints["display_aspect_ratio"])
            check_type(argname="argument fixed_gop", value=fixed_gop, expected_type=type_hints["fixed_gop"])
            check_type(argname="argument frame_rate", value=frame_rate, expected_type=type_hints["frame_rate"])
            check_type(argname="argument keyframes_max_dist", value=keyframes_max_dist, expected_type=type_hints["keyframes_max_dist"])
            check_type(argname="argument max_frame_rate", value=max_frame_rate, expected_type=type_hints["max_frame_rate"])
            check_type(argname="argument max_height", value=max_height, expected_type=type_hints["max_height"])
            check_type(argname="argument max_width", value=max_width, expected_type=type_hints["max_width"])
            check_type(argname="argument padding_policy", value=padding_policy, expected_type=type_hints["padding_policy"])
            check_type(argname="argument resolution", value=resolution, expected_type=type_hints["resolution"])
            check_type(argname="argument sizing_policy", value=sizing_policy, expected_type=type_hints["sizing_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aspect_ratio is not None:
            self._values["aspect_ratio"] = aspect_ratio
        if bit_rate is not None:
            self._values["bit_rate"] = bit_rate
        if codec is not None:
            self._values["codec"] = codec
        if display_aspect_ratio is not None:
            self._values["display_aspect_ratio"] = display_aspect_ratio
        if fixed_gop is not None:
            self._values["fixed_gop"] = fixed_gop
        if frame_rate is not None:
            self._values["frame_rate"] = frame_rate
        if keyframes_max_dist is not None:
            self._values["keyframes_max_dist"] = keyframes_max_dist
        if max_frame_rate is not None:
            self._values["max_frame_rate"] = max_frame_rate
        if max_height is not None:
            self._values["max_height"] = max_height
        if max_width is not None:
            self._values["max_width"] = max_width
        if padding_policy is not None:
            self._values["padding_policy"] = padding_policy
        if resolution is not None:
            self._values["resolution"] = resolution
        if sizing_policy is not None:
            self._values["sizing_policy"] = sizing_policy

    @builtins.property
    def aspect_ratio(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#aspect_ratio ElastictranscoderPreset#aspect_ratio}.'''
        result = self._values.get("aspect_ratio")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bit_rate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#bit_rate ElastictranscoderPreset#bit_rate}.'''
        result = self._values.get("bit_rate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codec(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#codec ElastictranscoderPreset#codec}.'''
        result = self._values.get("codec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_aspect_ratio(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#display_aspect_ratio ElastictranscoderPreset#display_aspect_ratio}.'''
        result = self._values.get("display_aspect_ratio")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_gop(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#fixed_gop ElastictranscoderPreset#fixed_gop}.'''
        result = self._values.get("fixed_gop")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def frame_rate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#frame_rate ElastictranscoderPreset#frame_rate}.'''
        result = self._values.get("frame_rate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keyframes_max_dist(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#keyframes_max_dist ElastictranscoderPreset#keyframes_max_dist}.'''
        result = self._values.get("keyframes_max_dist")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_frame_rate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_frame_rate ElastictranscoderPreset#max_frame_rate}.'''
        result = self._values.get("max_frame_rate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_height(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_height ElastictranscoderPreset#max_height}.'''
        result = self._values.get("max_height")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_width(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_width ElastictranscoderPreset#max_width}.'''
        result = self._values.get("max_width")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def padding_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#padding_policy ElastictranscoderPreset#padding_policy}.'''
        result = self._values.get("padding_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolution(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#resolution ElastictranscoderPreset#resolution}.'''
        result = self._values.get("resolution")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sizing_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sizing_policy ElastictranscoderPreset#sizing_policy}.'''
        result = self._values.get("sizing_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPresetVideo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastictranscoderPresetVideoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetVideoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f1ebea6148e3ea1c9af8838e720b16550e4925b89e3cd20fe751492b2b11eee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAspectRatio")
    def reset_aspect_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAspectRatio", []))

    @jsii.member(jsii_name="resetBitRate")
    def reset_bit_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitRate", []))

    @jsii.member(jsii_name="resetCodec")
    def reset_codec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodec", []))

    @jsii.member(jsii_name="resetDisplayAspectRatio")
    def reset_display_aspect_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayAspectRatio", []))

    @jsii.member(jsii_name="resetFixedGop")
    def reset_fixed_gop(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedGop", []))

    @jsii.member(jsii_name="resetFrameRate")
    def reset_frame_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrameRate", []))

    @jsii.member(jsii_name="resetKeyframesMaxDist")
    def reset_keyframes_max_dist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyframesMaxDist", []))

    @jsii.member(jsii_name="resetMaxFrameRate")
    def reset_max_frame_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFrameRate", []))

    @jsii.member(jsii_name="resetMaxHeight")
    def reset_max_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxHeight", []))

    @jsii.member(jsii_name="resetMaxWidth")
    def reset_max_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxWidth", []))

    @jsii.member(jsii_name="resetPaddingPolicy")
    def reset_padding_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaddingPolicy", []))

    @jsii.member(jsii_name="resetResolution")
    def reset_resolution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResolution", []))

    @jsii.member(jsii_name="resetSizingPolicy")
    def reset_sizing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizingPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="aspectRatioInput")
    def aspect_ratio_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aspectRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="bitRateInput")
    def bit_rate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bitRateInput"))

    @builtins.property
    @jsii.member(jsii_name="codecInput")
    def codec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codecInput"))

    @builtins.property
    @jsii.member(jsii_name="displayAspectRatioInput")
    def display_aspect_ratio_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayAspectRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedGopInput")
    def fixed_gop_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedGopInput"))

    @builtins.property
    @jsii.member(jsii_name="frameRateInput")
    def frame_rate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frameRateInput"))

    @builtins.property
    @jsii.member(jsii_name="keyframesMaxDistInput")
    def keyframes_max_dist_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyframesMaxDistInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFrameRateInput")
    def max_frame_rate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxFrameRateInput"))

    @builtins.property
    @jsii.member(jsii_name="maxHeightInput")
    def max_height_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxHeightInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWidthInput")
    def max_width_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxWidthInput"))

    @builtins.property
    @jsii.member(jsii_name="paddingPolicyInput")
    def padding_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "paddingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="resolutionInput")
    def resolution_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resolutionInput"))

    @builtins.property
    @jsii.member(jsii_name="sizingPolicyInput")
    def sizing_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="aspectRatio")
    def aspect_ratio(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aspectRatio"))

    @aspect_ratio.setter
    def aspect_ratio(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f6efb9b6b7e373e92bd5c48da21231a4d541b62d5a2ca4ec039fe5ee869b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aspectRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bitRate")
    def bit_rate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bitRate"))

    @bit_rate.setter
    def bit_rate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701c49824e128c09d33e9cd9464952fcdd6362f42fbe30cb1ca914af733fe47c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codec")
    def codec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codec"))

    @codec.setter
    def codec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e4f2e79325c5ab73b1547ce4f3df9e37ae2716db22c088d5a88a2cdd910fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayAspectRatio")
    def display_aspect_ratio(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayAspectRatio"))

    @display_aspect_ratio.setter
    def display_aspect_ratio(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6d65a3b4bd824ebef9587557d51df28c23831341ac0ac0be1dd7a63e8dff48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayAspectRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedGop")
    def fixed_gop(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedGop"))

    @fixed_gop.setter
    def fixed_gop(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7945be48ec79a0993af726f95e2f9bc0e74b4148d620ffdb9fa7d8b95454f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedGop", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frameRate")
    def frame_rate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frameRate"))

    @frame_rate.setter
    def frame_rate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530d9c85e75fb4f24b6734fdb172d6180630ef92d5628f825b06dd17eb0eb053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frameRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyframesMaxDist")
    def keyframes_max_dist(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyframesMaxDist"))

    @keyframes_max_dist.setter
    def keyframes_max_dist(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f356af7ef6bea267cd6615ceb1ab3ec7f8d3090d0e1053b413d6b7df4c561e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyframesMaxDist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFrameRate")
    def max_frame_rate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxFrameRate"))

    @max_frame_rate.setter
    def max_frame_rate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd3a026fe1f5488c133d3d2b6ad5f1a60ad8a2a6569300bb9fab9687795e720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFrameRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxHeight")
    def max_height(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxHeight"))

    @max_height.setter
    def max_height(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a624a419acabe10952976f2d14484766dc298f5f5ac6258e15ef72232c999dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxHeight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWidth")
    def max_width(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxWidth"))

    @max_width.setter
    def max_width(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e02fff53aff2058468cfee83e0735482c98b94c42fa9dd913067fb89d8eb9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paddingPolicy")
    def padding_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "paddingPolicy"))

    @padding_policy.setter
    def padding_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e90725f3b6a5602778c526e98d19ec311eb6bb33bae72118fec2e849f582e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paddingPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resolution")
    def resolution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resolution"))

    @resolution.setter
    def resolution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e60d2f6072bd0221d8eab7ff105364b2adf7d5c8eabbfdfc88608848983d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizingPolicy")
    def sizing_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizingPolicy"))

    @sizing_policy.setter
    def sizing_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83454d6eeb695a3fab1cae8552bd7fd5c055a23c7ebb9730f2e1f3d9a8642070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizingPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElastictranscoderPresetVideo]:
        return typing.cast(typing.Optional[ElastictranscoderPresetVideo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElastictranscoderPresetVideo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5431ede549e438d20081fba95492922788e43fd3550f1f0d55a12c837108fcb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetVideoWatermarks",
    jsii_struct_bases=[],
    name_mapping={
        "horizontal_align": "horizontalAlign",
        "horizontal_offset": "horizontalOffset",
        "id": "id",
        "max_height": "maxHeight",
        "max_width": "maxWidth",
        "opacity": "opacity",
        "sizing_policy": "sizingPolicy",
        "target": "target",
        "vertical_align": "verticalAlign",
        "vertical_offset": "verticalOffset",
    },
)
class ElastictranscoderPresetVideoWatermarks:
    def __init__(
        self,
        *,
        horizontal_align: typing.Optional[builtins.str] = None,
        horizontal_offset: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_height: typing.Optional[builtins.str] = None,
        max_width: typing.Optional[builtins.str] = None,
        opacity: typing.Optional[builtins.str] = None,
        sizing_policy: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        vertical_align: typing.Optional[builtins.str] = None,
        vertical_offset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param horizontal_align: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#horizontal_align ElastictranscoderPreset#horizontal_align}.
        :param horizontal_offset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#horizontal_offset ElastictranscoderPreset#horizontal_offset}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#id ElastictranscoderPreset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_height: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_height ElastictranscoderPreset#max_height}.
        :param max_width: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_width ElastictranscoderPreset#max_width}.
        :param opacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#opacity ElastictranscoderPreset#opacity}.
        :param sizing_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sizing_policy ElastictranscoderPreset#sizing_policy}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#target ElastictranscoderPreset#target}.
        :param vertical_align: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#vertical_align ElastictranscoderPreset#vertical_align}.
        :param vertical_offset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#vertical_offset ElastictranscoderPreset#vertical_offset}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43622e3a97669ed6a04eef06854299b37c50e54918e169876c0be5b1a5b9a5ea)
            check_type(argname="argument horizontal_align", value=horizontal_align, expected_type=type_hints["horizontal_align"])
            check_type(argname="argument horizontal_offset", value=horizontal_offset, expected_type=type_hints["horizontal_offset"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_height", value=max_height, expected_type=type_hints["max_height"])
            check_type(argname="argument max_width", value=max_width, expected_type=type_hints["max_width"])
            check_type(argname="argument opacity", value=opacity, expected_type=type_hints["opacity"])
            check_type(argname="argument sizing_policy", value=sizing_policy, expected_type=type_hints["sizing_policy"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument vertical_align", value=vertical_align, expected_type=type_hints["vertical_align"])
            check_type(argname="argument vertical_offset", value=vertical_offset, expected_type=type_hints["vertical_offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if horizontal_align is not None:
            self._values["horizontal_align"] = horizontal_align
        if horizontal_offset is not None:
            self._values["horizontal_offset"] = horizontal_offset
        if id is not None:
            self._values["id"] = id
        if max_height is not None:
            self._values["max_height"] = max_height
        if max_width is not None:
            self._values["max_width"] = max_width
        if opacity is not None:
            self._values["opacity"] = opacity
        if sizing_policy is not None:
            self._values["sizing_policy"] = sizing_policy
        if target is not None:
            self._values["target"] = target
        if vertical_align is not None:
            self._values["vertical_align"] = vertical_align
        if vertical_offset is not None:
            self._values["vertical_offset"] = vertical_offset

    @builtins.property
    def horizontal_align(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#horizontal_align ElastictranscoderPreset#horizontal_align}.'''
        result = self._values.get("horizontal_align")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def horizontal_offset(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#horizontal_offset ElastictranscoderPreset#horizontal_offset}.'''
        result = self._values.get("horizontal_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#id ElastictranscoderPreset#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_height(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_height ElastictranscoderPreset#max_height}.'''
        result = self._values.get("max_height")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_width(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#max_width ElastictranscoderPreset#max_width}.'''
        result = self._values.get("max_width")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def opacity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#opacity ElastictranscoderPreset#opacity}.'''
        result = self._values.get("opacity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sizing_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#sizing_policy ElastictranscoderPreset#sizing_policy}.'''
        result = self._values.get("sizing_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#target ElastictranscoderPreset#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vertical_align(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#vertical_align ElastictranscoderPreset#vertical_align}.'''
        result = self._values.get("vertical_align")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vertical_offset(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_preset#vertical_offset ElastictranscoderPreset#vertical_offset}.'''
        result = self._values.get("vertical_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPresetVideoWatermarks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastictranscoderPresetVideoWatermarksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetVideoWatermarksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__323b9566cf1f8206e22ad10080a905828cfa48580d057baf31595926302738d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ElastictranscoderPresetVideoWatermarksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b3bf0fd0b8712ef351676dfd091af793fab424543d5c19e733928be7529487)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElastictranscoderPresetVideoWatermarksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982e4bc8bbba6615686303156ac69c5884c6c3d376beec08475aeac87a6beae3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e12d933f0752d7d94be0cddc69c91ab387a30219901a8ae9bc2acb08543a5572)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f5a092dc54adf3ad21bf5f6016ee8adb98c7eff1502ff77081922a2b5ea3a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPresetVideoWatermarks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPresetVideoWatermarks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPresetVideoWatermarks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e457f4d038cfeb1df40aaf494044d76b9701fe5863dab118b56fff33adbb4c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ElastictranscoderPresetVideoWatermarksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPreset.ElastictranscoderPresetVideoWatermarksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f53bb80e11011990b9577db84c1f833570d2077dfed9c5567f422919c76488d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHorizontalAlign")
    def reset_horizontal_align(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHorizontalAlign", []))

    @jsii.member(jsii_name="resetHorizontalOffset")
    def reset_horizontal_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHorizontalOffset", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxHeight")
    def reset_max_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxHeight", []))

    @jsii.member(jsii_name="resetMaxWidth")
    def reset_max_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxWidth", []))

    @jsii.member(jsii_name="resetOpacity")
    def reset_opacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpacity", []))

    @jsii.member(jsii_name="resetSizingPolicy")
    def reset_sizing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizingPolicy", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetVerticalAlign")
    def reset_vertical_align(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerticalAlign", []))

    @jsii.member(jsii_name="resetVerticalOffset")
    def reset_vertical_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerticalOffset", []))

    @builtins.property
    @jsii.member(jsii_name="horizontalAlignInput")
    def horizontal_align_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "horizontalAlignInput"))

    @builtins.property
    @jsii.member(jsii_name="horizontalOffsetInput")
    def horizontal_offset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "horizontalOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxHeightInput")
    def max_height_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxHeightInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWidthInput")
    def max_width_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxWidthInput"))

    @builtins.property
    @jsii.member(jsii_name="opacityInput")
    def opacity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "opacityInput"))

    @builtins.property
    @jsii.member(jsii_name="sizingPolicyInput")
    def sizing_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="verticalAlignInput")
    def vertical_align_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "verticalAlignInput"))

    @builtins.property
    @jsii.member(jsii_name="verticalOffsetInput")
    def vertical_offset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "verticalOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="horizontalAlign")
    def horizontal_align(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "horizontalAlign"))

    @horizontal_align.setter
    def horizontal_align(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9030077efa9de4fe3a48cac3a6a896bbbb12f94bba3ae9fe7418c772b76048a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "horizontalAlign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="horizontalOffset")
    def horizontal_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "horizontalOffset"))

    @horizontal_offset.setter
    def horizontal_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70847c315e193650476b16aa5ddb66718f614f93ecae6b7b261108c8424652d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "horizontalOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ae14f5427b0bc50b54f4b0eb2aa4ce76a656005da3024b79b0606b7ee1947d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxHeight")
    def max_height(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxHeight"))

    @max_height.setter
    def max_height(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df2f6e7c2df265d71dba9c5f1f5ae7a5e13f0d245b7dba6790aa6ef280ebc38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxHeight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWidth")
    def max_width(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxWidth"))

    @max_width.setter
    def max_width(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126962048073427869873a4f7f0dbb1757e6e70986f77d2ae095f6879a56b254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="opacity")
    def opacity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "opacity"))

    @opacity.setter
    def opacity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75a9c6b4404a3fafd84794ba542cb12cb9f19a9fc403722a4e7fcc3323d56d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "opacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizingPolicy")
    def sizing_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizingPolicy"))

    @sizing_policy.setter
    def sizing_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00bab675929dc6d96ece45418eba113a8f8f00c1792fefb69b3949798062c72a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizingPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71965d4c1cbd7bba3f207ffd0d226e91d5f7da962711c721f41954609956b16f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verticalAlign")
    def vertical_align(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verticalAlign"))

    @vertical_align.setter
    def vertical_align(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7583e1ec0bbe1328c10503dc26960c022bf3507152fb1af19becdcc6eec19d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verticalAlign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verticalOffset")
    def vertical_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verticalOffset"))

    @vertical_offset.setter
    def vertical_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a90e184d5fe0e0423836352446bc5cd2f11a65614124c69c8b1a365e536c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verticalOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPresetVideoWatermarks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPresetVideoWatermarks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPresetVideoWatermarks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8ee155c554e15e6cccdda7ee124c4b7ed20bc88d723db4ffc44ba010495a1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ElastictranscoderPreset",
    "ElastictranscoderPresetAudio",
    "ElastictranscoderPresetAudioCodecOptions",
    "ElastictranscoderPresetAudioCodecOptionsOutputReference",
    "ElastictranscoderPresetAudioOutputReference",
    "ElastictranscoderPresetConfig",
    "ElastictranscoderPresetThumbnails",
    "ElastictranscoderPresetThumbnailsOutputReference",
    "ElastictranscoderPresetVideo",
    "ElastictranscoderPresetVideoOutputReference",
    "ElastictranscoderPresetVideoWatermarks",
    "ElastictranscoderPresetVideoWatermarksList",
    "ElastictranscoderPresetVideoWatermarksOutputReference",
]

publication.publish()

def _typecheckingstub__0d50a118f3b1d9ddba04be25eeeb8552bd4ee623fc8c9fff8703f56c41f5981d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    container: builtins.str,
    audio: typing.Optional[typing.Union[ElastictranscoderPresetAudio, typing.Dict[builtins.str, typing.Any]]] = None,
    audio_codec_options: typing.Optional[typing.Union[ElastictranscoderPresetAudioCodecOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    thumbnails: typing.Optional[typing.Union[ElastictranscoderPresetThumbnails, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    video: typing.Optional[typing.Union[ElastictranscoderPresetVideo, typing.Dict[builtins.str, typing.Any]]] = None,
    video_codec_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    video_watermarks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastictranscoderPresetVideoWatermarks, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__29f1c0eee7e0e1c1c8270df0abb850f4ce0becb11f036e7d2905930d020620db(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23a8fa356a9ead71e171bd1bbce60b883698c239c396124b95582ab5cb17084(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastictranscoderPresetVideoWatermarks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42889b966c0a571fbeefaf50f046e29e81b51bf35b46bf4f6b28e7e269820369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6406d802fdd1344875f4f7cc77672fea7469a243381027ad41bab45271a22b13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13920b8064443704857c8e0b11a58d9d411daedbe754bda7ce7a5b5a583cdf4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38ce4638031beffd1f98d2ec24ebd887348049ccd43fc5170bc5e32e1b16e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1952f546c01156c3c15855ce391048caafda0477f90525800f186917b80ea7b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445e7310128b1d747b95cacc758c75f85a72bb372baa0eef44a22b040df3df71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf0bba8542bd29b78a2ce4d1071ef69ed985cf4c589a7b3cdb2824460d75621(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa54a95d777a8efa116c5004553a12a3fb790cb5f400606821f5cb52b6a3f66e(
    *,
    audio_packing_mode: typing.Optional[builtins.str] = None,
    bit_rate: typing.Optional[builtins.str] = None,
    channels: typing.Optional[builtins.str] = None,
    codec: typing.Optional[builtins.str] = None,
    sample_rate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424593bb86ea17a56111457e6785079b8be35426cc607f00ddc3651231fbe7d8(
    *,
    bit_depth: typing.Optional[builtins.str] = None,
    bit_order: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    signed: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50e25ff6a09ef3a08d8f2d7da8b984dbebe9496a73c412861b2cd5218701b24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c074b3513f4d926929146565eedbb8076d9c6f8c64b70c160f0b94999863b93c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5086d54e590da34f040ed32071c9414095acc49f64c7cfcdebef2923afb86c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3cf09e80395d9bff13b7257c3b01f403f4c6a009491d7637db4e704d253baf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27adac483b357caf6977c921d371d28c2a97bfdb7fb5460542dc1d412f52d3cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60ae960250b44938ee79e7548451a2b9c397249362201c45fd236d56d151376(
    value: typing.Optional[ElastictranscoderPresetAudioCodecOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8c35670fa2d1ba6d587d97ae63c153605503a73791424e4a2345fb6be38181(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b665e62b7d7f51b37c7cc09cc7f12f217cf941ad0a643fa305424d25d07bf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee8cacaf49b630221ff7a184aca810080905162f694682b4d8622531735905f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54479fd4ead551477b484f1f027e6e9fd4f534d05f5e263cc4168cea1f80f533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28df4833114a65cee854539b59d2b780f7c01a287d237c13adb4695ccdc92ca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65c3c175d430586e381a66d97be29a921b44eeec76a62080d9701f9ee842577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c901ef9dbf4924e7552105b65d631971507ad601b271c2e4d7ad48170decc578(
    value: typing.Optional[ElastictranscoderPresetAudio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2165084cf446e180755a5a9359de1df7623c26dd4a8b59a4bd2a1cd77438d8a7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container: builtins.str,
    audio: typing.Optional[typing.Union[ElastictranscoderPresetAudio, typing.Dict[builtins.str, typing.Any]]] = None,
    audio_codec_options: typing.Optional[typing.Union[ElastictranscoderPresetAudioCodecOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    thumbnails: typing.Optional[typing.Union[ElastictranscoderPresetThumbnails, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    video: typing.Optional[typing.Union[ElastictranscoderPresetVideo, typing.Dict[builtins.str, typing.Any]]] = None,
    video_codec_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    video_watermarks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastictranscoderPresetVideoWatermarks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b7c140d96559acb09639831d7302ace24089b4446f96b689e3dfd27c63618d(
    *,
    aspect_ratio: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    interval: typing.Optional[builtins.str] = None,
    max_height: typing.Optional[builtins.str] = None,
    max_width: typing.Optional[builtins.str] = None,
    padding_policy: typing.Optional[builtins.str] = None,
    resolution: typing.Optional[builtins.str] = None,
    sizing_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723778c9715854eb2fd7ba28f1b5fc8c40c23f5c80f63da7e5b1074a5ed6083e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4673f0cdbd7c3fc7fa533aead64a103c9442fc763324f215b6bf32afd2df0957(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047559658ec7d7d1132fc8013ffb9d44d09a07510b850b7c58e0501944309669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4299a0c51e6c7494d7356ad1bcd23fe7555ce8c8de61d7e1f1b1839c2eab139c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901b3fdbe282c3372935bf06ae0392edf162c11f83ff22c4e04e90d249fd24b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac621cbeca8efb53dae0e797bdfaf1bd42ad24f44a12972f4f0465b93e1f8453(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4311a66040d81e530b7944cf5e961574e98885900202fe4a32989c60886bce61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52db27f9ade1555f3b4b5a5e89d9f5feb75a3e9ace08a24dbb64916a13d4f9cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b61a38610e0d6bdba569f6814a79080223bd9382a022507a68ab5e4f572425c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7049a06eb46ad18e2e8d475bc2bbb8b2b07e9cae02f450a06c53a04b7d2d193(
    value: typing.Optional[ElastictranscoderPresetThumbnails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045da46a0caa4dfc1f124fe8b53e3a7d69003d57f347a3c9ee855a87999a4d7d(
    *,
    aspect_ratio: typing.Optional[builtins.str] = None,
    bit_rate: typing.Optional[builtins.str] = None,
    codec: typing.Optional[builtins.str] = None,
    display_aspect_ratio: typing.Optional[builtins.str] = None,
    fixed_gop: typing.Optional[builtins.str] = None,
    frame_rate: typing.Optional[builtins.str] = None,
    keyframes_max_dist: typing.Optional[builtins.str] = None,
    max_frame_rate: typing.Optional[builtins.str] = None,
    max_height: typing.Optional[builtins.str] = None,
    max_width: typing.Optional[builtins.str] = None,
    padding_policy: typing.Optional[builtins.str] = None,
    resolution: typing.Optional[builtins.str] = None,
    sizing_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1ebea6148e3ea1c9af8838e720b16550e4925b89e3cd20fe751492b2b11eee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f6efb9b6b7e373e92bd5c48da21231a4d541b62d5a2ca4ec039fe5ee869b4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701c49824e128c09d33e9cd9464952fcdd6362f42fbe30cb1ca914af733fe47c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e4f2e79325c5ab73b1547ce4f3df9e37ae2716db22c088d5a88a2cdd910fb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6d65a3b4bd824ebef9587557d51df28c23831341ac0ac0be1dd7a63e8dff48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7945be48ec79a0993af726f95e2f9bc0e74b4148d620ffdb9fa7d8b95454f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530d9c85e75fb4f24b6734fdb172d6180630ef92d5628f825b06dd17eb0eb053(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f356af7ef6bea267cd6615ceb1ab3ec7f8d3090d0e1053b413d6b7df4c561e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd3a026fe1f5488c133d3d2b6ad5f1a60ad8a2a6569300bb9fab9687795e720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a624a419acabe10952976f2d14484766dc298f5f5ac6258e15ef72232c999dfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e02fff53aff2058468cfee83e0735482c98b94c42fa9dd913067fb89d8eb9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e90725f3b6a5602778c526e98d19ec311eb6bb33bae72118fec2e849f582e32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e60d2f6072bd0221d8eab7ff105364b2adf7d5c8eabbfdfc88608848983d2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83454d6eeb695a3fab1cae8552bd7fd5c055a23c7ebb9730f2e1f3d9a8642070(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5431ede549e438d20081fba95492922788e43fd3550f1f0d55a12c837108fcb1(
    value: typing.Optional[ElastictranscoderPresetVideo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43622e3a97669ed6a04eef06854299b37c50e54918e169876c0be5b1a5b9a5ea(
    *,
    horizontal_align: typing.Optional[builtins.str] = None,
    horizontal_offset: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_height: typing.Optional[builtins.str] = None,
    max_width: typing.Optional[builtins.str] = None,
    opacity: typing.Optional[builtins.str] = None,
    sizing_policy: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    vertical_align: typing.Optional[builtins.str] = None,
    vertical_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323b9566cf1f8206e22ad10080a905828cfa48580d057baf31595926302738d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b3bf0fd0b8712ef351676dfd091af793fab424543d5c19e733928be7529487(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982e4bc8bbba6615686303156ac69c5884c6c3d376beec08475aeac87a6beae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12d933f0752d7d94be0cddc69c91ab387a30219901a8ae9bc2acb08543a5572(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5a092dc54adf3ad21bf5f6016ee8adb98c7eff1502ff77081922a2b5ea3a9f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e457f4d038cfeb1df40aaf494044d76b9701fe5863dab118b56fff33adbb4c6c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPresetVideoWatermarks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f53bb80e11011990b9577db84c1f833570d2077dfed9c5567f422919c76488d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9030077efa9de4fe3a48cac3a6a896bbbb12f94bba3ae9fe7418c772b76048a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70847c315e193650476b16aa5ddb66718f614f93ecae6b7b261108c8424652d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ae14f5427b0bc50b54f4b0eb2aa4ce76a656005da3024b79b0606b7ee1947d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df2f6e7c2df265d71dba9c5f1f5ae7a5e13f0d245b7dba6790aa6ef280ebc38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126962048073427869873a4f7f0dbb1757e6e70986f77d2ae095f6879a56b254(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75a9c6b4404a3fafd84794ba542cb12cb9f19a9fc403722a4e7fcc3323d56d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00bab675929dc6d96ece45418eba113a8f8f00c1792fefb69b3949798062c72a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71965d4c1cbd7bba3f207ffd0d226e91d5f7da962711c721f41954609956b16f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7583e1ec0bbe1328c10503dc26960c022bf3507152fb1af19becdcc6eec19d57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a90e184d5fe0e0423836352446bc5cd2f11a65614124c69c8b1a365e536c9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8ee155c554e15e6cccdda7ee124c4b7ed20bc88d723db4ffc44ba010495a1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPresetVideoWatermarks]],
) -> None:
    """Type checking stubs"""
    pass
