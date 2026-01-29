r'''
# `aws_cloudfront_field_level_encryption_config`

Refer to the Terraform Registry for docs: [`aws_cloudfront_field_level_encryption_config`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config).
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


class CloudfrontFieldLevelEncryptionConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config aws_cloudfront_field_level_encryption_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        content_type_profile_config: typing.Union["CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig", typing.Dict[builtins.str, typing.Any]],
        query_arg_profile_config: typing.Union["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig", typing.Dict[builtins.str, typing.Any]],
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config aws_cloudfront_field_level_encryption_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param content_type_profile_config: content_type_profile_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#content_type_profile_config CloudfrontFieldLevelEncryptionConfig#content_type_profile_config}
        :param query_arg_profile_config: query_arg_profile_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#query_arg_profile_config CloudfrontFieldLevelEncryptionConfig#query_arg_profile_config}
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#comment CloudfrontFieldLevelEncryptionConfig#comment}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#id CloudfrontFieldLevelEncryptionConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db38eae4ee0039c833f9fa6882493dff97d58ba1ee3a09c00ca2cfb66144202)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudfrontFieldLevelEncryptionConfigConfig(
            content_type_profile_config=content_type_profile_config,
            query_arg_profile_config=query_arg_profile_config,
            comment=comment,
            id=id,
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
        '''Generates CDKTF code for importing a CloudfrontFieldLevelEncryptionConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudfrontFieldLevelEncryptionConfig to import.
        :param import_from_id: The id of the existing CloudfrontFieldLevelEncryptionConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudfrontFieldLevelEncryptionConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543f8cd507cade202f7ba211e71a57a43c027f4afc87383f5428965413e170e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContentTypeProfileConfig")
    def put_content_type_profile_config(
        self,
        *,
        content_type_profiles: typing.Union["CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles", typing.Dict[builtins.str, typing.Any]],
        forward_when_content_type_is_unknown: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param content_type_profiles: content_type_profiles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#content_type_profiles CloudfrontFieldLevelEncryptionConfig#content_type_profiles}
        :param forward_when_content_type_is_unknown: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#forward_when_content_type_is_unknown CloudfrontFieldLevelEncryptionConfig#forward_when_content_type_is_unknown}.
        '''
        value = CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig(
            content_type_profiles=content_type_profiles,
            forward_when_content_type_is_unknown=forward_when_content_type_is_unknown,
        )

        return typing.cast(None, jsii.invoke(self, "putContentTypeProfileConfig", [value]))

    @jsii.member(jsii_name="putQueryArgProfileConfig")
    def put_query_arg_profile_config(
        self,
        *,
        forward_when_query_arg_profile_is_unknown: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        query_arg_profiles: typing.Optional[typing.Union["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param forward_when_query_arg_profile_is_unknown: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#forward_when_query_arg_profile_is_unknown CloudfrontFieldLevelEncryptionConfig#forward_when_query_arg_profile_is_unknown}.
        :param query_arg_profiles: query_arg_profiles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#query_arg_profiles CloudfrontFieldLevelEncryptionConfig#query_arg_profiles}
        '''
        value = CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig(
            forward_when_query_arg_profile_is_unknown=forward_when_query_arg_profile_is_unknown,
            query_arg_profiles=query_arg_profiles,
        )

        return typing.cast(None, jsii.invoke(self, "putQueryArgProfileConfig", [value]))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="callerReference")
    def caller_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callerReference"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeProfileConfig")
    def content_type_profile_config(
        self,
    ) -> "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigOutputReference":
        return typing.cast("CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigOutputReference", jsii.get(self, "contentTypeProfileConfig"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="queryArgProfileConfig")
    def query_arg_profile_config(
        self,
    ) -> "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigOutputReference":
        return typing.cast("CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigOutputReference", jsii.get(self, "queryArgProfileConfig"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeProfileConfigInput")
    def content_type_profile_config_input(
        self,
    ) -> typing.Optional["CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig"]:
        return typing.cast(typing.Optional["CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig"], jsii.get(self, "contentTypeProfileConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="queryArgProfileConfigInput")
    def query_arg_profile_config_input(
        self,
    ) -> typing.Optional["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig"]:
        return typing.cast(typing.Optional["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig"], jsii.get(self, "queryArgProfileConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c0a1d67be676988eec44474b7981a874a674e1363c9d97ca928e89a8ee37ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d31b4a3cef7f08ed1f0804c7928e5eaeaf455b0b0b69f55dc7a3a4e6373e9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "content_type_profile_config": "contentTypeProfileConfig",
        "query_arg_profile_config": "queryArgProfileConfig",
        "comment": "comment",
        "id": "id",
    },
)
class CloudfrontFieldLevelEncryptionConfigConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        content_type_profile_config: typing.Union["CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig", typing.Dict[builtins.str, typing.Any]],
        query_arg_profile_config: typing.Union["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig", typing.Dict[builtins.str, typing.Any]],
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param content_type_profile_config: content_type_profile_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#content_type_profile_config CloudfrontFieldLevelEncryptionConfig#content_type_profile_config}
        :param query_arg_profile_config: query_arg_profile_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#query_arg_profile_config CloudfrontFieldLevelEncryptionConfig#query_arg_profile_config}
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#comment CloudfrontFieldLevelEncryptionConfig#comment}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#id CloudfrontFieldLevelEncryptionConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(content_type_profile_config, dict):
            content_type_profile_config = CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig(**content_type_profile_config)
        if isinstance(query_arg_profile_config, dict):
            query_arg_profile_config = CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig(**query_arg_profile_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42701c77733e5eb5d45b58ae41849b79196ef57ece77e8d623279dd03dcaa976)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument content_type_profile_config", value=content_type_profile_config, expected_type=type_hints["content_type_profile_config"])
            check_type(argname="argument query_arg_profile_config", value=query_arg_profile_config, expected_type=type_hints["query_arg_profile_config"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_type_profile_config": content_type_profile_config,
            "query_arg_profile_config": query_arg_profile_config,
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
        if comment is not None:
            self._values["comment"] = comment
        if id is not None:
            self._values["id"] = id

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
    def content_type_profile_config(
        self,
    ) -> "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig":
        '''content_type_profile_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#content_type_profile_config CloudfrontFieldLevelEncryptionConfig#content_type_profile_config}
        '''
        result = self._values.get("content_type_profile_config")
        assert result is not None, "Required property 'content_type_profile_config' is missing"
        return typing.cast("CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig", result)

    @builtins.property
    def query_arg_profile_config(
        self,
    ) -> "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig":
        '''query_arg_profile_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#query_arg_profile_config CloudfrontFieldLevelEncryptionConfig#query_arg_profile_config}
        '''
        result = self._values.get("query_arg_profile_config")
        assert result is not None, "Required property 'query_arg_profile_config' is missing"
        return typing.cast("CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig", result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#comment CloudfrontFieldLevelEncryptionConfig#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#id CloudfrontFieldLevelEncryptionConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontFieldLevelEncryptionConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig",
    jsii_struct_bases=[],
    name_mapping={
        "content_type_profiles": "contentTypeProfiles",
        "forward_when_content_type_is_unknown": "forwardWhenContentTypeIsUnknown",
    },
)
class CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig:
    def __init__(
        self,
        *,
        content_type_profiles: typing.Union["CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles", typing.Dict[builtins.str, typing.Any]],
        forward_when_content_type_is_unknown: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param content_type_profiles: content_type_profiles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#content_type_profiles CloudfrontFieldLevelEncryptionConfig#content_type_profiles}
        :param forward_when_content_type_is_unknown: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#forward_when_content_type_is_unknown CloudfrontFieldLevelEncryptionConfig#forward_when_content_type_is_unknown}.
        '''
        if isinstance(content_type_profiles, dict):
            content_type_profiles = CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles(**content_type_profiles)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085d1d406b1dd7d5a3ecf05e6da8def99329faa3d976534b47d7d8bbb929beec)
            check_type(argname="argument content_type_profiles", value=content_type_profiles, expected_type=type_hints["content_type_profiles"])
            check_type(argname="argument forward_when_content_type_is_unknown", value=forward_when_content_type_is_unknown, expected_type=type_hints["forward_when_content_type_is_unknown"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_type_profiles": content_type_profiles,
            "forward_when_content_type_is_unknown": forward_when_content_type_is_unknown,
        }

    @builtins.property
    def content_type_profiles(
        self,
    ) -> "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles":
        '''content_type_profiles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#content_type_profiles CloudfrontFieldLevelEncryptionConfig#content_type_profiles}
        '''
        result = self._values.get("content_type_profiles")
        assert result is not None, "Required property 'content_type_profiles' is missing"
        return typing.cast("CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles", result)

    @builtins.property
    def forward_when_content_type_is_unknown(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#forward_when_content_type_is_unknown CloudfrontFieldLevelEncryptionConfig#forward_when_content_type_is_unknown}.'''
        result = self._values.get("forward_when_content_type_is_unknown")
        assert result is not None, "Required property 'forward_when_content_type_is_unknown' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles:
    def __init__(
        self,
        *,
        items: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#items CloudfrontFieldLevelEncryptionConfig#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7009dedac4ff1e7a406fc122d542f648b99019f8e7a945bff79b27e6223186d)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "items": items,
        }

    @builtins.property
    def items(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems"]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#items CloudfrontFieldLevelEncryptionConfig#items}
        '''
        result = self._values.get("items")
        assert result is not None, "Required property 'items' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems",
    jsii_struct_bases=[],
    name_mapping={
        "content_type": "contentType",
        "format": "format",
        "profile_id": "profileId",
    },
)
class CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems:
    def __init__(
        self,
        *,
        content_type: builtins.str,
        format: builtins.str,
        profile_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#content_type CloudfrontFieldLevelEncryptionConfig#content_type}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#format CloudfrontFieldLevelEncryptionConfig#format}.
        :param profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#profile_id CloudfrontFieldLevelEncryptionConfig#profile_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b450491bf751ca366e7ba52ee507e2e5d6d4e2ffd323bc6226ceff26eb60d4bf)
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument profile_id", value=profile_id, expected_type=type_hints["profile_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_type": content_type,
            "format": format,
        }
        if profile_id is not None:
            self._values["profile_id"] = profile_id

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#content_type CloudfrontFieldLevelEncryptionConfig#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#format CloudfrontFieldLevelEncryptionConfig#format}.'''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#profile_id CloudfrontFieldLevelEncryptionConfig#profile_id}.'''
        result = self._values.get("profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5fe494371dc082b7eddf88f3aa2795bbc9f7a7d78bbcf38098427d8bddafb2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02403fe7e8bd3ab11c9d5bfbe4967a051259c1c16866f075afe0842d148ac12a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7edcd16e63f6a910131a99070c333a355b25d7976b02870ec88befdf25a100e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d60be0a27df50d84a76c2df02fa1589c16da1fbc6eb30902ba6d389bb0827272)
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
            type_hints = typing.get_type_hints(_typecheckingstub__addc15894f8ff71fe91642bdda5de73b43a74c303dc47815d42790f1a23b2587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d970bb69cd254f9cf34d9b90d8000662f23ec70f052ae8fa02adfcd06c84663b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19e5e438cef835e1075e4a4db6e9bb869eaa28638d20ce2526f2cf4f29ecc44e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetProfileId")
    def reset_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileId", []))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="profileIdInput")
    def profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd30d84f5ea714264efc38293cad829224c7e7132b2d2ae66101a96ef18b442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c00463d1a8ed224f60dcc0bd6117257e20c32bae871413b7c2b095a8194f9d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileId")
    def profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profileId"))

    @profile_id.setter
    def profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71def5d8ade9c9a0e2e2bfc430ef32ed4037f6c9d18b97c82b927bfb2546bb94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81eb5e16082f5f2d35b6cb9ed4d5a5db3bdd7d366b5152337aacb84821986a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44a5ffcc5b7dfe28aa2d6f6ad7aabf9f122e34c3e53dd7c59ccf82216b62783c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546207a90d692a22ae46b559f1b9d38fb284e287f266659f1334557b793834da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItems", [value]))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(
        self,
    ) -> CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItemsList:
        return typing.cast(CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems]]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles]:
        return typing.cast(typing.Optional[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6411527e62ade3674235011eea865aaf5dfae31694c060765f7f7a97e67d0322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4ac6a0b39efa6e1feb8814adb0e66edb498d8d898731b170b734922102765a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContentTypeProfiles")
    def put_content_type_profiles(
        self,
        *,
        items: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#items CloudfrontFieldLevelEncryptionConfig#items}
        '''
        value = CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles(
            items=items
        )

        return typing.cast(None, jsii.invoke(self, "putContentTypeProfiles", [value]))

    @builtins.property
    @jsii.member(jsii_name="contentTypeProfiles")
    def content_type_profiles(
        self,
    ) -> CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesOutputReference:
        return typing.cast(CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesOutputReference, jsii.get(self, "contentTypeProfiles"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeProfilesInput")
    def content_type_profiles_input(
        self,
    ) -> typing.Optional[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles]:
        return typing.cast(typing.Optional[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles], jsii.get(self, "contentTypeProfilesInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardWhenContentTypeIsUnknownInput")
    def forward_when_content_type_is_unknown_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forwardWhenContentTypeIsUnknownInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardWhenContentTypeIsUnknown")
    def forward_when_content_type_is_unknown(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forwardWhenContentTypeIsUnknown"))

    @forward_when_content_type_is_unknown.setter
    def forward_when_content_type_is_unknown(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d7830377efb4d58c2518412b03aed9f9a0385cbe73658f5a3097865351cf08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardWhenContentTypeIsUnknown", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig]:
        return typing.cast(typing.Optional[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb9a6f8ec5d6938084bd32995e5d03a8a7757fd83c37e194186969676d1d58a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig",
    jsii_struct_bases=[],
    name_mapping={
        "forward_when_query_arg_profile_is_unknown": "forwardWhenQueryArgProfileIsUnknown",
        "query_arg_profiles": "queryArgProfiles",
    },
)
class CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig:
    def __init__(
        self,
        *,
        forward_when_query_arg_profile_is_unknown: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        query_arg_profiles: typing.Optional[typing.Union["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param forward_when_query_arg_profile_is_unknown: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#forward_when_query_arg_profile_is_unknown CloudfrontFieldLevelEncryptionConfig#forward_when_query_arg_profile_is_unknown}.
        :param query_arg_profiles: query_arg_profiles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#query_arg_profiles CloudfrontFieldLevelEncryptionConfig#query_arg_profiles}
        '''
        if isinstance(query_arg_profiles, dict):
            query_arg_profiles = CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles(**query_arg_profiles)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590c902a4e601c37aa13b6919a025efcf78be1037885435e07d00f90a0b7413f)
            check_type(argname="argument forward_when_query_arg_profile_is_unknown", value=forward_when_query_arg_profile_is_unknown, expected_type=type_hints["forward_when_query_arg_profile_is_unknown"])
            check_type(argname="argument query_arg_profiles", value=query_arg_profiles, expected_type=type_hints["query_arg_profiles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "forward_when_query_arg_profile_is_unknown": forward_when_query_arg_profile_is_unknown,
        }
        if query_arg_profiles is not None:
            self._values["query_arg_profiles"] = query_arg_profiles

    @builtins.property
    def forward_when_query_arg_profile_is_unknown(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#forward_when_query_arg_profile_is_unknown CloudfrontFieldLevelEncryptionConfig#forward_when_query_arg_profile_is_unknown}.'''
        result = self._values.get("forward_when_query_arg_profile_is_unknown")
        assert result is not None, "Required property 'forward_when_query_arg_profile_is_unknown' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def query_arg_profiles(
        self,
    ) -> typing.Optional["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles"]:
        '''query_arg_profiles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#query_arg_profiles CloudfrontFieldLevelEncryptionConfig#query_arg_profiles}
        '''
        result = self._values.get("query_arg_profiles")
        return typing.cast(typing.Optional["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf3d5139787d5a4ba083fc0887b33af1834ede079a7f9955f92f049bae67b83f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putQueryArgProfiles")
    def put_query_arg_profiles(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#items CloudfrontFieldLevelEncryptionConfig#items}
        '''
        value = CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles(
            items=items
        )

        return typing.cast(None, jsii.invoke(self, "putQueryArgProfiles", [value]))

    @jsii.member(jsii_name="resetQueryArgProfiles")
    def reset_query_arg_profiles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryArgProfiles", []))

    @builtins.property
    @jsii.member(jsii_name="queryArgProfiles")
    def query_arg_profiles(
        self,
    ) -> "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesOutputReference":
        return typing.cast("CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesOutputReference", jsii.get(self, "queryArgProfiles"))

    @builtins.property
    @jsii.member(jsii_name="forwardWhenQueryArgProfileIsUnknownInput")
    def forward_when_query_arg_profile_is_unknown_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forwardWhenQueryArgProfileIsUnknownInput"))

    @builtins.property
    @jsii.member(jsii_name="queryArgProfilesInput")
    def query_arg_profiles_input(
        self,
    ) -> typing.Optional["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles"]:
        return typing.cast(typing.Optional["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles"], jsii.get(self, "queryArgProfilesInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardWhenQueryArgProfileIsUnknown")
    def forward_when_query_arg_profile_is_unknown(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forwardWhenQueryArgProfileIsUnknown"))

    @forward_when_query_arg_profile_is_unknown.setter
    def forward_when_query_arg_profile_is_unknown(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08db6aaee68504547359dd6fd121b5ecb14cafb155c162dee8f5d969d2f8cdbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardWhenQueryArgProfileIsUnknown", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig]:
        return typing.cast(typing.Optional[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5697650e57bc48b5a3a35eb73c8760f7f9c6f82ac2ec9969dad8eb8fa993124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#items CloudfrontFieldLevelEncryptionConfig#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e495c6f1966f73137ec9ad6375788830a5a86c8989633f6f8578b54a871cba)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#items CloudfrontFieldLevelEncryptionConfig#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems",
    jsii_struct_bases=[],
    name_mapping={"profile_id": "profileId", "query_arg": "queryArg"},
)
class CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems:
    def __init__(self, *, profile_id: builtins.str, query_arg: builtins.str) -> None:
        '''
        :param profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#profile_id CloudfrontFieldLevelEncryptionConfig#profile_id}.
        :param query_arg: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#query_arg CloudfrontFieldLevelEncryptionConfig#query_arg}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2894311044a036def8e058fcd0b9d50ea81b4dea145f39bd010b25a0d45eb515)
            check_type(argname="argument profile_id", value=profile_id, expected_type=type_hints["profile_id"])
            check_type(argname="argument query_arg", value=query_arg, expected_type=type_hints["query_arg"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "profile_id": profile_id,
            "query_arg": query_arg,
        }

    @builtins.property
    def profile_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#profile_id CloudfrontFieldLevelEncryptionConfig#profile_id}.'''
        result = self._values.get("profile_id")
        assert result is not None, "Required property 'profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query_arg(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_field_level_encryption_config#query_arg CloudfrontFieldLevelEncryptionConfig#query_arg}.'''
        result = self._values.get("query_arg")
        assert result is not None, "Required property 'query_arg' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__951c6321bc2235546c4d39f1ab5ec4d3a2d4818c59bdf9fb38af49797f739a76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d86456c4b94b32c564c98260236d3a4399e7abcead76ed0d21a9806e4ff2a5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a039b5427932b151b47265c93d01745fd3df87a342b469cec606cd077b475220)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfa7f9885541dab7cf40c49ec62c274ec9a8044cbd5225a262ecfc86e3f29161)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8288ca5c5561478a71dbc164a7e5598519482228f7b047cefe32de3475d72030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e9ec9d22167a507d47b0c62c16d8e1a662fe7c8b28c0520f97d4226a748bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3ee18bc68c0816c99717dd2288a726dd2bbd45422d24447133a54cdbf747480)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="profileIdInput")
    def profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryArgInput")
    def query_arg_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryArgInput"))

    @builtins.property
    @jsii.member(jsii_name="profileId")
    def profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profileId"))

    @profile_id.setter
    def profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c107f6c723c229dac224a863f73e0b5cded32f8fe9a147390a47727f2cc34b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryArg")
    def query_arg(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryArg"))

    @query_arg.setter
    def query_arg(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b7fd46f00d720b7fb562ed787a336e2454b07646768e3d7e7506ac94ffb289e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryArg", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee1ca4875a4a859566b19e285fd2973b59538fa5b290d4d540c3ad859677cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontFieldLevelEncryptionConfig.CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cb79c44b889b67552de5b4145fdc16a63a0e2432de5900a224688ed510cc4f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1bc7797b2d3465aa07134ddbc27ffcf106a46f35b08e2c6136f07e629d970fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItems", [value]))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(
        self,
    ) -> CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItemsList:
        return typing.cast(CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems]]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles]:
        return typing.cast(typing.Optional[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccbab3cf19148a2a0469dbc2b9b3a4719e6a0425dcdd31f0bbfd9e7c36942b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudfrontFieldLevelEncryptionConfig",
    "CloudfrontFieldLevelEncryptionConfigConfig",
    "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig",
    "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles",
    "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems",
    "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItemsList",
    "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItemsOutputReference",
    "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesOutputReference",
    "CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigOutputReference",
    "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig",
    "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigOutputReference",
    "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles",
    "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems",
    "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItemsList",
    "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItemsOutputReference",
    "CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesOutputReference",
]

publication.publish()

def _typecheckingstub__7db38eae4ee0039c833f9fa6882493dff97d58ba1ee3a09c00ca2cfb66144202(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    content_type_profile_config: typing.Union[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig, typing.Dict[builtins.str, typing.Any]],
    query_arg_profile_config: typing.Union[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig, typing.Dict[builtins.str, typing.Any]],
    comment: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__543f8cd507cade202f7ba211e71a57a43c027f4afc87383f5428965413e170e7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c0a1d67be676988eec44474b7981a874a674e1363c9d97ca928e89a8ee37ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d31b4a3cef7f08ed1f0804c7928e5eaeaf455b0b0b69f55dc7a3a4e6373e9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42701c77733e5eb5d45b58ae41849b79196ef57ece77e8d623279dd03dcaa976(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    content_type_profile_config: typing.Union[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig, typing.Dict[builtins.str, typing.Any]],
    query_arg_profile_config: typing.Union[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig, typing.Dict[builtins.str, typing.Any]],
    comment: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085d1d406b1dd7d5a3ecf05e6da8def99329faa3d976534b47d7d8bbb929beec(
    *,
    content_type_profiles: typing.Union[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles, typing.Dict[builtins.str, typing.Any]],
    forward_when_content_type_is_unknown: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7009dedac4ff1e7a406fc122d542f648b99019f8e7a945bff79b27e6223186d(
    *,
    items: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b450491bf751ca366e7ba52ee507e2e5d6d4e2ffd323bc6226ceff26eb60d4bf(
    *,
    content_type: builtins.str,
    format: builtins.str,
    profile_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fe494371dc082b7eddf88f3aa2795bbc9f7a7d78bbcf38098427d8bddafb2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02403fe7e8bd3ab11c9d5bfbe4967a051259c1c16866f075afe0842d148ac12a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7edcd16e63f6a910131a99070c333a355b25d7976b02870ec88befdf25a100e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60be0a27df50d84a76c2df02fa1589c16da1fbc6eb30902ba6d389bb0827272(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__addc15894f8ff71fe91642bdda5de73b43a74c303dc47815d42790f1a23b2587(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d970bb69cd254f9cf34d9b90d8000662f23ec70f052ae8fa02adfcd06c84663b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e5e438cef835e1075e4a4db6e9bb869eaa28638d20ce2526f2cf4f29ecc44e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd30d84f5ea714264efc38293cad829224c7e7132b2d2ae66101a96ef18b442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c00463d1a8ed224f60dcc0bd6117257e20c32bae871413b7c2b095a8194f9d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71def5d8ade9c9a0e2e2bfc430ef32ed4037f6c9d18b97c82b927bfb2546bb94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81eb5e16082f5f2d35b6cb9ed4d5a5db3bdd7d366b5152337aacb84821986a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a5ffcc5b7dfe28aa2d6f6ad7aabf9f122e34c3e53dd7c59ccf82216b62783c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546207a90d692a22ae46b559f1b9d38fb284e287f266659f1334557b793834da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfilesItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6411527e62ade3674235011eea865aaf5dfae31694c060765f7f7a97e67d0322(
    value: typing.Optional[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfigContentTypeProfiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ac6a0b39efa6e1feb8814adb0e66edb498d8d898731b170b734922102765a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d7830377efb4d58c2518412b03aed9f9a0385cbe73658f5a3097865351cf08(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb9a6f8ec5d6938084bd32995e5d03a8a7757fd83c37e194186969676d1d58a(
    value: typing.Optional[CloudfrontFieldLevelEncryptionConfigContentTypeProfileConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590c902a4e601c37aa13b6919a025efcf78be1037885435e07d00f90a0b7413f(
    *,
    forward_when_query_arg_profile_is_unknown: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    query_arg_profiles: typing.Optional[typing.Union[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3d5139787d5a4ba083fc0887b33af1834ede079a7f9955f92f049bae67b83f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08db6aaee68504547359dd6fd121b5ecb14cafb155c162dee8f5d969d2f8cdbb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5697650e57bc48b5a3a35eb73c8760f7f9c6f82ac2ec9969dad8eb8fa993124(
    value: typing.Optional[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e495c6f1966f73137ec9ad6375788830a5a86c8989633f6f8578b54a871cba(
    *,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2894311044a036def8e058fcd0b9d50ea81b4dea145f39bd010b25a0d45eb515(
    *,
    profile_id: builtins.str,
    query_arg: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951c6321bc2235546c4d39f1ab5ec4d3a2d4818c59bdf9fb38af49797f739a76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d86456c4b94b32c564c98260236d3a4399e7abcead76ed0d21a9806e4ff2a5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a039b5427932b151b47265c93d01745fd3df87a342b469cec606cd077b475220(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa7f9885541dab7cf40c49ec62c274ec9a8044cbd5225a262ecfc86e3f29161(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8288ca5c5561478a71dbc164a7e5598519482228f7b047cefe32de3475d72030(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e9ec9d22167a507d47b0c62c16d8e1a662fe7c8b28c0520f97d4226a748bcc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ee18bc68c0816c99717dd2288a726dd2bbd45422d24447133a54cdbf747480(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c107f6c723c229dac224a863f73e0b5cded32f8fe9a147390a47727f2cc34b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7fd46f00d720b7fb562ed787a336e2454b07646768e3d7e7506ac94ffb289e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee1ca4875a4a859566b19e285fd2973b59538fa5b290d4d540c3ad859677cf7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb79c44b889b67552de5b4145fdc16a63a0e2432de5900a224688ed510cc4f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1bc7797b2d3465aa07134ddbc27ffcf106a46f35b08e2c6136f07e629d970fc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfilesItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbab3cf19148a2a0469dbc2b9b3a4719e6a0425dcdd31f0bbfd9e7c36942b9b(
    value: typing.Optional[CloudfrontFieldLevelEncryptionConfigQueryArgProfileConfigQueryArgProfiles],
) -> None:
    """Type checking stubs"""
    pass
