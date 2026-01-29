r'''
# `aws_s3control_storage_lens_configuration`

Refer to the Terraform Registry for docs: [`aws_s3control_storage_lens_configuration`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration).
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


class S3ControlStorageLensConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration aws_s3control_storage_lens_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        config_id: builtins.str,
        storage_lens_configuration: typing.Union["S3ControlStorageLensConfigurationStorageLensConfiguration", typing.Dict[builtins.str, typing.Any]],
        account_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration aws_s3control_storage_lens_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param config_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#config_id S3ControlStorageLensConfiguration#config_id}.
        :param storage_lens_configuration: storage_lens_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#storage_lens_configuration S3ControlStorageLensConfiguration#storage_lens_configuration}
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#account_id S3ControlStorageLensConfiguration#account_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#id S3ControlStorageLensConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#region S3ControlStorageLensConfiguration#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#tags S3ControlStorageLensConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#tags_all S3ControlStorageLensConfiguration#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea9449b99e88b68ec964d3d3769908d24e51705966e9426294a0f05b17f41687)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = S3ControlStorageLensConfigurationConfig(
            config_id=config_id,
            storage_lens_configuration=storage_lens_configuration,
            account_id=account_id,
            id=id,
            region=region,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a S3ControlStorageLensConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the S3ControlStorageLensConfiguration to import.
        :param import_from_id: The id of the existing S3ControlStorageLensConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the S3ControlStorageLensConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357721cfcbdf1c2cabd127d0b6a4479ffc04555d3dc17502a9ef7d80c5d6e489)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putStorageLensConfiguration")
    def put_storage_lens_configuration(
        self,
        *,
        account_level: typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        aws_org: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg", typing.Dict[builtins.str, typing.Any]]] = None,
        data_export: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationDataExport", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationExclude", typing.Dict[builtins.str, typing.Any]]] = None,
        include: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationInclude", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param account_level: account_level block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#account_level S3ControlStorageLensConfiguration#account_level}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        :param aws_org: aws_org block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#aws_org S3ControlStorageLensConfiguration#aws_org}
        :param data_export: data_export block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#data_export S3ControlStorageLensConfiguration#data_export}
        :param exclude: exclude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#exclude S3ControlStorageLensConfiguration#exclude}
        :param include: include block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#include S3ControlStorageLensConfiguration#include}
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfiguration(
            account_level=account_level,
            enabled=enabled,
            aws_org=aws_org,
            data_export=data_export,
            exclude=exclude,
            include=include,
        )

        return typing.cast(None, jsii.invoke(self, "putStorageLensConfiguration", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="storageLensConfiguration")
    def storage_lens_configuration(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationOutputReference":
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationOutputReference", jsii.get(self, "storageLensConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configIdInput")
    def config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="storageLensConfigurationInput")
    def storage_lens_configuration_input(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfiguration"]:
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfiguration"], jsii.get(self, "storageLensConfigurationInput"))

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
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbb608588f50e1b4ea1c591acb9da3bb6758ee8e4492f221a5c117d240850fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configId")
    def config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configId"))

    @config_id.setter
    def config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2e38ec5957ee5de12cb3f7887e851b9c083275c4b81f59952ea1fe95114f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10dc71d3bcbc78ce9b1d3a001afb2dfeb3f9a6de18b08d1edf55192c0b372247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b042f77c7c49188439f47a291f173f67831e0ad9a1d8a21fe7dab27c3e85b04a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d5568d3d0e7e156d84ddfbff0eea1a6af265cd088b8b9ffb2afbe400451278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885fb334e39fb7620884bf2ae6d705a74938194c7bfdfe124abc273b0659ce42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "config_id": "configId",
        "storage_lens_configuration": "storageLensConfiguration",
        "account_id": "accountId",
        "id": "id",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class S3ControlStorageLensConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config_id: builtins.str,
        storage_lens_configuration: typing.Union["S3ControlStorageLensConfigurationStorageLensConfiguration", typing.Dict[builtins.str, typing.Any]],
        account_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param config_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#config_id S3ControlStorageLensConfiguration#config_id}.
        :param storage_lens_configuration: storage_lens_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#storage_lens_configuration S3ControlStorageLensConfiguration#storage_lens_configuration}
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#account_id S3ControlStorageLensConfiguration#account_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#id S3ControlStorageLensConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#region S3ControlStorageLensConfiguration#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#tags S3ControlStorageLensConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#tags_all S3ControlStorageLensConfiguration#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(storage_lens_configuration, dict):
            storage_lens_configuration = S3ControlStorageLensConfigurationStorageLensConfiguration(**storage_lens_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4d6172c6d3d93d5e199470ac0346f264bde66c5afbd77466d54b2db076aff8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument config_id", value=config_id, expected_type=type_hints["config_id"])
            check_type(argname="argument storage_lens_configuration", value=storage_lens_configuration, expected_type=type_hints["storage_lens_configuration"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_id": config_id,
            "storage_lens_configuration": storage_lens_configuration,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def config_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#config_id S3ControlStorageLensConfiguration#config_id}.'''
        result = self._values.get("config_id")
        assert result is not None, "Required property 'config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_lens_configuration(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfiguration":
        '''storage_lens_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#storage_lens_configuration S3ControlStorageLensConfiguration#storage_lens_configuration}
        '''
        result = self._values.get("storage_lens_configuration")
        assert result is not None, "Required property 'storage_lens_configuration' is missing"
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfiguration", result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#account_id S3ControlStorageLensConfiguration#account_id}.'''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#id S3ControlStorageLensConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#region S3ControlStorageLensConfiguration#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#tags S3ControlStorageLensConfiguration#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#tags_all S3ControlStorageLensConfiguration#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "account_level": "accountLevel",
        "enabled": "enabled",
        "aws_org": "awsOrg",
        "data_export": "dataExport",
        "exclude": "exclude",
        "include": "include",
    },
)
class S3ControlStorageLensConfigurationStorageLensConfiguration:
    def __init__(
        self,
        *,
        account_level: typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        aws_org: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg", typing.Dict[builtins.str, typing.Any]]] = None,
        data_export: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationDataExport", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationExclude", typing.Dict[builtins.str, typing.Any]]] = None,
        include: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationInclude", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param account_level: account_level block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#account_level S3ControlStorageLensConfiguration#account_level}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        :param aws_org: aws_org block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#aws_org S3ControlStorageLensConfiguration#aws_org}
        :param data_export: data_export block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#data_export S3ControlStorageLensConfiguration#data_export}
        :param exclude: exclude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#exclude S3ControlStorageLensConfiguration#exclude}
        :param include: include block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#include S3ControlStorageLensConfiguration#include}
        '''
        if isinstance(account_level, dict):
            account_level = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel(**account_level)
        if isinstance(aws_org, dict):
            aws_org = S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg(**aws_org)
        if isinstance(data_export, dict):
            data_export = S3ControlStorageLensConfigurationStorageLensConfigurationDataExport(**data_export)
        if isinstance(exclude, dict):
            exclude = S3ControlStorageLensConfigurationStorageLensConfigurationExclude(**exclude)
        if isinstance(include, dict):
            include = S3ControlStorageLensConfigurationStorageLensConfigurationInclude(**include)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97c89204c3f27c900c9d43735415c75d48cf40866b1e93bdfaa8199dfd9f34d)
            check_type(argname="argument account_level", value=account_level, expected_type=type_hints["account_level"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument aws_org", value=aws_org, expected_type=type_hints["aws_org"])
            check_type(argname="argument data_export", value=data_export, expected_type=type_hints["data_export"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_level": account_level,
            "enabled": enabled,
        }
        if aws_org is not None:
            self._values["aws_org"] = aws_org
        if data_export is not None:
            self._values["data_export"] = data_export
        if exclude is not None:
            self._values["exclude"] = exclude
        if include is not None:
            self._values["include"] = include

    @builtins.property
    def account_level(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel":
        '''account_level block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#account_level S3ControlStorageLensConfiguration#account_level}
        '''
        result = self._values.get("account_level")
        assert result is not None, "Required property 'account_level' is missing"
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel", result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def aws_org(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg"]:
        '''aws_org block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#aws_org S3ControlStorageLensConfiguration#aws_org}
        '''
        result = self._values.get("aws_org")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg"], result)

    @builtins.property
    def data_export(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExport"]:
        '''data_export block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#data_export S3ControlStorageLensConfiguration#data_export}
        '''
        result = self._values.get("data_export")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExport"], result)

    @builtins.property
    def exclude(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationExclude"]:
        '''exclude block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#exclude S3ControlStorageLensConfiguration#exclude}
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationExclude"], result)

    @builtins.property
    def include(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationInclude"]:
        '''include block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#include S3ControlStorageLensConfiguration#include}
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationInclude"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_level": "bucketLevel",
        "activity_metrics": "activityMetrics",
        "advanced_cost_optimization_metrics": "advancedCostOptimizationMetrics",
        "advanced_data_protection_metrics": "advancedDataProtectionMetrics",
        "detailed_status_code_metrics": "detailedStatusCodeMetrics",
    },
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel:
    def __init__(
        self,
        *,
        bucket_level: typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel", typing.Dict[builtins.str, typing.Any]],
        activity_metrics: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_cost_optimization_metrics: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_data_protection_metrics: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        detailed_status_code_metrics: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_level: bucket_level block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#bucket_level S3ControlStorageLensConfiguration#bucket_level}
        :param activity_metrics: activity_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#activity_metrics S3ControlStorageLensConfiguration#activity_metrics}
        :param advanced_cost_optimization_metrics: advanced_cost_optimization_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_cost_optimization_metrics S3ControlStorageLensConfiguration#advanced_cost_optimization_metrics}
        :param advanced_data_protection_metrics: advanced_data_protection_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_data_protection_metrics S3ControlStorageLensConfiguration#advanced_data_protection_metrics}
        :param detailed_status_code_metrics: detailed_status_code_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#detailed_status_code_metrics S3ControlStorageLensConfiguration#detailed_status_code_metrics}
        '''
        if isinstance(bucket_level, dict):
            bucket_level = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel(**bucket_level)
        if isinstance(activity_metrics, dict):
            activity_metrics = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics(**activity_metrics)
        if isinstance(advanced_cost_optimization_metrics, dict):
            advanced_cost_optimization_metrics = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics(**advanced_cost_optimization_metrics)
        if isinstance(advanced_data_protection_metrics, dict):
            advanced_data_protection_metrics = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics(**advanced_data_protection_metrics)
        if isinstance(detailed_status_code_metrics, dict):
            detailed_status_code_metrics = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics(**detailed_status_code_metrics)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c724aeb900590fa4dff1969d619abbea63c44130e30901a38ea68a86905fa82)
            check_type(argname="argument bucket_level", value=bucket_level, expected_type=type_hints["bucket_level"])
            check_type(argname="argument activity_metrics", value=activity_metrics, expected_type=type_hints["activity_metrics"])
            check_type(argname="argument advanced_cost_optimization_metrics", value=advanced_cost_optimization_metrics, expected_type=type_hints["advanced_cost_optimization_metrics"])
            check_type(argname="argument advanced_data_protection_metrics", value=advanced_data_protection_metrics, expected_type=type_hints["advanced_data_protection_metrics"])
            check_type(argname="argument detailed_status_code_metrics", value=detailed_status_code_metrics, expected_type=type_hints["detailed_status_code_metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_level": bucket_level,
        }
        if activity_metrics is not None:
            self._values["activity_metrics"] = activity_metrics
        if advanced_cost_optimization_metrics is not None:
            self._values["advanced_cost_optimization_metrics"] = advanced_cost_optimization_metrics
        if advanced_data_protection_metrics is not None:
            self._values["advanced_data_protection_metrics"] = advanced_data_protection_metrics
        if detailed_status_code_metrics is not None:
            self._values["detailed_status_code_metrics"] = detailed_status_code_metrics

    @builtins.property
    def bucket_level(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel":
        '''bucket_level block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#bucket_level S3ControlStorageLensConfiguration#bucket_level}
        '''
        result = self._values.get("bucket_level")
        assert result is not None, "Required property 'bucket_level' is missing"
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel", result)

    @builtins.property
    def activity_metrics(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics"]:
        '''activity_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#activity_metrics S3ControlStorageLensConfiguration#activity_metrics}
        '''
        result = self._values.get("activity_metrics")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics"], result)

    @builtins.property
    def advanced_cost_optimization_metrics(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics"]:
        '''advanced_cost_optimization_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_cost_optimization_metrics S3ControlStorageLensConfiguration#advanced_cost_optimization_metrics}
        '''
        result = self._values.get("advanced_cost_optimization_metrics")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics"], result)

    @builtins.property
    def advanced_data_protection_metrics(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics"]:
        '''advanced_data_protection_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_data_protection_metrics S3ControlStorageLensConfiguration#advanced_data_protection_metrics}
        '''
        result = self._values.get("advanced_data_protection_metrics")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics"], result)

    @builtins.property
    def detailed_status_code_metrics(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics"]:
        '''detailed_status_code_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#detailed_status_code_metrics S3ControlStorageLensConfiguration#detailed_status_code_metrics}
        '''
        result = self._values.get("detailed_status_code_metrics")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec824be9f29b626667812dc2c89fda39e1fb759ded0a05d77b8452c2f771eb18)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a844bddda86820d5f1edce0033b3b42b0a6c798f28b942c8d1102c8010fae9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fd98ca39b83628d6ff99b22976db3c6c91fc7c55cab7d657b667514557a4416c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1f3ad1b41fdec59f1146412aacee52bdb69271920950088fe32fc36cfa731e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046e4a8df008a2ca1fd9712c1dd7ab13f408a8f761c78d2215ca4ea9129d37e8)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__199b73085a5412c828d200a54b4065646c8570c2948dddb82ed301204b4b6992)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ce07736026c05e609b4af3d1770cb5c28a67ef8a7ed4ff4cb15d810185c6552a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11269f5d6317b5d01baf6509d3f0520bf3a615c07ed1b05e129819a884d6e00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba195e1d48477c31c7eba44dc70e1bd3f172fcbf30e174c701a62285f4ffa7e)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ae1d0f52ea44eb25da3a2a8b1258098b87e037d658a91054736ffa2a0497f18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ca87b8888c01afe05e1f23dd1f36ef01b5d24ca800bf6bee7a036a05b2265f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d0d1ade2032f778b30d80ea4f657717f65a6c52b74bcc5095c038913b6debf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel",
    jsii_struct_bases=[],
    name_mapping={
        "activity_metrics": "activityMetrics",
        "advanced_cost_optimization_metrics": "advancedCostOptimizationMetrics",
        "advanced_data_protection_metrics": "advancedDataProtectionMetrics",
        "detailed_status_code_metrics": "detailedStatusCodeMetrics",
        "prefix_level": "prefixLevel",
    },
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel:
    def __init__(
        self,
        *,
        activity_metrics: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_cost_optimization_metrics: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_data_protection_metrics: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        detailed_status_code_metrics: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix_level: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param activity_metrics: activity_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#activity_metrics S3ControlStorageLensConfiguration#activity_metrics}
        :param advanced_cost_optimization_metrics: advanced_cost_optimization_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_cost_optimization_metrics S3ControlStorageLensConfiguration#advanced_cost_optimization_metrics}
        :param advanced_data_protection_metrics: advanced_data_protection_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_data_protection_metrics S3ControlStorageLensConfiguration#advanced_data_protection_metrics}
        :param detailed_status_code_metrics: detailed_status_code_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#detailed_status_code_metrics S3ControlStorageLensConfiguration#detailed_status_code_metrics}
        :param prefix_level: prefix_level block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#prefix_level S3ControlStorageLensConfiguration#prefix_level}
        '''
        if isinstance(activity_metrics, dict):
            activity_metrics = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics(**activity_metrics)
        if isinstance(advanced_cost_optimization_metrics, dict):
            advanced_cost_optimization_metrics = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics(**advanced_cost_optimization_metrics)
        if isinstance(advanced_data_protection_metrics, dict):
            advanced_data_protection_metrics = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics(**advanced_data_protection_metrics)
        if isinstance(detailed_status_code_metrics, dict):
            detailed_status_code_metrics = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics(**detailed_status_code_metrics)
        if isinstance(prefix_level, dict):
            prefix_level = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel(**prefix_level)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42eb4403cb67b3e30a7eafac1e34ffa68d39510aacf3c9496e0d5fe69bd2aec2)
            check_type(argname="argument activity_metrics", value=activity_metrics, expected_type=type_hints["activity_metrics"])
            check_type(argname="argument advanced_cost_optimization_metrics", value=advanced_cost_optimization_metrics, expected_type=type_hints["advanced_cost_optimization_metrics"])
            check_type(argname="argument advanced_data_protection_metrics", value=advanced_data_protection_metrics, expected_type=type_hints["advanced_data_protection_metrics"])
            check_type(argname="argument detailed_status_code_metrics", value=detailed_status_code_metrics, expected_type=type_hints["detailed_status_code_metrics"])
            check_type(argname="argument prefix_level", value=prefix_level, expected_type=type_hints["prefix_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if activity_metrics is not None:
            self._values["activity_metrics"] = activity_metrics
        if advanced_cost_optimization_metrics is not None:
            self._values["advanced_cost_optimization_metrics"] = advanced_cost_optimization_metrics
        if advanced_data_protection_metrics is not None:
            self._values["advanced_data_protection_metrics"] = advanced_data_protection_metrics
        if detailed_status_code_metrics is not None:
            self._values["detailed_status_code_metrics"] = detailed_status_code_metrics
        if prefix_level is not None:
            self._values["prefix_level"] = prefix_level

    @builtins.property
    def activity_metrics(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics"]:
        '''activity_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#activity_metrics S3ControlStorageLensConfiguration#activity_metrics}
        '''
        result = self._values.get("activity_metrics")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics"], result)

    @builtins.property
    def advanced_cost_optimization_metrics(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics"]:
        '''advanced_cost_optimization_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_cost_optimization_metrics S3ControlStorageLensConfiguration#advanced_cost_optimization_metrics}
        '''
        result = self._values.get("advanced_cost_optimization_metrics")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics"], result)

    @builtins.property
    def advanced_data_protection_metrics(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics"]:
        '''advanced_data_protection_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_data_protection_metrics S3ControlStorageLensConfiguration#advanced_data_protection_metrics}
        '''
        result = self._values.get("advanced_data_protection_metrics")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics"], result)

    @builtins.property
    def detailed_status_code_metrics(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics"]:
        '''detailed_status_code_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#detailed_status_code_metrics S3ControlStorageLensConfiguration#detailed_status_code_metrics}
        '''
        result = self._values.get("detailed_status_code_metrics")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics"], result)

    @builtins.property
    def prefix_level(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel"]:
        '''prefix_level block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#prefix_level S3ControlStorageLensConfiguration#prefix_level}
        '''
        result = self._values.get("prefix_level")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f138c23115cbfb9f46a675516be9c7a54fbe99e14057ccbbe6ab62c2794ecc42)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db665f90d0a48a9bebb8e2d32656a4b7842a7ab638de72f9910ce0d03d3d7aeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b7f1e28bb62ecd9063cab589e4bebcf66990db7ec9a17c526decf919733ed362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1048467cad80af2ed72a86d3af09906514be045cf83139dad7e3f00f4c080ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd398a1f61a22c335979e53cfac25a0ecadf2f4fcfe86ae893bf6dc41846a1d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61ec8241385c4395377601a65f07c3f924953fab3c2d59765793b8a8416a6074)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__946d9ca875c9c4f9c523c2ebe5ee6fd53c0d7a92d0bfa96feeb42b9bfdb4c72d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7d9044279f781977d99ac0f92681e006a42de84557f1e7e8083598e4c83d94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a951eca099369c4b6531461531200d3aa4caf57ac4a66a6d7d8058bffc65a2c)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26d0d21c875441eb1fd6389f9ac801ff7a5257588330d0428681dc4a0c3630af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2b90f328c146c9ed7dec988e8fe291170bc082306554102bae7dfe316958bf65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9324fabd8568d931c0d11827c95cfeb630a87ac5b6c7fa27965faf143be789c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b1f3d8126f3fc40c2aee61b106da1e829c1fbaeb89a75aab0389935781b531)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8338128bf1b5272841486f34ac3bea49f4897f05a6dfaa74bccfa5c32dc76bec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b55af963fcb592e3ddf0b191f5444e27bdc8e6f912159a82e10f3c59725d76d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1febf6dddf1bd90b988b9e72d64eec802e3f50d980a4446ea3fa2a6fc449a9a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a101075f84ee8c1aface629958264f05d722ac17657d8aa42611e903a8988ac7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActivityMetrics")
    def put_activity_metrics(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putActivityMetrics", [value]))

    @jsii.member(jsii_name="putAdvancedCostOptimizationMetrics")
    def put_advanced_cost_optimization_metrics(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedCostOptimizationMetrics", [value]))

    @jsii.member(jsii_name="putAdvancedDataProtectionMetrics")
    def put_advanced_data_protection_metrics(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedDataProtectionMetrics", [value]))

    @jsii.member(jsii_name="putDetailedStatusCodeMetrics")
    def put_detailed_status_code_metrics(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putDetailedStatusCodeMetrics", [value]))

    @jsii.member(jsii_name="putPrefixLevel")
    def put_prefix_level(
        self,
        *,
        storage_metrics: typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param storage_metrics: storage_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#storage_metrics S3ControlStorageLensConfiguration#storage_metrics}
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel(
            storage_metrics=storage_metrics
        )

        return typing.cast(None, jsii.invoke(self, "putPrefixLevel", [value]))

    @jsii.member(jsii_name="resetActivityMetrics")
    def reset_activity_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivityMetrics", []))

    @jsii.member(jsii_name="resetAdvancedCostOptimizationMetrics")
    def reset_advanced_cost_optimization_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedCostOptimizationMetrics", []))

    @jsii.member(jsii_name="resetAdvancedDataProtectionMetrics")
    def reset_advanced_data_protection_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedDataProtectionMetrics", []))

    @jsii.member(jsii_name="resetDetailedStatusCodeMetrics")
    def reset_detailed_status_code_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetailedStatusCodeMetrics", []))

    @jsii.member(jsii_name="resetPrefixLevel")
    def reset_prefix_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixLevel", []))

    @builtins.property
    @jsii.member(jsii_name="activityMetrics")
    def activity_metrics(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetricsOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetricsOutputReference, jsii.get(self, "activityMetrics"))

    @builtins.property
    @jsii.member(jsii_name="advancedCostOptimizationMetrics")
    def advanced_cost_optimization_metrics(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetricsOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetricsOutputReference, jsii.get(self, "advancedCostOptimizationMetrics"))

    @builtins.property
    @jsii.member(jsii_name="advancedDataProtectionMetrics")
    def advanced_data_protection_metrics(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetricsOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetricsOutputReference, jsii.get(self, "advancedDataProtectionMetrics"))

    @builtins.property
    @jsii.member(jsii_name="detailedStatusCodeMetrics")
    def detailed_status_code_metrics(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetricsOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetricsOutputReference, jsii.get(self, "detailedStatusCodeMetrics"))

    @builtins.property
    @jsii.member(jsii_name="prefixLevel")
    def prefix_level(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelOutputReference":
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelOutputReference", jsii.get(self, "prefixLevel"))

    @builtins.property
    @jsii.member(jsii_name="activityMetricsInput")
    def activity_metrics_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics], jsii.get(self, "activityMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedCostOptimizationMetricsInput")
    def advanced_cost_optimization_metrics_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics], jsii.get(self, "advancedCostOptimizationMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedDataProtectionMetricsInput")
    def advanced_data_protection_metrics_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics], jsii.get(self, "advancedDataProtectionMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="detailedStatusCodeMetricsInput")
    def detailed_status_code_metrics_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics], jsii.get(self, "detailedStatusCodeMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixLevelInput")
    def prefix_level_input(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel"]:
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel"], jsii.get(self, "prefixLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d62cfbc3b0fc4e48439e03c673b14b0ad17105395f3bdba9c4a49674dca580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel",
    jsii_struct_bases=[],
    name_mapping={"storage_metrics": "storageMetrics"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel:
    def __init__(
        self,
        *,
        storage_metrics: typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param storage_metrics: storage_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#storage_metrics S3ControlStorageLensConfiguration#storage_metrics}
        '''
        if isinstance(storage_metrics, dict):
            storage_metrics = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics(**storage_metrics)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a12dd93b5bc71f00c67d4d49081e490f967c4ea0df9d5738a1ba346c4a16b818)
            check_type(argname="argument storage_metrics", value=storage_metrics, expected_type=type_hints["storage_metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_metrics": storage_metrics,
        }

    @builtins.property
    def storage_metrics(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics":
        '''storage_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#storage_metrics S3ControlStorageLensConfiguration#storage_metrics}
        '''
        result = self._values.get("storage_metrics")
        assert result is not None, "Required property 'storage_metrics' is missing"
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__969bc60c36061384bc9b39b33b407c5eeda82a6eeda48a7817e2df5c95258271)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStorageMetrics")
    def put_storage_metrics(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selection_criteria: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        :param selection_criteria: selection_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#selection_criteria S3ControlStorageLensConfiguration#selection_criteria}
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics(
            enabled=enabled, selection_criteria=selection_criteria
        )

        return typing.cast(None, jsii.invoke(self, "putStorageMetrics", [value]))

    @builtins.property
    @jsii.member(jsii_name="storageMetrics")
    def storage_metrics(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsOutputReference":
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsOutputReference", jsii.get(self, "storageMetrics"))

    @builtins.property
    @jsii.member(jsii_name="storageMetricsInput")
    def storage_metrics_input(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics"]:
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics"], jsii.get(self, "storageMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9722e347485b4084d18e58088edff4a7bb807d71e6729e2bac3efcf16af111f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "selection_criteria": "selectionCriteria"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selection_criteria: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        :param selection_criteria: selection_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#selection_criteria S3ControlStorageLensConfiguration#selection_criteria}
        '''
        if isinstance(selection_criteria, dict):
            selection_criteria = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria(**selection_criteria)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a47bb3e4e39df8b8a4f5cba947af543adc4bad2765d70291acbcfab844ea08)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument selection_criteria", value=selection_criteria, expected_type=type_hints["selection_criteria"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if selection_criteria is not None:
            self._values["selection_criteria"] = selection_criteria

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def selection_criteria(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria"]:
        '''selection_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#selection_criteria S3ControlStorageLensConfiguration#selection_criteria}
        '''
        result = self._values.get("selection_criteria")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32de3286b8201d5753054df819381b25f1b040cdcfdcaa86fba74dba69ed6fcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelectionCriteria")
    def put_selection_criteria(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        max_depth: typing.Optional[jsii.Number] = None,
        min_storage_bytes_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#delimiter S3ControlStorageLensConfiguration#delimiter}.
        :param max_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#max_depth S3ControlStorageLensConfiguration#max_depth}.
        :param min_storage_bytes_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#min_storage_bytes_percentage S3ControlStorageLensConfiguration#min_storage_bytes_percentage}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria(
            delimiter=delimiter,
            max_depth=max_depth,
            min_storage_bytes_percentage=min_storage_bytes_percentage,
        )

        return typing.cast(None, jsii.invoke(self, "putSelectionCriteria", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetSelectionCriteria")
    def reset_selection_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectionCriteria", []))

    @builtins.property
    @jsii.member(jsii_name="selectionCriteria")
    def selection_criteria(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteriaOutputReference":
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteriaOutputReference", jsii.get(self, "selectionCriteria"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="selectionCriteriaInput")
    def selection_criteria_input(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria"]:
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria"], jsii.get(self, "selectionCriteriaInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__db5f26b36131ac90d3dc790604e618181a78e18b6b3f9249e2fde27f9ff29eab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab6745aa8ad302bd2a5b1d7a4a7da04cfa6ad0a585986faf80b685b67b44a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "delimiter": "delimiter",
        "max_depth": "maxDepth",
        "min_storage_bytes_percentage": "minStorageBytesPercentage",
    },
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria:
    def __init__(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        max_depth: typing.Optional[jsii.Number] = None,
        min_storage_bytes_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#delimiter S3ControlStorageLensConfiguration#delimiter}.
        :param max_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#max_depth S3ControlStorageLensConfiguration#max_depth}.
        :param min_storage_bytes_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#min_storage_bytes_percentage S3ControlStorageLensConfiguration#min_storage_bytes_percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e5a1cf1ce5973ed3457157b7fcaefbbc77eba7a4ddcbe89a2d127d55a75e80)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument max_depth", value=max_depth, expected_type=type_hints["max_depth"])
            check_type(argname="argument min_storage_bytes_percentage", value=min_storage_bytes_percentage, expected_type=type_hints["min_storage_bytes_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if max_depth is not None:
            self._values["max_depth"] = max_depth
        if min_storage_bytes_percentage is not None:
            self._values["min_storage_bytes_percentage"] = min_storage_bytes_percentage

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#delimiter S3ControlStorageLensConfiguration#delimiter}.'''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_depth(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#max_depth S3ControlStorageLensConfiguration#max_depth}.'''
        result = self._values.get("max_depth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_storage_bytes_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#min_storage_bytes_percentage S3ControlStorageLensConfiguration#min_storage_bytes_percentage}.'''
        result = self._values.get("min_storage_bytes_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d650c2801d3c650a1b9d4df7ba51af208d6759dcd54de8a8c68219d8978b9e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelimiter")
    def reset_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelimiter", []))

    @jsii.member(jsii_name="resetMaxDepth")
    def reset_max_depth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDepth", []))

    @jsii.member(jsii_name="resetMinStorageBytesPercentage")
    def reset_min_storage_bytes_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinStorageBytesPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDepthInput")
    def max_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="minStorageBytesPercentageInput")
    def min_storage_bytes_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minStorageBytesPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02909aaa3b5241e2d0ef58f4aaa325a1023bdbba7710dc1adb9e3c631215a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDepth")
    def max_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDepth"))

    @max_depth.setter
    def max_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7bd51d062ca595ed6b90384c37fdb4866dc823ca080b35cfa4ed3010c80da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minStorageBytesPercentage")
    def min_storage_bytes_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minStorageBytesPercentage"))

    @min_storage_bytes_percentage.setter
    def min_storage_bytes_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c4db21dc0dc0ad002bd4c50990fba2869ac1ee8f7fa42dbc2df9de92bfd196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minStorageBytesPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af54426dcd75a31dd0ad4d6626711ebb15db798ae7fe2879ffd0d268f413254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80280c5a2665e01a46b050a5589535b6093ecb2132444f671d99ad9e2189b2b2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c146caeb1b94907fd0ee10d7c8e44b9eadf9e839e27e07e703a7e31ca483592)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e3900b9d0a2464c60e74fe1e2cc96e903c213080bd836bdc17f0eca7d60d91ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddfd5d5161b70a7065080f33e1b90a5b4a7424872a623759942b06cc71aeb7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a785a4123555f1cc145aec594ec3975a502b8ebe72945e490c0f2c5769f20b25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActivityMetrics")
    def put_activity_metrics(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putActivityMetrics", [value]))

    @jsii.member(jsii_name="putAdvancedCostOptimizationMetrics")
    def put_advanced_cost_optimization_metrics(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedCostOptimizationMetrics", [value]))

    @jsii.member(jsii_name="putAdvancedDataProtectionMetrics")
    def put_advanced_data_protection_metrics(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedDataProtectionMetrics", [value]))

    @jsii.member(jsii_name="putBucketLevel")
    def put_bucket_level(
        self,
        *,
        activity_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_cost_optimization_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_data_protection_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
        detailed_status_code_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
        prefix_level: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param activity_metrics: activity_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#activity_metrics S3ControlStorageLensConfiguration#activity_metrics}
        :param advanced_cost_optimization_metrics: advanced_cost_optimization_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_cost_optimization_metrics S3ControlStorageLensConfiguration#advanced_cost_optimization_metrics}
        :param advanced_data_protection_metrics: advanced_data_protection_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_data_protection_metrics S3ControlStorageLensConfiguration#advanced_data_protection_metrics}
        :param detailed_status_code_metrics: detailed_status_code_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#detailed_status_code_metrics S3ControlStorageLensConfiguration#detailed_status_code_metrics}
        :param prefix_level: prefix_level block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#prefix_level S3ControlStorageLensConfiguration#prefix_level}
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel(
            activity_metrics=activity_metrics,
            advanced_cost_optimization_metrics=advanced_cost_optimization_metrics,
            advanced_data_protection_metrics=advanced_data_protection_metrics,
            detailed_status_code_metrics=detailed_status_code_metrics,
            prefix_level=prefix_level,
        )

        return typing.cast(None, jsii.invoke(self, "putBucketLevel", [value]))

    @jsii.member(jsii_name="putDetailedStatusCodeMetrics")
    def put_detailed_status_code_metrics(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putDetailedStatusCodeMetrics", [value]))

    @jsii.member(jsii_name="resetActivityMetrics")
    def reset_activity_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivityMetrics", []))

    @jsii.member(jsii_name="resetAdvancedCostOptimizationMetrics")
    def reset_advanced_cost_optimization_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedCostOptimizationMetrics", []))

    @jsii.member(jsii_name="resetAdvancedDataProtectionMetrics")
    def reset_advanced_data_protection_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedDataProtectionMetrics", []))

    @jsii.member(jsii_name="resetDetailedStatusCodeMetrics")
    def reset_detailed_status_code_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetailedStatusCodeMetrics", []))

    @builtins.property
    @jsii.member(jsii_name="activityMetrics")
    def activity_metrics(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetricsOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetricsOutputReference, jsii.get(self, "activityMetrics"))

    @builtins.property
    @jsii.member(jsii_name="advancedCostOptimizationMetrics")
    def advanced_cost_optimization_metrics(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetricsOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetricsOutputReference, jsii.get(self, "advancedCostOptimizationMetrics"))

    @builtins.property
    @jsii.member(jsii_name="advancedDataProtectionMetrics")
    def advanced_data_protection_metrics(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetricsOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetricsOutputReference, jsii.get(self, "advancedDataProtectionMetrics"))

    @builtins.property
    @jsii.member(jsii_name="bucketLevel")
    def bucket_level(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelOutputReference, jsii.get(self, "bucketLevel"))

    @builtins.property
    @jsii.member(jsii_name="detailedStatusCodeMetrics")
    def detailed_status_code_metrics(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetricsOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetricsOutputReference, jsii.get(self, "detailedStatusCodeMetrics"))

    @builtins.property
    @jsii.member(jsii_name="activityMetricsInput")
    def activity_metrics_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics], jsii.get(self, "activityMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedCostOptimizationMetricsInput")
    def advanced_cost_optimization_metrics_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics], jsii.get(self, "advancedCostOptimizationMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedDataProtectionMetricsInput")
    def advanced_data_protection_metrics_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics], jsii.get(self, "advancedDataProtectionMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketLevelInput")
    def bucket_level_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel], jsii.get(self, "bucketLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="detailedStatusCodeMetricsInput")
    def detailed_status_code_metrics_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics], jsii.get(self, "detailedStatusCodeMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a94c6f52ea61304956b326c2a1c8bca72fe925002d5f9c3a8f4354e1776260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg:
    def __init__(self, *, arn: builtins.str) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#arn S3ControlStorageLensConfiguration#arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395b18018166535ee3e0df723d0b0f7b6eec6138866ca7e1fc0f08e3c6a1677f)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
        }

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#arn S3ControlStorageLensConfiguration#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0286a200518c474e7e09d17f71b3d8cd1c01c50ef6c5135d214eb569b81f79f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__b521c43abbc97bb02ed3d0285ca4f247c1e48a190765801d16934ba022b529c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__950bc829fe11efcf281fba6ef82bb871a6a1bcf208b913b53e2a94a5c499e10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExport",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_watch_metrics": "cloudWatchMetrics",
        "s3_bucket_destination": "s3BucketDestination",
    },
)
class S3ControlStorageLensConfigurationStorageLensConfigurationDataExport:
    def __init__(
        self,
        *,
        cloud_watch_metrics: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_bucket_destination: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_watch_metrics: cloud_watch_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#cloud_watch_metrics S3ControlStorageLensConfiguration#cloud_watch_metrics}
        :param s3_bucket_destination: s3_bucket_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#s3_bucket_destination S3ControlStorageLensConfiguration#s3_bucket_destination}
        '''
        if isinstance(cloud_watch_metrics, dict):
            cloud_watch_metrics = S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics(**cloud_watch_metrics)
        if isinstance(s3_bucket_destination, dict):
            s3_bucket_destination = S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination(**s3_bucket_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d305cdf74115f0e41af2c28c0895113a848d12eee3c139e6090f331eb64c3761)
            check_type(argname="argument cloud_watch_metrics", value=cloud_watch_metrics, expected_type=type_hints["cloud_watch_metrics"])
            check_type(argname="argument s3_bucket_destination", value=s3_bucket_destination, expected_type=type_hints["s3_bucket_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_watch_metrics is not None:
            self._values["cloud_watch_metrics"] = cloud_watch_metrics
        if s3_bucket_destination is not None:
            self._values["s3_bucket_destination"] = s3_bucket_destination

    @builtins.property
    def cloud_watch_metrics(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics"]:
        '''cloud_watch_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#cloud_watch_metrics S3ControlStorageLensConfiguration#cloud_watch_metrics}
        '''
        result = self._values.get("cloud_watch_metrics")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics"], result)

    @builtins.property
    def s3_bucket_destination(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination"]:
        '''s3_bucket_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#s3_bucket_destination S3ControlStorageLensConfiguration#s3_bucket_destination}
        '''
        result = self._values.get("s3_bucket_destination")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationDataExport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf52a3a0e623c7fa6d11bba3feccd782a9d85f97ca82cd8475d0189b69a4ae76)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11e610fbb9e5a5c9b578ebb1636fc3b3a5c60aa27f8f206e2c728fb63f06a37a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39cfc2f50de9271711795665aa256aeca90a9de6d43a8f44ed7902b3443823c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b8372b6c124c40564292b74c17194ff894fe960112099e0c7fbc3f0cd47702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6808983bb0c60a704ed91435cc1ad28e96fd982c2cffb311bb58ce64429e3f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudWatchMetrics")
    def put_cloud_watch_metrics(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#enabled S3ControlStorageLensConfiguration#enabled}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putCloudWatchMetrics", [value]))

    @jsii.member(jsii_name="putS3BucketDestination")
    def put_s3_bucket_destination(
        self,
        *,
        account_id: builtins.str,
        arn: builtins.str,
        format: builtins.str,
        output_schema_version: builtins.str,
        encryption: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#account_id S3ControlStorageLensConfiguration#account_id}.
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#arn S3ControlStorageLensConfiguration#arn}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#format S3ControlStorageLensConfiguration#format}.
        :param output_schema_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#output_schema_version S3ControlStorageLensConfiguration#output_schema_version}.
        :param encryption: encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#encryption S3ControlStorageLensConfiguration#encryption}
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#prefix S3ControlStorageLensConfiguration#prefix}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination(
            account_id=account_id,
            arn=arn,
            format=format,
            output_schema_version=output_schema_version,
            encryption=encryption,
            prefix=prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putS3BucketDestination", [value]))

    @jsii.member(jsii_name="resetCloudWatchMetrics")
    def reset_cloud_watch_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudWatchMetrics", []))

    @jsii.member(jsii_name="resetS3BucketDestination")
    def reset_s3_bucket_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BucketDestination", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchMetrics")
    def cloud_watch_metrics(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetricsOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetricsOutputReference, jsii.get(self, "cloudWatchMetrics"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketDestination")
    def s3_bucket_destination(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationOutputReference":
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationOutputReference", jsii.get(self, "s3BucketDestination"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchMetricsInput")
    def cloud_watch_metrics_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics], jsii.get(self, "cloudWatchMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketDestinationInput")
    def s3_bucket_destination_input(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination"]:
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination"], jsii.get(self, "s3BucketDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExport]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExport],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6adaf0c0357d96fdafde789c26e61df025a8874338f4613ea19b76dfe43eacf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "arn": "arn",
        "format": "format",
        "output_schema_version": "outputSchemaVersion",
        "encryption": "encryption",
        "prefix": "prefix",
    },
)
class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        arn: builtins.str,
        format: builtins.str,
        output_schema_version: builtins.str,
        encryption: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#account_id S3ControlStorageLensConfiguration#account_id}.
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#arn S3ControlStorageLensConfiguration#arn}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#format S3ControlStorageLensConfiguration#format}.
        :param output_schema_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#output_schema_version S3ControlStorageLensConfiguration#output_schema_version}.
        :param encryption: encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#encryption S3ControlStorageLensConfiguration#encryption}
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#prefix S3ControlStorageLensConfiguration#prefix}.
        '''
        if isinstance(encryption, dict):
            encryption = S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption(**encryption)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa8c1a1f71afc2a6efcbfd6257e481828137eb627e926ed0623c4769f77b5e0)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument output_schema_version", value=output_schema_version, expected_type=type_hints["output_schema_version"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "arn": arn,
            "format": format,
            "output_schema_version": output_schema_version,
        }
        if encryption is not None:
            self._values["encryption"] = encryption
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#account_id S3ControlStorageLensConfiguration#account_id}.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#arn S3ControlStorageLensConfiguration#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#format S3ControlStorageLensConfiguration#format}.'''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_schema_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#output_schema_version S3ControlStorageLensConfiguration#output_schema_version}.'''
        result = self._values.get("output_schema_version")
        assert result is not None, "Required property 'output_schema_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption"]:
        '''encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#encryption S3ControlStorageLensConfiguration#encryption}
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption"], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#prefix S3ControlStorageLensConfiguration#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption",
    jsii_struct_bases=[],
    name_mapping={"sse_kms": "sseKms", "sse_s3": "sseS3"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption:
    def __init__(
        self,
        *,
        sse_kms: typing.Optional[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms", typing.Dict[builtins.str, typing.Any]]] = None,
        sse_s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param sse_kms: sse_kms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#sse_kms S3ControlStorageLensConfiguration#sse_kms}
        :param sse_s3: sse_s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#sse_s3 S3ControlStorageLensConfiguration#sse_s3}
        '''
        if isinstance(sse_kms, dict):
            sse_kms = S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms(**sse_kms)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc5ced2fc7b2ba7232aba8bfdf550f02e3b733c90a94673410ea89f87139bee)
            check_type(argname="argument sse_kms", value=sse_kms, expected_type=type_hints["sse_kms"])
            check_type(argname="argument sse_s3", value=sse_s3, expected_type=type_hints["sse_s3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sse_kms is not None:
            self._values["sse_kms"] = sse_kms
        if sse_s3 is not None:
            self._values["sse_s3"] = sse_s3

    @builtins.property
    def sse_kms(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms"]:
        '''sse_kms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#sse_kms S3ControlStorageLensConfiguration#sse_kms}
        '''
        result = self._values.get("sse_kms")
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms"], result)

    @builtins.property
    def sse_s3(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3"]]]:
        '''sse_s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#sse_s3 S3ControlStorageLensConfiguration#sse_s3}
        '''
        result = self._values.get("sse_s3")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__626d71cc89e2a859d2ff7119ca8c12d44666a4021ec9db5149997c9db55719da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSseKms")
    def put_sse_kms(self, *, key_id: builtins.str) -> None:
        '''
        :param key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#key_id S3ControlStorageLensConfiguration#key_id}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms(
            key_id=key_id
        )

        return typing.cast(None, jsii.invoke(self, "putSseKms", [value]))

    @jsii.member(jsii_name="putSseS3")
    def put_sse_s3(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f5d0d5adc5d287a8689ca433fba45c52de5afc8fd644d9840156053563bdb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSseS3", [value]))

    @jsii.member(jsii_name="resetSseKms")
    def reset_sse_kms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSseKms", []))

    @jsii.member(jsii_name="resetSseS3")
    def reset_sse_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSseS3", []))

    @builtins.property
    @jsii.member(jsii_name="sseKms")
    def sse_kms(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKmsOutputReference":
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKmsOutputReference", jsii.get(self, "sseKms"))

    @builtins.property
    @jsii.member(jsii_name="sseS3")
    def sse_s3(
        self,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3List":
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3List", jsii.get(self, "sseS3"))

    @builtins.property
    @jsii.member(jsii_name="sseKmsInput")
    def sse_kms_input(
        self,
    ) -> typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms"]:
        return typing.cast(typing.Optional["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms"], jsii.get(self, "sseKmsInput"))

    @builtins.property
    @jsii.member(jsii_name="sseS3Input")
    def sse_s3_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3"]]], jsii.get(self, "sseS3Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89559f8402347902ca6db6eea5f10dcc91f51fc8103a3fa23af76f724a29e258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms",
    jsii_struct_bases=[],
    name_mapping={"key_id": "keyId"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms:
    def __init__(self, *, key_id: builtins.str) -> None:
        '''
        :param key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#key_id S3ControlStorageLensConfiguration#key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1e0cea7def5f2b2c1f5dfcf31a7e1041aea9c82780056fa4425dc8394a4fdc1)
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_id": key_id,
        }

    @builtins.property
    def key_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#key_id S3ControlStorageLensConfiguration#key_id}.'''
        result = self._values.get("key_id")
        assert result is not None, "Required property 'key_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKmsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKmsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bbe895744381fcdc0aca8188ed206d7fd54e2d3ca1b62a45dc4cbfbb2fa2264)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyIdInput")
    def key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @key_id.setter
    def key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02f5c768b3558162f144f1d3dd514fdd39208cff6cea4e18896bf0281a5bdc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd6cf618830ab8b215e7f3d4f194ed8f48a74c0343379c3d703b6b515b068b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3",
    jsii_struct_bases=[],
    name_mapping={},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9556bef73608ea3844f9a13aa32d7b7ae29be3fada685b627689f6ba90032a84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cadc71740d23496966317e6b3843b98743ce1eecc1e96916fdd4bee1a4a131c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55755a0405f6b1827deb9742085d459e97b37b48441bd4f3ea5221653ab982fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa03a644f64c0c8608452b43a51491776ddfc336dcc6451ba846e981f4da16af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e3596b5f6eb8beb4ddec251579080869431d3218de82a20eeacc1f3060127a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d97afcb9271d10ead5a2eddd809a7c82bbd11e5794be19b5b9187a106688ddfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__905dfd645ba94e84b8bc5938f3f90ada4062b7fa355091929fe6de4362bdf365)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0cd2e914110a76cf179514234c247957d551c26b862ae71e040709c06009b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__444bd27a0c42db4f9d77956bfd073cdf7fc6565bfd69ede77988acef0abd3d26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEncryption")
    def put_encryption(
        self,
        *,
        sse_kms: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms, typing.Dict[builtins.str, typing.Any]]] = None,
        sse_s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param sse_kms: sse_kms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#sse_kms S3ControlStorageLensConfiguration#sse_kms}
        :param sse_s3: sse_s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#sse_s3 S3ControlStorageLensConfiguration#sse_s3}
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption(
            sse_kms=sse_kms, sse_s3=sse_s3
        )

        return typing.cast(None, jsii.invoke(self, "putEncryption", [value]))

    @jsii.member(jsii_name="resetEncryption")
    def reset_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryption", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionOutputReference, jsii.get(self, "encryption"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInput")
    def encryption_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption], jsii.get(self, "encryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="outputSchemaVersionInput")
    def output_schema_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputSchemaVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d19b182240e6413446c71f6d3cd1a373283a78ee535cd4c16f90d82adbfb1a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2881da7d0576881a681df8443942f2499b53be6a48fea15ad4ec8dad7593789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85510f6742429d90ed120d5867eb6f38de193c9e17446d616036ace8eaea7e9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputSchemaVersion")
    def output_schema_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputSchemaVersion"))

    @output_schema_version.setter
    def output_schema_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5984f8c3e126bcf444454905f3ba14f8c95cd3334f590367286f77fe08d2f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputSchemaVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4f27d6006e70e27452434b3689371f9c1c2dac081af37b20c17114ee4b7119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0991bff9db0dcae0cc7f6b1b868b9ddf6ed3621b7ea4db7dc551883b5e64c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationExclude",
    jsii_struct_bases=[],
    name_mapping={"buckets": "buckets", "regions": "regions"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationExclude:
    def __init__(
        self,
        *,
        buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param buckets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#buckets S3ControlStorageLensConfiguration#buckets}.
        :param regions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#regions S3ControlStorageLensConfiguration#regions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12434079cdc92411072fa15e1c9830ff3c26fa4049136d03fbef27039b3b20d5)
            check_type(argname="argument buckets", value=buckets, expected_type=type_hints["buckets"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if buckets is not None:
            self._values["buckets"] = buckets
        if regions is not None:
            self._values["regions"] = regions

    @builtins.property
    def buckets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#buckets S3ControlStorageLensConfiguration#buckets}.'''
        result = self._values.get("buckets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#regions S3ControlStorageLensConfiguration#regions}.'''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationExclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationExcludeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationExcludeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1ca3bb339a98cdbd1eba71cfa8898fe334f2c509bf54cc8d58f73278f4bd28a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBuckets")
    def reset_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuckets", []))

    @jsii.member(jsii_name="resetRegions")
    def reset_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegions", []))

    @builtins.property
    @jsii.member(jsii_name="bucketsInput")
    def buckets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionsInput")
    def regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "regionsInput"))

    @builtins.property
    @jsii.member(jsii_name="buckets")
    def buckets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "buckets"))

    @buckets.setter
    def buckets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea00750469e9164b3dbf586df0ecfb7c5770153fc32fe130fe7a60575aa8cf16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regions")
    def regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regions"))

    @regions.setter
    def regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10e4199c9380d54ee132d77f60b13e811b879d248ae2cbacccc3c1b5e2459d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationExclude]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationExclude], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationExclude],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cde63f706324dba62a070bb0d56de2c5130db4252c1927d2d101ededb533ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationInclude",
    jsii_struct_bases=[],
    name_mapping={"buckets": "buckets", "regions": "regions"},
)
class S3ControlStorageLensConfigurationStorageLensConfigurationInclude:
    def __init__(
        self,
        *,
        buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param buckets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#buckets S3ControlStorageLensConfiguration#buckets}.
        :param regions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#regions S3ControlStorageLensConfiguration#regions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1289900ce22fcd7c69e61530063476b18e0190353af8a81a16a722572666a0fd)
            check_type(argname="argument buckets", value=buckets, expected_type=type_hints["buckets"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if buckets is not None:
            self._values["buckets"] = buckets
        if regions is not None:
            self._values["regions"] = regions

    @builtins.property
    def buckets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#buckets S3ControlStorageLensConfiguration#buckets}.'''
        result = self._values.get("buckets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#regions S3ControlStorageLensConfiguration#regions}.'''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ControlStorageLensConfigurationStorageLensConfigurationInclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ControlStorageLensConfigurationStorageLensConfigurationIncludeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationIncludeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55064e996a6f3da8328d1a15b1f18ea2d9e0ffa0650cd03f6ba1eb92ad3e22d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBuckets")
    def reset_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuckets", []))

    @jsii.member(jsii_name="resetRegions")
    def reset_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegions", []))

    @builtins.property
    @jsii.member(jsii_name="bucketsInput")
    def buckets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionsInput")
    def regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "regionsInput"))

    @builtins.property
    @jsii.member(jsii_name="buckets")
    def buckets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "buckets"))

    @buckets.setter
    def buckets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b0165678fd1730d6dc06cd11a2eac9942bf105b7f365150ed6f19cd8d3f856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regions")
    def regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regions"))

    @regions.setter
    def regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e03b03c0c91d1b69d64d4d0ced909a399a5390e9eb64651501493b6c0bace895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationInclude]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationInclude], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationInclude],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573b943ebd1565c42455aa527ddb26aad2cac3ad8881e519a146e38a49781c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3ControlStorageLensConfigurationStorageLensConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.s3ControlStorageLensConfiguration.S3ControlStorageLensConfigurationStorageLensConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a0321b5ac6a97588dbba10272cd1e087804679787a875068c4a7b7840cd0902)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccountLevel")
    def put_account_level(
        self,
        *,
        bucket_level: typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel, typing.Dict[builtins.str, typing.Any]],
        activity_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_cost_optimization_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_data_protection_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
        detailed_status_code_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_level: bucket_level block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#bucket_level S3ControlStorageLensConfiguration#bucket_level}
        :param activity_metrics: activity_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#activity_metrics S3ControlStorageLensConfiguration#activity_metrics}
        :param advanced_cost_optimization_metrics: advanced_cost_optimization_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_cost_optimization_metrics S3ControlStorageLensConfiguration#advanced_cost_optimization_metrics}
        :param advanced_data_protection_metrics: advanced_data_protection_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#advanced_data_protection_metrics S3ControlStorageLensConfiguration#advanced_data_protection_metrics}
        :param detailed_status_code_metrics: detailed_status_code_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#detailed_status_code_metrics S3ControlStorageLensConfiguration#detailed_status_code_metrics}
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel(
            bucket_level=bucket_level,
            activity_metrics=activity_metrics,
            advanced_cost_optimization_metrics=advanced_cost_optimization_metrics,
            advanced_data_protection_metrics=advanced_data_protection_metrics,
            detailed_status_code_metrics=detailed_status_code_metrics,
        )

        return typing.cast(None, jsii.invoke(self, "putAccountLevel", [value]))

    @jsii.member(jsii_name="putAwsOrg")
    def put_aws_org(self, *, arn: builtins.str) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#arn S3ControlStorageLensConfiguration#arn}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg(
            arn=arn
        )

        return typing.cast(None, jsii.invoke(self, "putAwsOrg", [value]))

    @jsii.member(jsii_name="putDataExport")
    def put_data_export(
        self,
        *,
        cloud_watch_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_bucket_destination: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_watch_metrics: cloud_watch_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#cloud_watch_metrics S3ControlStorageLensConfiguration#cloud_watch_metrics}
        :param s3_bucket_destination: s3_bucket_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#s3_bucket_destination S3ControlStorageLensConfiguration#s3_bucket_destination}
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationDataExport(
            cloud_watch_metrics=cloud_watch_metrics,
            s3_bucket_destination=s3_bucket_destination,
        )

        return typing.cast(None, jsii.invoke(self, "putDataExport", [value]))

    @jsii.member(jsii_name="putExclude")
    def put_exclude(
        self,
        *,
        buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param buckets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#buckets S3ControlStorageLensConfiguration#buckets}.
        :param regions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#regions S3ControlStorageLensConfiguration#regions}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationExclude(
            buckets=buckets, regions=regions
        )

        return typing.cast(None, jsii.invoke(self, "putExclude", [value]))

    @jsii.member(jsii_name="putInclude")
    def put_include(
        self,
        *,
        buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param buckets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#buckets S3ControlStorageLensConfiguration#buckets}.
        :param regions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/s3control_storage_lens_configuration#regions S3ControlStorageLensConfiguration#regions}.
        '''
        value = S3ControlStorageLensConfigurationStorageLensConfigurationInclude(
            buckets=buckets, regions=regions
        )

        return typing.cast(None, jsii.invoke(self, "putInclude", [value]))

    @jsii.member(jsii_name="resetAwsOrg")
    def reset_aws_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsOrg", []))

    @jsii.member(jsii_name="resetDataExport")
    def reset_data_export(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataExport", []))

    @jsii.member(jsii_name="resetExclude")
    def reset_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclude", []))

    @jsii.member(jsii_name="resetInclude")
    def reset_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInclude", []))

    @builtins.property
    @jsii.member(jsii_name="accountLevel")
    def account_level(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelOutputReference, jsii.get(self, "accountLevel"))

    @builtins.property
    @jsii.member(jsii_name="awsOrg")
    def aws_org(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrgOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrgOutputReference, jsii.get(self, "awsOrg"))

    @builtins.property
    @jsii.member(jsii_name="dataExport")
    def data_export(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationDataExportOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationDataExportOutputReference, jsii.get(self, "dataExport"))

    @builtins.property
    @jsii.member(jsii_name="exclude")
    def exclude(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationExcludeOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationExcludeOutputReference, jsii.get(self, "exclude"))

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(
        self,
    ) -> S3ControlStorageLensConfigurationStorageLensConfigurationIncludeOutputReference:
        return typing.cast(S3ControlStorageLensConfigurationStorageLensConfigurationIncludeOutputReference, jsii.get(self, "include"))

    @builtins.property
    @jsii.member(jsii_name="accountLevelInput")
    def account_level_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel], jsii.get(self, "accountLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="awsOrgInput")
    def aws_org_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg], jsii.get(self, "awsOrgInput"))

    @builtins.property
    @jsii.member(jsii_name="dataExportInput")
    def data_export_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExport]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExport], jsii.get(self, "dataExportInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeInput")
    def exclude_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationExclude]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationExclude], jsii.get(self, "excludeInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInput")
    def include_input(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationInclude]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationInclude], jsii.get(self, "includeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fa687f4ec53f1006698eb6388500cf8d57b7f1e1d337194576d0625e57c303db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[S3ControlStorageLensConfigurationStorageLensConfiguration]:
        return typing.cast(typing.Optional[S3ControlStorageLensConfigurationStorageLensConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ad058ac765c19bd7cb7d7939ffc997653e6074478cd5401415c871a88f568b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "S3ControlStorageLensConfiguration",
    "S3ControlStorageLensConfigurationConfig",
    "S3ControlStorageLensConfigurationStorageLensConfiguration",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetricsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetricsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetricsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetricsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetricsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetricsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetricsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteriaOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetricsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg",
    "S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrgOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExport",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetricsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKmsOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3List",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3OutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationExclude",
    "S3ControlStorageLensConfigurationStorageLensConfigurationExcludeOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationInclude",
    "S3ControlStorageLensConfigurationStorageLensConfigurationIncludeOutputReference",
    "S3ControlStorageLensConfigurationStorageLensConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__ea9449b99e88b68ec964d3d3769908d24e51705966e9426294a0f05b17f41687(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    config_id: builtins.str,
    storage_lens_configuration: typing.Union[S3ControlStorageLensConfigurationStorageLensConfiguration, typing.Dict[builtins.str, typing.Any]],
    account_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__357721cfcbdf1c2cabd127d0b6a4479ffc04555d3dc17502a9ef7d80c5d6e489(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbb608588f50e1b4ea1c591acb9da3bb6758ee8e4492f221a5c117d240850fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2e38ec5957ee5de12cb3f7887e851b9c083275c4b81f59952ea1fe95114f9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dc71d3bcbc78ce9b1d3a001afb2dfeb3f9a6de18b08d1edf55192c0b372247(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b042f77c7c49188439f47a291f173f67831e0ad9a1d8a21fe7dab27c3e85b04a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d5568d3d0e7e156d84ddfbff0eea1a6af265cd088b8b9ffb2afbe400451278(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885fb334e39fb7620884bf2ae6d705a74938194c7bfdfe124abc273b0659ce42(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4d6172c6d3d93d5e199470ac0346f264bde66c5afbd77466d54b2db076aff8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_id: builtins.str,
    storage_lens_configuration: typing.Union[S3ControlStorageLensConfigurationStorageLensConfiguration, typing.Dict[builtins.str, typing.Any]],
    account_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97c89204c3f27c900c9d43735415c75d48cf40866b1e93bdfaa8199dfd9f34d(
    *,
    account_level: typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    aws_org: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg, typing.Dict[builtins.str, typing.Any]]] = None,
    data_export: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExport, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationExclude, typing.Dict[builtins.str, typing.Any]]] = None,
    include: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationInclude, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c724aeb900590fa4dff1969d619abbea63c44130e30901a38ea68a86905fa82(
    *,
    bucket_level: typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel, typing.Dict[builtins.str, typing.Any]],
    activity_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_cost_optimization_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_data_protection_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    detailed_status_code_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec824be9f29b626667812dc2c89fda39e1fb759ded0a05d77b8452c2f771eb18(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a844bddda86820d5f1edce0033b3b42b0a6c798f28b942c8d1102c8010fae9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd98ca39b83628d6ff99b22976db3c6c91fc7c55cab7d657b667514557a4416c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1f3ad1b41fdec59f1146412aacee52bdb69271920950088fe32fc36cfa731e(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelActivityMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046e4a8df008a2ca1fd9712c1dd7ab13f408a8f761c78d2215ca4ea9129d37e8(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199b73085a5412c828d200a54b4065646c8570c2948dddb82ed301204b4b6992(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce07736026c05e609b4af3d1770cb5c28a67ef8a7ed4ff4cb15d810185c6552a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11269f5d6317b5d01baf6509d3f0520bf3a615c07ed1b05e129819a884d6e00(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedCostOptimizationMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba195e1d48477c31c7eba44dc70e1bd3f172fcbf30e174c701a62285f4ffa7e(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae1d0f52ea44eb25da3a2a8b1258098b87e037d658a91054736ffa2a0497f18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca87b8888c01afe05e1f23dd1f36ef01b5d24ca800bf6bee7a036a05b2265f47(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d0d1ade2032f778b30d80ea4f657717f65a6c52b74bcc5095c038913b6debf(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelAdvancedDataProtectionMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42eb4403cb67b3e30a7eafac1e34ffa68d39510aacf3c9496e0d5fe69bd2aec2(
    *,
    activity_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_cost_optimization_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_data_protection_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    detailed_status_code_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix_level: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f138c23115cbfb9f46a675516be9c7a54fbe99e14057ccbbe6ab62c2794ecc42(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db665f90d0a48a9bebb8e2d32656a4b7842a7ab638de72f9910ce0d03d3d7aeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f1e28bb62ecd9063cab589e4bebcf66990db7ec9a17c526decf919733ed362(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1048467cad80af2ed72a86d3af09906514be045cf83139dad7e3f00f4c080ea(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelActivityMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd398a1f61a22c335979e53cfac25a0ecadf2f4fcfe86ae893bf6dc41846a1d(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ec8241385c4395377601a65f07c3f924953fab3c2d59765793b8a8416a6074(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946d9ca875c9c4f9c523c2ebe5ee6fd53c0d7a92d0bfa96feeb42b9bfdb4c72d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7d9044279f781977d99ac0f92681e006a42de84557f1e7e8083598e4c83d94(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedCostOptimizationMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a951eca099369c4b6531461531200d3aa4caf57ac4a66a6d7d8058bffc65a2c(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d0d21c875441eb1fd6389f9ac801ff7a5257588330d0428681dc4a0c3630af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b90f328c146c9ed7dec988e8fe291170bc082306554102bae7dfe316958bf65(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9324fabd8568d931c0d11827c95cfeb630a87ac5b6c7fa27965faf143be789c(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelAdvancedDataProtectionMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b1f3d8126f3fc40c2aee61b106da1e829c1fbaeb89a75aab0389935781b531(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8338128bf1b5272841486f34ac3bea49f4897f05a6dfaa74bccfa5c32dc76bec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55af963fcb592e3ddf0b191f5444e27bdc8e6f912159a82e10f3c59725d76d5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1febf6dddf1bd90b988b9e72d64eec802e3f50d980a4446ea3fa2a6fc449a9a2(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelDetailedStatusCodeMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a101075f84ee8c1aface629958264f05d722ac17657d8aa42611e903a8988ac7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d62cfbc3b0fc4e48439e03c673b14b0ad17105395f3bdba9c4a49674dca580(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12dd93b5bc71f00c67d4d49081e490f967c4ea0df9d5738a1ba346c4a16b818(
    *,
    storage_metrics: typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969bc60c36061384bc9b39b33b407c5eeda82a6eeda48a7817e2df5c95258271(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9722e347485b4084d18e58088edff4a7bb807d71e6729e2bac3efcf16af111f(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a47bb3e4e39df8b8a4f5cba947af543adc4bad2765d70291acbcfab844ea08(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    selection_criteria: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32de3286b8201d5753054df819381b25f1b040cdcfdcaa86fba74dba69ed6fcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5f26b36131ac90d3dc790604e618181a78e18b6b3f9249e2fde27f9ff29eab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab6745aa8ad302bd2a5b1d7a4a7da04cfa6ad0a585986faf80b685b67b44a59(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e5a1cf1ce5973ed3457157b7fcaefbbc77eba7a4ddcbe89a2d127d55a75e80(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    max_depth: typing.Optional[jsii.Number] = None,
    min_storage_bytes_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d650c2801d3c650a1b9d4df7ba51af208d6759dcd54de8a8c68219d8978b9e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02909aaa3b5241e2d0ef58f4aaa325a1023bdbba7710dc1adb9e3c631215a33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7bd51d062ca595ed6b90384c37fdb4866dc823ca080b35cfa4ed3010c80da0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c4db21dc0dc0ad002bd4c50990fba2869ac1ee8f7fa42dbc2df9de92bfd196(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af54426dcd75a31dd0ad4d6626711ebb15db798ae7fe2879ffd0d268f413254(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelBucketLevelPrefixLevelStorageMetricsSelectionCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80280c5a2665e01a46b050a5589535b6093ecb2132444f671d99ad9e2189b2b2(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c146caeb1b94907fd0ee10d7c8e44b9eadf9e839e27e07e703a7e31ca483592(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3900b9d0a2464c60e74fe1e2cc96e903c213080bd836bdc17f0eca7d60d91ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddfd5d5161b70a7065080f33e1b90a5b4a7424872a623759942b06cc71aeb7f(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevelDetailedStatusCodeMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a785a4123555f1cc145aec594ec3975a502b8ebe72945e490c0f2c5769f20b25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a94c6f52ea61304956b326c2a1c8bca72fe925002d5f9c3a8f4354e1776260(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAccountLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395b18018166535ee3e0df723d0b0f7b6eec6138866ca7e1fc0f08e3c6a1677f(
    *,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0286a200518c474e7e09d17f71b3d8cd1c01c50ef6c5135d214eb569b81f79f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b521c43abbc97bb02ed3d0285ca4f247c1e48a190765801d16934ba022b529c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950bc829fe11efcf281fba6ef82bb871a6a1bcf208b913b53e2a94a5c499e10e(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationAwsOrg],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d305cdf74115f0e41af2c28c0895113a848d12eee3c139e6090f331eb64c3761(
    *,
    cloud_watch_metrics: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_bucket_destination: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf52a3a0e623c7fa6d11bba3feccd782a9d85f97ca82cd8475d0189b69a4ae76(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e610fbb9e5a5c9b578ebb1636fc3b3a5c60aa27f8f206e2c728fb63f06a37a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39cfc2f50de9271711795665aa256aeca90a9de6d43a8f44ed7902b3443823c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b8372b6c124c40564292b74c17194ff894fe960112099e0c7fbc3f0cd47702(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportCloudWatchMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6808983bb0c60a704ed91435cc1ad28e96fd982c2cffb311bb58ce64429e3f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6adaf0c0357d96fdafde789c26e61df025a8874338f4613ea19b76dfe43eacf(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa8c1a1f71afc2a6efcbfd6257e481828137eb627e926ed0623c4769f77b5e0(
    *,
    account_id: builtins.str,
    arn: builtins.str,
    format: builtins.str,
    output_schema_version: builtins.str,
    encryption: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc5ced2fc7b2ba7232aba8bfdf550f02e3b733c90a94673410ea89f87139bee(
    *,
    sse_kms: typing.Optional[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms, typing.Dict[builtins.str, typing.Any]]] = None,
    sse_s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626d71cc89e2a859d2ff7119ca8c12d44666a4021ec9db5149997c9db55719da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f5d0d5adc5d287a8689ca433fba45c52de5afc8fd644d9840156053563bdb8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89559f8402347902ca6db6eea5f10dcc91f51fc8103a3fa23af76f724a29e258(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e0cea7def5f2b2c1f5dfcf31a7e1041aea9c82780056fa4425dc8394a4fdc1(
    *,
    key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbe895744381fcdc0aca8188ed206d7fd54e2d3ca1b62a45dc4cbfbb2fa2264(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02f5c768b3558162f144f1d3dd514fdd39208cff6cea4e18896bf0281a5bdc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd6cf618830ab8b215e7f3d4f194ed8f48a74c0343379c3d703b6b515b068b6(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseKms],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9556bef73608ea3844f9a13aa32d7b7ae29be3fada685b627689f6ba90032a84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cadc71740d23496966317e6b3843b98743ce1eecc1e96916fdd4bee1a4a131c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55755a0405f6b1827deb9742085d459e97b37b48441bd4f3ea5221653ab982fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa03a644f64c0c8608452b43a51491776ddfc336dcc6451ba846e981f4da16af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3596b5f6eb8beb4ddec251579080869431d3218de82a20eeacc1f3060127a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97afcb9271d10ead5a2eddd809a7c82bbd11e5794be19b5b9187a106688ddfb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905dfd645ba94e84b8bc5938f3f90ada4062b7fa355091929fe6de4362bdf365(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0cd2e914110a76cf179514234c247957d551c26b862ae71e040709c06009b7a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestinationEncryptionSseS3]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444bd27a0c42db4f9d77956bfd073cdf7fc6565bfd69ede77988acef0abd3d26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d19b182240e6413446c71f6d3cd1a373283a78ee535cd4c16f90d82adbfb1a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2881da7d0576881a681df8443942f2499b53be6a48fea15ad4ec8dad7593789(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85510f6742429d90ed120d5867eb6f38de193c9e17446d616036ace8eaea7e9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5984f8c3e126bcf444454905f3ba14f8c95cd3334f590367286f77fe08d2f5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4f27d6006e70e27452434b3689371f9c1c2dac081af37b20c17114ee4b7119(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0991bff9db0dcae0cc7f6b1b868b9ddf6ed3621b7ea4db7dc551883b5e64c5(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationDataExportS3BucketDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12434079cdc92411072fa15e1c9830ff3c26fa4049136d03fbef27039b3b20d5(
    *,
    buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ca3bb339a98cdbd1eba71cfa8898fe334f2c509bf54cc8d58f73278f4bd28a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea00750469e9164b3dbf586df0ecfb7c5770153fc32fe130fe7a60575aa8cf16(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10e4199c9380d54ee132d77f60b13e811b879d248ae2cbacccc3c1b5e2459d4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cde63f706324dba62a070bb0d56de2c5130db4252c1927d2d101ededb533ba1(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationExclude],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1289900ce22fcd7c69e61530063476b18e0190353af8a81a16a722572666a0fd(
    *,
    buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55064e996a6f3da8328d1a15b1f18ea2d9e0ffa0650cd03f6ba1eb92ad3e22d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b0165678fd1730d6dc06cd11a2eac9942bf105b7f365150ed6f19cd8d3f856(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03b03c0c91d1b69d64d4d0ced909a399a5390e9eb64651501493b6c0bace895(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573b943ebd1565c42455aa527ddb26aad2cac3ad8881e519a146e38a49781c99(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfigurationInclude],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0321b5ac6a97588dbba10272cd1e087804679787a875068c4a7b7840cd0902(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa687f4ec53f1006698eb6388500cf8d57b7f1e1d337194576d0625e57c303db(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ad058ac765c19bd7cb7d7939ffc997653e6074478cd5401415c871a88f568b(
    value: typing.Optional[S3ControlStorageLensConfigurationStorageLensConfiguration],
) -> None:
    """Type checking stubs"""
    pass
