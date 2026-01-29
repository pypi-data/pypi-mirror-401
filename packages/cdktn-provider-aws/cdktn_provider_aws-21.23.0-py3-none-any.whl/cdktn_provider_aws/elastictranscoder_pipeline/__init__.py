r'''
# `aws_elastictranscoder_pipeline`

Refer to the Terraform Registry for docs: [`aws_elastictranscoder_pipeline`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline).
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


class ElastictranscoderPipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipeline",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline aws_elastictranscoder_pipeline}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        input_bucket: builtins.str,
        role: builtins.str,
        aws_kms_key_arn: typing.Optional[builtins.str] = None,
        content_config: typing.Optional[typing.Union["ElastictranscoderPipelineContentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        content_config_permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastictranscoderPipelineContentConfigPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Union["ElastictranscoderPipelineNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        output_bucket: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        thumbnail_config: typing.Optional[typing.Union["ElastictranscoderPipelineThumbnailConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        thumbnail_config_permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastictranscoderPipelineThumbnailConfigPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline aws_elastictranscoder_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param input_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#input_bucket ElastictranscoderPipeline#input_bucket}.
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#role ElastictranscoderPipeline#role}.
        :param aws_kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#aws_kms_key_arn ElastictranscoderPipeline#aws_kms_key_arn}.
        :param content_config: content_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#content_config ElastictranscoderPipeline#content_config}
        :param content_config_permissions: content_config_permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#content_config_permissions ElastictranscoderPipeline#content_config_permissions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#id ElastictranscoderPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#name ElastictranscoderPipeline#name}.
        :param notifications: notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#notifications ElastictranscoderPipeline#notifications}
        :param output_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#output_bucket ElastictranscoderPipeline#output_bucket}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#region ElastictranscoderPipeline#region}
        :param thumbnail_config: thumbnail_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#thumbnail_config ElastictranscoderPipeline#thumbnail_config}
        :param thumbnail_config_permissions: thumbnail_config_permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#thumbnail_config_permissions ElastictranscoderPipeline#thumbnail_config_permissions}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a181c4148fd8517c73cd9265073d8d2301c8946302a2b527efc94cdf023e18)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ElastictranscoderPipelineConfig(
            input_bucket=input_bucket,
            role=role,
            aws_kms_key_arn=aws_kms_key_arn,
            content_config=content_config,
            content_config_permissions=content_config_permissions,
            id=id,
            name=name,
            notifications=notifications,
            output_bucket=output_bucket,
            region=region,
            thumbnail_config=thumbnail_config,
            thumbnail_config_permissions=thumbnail_config_permissions,
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
        '''Generates CDKTF code for importing a ElastictranscoderPipeline resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ElastictranscoderPipeline to import.
        :param import_from_id: The id of the existing ElastictranscoderPipeline that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ElastictranscoderPipeline to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a2735d7128bc8375fffbc6492dcf6cc35ab59dfcd362d1f9181c7968e9d362)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContentConfig")
    def put_content_config(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#bucket ElastictranscoderPipeline#bucket}.
        :param storage_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#storage_class ElastictranscoderPipeline#storage_class}.
        '''
        value = ElastictranscoderPipelineContentConfig(
            bucket=bucket, storage_class=storage_class
        )

        return typing.cast(None, jsii.invoke(self, "putContentConfig", [value]))

    @jsii.member(jsii_name="putContentConfigPermissions")
    def put_content_config_permissions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastictranscoderPipelineContentConfigPermissions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4080404a3aa00f635f05b1d5713e03e11629a9ce1c845b0f3fd47d7cb4b7a5da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContentConfigPermissions", [value]))

    @jsii.member(jsii_name="putNotifications")
    def put_notifications(
        self,
        *,
        completed: typing.Optional[builtins.str] = None,
        error: typing.Optional[builtins.str] = None,
        progressing: typing.Optional[builtins.str] = None,
        warning: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param completed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#completed ElastictranscoderPipeline#completed}.
        :param error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#error ElastictranscoderPipeline#error}.
        :param progressing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#progressing ElastictranscoderPipeline#progressing}.
        :param warning: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#warning ElastictranscoderPipeline#warning}.
        '''
        value = ElastictranscoderPipelineNotifications(
            completed=completed, error=error, progressing=progressing, warning=warning
        )

        return typing.cast(None, jsii.invoke(self, "putNotifications", [value]))

    @jsii.member(jsii_name="putThumbnailConfig")
    def put_thumbnail_config(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#bucket ElastictranscoderPipeline#bucket}.
        :param storage_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#storage_class ElastictranscoderPipeline#storage_class}.
        '''
        value = ElastictranscoderPipelineThumbnailConfig(
            bucket=bucket, storage_class=storage_class
        )

        return typing.cast(None, jsii.invoke(self, "putThumbnailConfig", [value]))

    @jsii.member(jsii_name="putThumbnailConfigPermissions")
    def put_thumbnail_config_permissions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastictranscoderPipelineThumbnailConfigPermissions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1357abe6d525bc31fdf7cc69cfab3c0a715b64861856fad4727a2ace4f0f40bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putThumbnailConfigPermissions", [value]))

    @jsii.member(jsii_name="resetAwsKmsKeyArn")
    def reset_aws_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsKmsKeyArn", []))

    @jsii.member(jsii_name="resetContentConfig")
    def reset_content_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentConfig", []))

    @jsii.member(jsii_name="resetContentConfigPermissions")
    def reset_content_config_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentConfigPermissions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNotifications")
    def reset_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifications", []))

    @jsii.member(jsii_name="resetOutputBucket")
    def reset_output_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputBucket", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetThumbnailConfig")
    def reset_thumbnail_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThumbnailConfig", []))

    @jsii.member(jsii_name="resetThumbnailConfigPermissions")
    def reset_thumbnail_config_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThumbnailConfigPermissions", []))

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
    @jsii.member(jsii_name="contentConfig")
    def content_config(self) -> "ElastictranscoderPipelineContentConfigOutputReference":
        return typing.cast("ElastictranscoderPipelineContentConfigOutputReference", jsii.get(self, "contentConfig"))

    @builtins.property
    @jsii.member(jsii_name="contentConfigPermissions")
    def content_config_permissions(
        self,
    ) -> "ElastictranscoderPipelineContentConfigPermissionsList":
        return typing.cast("ElastictranscoderPipelineContentConfigPermissionsList", jsii.get(self, "contentConfigPermissions"))

    @builtins.property
    @jsii.member(jsii_name="notifications")
    def notifications(self) -> "ElastictranscoderPipelineNotificationsOutputReference":
        return typing.cast("ElastictranscoderPipelineNotificationsOutputReference", jsii.get(self, "notifications"))

    @builtins.property
    @jsii.member(jsii_name="thumbnailConfig")
    def thumbnail_config(
        self,
    ) -> "ElastictranscoderPipelineThumbnailConfigOutputReference":
        return typing.cast("ElastictranscoderPipelineThumbnailConfigOutputReference", jsii.get(self, "thumbnailConfig"))

    @builtins.property
    @jsii.member(jsii_name="thumbnailConfigPermissions")
    def thumbnail_config_permissions(
        self,
    ) -> "ElastictranscoderPipelineThumbnailConfigPermissionsList":
        return typing.cast("ElastictranscoderPipelineThumbnailConfigPermissionsList", jsii.get(self, "thumbnailConfigPermissions"))

    @builtins.property
    @jsii.member(jsii_name="awsKmsKeyArnInput")
    def aws_kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsKmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="contentConfigInput")
    def content_config_input(
        self,
    ) -> typing.Optional["ElastictranscoderPipelineContentConfig"]:
        return typing.cast(typing.Optional["ElastictranscoderPipelineContentConfig"], jsii.get(self, "contentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="contentConfigPermissionsInput")
    def content_config_permissions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPipelineContentConfigPermissions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPipelineContentConfigPermissions"]]], jsii.get(self, "contentConfigPermissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inputBucketInput")
    def input_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationsInput")
    def notifications_input(
        self,
    ) -> typing.Optional["ElastictranscoderPipelineNotifications"]:
        return typing.cast(typing.Optional["ElastictranscoderPipelineNotifications"], jsii.get(self, "notificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="outputBucketInput")
    def output_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbnailConfigInput")
    def thumbnail_config_input(
        self,
    ) -> typing.Optional["ElastictranscoderPipelineThumbnailConfig"]:
        return typing.cast(typing.Optional["ElastictranscoderPipelineThumbnailConfig"], jsii.get(self, "thumbnailConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbnailConfigPermissionsInput")
    def thumbnail_config_permissions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPipelineThumbnailConfigPermissions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPipelineThumbnailConfigPermissions"]]], jsii.get(self, "thumbnailConfigPermissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="awsKmsKeyArn")
    def aws_kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsKmsKeyArn"))

    @aws_kms_key_arn.setter
    def aws_kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7231f17c43929d730d630355512356e5db55b48bb026abaededbc3027c23da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsKmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f2197df6c2db619b740ddd1b373e96eb4157ecd47cd3fea4d28185902eca77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputBucket")
    def input_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputBucket"))

    @input_bucket.setter
    def input_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95328af56ad3d7fff73ffb41da836761aff2a6baa14315a6826a6d302ae11dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb77a6c06f6c2abe8c4a77d5961a054aa3d7bc70ecb4d52e1892f856ac1111c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputBucket")
    def output_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputBucket"))

    @output_bucket.setter
    def output_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58fa8827335d6e1c92801b899faa498494bb9f917d65ca85ca352fb4c7287cde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c4bbd165d8bab6bcf76b002b7923d6770236262dc4013e08ee8e3cc086663b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19ea475c797736dee07f158fc68fd183e5b42dec79ff986ffcb3e97a0de1c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "input_bucket": "inputBucket",
        "role": "role",
        "aws_kms_key_arn": "awsKmsKeyArn",
        "content_config": "contentConfig",
        "content_config_permissions": "contentConfigPermissions",
        "id": "id",
        "name": "name",
        "notifications": "notifications",
        "output_bucket": "outputBucket",
        "region": "region",
        "thumbnail_config": "thumbnailConfig",
        "thumbnail_config_permissions": "thumbnailConfigPermissions",
    },
)
class ElastictranscoderPipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        input_bucket: builtins.str,
        role: builtins.str,
        aws_kms_key_arn: typing.Optional[builtins.str] = None,
        content_config: typing.Optional[typing.Union["ElastictranscoderPipelineContentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        content_config_permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastictranscoderPipelineContentConfigPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Union["ElastictranscoderPipelineNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        output_bucket: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        thumbnail_config: typing.Optional[typing.Union["ElastictranscoderPipelineThumbnailConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        thumbnail_config_permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElastictranscoderPipelineThumbnailConfigPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param input_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#input_bucket ElastictranscoderPipeline#input_bucket}.
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#role ElastictranscoderPipeline#role}.
        :param aws_kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#aws_kms_key_arn ElastictranscoderPipeline#aws_kms_key_arn}.
        :param content_config: content_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#content_config ElastictranscoderPipeline#content_config}
        :param content_config_permissions: content_config_permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#content_config_permissions ElastictranscoderPipeline#content_config_permissions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#id ElastictranscoderPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#name ElastictranscoderPipeline#name}.
        :param notifications: notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#notifications ElastictranscoderPipeline#notifications}
        :param output_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#output_bucket ElastictranscoderPipeline#output_bucket}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#region ElastictranscoderPipeline#region}
        :param thumbnail_config: thumbnail_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#thumbnail_config ElastictranscoderPipeline#thumbnail_config}
        :param thumbnail_config_permissions: thumbnail_config_permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#thumbnail_config_permissions ElastictranscoderPipeline#thumbnail_config_permissions}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(content_config, dict):
            content_config = ElastictranscoderPipelineContentConfig(**content_config)
        if isinstance(notifications, dict):
            notifications = ElastictranscoderPipelineNotifications(**notifications)
        if isinstance(thumbnail_config, dict):
            thumbnail_config = ElastictranscoderPipelineThumbnailConfig(**thumbnail_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3097fcb10cfd22dba0f3109ca51a2ca70520617fb2e8af72a1994420bc6db1a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument input_bucket", value=input_bucket, expected_type=type_hints["input_bucket"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument aws_kms_key_arn", value=aws_kms_key_arn, expected_type=type_hints["aws_kms_key_arn"])
            check_type(argname="argument content_config", value=content_config, expected_type=type_hints["content_config"])
            check_type(argname="argument content_config_permissions", value=content_config_permissions, expected_type=type_hints["content_config_permissions"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
            check_type(argname="argument output_bucket", value=output_bucket, expected_type=type_hints["output_bucket"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument thumbnail_config", value=thumbnail_config, expected_type=type_hints["thumbnail_config"])
            check_type(argname="argument thumbnail_config_permissions", value=thumbnail_config_permissions, expected_type=type_hints["thumbnail_config_permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_bucket": input_bucket,
            "role": role,
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
        if aws_kms_key_arn is not None:
            self._values["aws_kms_key_arn"] = aws_kms_key_arn
        if content_config is not None:
            self._values["content_config"] = content_config
        if content_config_permissions is not None:
            self._values["content_config_permissions"] = content_config_permissions
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if notifications is not None:
            self._values["notifications"] = notifications
        if output_bucket is not None:
            self._values["output_bucket"] = output_bucket
        if region is not None:
            self._values["region"] = region
        if thumbnail_config is not None:
            self._values["thumbnail_config"] = thumbnail_config
        if thumbnail_config_permissions is not None:
            self._values["thumbnail_config_permissions"] = thumbnail_config_permissions

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
    def input_bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#input_bucket ElastictranscoderPipeline#input_bucket}.'''
        result = self._values.get("input_bucket")
        assert result is not None, "Required property 'input_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#role ElastictranscoderPipeline#role}.'''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#aws_kms_key_arn ElastictranscoderPipeline#aws_kms_key_arn}.'''
        result = self._values.get("aws_kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_config(
        self,
    ) -> typing.Optional["ElastictranscoderPipelineContentConfig"]:
        '''content_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#content_config ElastictranscoderPipeline#content_config}
        '''
        result = self._values.get("content_config")
        return typing.cast(typing.Optional["ElastictranscoderPipelineContentConfig"], result)

    @builtins.property
    def content_config_permissions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPipelineContentConfigPermissions"]]]:
        '''content_config_permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#content_config_permissions ElastictranscoderPipeline#content_config_permissions}
        '''
        result = self._values.get("content_config_permissions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPipelineContentConfigPermissions"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#id ElastictranscoderPipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#name ElastictranscoderPipeline#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notifications(
        self,
    ) -> typing.Optional["ElastictranscoderPipelineNotifications"]:
        '''notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#notifications ElastictranscoderPipeline#notifications}
        '''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional["ElastictranscoderPipelineNotifications"], result)

    @builtins.property
    def output_bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#output_bucket ElastictranscoderPipeline#output_bucket}.'''
        result = self._values.get("output_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#region ElastictranscoderPipeline#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thumbnail_config(
        self,
    ) -> typing.Optional["ElastictranscoderPipelineThumbnailConfig"]:
        '''thumbnail_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#thumbnail_config ElastictranscoderPipeline#thumbnail_config}
        '''
        result = self._values.get("thumbnail_config")
        return typing.cast(typing.Optional["ElastictranscoderPipelineThumbnailConfig"], result)

    @builtins.property
    def thumbnail_config_permissions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPipelineThumbnailConfigPermissions"]]]:
        '''thumbnail_config_permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#thumbnail_config_permissions ElastictranscoderPipeline#thumbnail_config_permissions}
        '''
        result = self._values.get("thumbnail_config_permissions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElastictranscoderPipelineThumbnailConfigPermissions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineContentConfig",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "storage_class": "storageClass"},
)
class ElastictranscoderPipelineContentConfig:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#bucket ElastictranscoderPipeline#bucket}.
        :param storage_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#storage_class ElastictranscoderPipeline#storage_class}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d460ba91e76a6fc967194816dbb8c8b80d1acb0e9215e8d1c482c4e7f01994)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if storage_class is not None:
            self._values["storage_class"] = storage_class

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#bucket ElastictranscoderPipeline#bucket}.'''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#storage_class ElastictranscoderPipeline#storage_class}.'''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPipelineContentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastictranscoderPipelineContentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineContentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__914e266baa25893b954386be6dfa30ae166a939e5282134f1c50946ebf7278b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetStorageClass")
    def reset_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageClass", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dae4d0a6c8d8b5ab6757bbae16fcb547a1f7d78f2a3f1a41e8ce3a7dd183818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2c91084ac090a4cd38154330b17d5f3e90c1e2dbf1e2f0fa72d05f7de2726d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElastictranscoderPipelineContentConfig]:
        return typing.cast(typing.Optional[ElastictranscoderPipelineContentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElastictranscoderPipelineContentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6012410e5c2d1aa6df2230eeef0a24465f69da3240a6e427f40ea9cca2878617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineContentConfigPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "access": "access",
        "grantee": "grantee",
        "grantee_type": "granteeType",
    },
)
class ElastictranscoderPipelineContentConfigPermissions:
    def __init__(
        self,
        *,
        access: typing.Optional[typing.Sequence[builtins.str]] = None,
        grantee: typing.Optional[builtins.str] = None,
        grantee_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#access ElastictranscoderPipeline#access}.
        :param grantee: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#grantee ElastictranscoderPipeline#grantee}.
        :param grantee_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#grantee_type ElastictranscoderPipeline#grantee_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00959dbf9a61ec38c6bd379311494a7fd33d9dca3591a4632c14b01092631db)
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument grantee_type", value=grantee_type, expected_type=type_hints["grantee_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access is not None:
            self._values["access"] = access
        if grantee is not None:
            self._values["grantee"] = grantee
        if grantee_type is not None:
            self._values["grantee_type"] = grantee_type

    @builtins.property
    def access(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#access ElastictranscoderPipeline#access}.'''
        result = self._values.get("access")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def grantee(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#grantee ElastictranscoderPipeline#grantee}.'''
        result = self._values.get("grantee")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grantee_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#grantee_type ElastictranscoderPipeline#grantee_type}.'''
        result = self._values.get("grantee_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPipelineContentConfigPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastictranscoderPipelineContentConfigPermissionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineContentConfigPermissionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7791026e2ed0424f361304f19def936e08446c0886aec424714a6982169534bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ElastictranscoderPipelineContentConfigPermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c1102b1e3f9a21479d18aa05e62c32d8126c078dc3214d40856415dad300c6b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElastictranscoderPipelineContentConfigPermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38673ae302ea271f13573015ddf3d31f8e351d70af91180916172b5ada02959)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffcef9daa2c97aefe6e8c61a29d87bd25add8837a26e446dbd3915c6406b20e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f4696a0c096e4e3321f8aba6d05276901f52d80267e9b77cf2bac016763f53d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPipelineContentConfigPermissions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPipelineContentConfigPermissions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPipelineContentConfigPermissions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67c86dbcb3452060066508e825b58618856a0a6ed72209d070eafdbab8cc269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ElastictranscoderPipelineContentConfigPermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineContentConfigPermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8b66867e8d6736c5a7a9a18050ec9010a151c3748d8c8207930d4d5addcf420)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccess")
    def reset_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccess", []))

    @jsii.member(jsii_name="resetGrantee")
    def reset_grantee(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrantee", []))

    @jsii.member(jsii_name="resetGranteeType")
    def reset_grantee_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGranteeType", []))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="granteeInput")
    def grantee_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "granteeInput"))

    @builtins.property
    @jsii.member(jsii_name="granteeTypeInput")
    def grantee_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "granteeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="access")
    def access(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "access"))

    @access.setter
    def access(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802df927ae0de7d79b29c7a6ad49de47d25dfbf805da84083befcce772c66e1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "access", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grantee")
    def grantee(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grantee"))

    @grantee.setter
    def grantee(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e189f9d54887df66dab69a8cc92394a41df7a7282291e150c1e5c1ffd35e795d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grantee", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="granteeType")
    def grantee_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "granteeType"))

    @grantee_type.setter
    def grantee_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5b680c939c3fa7fb387a91614d3317244ac8e0dbf34616e329271bba961c2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "granteeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPipelineContentConfigPermissions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPipelineContentConfigPermissions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPipelineContentConfigPermissions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5337160628e666718d573b36f610ac13e68693d7d22d12059a2f84bd3cf978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "completed": "completed",
        "error": "error",
        "progressing": "progressing",
        "warning": "warning",
    },
)
class ElastictranscoderPipelineNotifications:
    def __init__(
        self,
        *,
        completed: typing.Optional[builtins.str] = None,
        error: typing.Optional[builtins.str] = None,
        progressing: typing.Optional[builtins.str] = None,
        warning: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param completed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#completed ElastictranscoderPipeline#completed}.
        :param error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#error ElastictranscoderPipeline#error}.
        :param progressing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#progressing ElastictranscoderPipeline#progressing}.
        :param warning: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#warning ElastictranscoderPipeline#warning}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56617c3d325a3d3a2e4599a61477aa619c4f83777a15fe6c74f692c50a3f338)
            check_type(argname="argument completed", value=completed, expected_type=type_hints["completed"])
            check_type(argname="argument error", value=error, expected_type=type_hints["error"])
            check_type(argname="argument progressing", value=progressing, expected_type=type_hints["progressing"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if completed is not None:
            self._values["completed"] = completed
        if error is not None:
            self._values["error"] = error
        if progressing is not None:
            self._values["progressing"] = progressing
        if warning is not None:
            self._values["warning"] = warning

    @builtins.property
    def completed(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#completed ElastictranscoderPipeline#completed}.'''
        result = self._values.get("completed")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#error ElastictranscoderPipeline#error}.'''
        result = self._values.get("error")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def progressing(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#progressing ElastictranscoderPipeline#progressing}.'''
        result = self._values.get("progressing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warning(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#warning ElastictranscoderPipeline#warning}.'''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPipelineNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastictranscoderPipelineNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bda0a5b8f4d7df62a8e6ae79664b1d120157d59200a7a0bd5633675e0db7779)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCompleted")
    def reset_completed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompleted", []))

    @jsii.member(jsii_name="resetError")
    def reset_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetError", []))

    @jsii.member(jsii_name="resetProgressing")
    def reset_progressing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProgressing", []))

    @jsii.member(jsii_name="resetWarning")
    def reset_warning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarning", []))

    @builtins.property
    @jsii.member(jsii_name="completedInput")
    def completed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "completedInput"))

    @builtins.property
    @jsii.member(jsii_name="errorInput")
    def error_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorInput"))

    @builtins.property
    @jsii.member(jsii_name="progressingInput")
    def progressing_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "progressingInput"))

    @builtins.property
    @jsii.member(jsii_name="warningInput")
    def warning_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warningInput"))

    @builtins.property
    @jsii.member(jsii_name="completed")
    def completed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "completed"))

    @completed.setter
    def completed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b459552714410e6dbbd5016b3a3c7ef40b81d3740cac8102a439fa6e7767b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "completed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "error"))

    @error.setter
    def error(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb5748efddf26fb37f8a8cc974f006816b42ce17023b9a567b3fc0b62f831dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "error", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="progressing")
    def progressing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "progressing"))

    @progressing.setter
    def progressing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefe84f18c3f65a63a5eebb8f59439468de359c2bac34b038e50aa1039a3ae5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "progressing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warning")
    def warning(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warning"))

    @warning.setter
    def warning(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0e7be267fd7a9590a6442605e0c283b7d027f0ba88535f49c07e5f99360619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElastictranscoderPipelineNotifications]:
        return typing.cast(typing.Optional[ElastictranscoderPipelineNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElastictranscoderPipelineNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36e8dc4689ee3bc6356378a14afae197cd7dc0dc73f430b9896ef658bae88e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineThumbnailConfig",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "storage_class": "storageClass"},
)
class ElastictranscoderPipelineThumbnailConfig:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#bucket ElastictranscoderPipeline#bucket}.
        :param storage_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#storage_class ElastictranscoderPipeline#storage_class}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ed3f3a34a32e7b64650e3f579761e9549c01d634be89215858fdc5b0a5a794)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if storage_class is not None:
            self._values["storage_class"] = storage_class

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#bucket ElastictranscoderPipeline#bucket}.'''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#storage_class ElastictranscoderPipeline#storage_class}.'''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPipelineThumbnailConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastictranscoderPipelineThumbnailConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineThumbnailConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad7abad9dde498cfa1cdfc32480a1e9606ceb7bcb9d7128a7ff9a1c70e1f7c0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetStorageClass")
    def reset_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageClass", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c41f21e9bcb8604f6de6a51932d89b1fa48961b02ec3f593f451f89179a220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679b21aad246a808ac175983591856aa30f51253185aa65aeaa79bd16b51a283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ElastictranscoderPipelineThumbnailConfig]:
        return typing.cast(typing.Optional[ElastictranscoderPipelineThumbnailConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElastictranscoderPipelineThumbnailConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3adc8fcbcf84f86d73233014a28f6fd302f052a33ec5832e3ded664315b64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineThumbnailConfigPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "access": "access",
        "grantee": "grantee",
        "grantee_type": "granteeType",
    },
)
class ElastictranscoderPipelineThumbnailConfigPermissions:
    def __init__(
        self,
        *,
        access: typing.Optional[typing.Sequence[builtins.str]] = None,
        grantee: typing.Optional[builtins.str] = None,
        grantee_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#access ElastictranscoderPipeline#access}.
        :param grantee: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#grantee ElastictranscoderPipeline#grantee}.
        :param grantee_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#grantee_type ElastictranscoderPipeline#grantee_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e068fc5c95107070701ce05f385034e1f6e57418dadd3384467d4ccf727a3c1f)
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument grantee_type", value=grantee_type, expected_type=type_hints["grantee_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access is not None:
            self._values["access"] = access
        if grantee is not None:
            self._values["grantee"] = grantee
        if grantee_type is not None:
            self._values["grantee_type"] = grantee_type

    @builtins.property
    def access(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#access ElastictranscoderPipeline#access}.'''
        result = self._values.get("access")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def grantee(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#grantee ElastictranscoderPipeline#grantee}.'''
        result = self._values.get("grantee")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grantee_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elastictranscoder_pipeline#grantee_type ElastictranscoderPipeline#grantee_type}.'''
        result = self._values.get("grantee_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastictranscoderPipelineThumbnailConfigPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElastictranscoderPipelineThumbnailConfigPermissionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineThumbnailConfigPermissionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fd83e45ad2dd06385ada68330f32e636cfd4c11878b727d9d1174fda7366243)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ElastictranscoderPipelineThumbnailConfigPermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3cf3049482e6d7595ef3c4dc869c36bd7c2379266edebf83434b7ceac38329)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElastictranscoderPipelineThumbnailConfigPermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aea8d9e8d2255af043fce5ebe5268c46ca94f14ecda9da5d5fb8d62b63c077a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df7f9a6d2cb35e553aeb0e4b58f0957d97b1b24fd908ddc93d78416cb2fa5829)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2ede725d209f9c59bca7ffbfcd30816328be148124b1fa84b97487ecdd29c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPipelineThumbnailConfigPermissions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPipelineThumbnailConfigPermissions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPipelineThumbnailConfigPermissions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f070fa8e3e74208adf744980cb36c79c08883c419ccab6938a6f14c59291846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ElastictranscoderPipelineThumbnailConfigPermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elastictranscoderPipeline.ElastictranscoderPipelineThumbnailConfigPermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__045b01abbe6d0216208cd9671acaa865cf56f20db0e77ece39e0fed65dcf951b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccess")
    def reset_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccess", []))

    @jsii.member(jsii_name="resetGrantee")
    def reset_grantee(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrantee", []))

    @jsii.member(jsii_name="resetGranteeType")
    def reset_grantee_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGranteeType", []))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="granteeInput")
    def grantee_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "granteeInput"))

    @builtins.property
    @jsii.member(jsii_name="granteeTypeInput")
    def grantee_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "granteeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="access")
    def access(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "access"))

    @access.setter
    def access(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4ed7457d55f7b728d6384f47d4eda959888668b29c61d0650db5bedefd011e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "access", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grantee")
    def grantee(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grantee"))

    @grantee.setter
    def grantee(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac561093363afa648bcc07a379b7a2bdb5a8b1e830c431bb72cc633284ed0bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grantee", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="granteeType")
    def grantee_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "granteeType"))

    @grantee_type.setter
    def grantee_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849c32b669b3b7dedc515f20662f588a27621508ff2f96fd4d38ea79c8c48384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "granteeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPipelineThumbnailConfigPermissions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPipelineThumbnailConfigPermissions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPipelineThumbnailConfigPermissions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b226e6decf23cba1a831aab3c4811978fc5115b385a654fc4cd4aa1fe69f9fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ElastictranscoderPipeline",
    "ElastictranscoderPipelineConfig",
    "ElastictranscoderPipelineContentConfig",
    "ElastictranscoderPipelineContentConfigOutputReference",
    "ElastictranscoderPipelineContentConfigPermissions",
    "ElastictranscoderPipelineContentConfigPermissionsList",
    "ElastictranscoderPipelineContentConfigPermissionsOutputReference",
    "ElastictranscoderPipelineNotifications",
    "ElastictranscoderPipelineNotificationsOutputReference",
    "ElastictranscoderPipelineThumbnailConfig",
    "ElastictranscoderPipelineThumbnailConfigOutputReference",
    "ElastictranscoderPipelineThumbnailConfigPermissions",
    "ElastictranscoderPipelineThumbnailConfigPermissionsList",
    "ElastictranscoderPipelineThumbnailConfigPermissionsOutputReference",
]

publication.publish()

def _typecheckingstub__63a181c4148fd8517c73cd9265073d8d2301c8946302a2b527efc94cdf023e18(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    input_bucket: builtins.str,
    role: builtins.str,
    aws_kms_key_arn: typing.Optional[builtins.str] = None,
    content_config: typing.Optional[typing.Union[ElastictranscoderPipelineContentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    content_config_permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastictranscoderPipelineContentConfigPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    notifications: typing.Optional[typing.Union[ElastictranscoderPipelineNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    output_bucket: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    thumbnail_config: typing.Optional[typing.Union[ElastictranscoderPipelineThumbnailConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    thumbnail_config_permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastictranscoderPipelineThumbnailConfigPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__c8a2735d7128bc8375fffbc6492dcf6cc35ab59dfcd362d1f9181c7968e9d362(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4080404a3aa00f635f05b1d5713e03e11629a9ce1c845b0f3fd47d7cb4b7a5da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastictranscoderPipelineContentConfigPermissions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1357abe6d525bc31fdf7cc69cfab3c0a715b64861856fad4727a2ace4f0f40bf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastictranscoderPipelineThumbnailConfigPermissions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7231f17c43929d730d630355512356e5db55b48bb026abaededbc3027c23da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f2197df6c2db619b740ddd1b373e96eb4157ecd47cd3fea4d28185902eca77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95328af56ad3d7fff73ffb41da836761aff2a6baa14315a6826a6d302ae11dd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb77a6c06f6c2abe8c4a77d5961a054aa3d7bc70ecb4d52e1892f856ac1111c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58fa8827335d6e1c92801b899faa498494bb9f917d65ca85ca352fb4c7287cde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c4bbd165d8bab6bcf76b002b7923d6770236262dc4013e08ee8e3cc086663b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19ea475c797736dee07f158fc68fd183e5b42dec79ff986ffcb3e97a0de1c41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3097fcb10cfd22dba0f3109ca51a2ca70520617fb2e8af72a1994420bc6db1a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    input_bucket: builtins.str,
    role: builtins.str,
    aws_kms_key_arn: typing.Optional[builtins.str] = None,
    content_config: typing.Optional[typing.Union[ElastictranscoderPipelineContentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    content_config_permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastictranscoderPipelineContentConfigPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    notifications: typing.Optional[typing.Union[ElastictranscoderPipelineNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    output_bucket: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    thumbnail_config: typing.Optional[typing.Union[ElastictranscoderPipelineThumbnailConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    thumbnail_config_permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElastictranscoderPipelineThumbnailConfigPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d460ba91e76a6fc967194816dbb8c8b80d1acb0e9215e8d1c482c4e7f01994(
    *,
    bucket: typing.Optional[builtins.str] = None,
    storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914e266baa25893b954386be6dfa30ae166a939e5282134f1c50946ebf7278b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dae4d0a6c8d8b5ab6757bbae16fcb547a1f7d78f2a3f1a41e8ce3a7dd183818(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2c91084ac090a4cd38154330b17d5f3e90c1e2dbf1e2f0fa72d05f7de2726d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6012410e5c2d1aa6df2230eeef0a24465f69da3240a6e427f40ea9cca2878617(
    value: typing.Optional[ElastictranscoderPipelineContentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00959dbf9a61ec38c6bd379311494a7fd33d9dca3591a4632c14b01092631db(
    *,
    access: typing.Optional[typing.Sequence[builtins.str]] = None,
    grantee: typing.Optional[builtins.str] = None,
    grantee_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7791026e2ed0424f361304f19def936e08446c0886aec424714a6982169534bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1102b1e3f9a21479d18aa05e62c32d8126c078dc3214d40856415dad300c6b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38673ae302ea271f13573015ddf3d31f8e351d70af91180916172b5ada02959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffcef9daa2c97aefe6e8c61a29d87bd25add8837a26e446dbd3915c6406b20e6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4696a0c096e4e3321f8aba6d05276901f52d80267e9b77cf2bac016763f53d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67c86dbcb3452060066508e825b58618856a0a6ed72209d070eafdbab8cc269(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPipelineContentConfigPermissions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b66867e8d6736c5a7a9a18050ec9010a151c3748d8c8207930d4d5addcf420(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802df927ae0de7d79b29c7a6ad49de47d25dfbf805da84083befcce772c66e1b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e189f9d54887df66dab69a8cc92394a41df7a7282291e150c1e5c1ffd35e795d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5b680c939c3fa7fb387a91614d3317244ac8e0dbf34616e329271bba961c2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5337160628e666718d573b36f610ac13e68693d7d22d12059a2f84bd3cf978(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPipelineContentConfigPermissions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56617c3d325a3d3a2e4599a61477aa619c4f83777a15fe6c74f692c50a3f338(
    *,
    completed: typing.Optional[builtins.str] = None,
    error: typing.Optional[builtins.str] = None,
    progressing: typing.Optional[builtins.str] = None,
    warning: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bda0a5b8f4d7df62a8e6ae79664b1d120157d59200a7a0bd5633675e0db7779(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b459552714410e6dbbd5016b3a3c7ef40b81d3740cac8102a439fa6e7767b0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb5748efddf26fb37f8a8cc974f006816b42ce17023b9a567b3fc0b62f831dc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefe84f18c3f65a63a5eebb8f59439468de359c2bac34b038e50aa1039a3ae5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0e7be267fd7a9590a6442605e0c283b7d027f0ba88535f49c07e5f99360619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36e8dc4689ee3bc6356378a14afae197cd7dc0dc73f430b9896ef658bae88e0(
    value: typing.Optional[ElastictranscoderPipelineNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ed3f3a34a32e7b64650e3f579761e9549c01d634be89215858fdc5b0a5a794(
    *,
    bucket: typing.Optional[builtins.str] = None,
    storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7abad9dde498cfa1cdfc32480a1e9606ceb7bcb9d7128a7ff9a1c70e1f7c0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c41f21e9bcb8604f6de6a51932d89b1fa48961b02ec3f593f451f89179a220(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679b21aad246a808ac175983591856aa30f51253185aa65aeaa79bd16b51a283(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3adc8fcbcf84f86d73233014a28f6fd302f052a33ec5832e3ded664315b64c(
    value: typing.Optional[ElastictranscoderPipelineThumbnailConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e068fc5c95107070701ce05f385034e1f6e57418dadd3384467d4ccf727a3c1f(
    *,
    access: typing.Optional[typing.Sequence[builtins.str]] = None,
    grantee: typing.Optional[builtins.str] = None,
    grantee_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd83e45ad2dd06385ada68330f32e636cfd4c11878b727d9d1174fda7366243(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3cf3049482e6d7595ef3c4dc869c36bd7c2379266edebf83434b7ceac38329(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aea8d9e8d2255af043fce5ebe5268c46ca94f14ecda9da5d5fb8d62b63c077a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7f9a6d2cb35e553aeb0e4b58f0957d97b1b24fd908ddc93d78416cb2fa5829(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ede725d209f9c59bca7ffbfcd30816328be148124b1fa84b97487ecdd29c69(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f070fa8e3e74208adf744980cb36c79c08883c419ccab6938a6f14c59291846(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElastictranscoderPipelineThumbnailConfigPermissions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045b01abbe6d0216208cd9671acaa865cf56f20db0e77ece39e0fed65dcf951b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4ed7457d55f7b728d6384f47d4eda959888668b29c61d0650db5bedefd011e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac561093363afa648bcc07a379b7a2bdb5a8b1e830c431bb72cc633284ed0bea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849c32b669b3b7dedc515f20662f588a27621508ff2f96fd4d38ea79c8c48384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b226e6decf23cba1a831aab3c4811978fc5115b385a654fc4cd4aa1fe69f9fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElastictranscoderPipelineThumbnailConfigPermissions]],
) -> None:
    """Type checking stubs"""
    pass
