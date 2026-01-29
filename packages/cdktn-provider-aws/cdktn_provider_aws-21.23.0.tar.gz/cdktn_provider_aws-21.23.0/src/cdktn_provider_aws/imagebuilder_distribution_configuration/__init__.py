r'''
# `aws_imagebuilder_distribution_configuration`

Refer to the Terraform Registry for docs: [`aws_imagebuilder_distribution_configuration`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration).
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


class ImagebuilderDistributionConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration aws_imagebuilder_distribution_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        distribution: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImagebuilderDistributionConfigurationDistribution", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration aws_imagebuilder_distribution_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param distribution: distribution block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#distribution ImagebuilderDistributionConfiguration#distribution}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#name ImagebuilderDistributionConfiguration#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#description ImagebuilderDistributionConfiguration#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#id ImagebuilderDistributionConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#region ImagebuilderDistributionConfiguration#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#tags ImagebuilderDistributionConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#tags_all ImagebuilderDistributionConfiguration#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf9406a02e9d8d24ab09288be42b978ddac1258772153f5e312d0a6911249e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ImagebuilderDistributionConfigurationConfig(
            distribution=distribution,
            name=name,
            description=description,
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
        '''Generates CDKTF code for importing a ImagebuilderDistributionConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ImagebuilderDistributionConfiguration to import.
        :param import_from_id: The id of the existing ImagebuilderDistributionConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ImagebuilderDistributionConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d9697a0b541a66c56ee35ebaf439c207593ed9eec21b39abc2de9075c07cdce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDistribution")
    def put_distribution(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImagebuilderDistributionConfigurationDistribution", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f3e36b1e9a3dc1c0da85d8bbdf688efd4baf24191e1f9918bbd136fc9e3899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDistribution", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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
    @jsii.member(jsii_name="dateCreated")
    def date_created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateCreated"))

    @builtins.property
    @jsii.member(jsii_name="dateUpdated")
    def date_updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateUpdated"))

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> "ImagebuilderDistributionConfigurationDistributionList":
        return typing.cast("ImagebuilderDistributionConfigurationDistributionList", jsii.get(self, "distribution"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionInput")
    def distribution_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistribution"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistribution"]]], jsii.get(self, "distributionInput"))

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
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12278dcf5998cdec378ae0f2049558580e5df7711aba21ee70c30a2f0867031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18ff0d3ab0f1d1da0add492356bb7c8fa606ba918ab27354bf6baab84daa3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7d18cb347dcd9a765fc12c0934b0d8c8fa658bf541e85e6bb1ef8ad4c6d421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8703a04faa89b9912987dc84d1e346bb040b15f02bfa930abf1935b6b003f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddaa2fe4abc0ddc829f8efc988c70750542e3e04ec0443237b98254a44a95b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570a8a05da5f90d307b9a03f726daab02aa2c2e04e60864a33b82c5dcf501283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "distribution": "distribution",
        "name": "name",
        "description": "description",
        "id": "id",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class ImagebuilderDistributionConfigurationConfig(
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
        distribution: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImagebuilderDistributionConfigurationDistribution", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
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
        :param distribution: distribution block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#distribution ImagebuilderDistributionConfiguration#distribution}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#name ImagebuilderDistributionConfiguration#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#description ImagebuilderDistributionConfiguration#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#id ImagebuilderDistributionConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#region ImagebuilderDistributionConfiguration#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#tags ImagebuilderDistributionConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#tags_all ImagebuilderDistributionConfiguration#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc76873f2f2810573080e83394fe3e759a5a8c6164afb0620318526e3283143)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "distribution": distribution,
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
        if description is not None:
            self._values["description"] = description
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
    def distribution(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistribution"]]:
        '''distribution block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#distribution ImagebuilderDistributionConfiguration#distribution}
        '''
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistribution"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#name ImagebuilderDistributionConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#description ImagebuilderDistributionConfiguration#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#id ImagebuilderDistributionConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#region ImagebuilderDistributionConfiguration#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#tags ImagebuilderDistributionConfiguration#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#tags_all ImagebuilderDistributionConfiguration#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistribution",
    jsii_struct_bases=[],
    name_mapping={
        "region": "region",
        "ami_distribution_configuration": "amiDistributionConfiguration",
        "container_distribution_configuration": "containerDistributionConfiguration",
        "fast_launch_configuration": "fastLaunchConfiguration",
        "launch_template_configuration": "launchTemplateConfiguration",
        "license_configuration_arns": "licenseConfigurationArns",
        "s3_export_configuration": "s3ExportConfiguration",
        "ssm_parameter_configuration": "ssmParameterConfiguration",
    },
)
class ImagebuilderDistributionConfigurationDistribution:
    def __init__(
        self,
        *,
        region: builtins.str,
        ami_distribution_configuration: typing.Optional[typing.Union["ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        container_distribution_configuration: typing.Optional[typing.Union["ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_launch_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        launch_template_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        license_configuration_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_export_configuration: typing.Optional[typing.Union["ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        ssm_parameter_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#region ImagebuilderDistributionConfiguration#region}.
        :param ami_distribution_configuration: ami_distribution_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#ami_distribution_configuration ImagebuilderDistributionConfiguration#ami_distribution_configuration}
        :param container_distribution_configuration: container_distribution_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#container_distribution_configuration ImagebuilderDistributionConfiguration#container_distribution_configuration}
        :param fast_launch_configuration: fast_launch_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#fast_launch_configuration ImagebuilderDistributionConfiguration#fast_launch_configuration}
        :param launch_template_configuration: launch_template_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_configuration ImagebuilderDistributionConfiguration#launch_template_configuration}
        :param license_configuration_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#license_configuration_arns ImagebuilderDistributionConfiguration#license_configuration_arns}.
        :param s3_export_configuration: s3_export_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#s3_export_configuration ImagebuilderDistributionConfiguration#s3_export_configuration}
        :param ssm_parameter_configuration: ssm_parameter_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#ssm_parameter_configuration ImagebuilderDistributionConfiguration#ssm_parameter_configuration}
        '''
        if isinstance(ami_distribution_configuration, dict):
            ami_distribution_configuration = ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration(**ami_distribution_configuration)
        if isinstance(container_distribution_configuration, dict):
            container_distribution_configuration = ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration(**container_distribution_configuration)
        if isinstance(s3_export_configuration, dict):
            s3_export_configuration = ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration(**s3_export_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063fe33d9c39316dff8b54de0719c1dec2fc26039350935e8e43e3741b280658)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument ami_distribution_configuration", value=ami_distribution_configuration, expected_type=type_hints["ami_distribution_configuration"])
            check_type(argname="argument container_distribution_configuration", value=container_distribution_configuration, expected_type=type_hints["container_distribution_configuration"])
            check_type(argname="argument fast_launch_configuration", value=fast_launch_configuration, expected_type=type_hints["fast_launch_configuration"])
            check_type(argname="argument launch_template_configuration", value=launch_template_configuration, expected_type=type_hints["launch_template_configuration"])
            check_type(argname="argument license_configuration_arns", value=license_configuration_arns, expected_type=type_hints["license_configuration_arns"])
            check_type(argname="argument s3_export_configuration", value=s3_export_configuration, expected_type=type_hints["s3_export_configuration"])
            check_type(argname="argument ssm_parameter_configuration", value=ssm_parameter_configuration, expected_type=type_hints["ssm_parameter_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region": region,
        }
        if ami_distribution_configuration is not None:
            self._values["ami_distribution_configuration"] = ami_distribution_configuration
        if container_distribution_configuration is not None:
            self._values["container_distribution_configuration"] = container_distribution_configuration
        if fast_launch_configuration is not None:
            self._values["fast_launch_configuration"] = fast_launch_configuration
        if launch_template_configuration is not None:
            self._values["launch_template_configuration"] = launch_template_configuration
        if license_configuration_arns is not None:
            self._values["license_configuration_arns"] = license_configuration_arns
        if s3_export_configuration is not None:
            self._values["s3_export_configuration"] = s3_export_configuration
        if ssm_parameter_configuration is not None:
            self._values["ssm_parameter_configuration"] = ssm_parameter_configuration

    @builtins.property
    def region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#region ImagebuilderDistributionConfiguration#region}.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ami_distribution_configuration(
        self,
    ) -> typing.Optional["ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration"]:
        '''ami_distribution_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#ami_distribution_configuration ImagebuilderDistributionConfiguration#ami_distribution_configuration}
        '''
        result = self._values.get("ami_distribution_configuration")
        return typing.cast(typing.Optional["ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration"], result)

    @builtins.property
    def container_distribution_configuration(
        self,
    ) -> typing.Optional["ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration"]:
        '''container_distribution_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#container_distribution_configuration ImagebuilderDistributionConfiguration#container_distribution_configuration}
        '''
        result = self._values.get("container_distribution_configuration")
        return typing.cast(typing.Optional["ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration"], result)

    @builtins.property
    def fast_launch_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration"]]]:
        '''fast_launch_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#fast_launch_configuration ImagebuilderDistributionConfiguration#fast_launch_configuration}
        '''
        result = self._values.get("fast_launch_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration"]]], result)

    @builtins.property
    def launch_template_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration"]]]:
        '''launch_template_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_configuration ImagebuilderDistributionConfiguration#launch_template_configuration}
        '''
        result = self._values.get("launch_template_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration"]]], result)

    @builtins.property
    def license_configuration_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#license_configuration_arns ImagebuilderDistributionConfiguration#license_configuration_arns}.'''
        result = self._values.get("license_configuration_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def s3_export_configuration(
        self,
    ) -> typing.Optional["ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration"]:
        '''s3_export_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#s3_export_configuration ImagebuilderDistributionConfiguration#s3_export_configuration}
        '''
        result = self._values.get("s3_export_configuration")
        return typing.cast(typing.Optional["ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration"], result)

    @builtins.property
    def ssm_parameter_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration"]]]:
        '''ssm_parameter_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#ssm_parameter_configuration ImagebuilderDistributionConfiguration#ssm_parameter_configuration}
        '''
        result = self._values.get("ssm_parameter_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistribution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "ami_tags": "amiTags",
        "description": "description",
        "kms_key_id": "kmsKeyId",
        "launch_permission": "launchPermission",
        "name": "name",
        "target_account_ids": "targetAccountIds",
    },
)
class ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration:
    def __init__(
        self,
        *,
        ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        launch_permission: typing.Optional[typing.Union["ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        target_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ami_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#ami_tags ImagebuilderDistributionConfiguration#ami_tags}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#description ImagebuilderDistributionConfiguration#description}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#kms_key_id ImagebuilderDistributionConfiguration#kms_key_id}.
        :param launch_permission: launch_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_permission ImagebuilderDistributionConfiguration#launch_permission}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#name ImagebuilderDistributionConfiguration#name}.
        :param target_account_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#target_account_ids ImagebuilderDistributionConfiguration#target_account_ids}.
        '''
        if isinstance(launch_permission, dict):
            launch_permission = ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission(**launch_permission)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365930475a46fc709e3b2fdff666353aca41b889eb89d9ab15ceb6a1044e59f5)
            check_type(argname="argument ami_tags", value=ami_tags, expected_type=type_hints["ami_tags"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument launch_permission", value=launch_permission, expected_type=type_hints["launch_permission"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target_account_ids", value=target_account_ids, expected_type=type_hints["target_account_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ami_tags is not None:
            self._values["ami_tags"] = ami_tags
        if description is not None:
            self._values["description"] = description
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if launch_permission is not None:
            self._values["launch_permission"] = launch_permission
        if name is not None:
            self._values["name"] = name
        if target_account_ids is not None:
            self._values["target_account_ids"] = target_account_ids

    @builtins.property
    def ami_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#ami_tags ImagebuilderDistributionConfiguration#ami_tags}.'''
        result = self._values.get("ami_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#description ImagebuilderDistributionConfiguration#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#kms_key_id ImagebuilderDistributionConfiguration#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_permission(
        self,
    ) -> typing.Optional["ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission"]:
        '''launch_permission block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_permission ImagebuilderDistributionConfiguration#launch_permission}
        '''
        result = self._values.get("launch_permission")
        return typing.cast(typing.Optional["ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#name ImagebuilderDistributionConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#target_account_ids ImagebuilderDistributionConfiguration#target_account_ids}.'''
        result = self._values.get("target_account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission",
    jsii_struct_bases=[],
    name_mapping={
        "organizational_unit_arns": "organizationalUnitArns",
        "organization_arns": "organizationArns",
        "user_groups": "userGroups",
        "user_ids": "userIds",
    },
)
class ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission:
    def __init__(
        self,
        *,
        organizational_unit_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param organizational_unit_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#organizational_unit_arns ImagebuilderDistributionConfiguration#organizational_unit_arns}.
        :param organization_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#organization_arns ImagebuilderDistributionConfiguration#organization_arns}.
        :param user_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#user_groups ImagebuilderDistributionConfiguration#user_groups}.
        :param user_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#user_ids ImagebuilderDistributionConfiguration#user_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649cc94b30720e427a010c2d110b2cf51aea2f7506ff80d50a119f80dbc52dce)
            check_type(argname="argument organizational_unit_arns", value=organizational_unit_arns, expected_type=type_hints["organizational_unit_arns"])
            check_type(argname="argument organization_arns", value=organization_arns, expected_type=type_hints["organization_arns"])
            check_type(argname="argument user_groups", value=user_groups, expected_type=type_hints["user_groups"])
            check_type(argname="argument user_ids", value=user_ids, expected_type=type_hints["user_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if organizational_unit_arns is not None:
            self._values["organizational_unit_arns"] = organizational_unit_arns
        if organization_arns is not None:
            self._values["organization_arns"] = organization_arns
        if user_groups is not None:
            self._values["user_groups"] = user_groups
        if user_ids is not None:
            self._values["user_ids"] = user_ids

    @builtins.property
    def organizational_unit_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#organizational_unit_arns ImagebuilderDistributionConfiguration#organizational_unit_arns}.'''
        result = self._values.get("organizational_unit_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def organization_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#organization_arns ImagebuilderDistributionConfiguration#organization_arns}.'''
        result = self._values.get("organization_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#user_groups ImagebuilderDistributionConfiguration#user_groups}.'''
        result = self._values.get("user_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#user_ids ImagebuilderDistributionConfiguration#user_ids}.'''
        result = self._values.get("user_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermissionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermissionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad7beb0c7c43bebbf1a520d7e7f6afb6843962883412e2f2bad9f794b3caf8d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOrganizationalUnitArns")
    def reset_organizational_unit_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationalUnitArns", []))

    @jsii.member(jsii_name="resetOrganizationArns")
    def reset_organization_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationArns", []))

    @jsii.member(jsii_name="resetUserGroups")
    def reset_user_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserGroups", []))

    @jsii.member(jsii_name="resetUserIds")
    def reset_user_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserIds", []))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitArnsInput")
    def organizational_unit_arns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "organizationalUnitArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationArnsInput")
    def organization_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "organizationArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="userGroupsInput")
    def user_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdsInput")
    def user_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitArns")
    def organizational_unit_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "organizationalUnitArns"))

    @organizational_unit_arns.setter
    def organizational_unit_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e11d4c3da7178c91a16edabfce4723f3b540252e91ea46e859674dadf4a01b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnitArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationArns")
    def organization_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "organizationArns"))

    @organization_arns.setter
    def organization_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07957831691fd971cdd1de101ce782822b0d4235317e348192d36d2de7af011d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userGroups")
    def user_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userGroups"))

    @user_groups.setter
    def user_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ce50e9095128b22bfb091ae5cd3a750bca4648c754a8dda14605b8b4e24124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userIds")
    def user_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userIds"))

    @user_ids.setter
    def user_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f2d05899e119dab365f87c8b9b2dcc74fd8176eb20fd86fae5bff49a6426dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102ef4cb185b2963222ab648ec27c8cdfa5b4f43f5b6f115804de10f4066e326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a1b340b9880588a2f0fe5e1af85789842e828c4c023c8ccb0c5490362404ae5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLaunchPermission")
    def put_launch_permission(
        self,
        *,
        organizational_unit_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param organizational_unit_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#organizational_unit_arns ImagebuilderDistributionConfiguration#organizational_unit_arns}.
        :param organization_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#organization_arns ImagebuilderDistributionConfiguration#organization_arns}.
        :param user_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#user_groups ImagebuilderDistributionConfiguration#user_groups}.
        :param user_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#user_ids ImagebuilderDistributionConfiguration#user_ids}.
        '''
        value = ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission(
            organizational_unit_arns=organizational_unit_arns,
            organization_arns=organization_arns,
            user_groups=user_groups,
            user_ids=user_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putLaunchPermission", [value]))

    @jsii.member(jsii_name="resetAmiTags")
    def reset_ami_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmiTags", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetLaunchPermission")
    def reset_launch_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchPermission", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetTargetAccountIds")
    def reset_target_account_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetAccountIds", []))

    @builtins.property
    @jsii.member(jsii_name="launchPermission")
    def launch_permission(
        self,
    ) -> ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermissionOutputReference:
        return typing.cast(ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermissionOutputReference, jsii.get(self, "launchPermission"))

    @builtins.property
    @jsii.member(jsii_name="amiTagsInput")
    def ami_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "amiTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="launchPermissionInput")
    def launch_permission_input(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission], jsii.get(self, "launchPermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetAccountIdsInput")
    def target_account_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetAccountIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="amiTags")
    def ami_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "amiTags"))

    @ami_tags.setter
    def ami_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142244f11b9a936fbc1d40f274710e5fa6b0c72605681f8ac1c637e85ade3c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amiTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9e8cf9f71dfc20f61c7d26c198c39d32fe611c67f842e0e1089fa6e5c5c82c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e30f4d813a6c6efe8c93349d2803463f471bf3ecde0d75531401b37c5ee87d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e784e489b03435f1e2675ba263bc5e1417bb28f4d781c94cb17dc06e5562a600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetAccountIds")
    def target_account_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetAccountIds"))

    @target_account_ids.setter
    def target_account_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1e1b99e71e08db2febf502294d0b77495417192be80a1613a5b399cc4c4811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetAccountIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594909d63459343d637982896b5b65a7ea10e9a9588449a2ae4d23d0cfed7482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "target_repository": "targetRepository",
        "container_tags": "containerTags",
        "description": "description",
    },
)
class ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration:
    def __init__(
        self,
        *,
        target_repository: typing.Union["ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository", typing.Dict[builtins.str, typing.Any]],
        container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_repository: target_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#target_repository ImagebuilderDistributionConfiguration#target_repository}
        :param container_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#container_tags ImagebuilderDistributionConfiguration#container_tags}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#description ImagebuilderDistributionConfiguration#description}.
        '''
        if isinstance(target_repository, dict):
            target_repository = ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository(**target_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__983a12a8807613d8ff05848ced9ac9bec379efb096bf2d1667aa02a3189aa2c4)
            check_type(argname="argument target_repository", value=target_repository, expected_type=type_hints["target_repository"])
            check_type(argname="argument container_tags", value=container_tags, expected_type=type_hints["container_tags"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_repository": target_repository,
        }
        if container_tags is not None:
            self._values["container_tags"] = container_tags
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def target_repository(
        self,
    ) -> "ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository":
        '''target_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#target_repository ImagebuilderDistributionConfiguration#target_repository}
        '''
        result = self._values.get("target_repository")
        assert result is not None, "Required property 'target_repository' is missing"
        return typing.cast("ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository", result)

    @builtins.property
    def container_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#container_tags ImagebuilderDistributionConfiguration#container_tags}.'''
        result = self._values.get("container_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#description ImagebuilderDistributionConfiguration#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62e39de7bda79297cf070936da34e3fa35945d6236a5c30c859a5a89d235c3c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTargetRepository")
    def put_target_repository(
        self,
        *,
        repository_name: builtins.str,
        service: builtins.str,
    ) -> None:
        '''
        :param repository_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#repository_name ImagebuilderDistributionConfiguration#repository_name}.
        :param service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#service ImagebuilderDistributionConfiguration#service}.
        '''
        value = ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository(
            repository_name=repository_name, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putTargetRepository", [value]))

    @jsii.member(jsii_name="resetContainerTags")
    def reset_container_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerTags", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="targetRepository")
    def target_repository(
        self,
    ) -> "ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepositoryOutputReference":
        return typing.cast("ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepositoryOutputReference", jsii.get(self, "targetRepository"))

    @builtins.property
    @jsii.member(jsii_name="containerTagsInput")
    def container_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "containerTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRepositoryInput")
    def target_repository_input(
        self,
    ) -> typing.Optional["ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository"]:
        return typing.cast(typing.Optional["ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository"], jsii.get(self, "targetRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="containerTags")
    def container_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "containerTags"))

    @container_tags.setter
    def container_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffdb495b0a41c8d5acf26415b39b6bfd0f29b12a17da9b1bbd96458a9d17eb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a8fe831060e6acc2857a92d8e72544aaf2ba70caeeacff4f7137fda454e5e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b52e75a2acf4fcb8b3bcc069ece64104d654e0e5f6de6774601b27b0b0e0be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository",
    jsii_struct_bases=[],
    name_mapping={"repository_name": "repositoryName", "service": "service"},
)
class ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository:
    def __init__(self, *, repository_name: builtins.str, service: builtins.str) -> None:
        '''
        :param repository_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#repository_name ImagebuilderDistributionConfiguration#repository_name}.
        :param service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#service ImagebuilderDistributionConfiguration#service}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14c50f36cbff43b702b3ec58f837ffe5dd6aa37bd9755821fdd63e8ed820c4b)
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_name": repository_name,
            "service": service,
        }

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#repository_name ImagebuilderDistributionConfiguration#repository_name}.'''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#service ImagebuilderDistributionConfiguration#service}.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60e775d485e06580c54120b748d7d5519eb936d569ebe7c7bf0e7b392d7c754d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="repositoryNameInput")
    def repository_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048c2e8632b731e31099fd7556fc32a7a14c168d1a0ad0ebaab9d1261e524fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618cba5cb26aaee1fe08e8b6eb99be7d4572aa764f4f01d06f06c1d218d47bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5961510166f1c58737edc47c347afc4337dc4026d7cb2c09cd6b09f60ff605a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "enabled": "enabled",
        "launch_template": "launchTemplate",
        "max_parallel_launches": "maxParallelLaunches",
        "snapshot_configuration": "snapshotConfiguration",
    },
)
class ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        launch_template: typing.Optional[typing.Union["ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        max_parallel_launches: typing.Optional[jsii.Number] = None,
        snapshot_configuration: typing.Optional[typing.Union["ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#account_id ImagebuilderDistributionConfiguration#account_id}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#enabled ImagebuilderDistributionConfiguration#enabled}.
        :param launch_template: launch_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template ImagebuilderDistributionConfiguration#launch_template}
        :param max_parallel_launches: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#max_parallel_launches ImagebuilderDistributionConfiguration#max_parallel_launches}.
        :param snapshot_configuration: snapshot_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#snapshot_configuration ImagebuilderDistributionConfiguration#snapshot_configuration}
        '''
        if isinstance(launch_template, dict):
            launch_template = ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate(**launch_template)
        if isinstance(snapshot_configuration, dict):
            snapshot_configuration = ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration(**snapshot_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9631b846bf5147e575ffeab8f2d5d41588f113fb04467322489e6d6dbd0ba72f)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument max_parallel_launches", value=max_parallel_launches, expected_type=type_hints["max_parallel_launches"])
            check_type(argname="argument snapshot_configuration", value=snapshot_configuration, expected_type=type_hints["snapshot_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "enabled": enabled,
        }
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if max_parallel_launches is not None:
            self._values["max_parallel_launches"] = max_parallel_launches
        if snapshot_configuration is not None:
            self._values["snapshot_configuration"] = snapshot_configuration

    @builtins.property
    def account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#account_id ImagebuilderDistributionConfiguration#account_id}.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#enabled ImagebuilderDistributionConfiguration#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def launch_template(
        self,
    ) -> typing.Optional["ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate"]:
        '''launch_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template ImagebuilderDistributionConfiguration#launch_template}
        '''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional["ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate"], result)

    @builtins.property
    def max_parallel_launches(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#max_parallel_launches ImagebuilderDistributionConfiguration#max_parallel_launches}.'''
        result = self._values.get("max_parallel_launches")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot_configuration(
        self,
    ) -> typing.Optional["ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration"]:
        '''snapshot_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#snapshot_configuration ImagebuilderDistributionConfiguration#snapshot_configuration}
        '''
        result = self._values.get("snapshot_configuration")
        return typing.cast(typing.Optional["ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "launch_template_id": "launchTemplateId",
        "launch_template_name": "launchTemplateName",
        "launch_template_version": "launchTemplateVersion",
    },
)
class ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate:
    def __init__(
        self,
        *,
        launch_template_id: typing.Optional[builtins.str] = None,
        launch_template_name: typing.Optional[builtins.str] = None,
        launch_template_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param launch_template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_id ImagebuilderDistributionConfiguration#launch_template_id}.
        :param launch_template_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_name ImagebuilderDistributionConfiguration#launch_template_name}.
        :param launch_template_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_version ImagebuilderDistributionConfiguration#launch_template_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c1bd32bdbed69c91c6f5a6bac7bb05919ef655a8d87761282a614ba3a58ab1)
            check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
            check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
            check_type(argname="argument launch_template_version", value=launch_template_version, expected_type=type_hints["launch_template_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if launch_template_id is not None:
            self._values["launch_template_id"] = launch_template_id
        if launch_template_name is not None:
            self._values["launch_template_name"] = launch_template_name
        if launch_template_version is not None:
            self._values["launch_template_version"] = launch_template_version

    @builtins.property
    def launch_template_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_id ImagebuilderDistributionConfiguration#launch_template_id}.'''
        result = self._values.get("launch_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_template_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_name ImagebuilderDistributionConfiguration#launch_template_name}.'''
        result = self._values.get("launch_template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_template_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_version ImagebuilderDistributionConfiguration#launch_template_version}.'''
        result = self._values.get("launch_template_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c7d364646f114de3bd1c8d6098bd017039e6d08f347ab62412e798ba8b28f6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLaunchTemplateId")
    def reset_launch_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchTemplateId", []))

    @jsii.member(jsii_name="resetLaunchTemplateName")
    def reset_launch_template_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchTemplateName", []))

    @jsii.member(jsii_name="resetLaunchTemplateVersion")
    def reset_launch_template_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchTemplateVersion", []))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateIdInput")
    def launch_template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateNameInput")
    def launch_template_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateVersionInput")
    def launch_template_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateId")
    def launch_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchTemplateId"))

    @launch_template_id.setter
    def launch_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea00c0183d92dd127c05573f8dfc5b1489bb3454cbf92ba4ec50a26bf180383b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchTemplateName")
    def launch_template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchTemplateName"))

    @launch_template_name.setter
    def launch_template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e3d7ac810ee8cd9c10474e3b05bc5274816865470acf77feb3773daca17677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchTemplateVersion")
    def launch_template_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchTemplateVersion"))

    @launch_template_version.setter
    def launch_template_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44765e87797161c1f2d75e3c5c12241ddcee58a7e5c82b572b0bac94491c9dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc13d0fd0904b1ee87f589ad935e6e69187329ce6f2d1e0bf6cbc506877568a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6dcfb9ed2f8835eb5da58e79956f289d0777d6d04a40d06bcc31cf7d8266e61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e669091db365379ae35abff9de44963d82daf3579921cb8744775d40776c65b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5bdbee20006b4e569df343fd3725380ef41fae04c9a24e02712ef92c52e7bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c00cd41d8cdb4ca1a03bfd86f5ba48922eff85eedbd3582499d5bbaf56433b23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35fe44628814637164d8134b4012b5fe9066be08eb10e7439d4c460b2dfde795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e97d7c9b39e659ed89edb133f9ac53b8ee4d0fb737a0f6cd9e4743cb5aa5413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__799d8b3dad552e5e5b9cd5e7eac8e271d4f203e031e2ef21e04c2d4875fca04d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLaunchTemplate")
    def put_launch_template(
        self,
        *,
        launch_template_id: typing.Optional[builtins.str] = None,
        launch_template_name: typing.Optional[builtins.str] = None,
        launch_template_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param launch_template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_id ImagebuilderDistributionConfiguration#launch_template_id}.
        :param launch_template_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_name ImagebuilderDistributionConfiguration#launch_template_name}.
        :param launch_template_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_version ImagebuilderDistributionConfiguration#launch_template_version}.
        '''
        value = ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate(
            launch_template_id=launch_template_id,
            launch_template_name=launch_template_name,
            launch_template_version=launch_template_version,
        )

        return typing.cast(None, jsii.invoke(self, "putLaunchTemplate", [value]))

    @jsii.member(jsii_name="putSnapshotConfiguration")
    def put_snapshot_configuration(
        self,
        *,
        target_resource_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_resource_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#target_resource_count ImagebuilderDistributionConfiguration#target_resource_count}.
        '''
        value = ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration(
            target_resource_count=target_resource_count
        )

        return typing.cast(None, jsii.invoke(self, "putSnapshotConfiguration", [value]))

    @jsii.member(jsii_name="resetLaunchTemplate")
    def reset_launch_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchTemplate", []))

    @jsii.member(jsii_name="resetMaxParallelLaunches")
    def reset_max_parallel_launches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxParallelLaunches", []))

    @jsii.member(jsii_name="resetSnapshotConfiguration")
    def reset_snapshot_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(
        self,
    ) -> ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplateOutputReference:
        return typing.cast(ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplateOutputReference, jsii.get(self, "launchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="snapshotConfiguration")
    def snapshot_configuration(
        self,
    ) -> "ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfigurationOutputReference":
        return typing.cast("ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfigurationOutputReference", jsii.get(self, "snapshotConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateInput")
    def launch_template_input(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate], jsii.get(self, "launchTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="maxParallelLaunchesInput")
    def max_parallel_launches_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxParallelLaunchesInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotConfigurationInput")
    def snapshot_configuration_input(
        self,
    ) -> typing.Optional["ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration"]:
        return typing.cast(typing.Optional["ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration"], jsii.get(self, "snapshotConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc675ea73485ee3f0343eb9bc3bb0ec809d6b731ac8baa9e823bb30c8bdc001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__4fceecdfee28c16678321dae14cc156e29dc233830e2a83544cfcccd5bf7b5d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxParallelLaunches")
    def max_parallel_launches(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxParallelLaunches"))

    @max_parallel_launches.setter
    def max_parallel_launches(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761ee44f5acbe5ff217f83483efdef25fce8fddfb9adfd5e49ca696195a54921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxParallelLaunches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a752e7037573e976e20f764dbaf64f556e3b0e349686ca74af4bacce88ae372d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration",
    jsii_struct_bases=[],
    name_mapping={"target_resource_count": "targetResourceCount"},
)
class ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration:
    def __init__(
        self,
        *,
        target_resource_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_resource_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#target_resource_count ImagebuilderDistributionConfiguration#target_resource_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b159439eb1ac2229f816947ac4d7ad676bdfa94c9250f428a9271111b7a88d)
            check_type(argname="argument target_resource_count", value=target_resource_count, expected_type=type_hints["target_resource_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if target_resource_count is not None:
            self._values["target_resource_count"] = target_resource_count

    @builtins.property
    def target_resource_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#target_resource_count ImagebuilderDistributionConfiguration#target_resource_count}.'''
        result = self._values.get("target_resource_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99d7164f7f9413e2ffdb3c8b805d6227f6b5d6fcc38945f3212dbf44c37ba7b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTargetResourceCount")
    def reset_target_resource_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResourceCount", []))

    @builtins.property
    @jsii.member(jsii_name="targetResourceCountInput")
    def target_resource_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetResourceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceCount")
    def target_resource_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetResourceCount"))

    @target_resource_count.setter
    def target_resource_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7acb9a5dd86295e63a099b86ed20fbab982107ed3f226b2ffdd4b4a6717c80a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResourceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f6f57c605be07a0c5ee4e0809dd6448d3b929511e63ddd8fa9e4aa5c90bc37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "launch_template_id": "launchTemplateId",
        "account_id": "accountId",
        "default": "default",
    },
)
class ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration:
    def __init__(
        self,
        *,
        launch_template_id: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param launch_template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_id ImagebuilderDistributionConfiguration#launch_template_id}.
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#account_id ImagebuilderDistributionConfiguration#account_id}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#default ImagebuilderDistributionConfiguration#default}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7438538adf3e5bf300fa51dd296c1afbe826069dc0ef10fdcfebd50969f08ed)
            check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "launch_template_id": launch_template_id,
        }
        if account_id is not None:
            self._values["account_id"] = account_id
        if default is not None:
            self._values["default"] = default

    @builtins.property
    def launch_template_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_template_id ImagebuilderDistributionConfiguration#launch_template_id}.'''
        result = self._values.get("launch_template_id")
        assert result is not None, "Required property 'launch_template_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#account_id ImagebuilderDistributionConfiguration#account_id}.'''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#default ImagebuilderDistributionConfiguration#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a4b3063405766db74e279492f92a025610e13ccba65dabb7df66a747ec809b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33d6ef585eaf28ccacab1f6f2aed6f30b1f64ad9dd1dfbc0fe582890465cd454)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0103186a1869a4626fd16a6ef177f23b1ea8899b9c83c748a885ecb2826d804c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f8c9c7e8824990af4d37110efcb2caa32ec096601ea660759c70926f5426866)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e466bf7f5d98862d0021900eb57ea3965b9ca81212a1b01f74fff7135b7324a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b767f7ddcac0e71f1d1675132894a295f98320e2af663808997c25eef55cc160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8726ab07313c941145e0c4606dbda8f83d9b31b3bfa4573a166bcce09b5a4ea4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateIdInput")
    def launch_template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3777acaf1eb94b3acc1e595408c2e6e8e906006fd4da96b7e0387bf4d569891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "default"))

    @default.setter
    def default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61f513369839d16ef0dcade2ab6b1085e794d4806930de819bdcbcc204630f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchTemplateId")
    def launch_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchTemplateId"))

    @launch_template_id.setter
    def launch_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a28c9375337e2c18565e24742ddfd3238afdde9604a96c22190536e2114cba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20103621cd5e1f44603e92fa995964e46ef20cdf7c6b684b91d760acef8a30d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImagebuilderDistributionConfigurationDistributionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f062a426493be6397d9ee2d0686a38c32bfa843819588428bf9473e16e64da33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ImagebuilderDistributionConfigurationDistributionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8ba90d49c805e99a392170c64e6dca6228ba99f6b3650a9c4998a625f81012)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ImagebuilderDistributionConfigurationDistributionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525f691c4d29d87bc99e2a24d6569470155b13fcaf77f56582b943f472ea2b05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6de4e8ace12f8b11e501a3855f6c09d887c672eba369f54fb24a894d5a565fe1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee95e6e4b50b00abc50ef21f0145374ec04ab736a7d1a809a3583b6fd94c9713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistribution]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistribution]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistribution]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5f14ffeafd21e9324011af0d1c3785e9e77f828e39526c36009fe729863891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImagebuilderDistributionConfigurationDistributionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e9f291a5b02ffe2d6124b9b234b7f6de84c7cc68f17f88cc0eb6b8ed8223358)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAmiDistributionConfiguration")
    def put_ami_distribution_configuration(
        self,
        *,
        ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        launch_permission: typing.Optional[typing.Union[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        target_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ami_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#ami_tags ImagebuilderDistributionConfiguration#ami_tags}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#description ImagebuilderDistributionConfiguration#description}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#kms_key_id ImagebuilderDistributionConfiguration#kms_key_id}.
        :param launch_permission: launch_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#launch_permission ImagebuilderDistributionConfiguration#launch_permission}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#name ImagebuilderDistributionConfiguration#name}.
        :param target_account_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#target_account_ids ImagebuilderDistributionConfiguration#target_account_ids}.
        '''
        value = ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration(
            ami_tags=ami_tags,
            description=description,
            kms_key_id=kms_key_id,
            launch_permission=launch_permission,
            name=name,
            target_account_ids=target_account_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putAmiDistributionConfiguration", [value]))

    @jsii.member(jsii_name="putContainerDistributionConfiguration")
    def put_container_distribution_configuration(
        self,
        *,
        target_repository: typing.Union[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository, typing.Dict[builtins.str, typing.Any]],
        container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_repository: target_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#target_repository ImagebuilderDistributionConfiguration#target_repository}
        :param container_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#container_tags ImagebuilderDistributionConfiguration#container_tags}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#description ImagebuilderDistributionConfiguration#description}.
        '''
        value = ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration(
            target_repository=target_repository,
            container_tags=container_tags,
            description=description,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerDistributionConfiguration", [value]))

    @jsii.member(jsii_name="putFastLaunchConfiguration")
    def put_fast_launch_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec99a14ec86003cc9b604e9570aea8dea2c9c95aadc765a98a481a981d37793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFastLaunchConfiguration", [value]))

    @jsii.member(jsii_name="putLaunchTemplateConfiguration")
    def put_launch_template_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c04481dc822392440e4c7f05d57880cc3a4776efa5b165074bb3942645a6c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLaunchTemplateConfiguration", [value]))

    @jsii.member(jsii_name="putS3ExportConfiguration")
    def put_s3_export_configuration(
        self,
        *,
        disk_image_format: builtins.str,
        role_name: builtins.str,
        s3_bucket: builtins.str,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_image_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#disk_image_format ImagebuilderDistributionConfiguration#disk_image_format}.
        :param role_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#role_name ImagebuilderDistributionConfiguration#role_name}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#s3_bucket ImagebuilderDistributionConfiguration#s3_bucket}.
        :param s3_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#s3_prefix ImagebuilderDistributionConfiguration#s3_prefix}.
        '''
        value = ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration(
            disk_image_format=disk_image_format,
            role_name=role_name,
            s3_bucket=s3_bucket,
            s3_prefix=s3_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putS3ExportConfiguration", [value]))

    @jsii.member(jsii_name="putSsmParameterConfiguration")
    def put_ssm_parameter_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfb8f277214e84d25bcab350eaa7ac096932eec3df17c60bcd5805382104d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSsmParameterConfiguration", [value]))

    @jsii.member(jsii_name="resetAmiDistributionConfiguration")
    def reset_ami_distribution_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmiDistributionConfiguration", []))

    @jsii.member(jsii_name="resetContainerDistributionConfiguration")
    def reset_container_distribution_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerDistributionConfiguration", []))

    @jsii.member(jsii_name="resetFastLaunchConfiguration")
    def reset_fast_launch_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFastLaunchConfiguration", []))

    @jsii.member(jsii_name="resetLaunchTemplateConfiguration")
    def reset_launch_template_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchTemplateConfiguration", []))

    @jsii.member(jsii_name="resetLicenseConfigurationArns")
    def reset_license_configuration_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseConfigurationArns", []))

    @jsii.member(jsii_name="resetS3ExportConfiguration")
    def reset_s3_export_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3ExportConfiguration", []))

    @jsii.member(jsii_name="resetSsmParameterConfiguration")
    def reset_ssm_parameter_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsmParameterConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="amiDistributionConfiguration")
    def ami_distribution_configuration(
        self,
    ) -> ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationOutputReference:
        return typing.cast(ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationOutputReference, jsii.get(self, "amiDistributionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="containerDistributionConfiguration")
    def container_distribution_configuration(
        self,
    ) -> ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationOutputReference:
        return typing.cast(ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationOutputReference, jsii.get(self, "containerDistributionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="fastLaunchConfiguration")
    def fast_launch_configuration(
        self,
    ) -> ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationList:
        return typing.cast(ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationList, jsii.get(self, "fastLaunchConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateConfiguration")
    def launch_template_configuration(
        self,
    ) -> ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfigurationList:
        return typing.cast(ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfigurationList, jsii.get(self, "launchTemplateConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3ExportConfiguration")
    def s3_export_configuration(
        self,
    ) -> "ImagebuilderDistributionConfigurationDistributionS3ExportConfigurationOutputReference":
        return typing.cast("ImagebuilderDistributionConfigurationDistributionS3ExportConfigurationOutputReference", jsii.get(self, "s3ExportConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="ssmParameterConfiguration")
    def ssm_parameter_configuration(
        self,
    ) -> "ImagebuilderDistributionConfigurationDistributionSsmParameterConfigurationList":
        return typing.cast("ImagebuilderDistributionConfigurationDistributionSsmParameterConfigurationList", jsii.get(self, "ssmParameterConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="amiDistributionConfigurationInput")
    def ami_distribution_configuration_input(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration], jsii.get(self, "amiDistributionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="containerDistributionConfigurationInput")
    def container_distribution_configuration_input(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration], jsii.get(self, "containerDistributionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="fastLaunchConfigurationInput")
    def fast_launch_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration]]], jsii.get(self, "fastLaunchConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateConfigurationInput")
    def launch_template_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration]]], jsii.get(self, "launchTemplateConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseConfigurationArnsInput")
    def license_configuration_arns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "licenseConfigurationArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="s3ExportConfigurationInput")
    def s3_export_configuration_input(
        self,
    ) -> typing.Optional["ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration"]:
        return typing.cast(typing.Optional["ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration"], jsii.get(self, "s3ExportConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="ssmParameterConfigurationInput")
    def ssm_parameter_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration"]]], jsii.get(self, "ssmParameterConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseConfigurationArns")
    def license_configuration_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "licenseConfigurationArns"))

    @license_configuration_arns.setter
    def license_configuration_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1733359519129e79fa0922976189193b00b83bf9bcab1876ddec7a09b58504e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseConfigurationArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fafeee3d705286a511038b5583ecc936a4341d0fbc710b564ae4abae5861644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistribution]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistribution]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistribution]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ce2ac20a5088a636c97dd1ecc2e0a8121cf7c0970506077ba6a3cbd59acb8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "disk_image_format": "diskImageFormat",
        "role_name": "roleName",
        "s3_bucket": "s3Bucket",
        "s3_prefix": "s3Prefix",
    },
)
class ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration:
    def __init__(
        self,
        *,
        disk_image_format: builtins.str,
        role_name: builtins.str,
        s3_bucket: builtins.str,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_image_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#disk_image_format ImagebuilderDistributionConfiguration#disk_image_format}.
        :param role_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#role_name ImagebuilderDistributionConfiguration#role_name}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#s3_bucket ImagebuilderDistributionConfiguration#s3_bucket}.
        :param s3_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#s3_prefix ImagebuilderDistributionConfiguration#s3_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db405fd4471d613bb5a55b59a8d7128b1b07219c24ed2eabaf18fb556c436277)
            check_type(argname="argument disk_image_format", value=disk_image_format, expected_type=type_hints["disk_image_format"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk_image_format": disk_image_format,
            "role_name": role_name,
            "s3_bucket": s3_bucket,
        }
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def disk_image_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#disk_image_format ImagebuilderDistributionConfiguration#disk_image_format}.'''
        result = self._values.get("disk_image_format")
        assert result is not None, "Required property 'disk_image_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#role_name ImagebuilderDistributionConfiguration#role_name}.'''
        result = self._values.get("role_name")
        assert result is not None, "Required property 'role_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#s3_bucket ImagebuilderDistributionConfiguration#s3_bucket}.'''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#s3_prefix ImagebuilderDistributionConfiguration#s3_prefix}.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderDistributionConfigurationDistributionS3ExportConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionS3ExportConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bae28a6ca719efb5e061134c996dc73ed65c6375a982cce78ca774ffc5e60b60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3Prefix")
    def reset_s3_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Prefix", []))

    @builtins.property
    @jsii.member(jsii_name="diskImageFormatInput")
    def disk_image_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskImageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="roleNameInput")
    def role_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketInput")
    def s3_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketInput"))

    @builtins.property
    @jsii.member(jsii_name="s3PrefixInput")
    def s3_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3PrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="diskImageFormat")
    def disk_image_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskImageFormat"))

    @disk_image_format.setter
    def disk_image_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f4c2aa8343e20d843cd878b25af7f2c7479d2642bcc2429304e054962a7c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskImageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleName"))

    @role_name.setter
    def role_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdbaa223402a108138d432c3d581933d6ce453999bc98bd211feaee36eb356a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7117c9717732a34f0b6d9440ed62e6ed16a68fce19889928624c8b214cf3256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Prefix")
    def s3_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Prefix"))

    @s3_prefix.setter
    def s3_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab8fe5e3b009d8cc8518161104410833601178289e033a142b49d4235e17176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration]:
        return typing.cast(typing.Optional[ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2288ced51012314e92ae57019a65f762c9ae9e009f82fd38b89e3961e27dc7df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_name": "parameterName",
        "ami_account_id": "amiAccountId",
        "data_type": "dataType",
    },
)
class ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration:
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        ami_account_id: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#parameter_name ImagebuilderDistributionConfiguration#parameter_name}.
        :param ami_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#ami_account_id ImagebuilderDistributionConfiguration#ami_account_id}.
        :param data_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#data_type ImagebuilderDistributionConfiguration#data_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827f2977d1f17d7099e6865eed3d82eb13723e4f48bde975c6b9a91f12234892)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument ami_account_id", value=ami_account_id, expected_type=type_hints["ami_account_id"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter_name": parameter_name,
        }
        if ami_account_id is not None:
            self._values["ami_account_id"] = ami_account_id
        if data_type is not None:
            self._values["data_type"] = data_type

    @builtins.property
    def parameter_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#parameter_name ImagebuilderDistributionConfiguration#parameter_name}.'''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ami_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#ami_account_id ImagebuilderDistributionConfiguration#ami_account_id}.'''
        result = self._values.get("ami_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/imagebuilder_distribution_configuration#data_type ImagebuilderDistributionConfiguration#data_type}.'''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderDistributionConfigurationDistributionSsmParameterConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionSsmParameterConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a884a23226cd533335420f0c513828e1fedba0c95bc469d676d909b79edce71d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ImagebuilderDistributionConfigurationDistributionSsmParameterConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca0c5d1221417a048cd96de64021e67f7bf26cee576798efc2a57a7fe9705a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ImagebuilderDistributionConfigurationDistributionSsmParameterConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9b951e0edd184fa2161093d1f48b21907cd455fb6f008e7dd27748fe3c8231)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ec72a1ea8a37382ac9c5d402e8ad525815cdd4c158248d0f86ec6643eb16f92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f9a2d57c62ed23aaca96782d9d9d9288cbfea64418a9a6a379f5e237f5d64f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff00b8082c3b6674d781ff13b93545a9ddb35509051ef8a3a3ebc3ea6cdda42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImagebuilderDistributionConfigurationDistributionSsmParameterConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.imagebuilderDistributionConfiguration.ImagebuilderDistributionConfigurationDistributionSsmParameterConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6403fb444a60da08f850a5d405d0e302a6a55aa334291769b26a9351c7e5b69b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAmiAccountId")
    def reset_ami_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmiAccountId", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @builtins.property
    @jsii.member(jsii_name="amiAccountIdInput")
    def ami_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "amiAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterNameInput")
    def parameter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="amiAccountId")
    def ami_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "amiAccountId"))

    @ami_account_id.setter
    def ami_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ad6d0956fb2cf43fe8ec94a6f89aee34c9bb2b642a5488b2d6096a1793296f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amiAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95954cbb2af363a0e899713c6715993b31a1575086724b7949994ded03422797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterName"))

    @parameter_name.setter
    def parameter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__986aba66f0f367fb3b3adf4f8ce1cf232deaef5828edf5b36ddf82b66cfa43ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb2913bb8246cfca33ce7d1ed5500e9eff5f1ec1b3553f4c33255a3be5d3738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ImagebuilderDistributionConfiguration",
    "ImagebuilderDistributionConfigurationConfig",
    "ImagebuilderDistributionConfigurationDistribution",
    "ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration",
    "ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission",
    "ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermissionOutputReference",
    "ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationOutputReference",
    "ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration",
    "ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationOutputReference",
    "ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository",
    "ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepositoryOutputReference",
    "ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration",
    "ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate",
    "ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplateOutputReference",
    "ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationList",
    "ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationOutputReference",
    "ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration",
    "ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfigurationOutputReference",
    "ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration",
    "ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfigurationList",
    "ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfigurationOutputReference",
    "ImagebuilderDistributionConfigurationDistributionList",
    "ImagebuilderDistributionConfigurationDistributionOutputReference",
    "ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration",
    "ImagebuilderDistributionConfigurationDistributionS3ExportConfigurationOutputReference",
    "ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration",
    "ImagebuilderDistributionConfigurationDistributionSsmParameterConfigurationList",
    "ImagebuilderDistributionConfigurationDistributionSsmParameterConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__dbf9406a02e9d8d24ab09288be42b978ddac1258772153f5e312d0a6911249e4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    distribution: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistribution, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__7d9697a0b541a66c56ee35ebaf439c207593ed9eec21b39abc2de9075c07cdce(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f3e36b1e9a3dc1c0da85d8bbdf688efd4baf24191e1f9918bbd136fc9e3899(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistribution, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12278dcf5998cdec378ae0f2049558580e5df7711aba21ee70c30a2f0867031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18ff0d3ab0f1d1da0add492356bb7c8fa606ba918ab27354bf6baab84daa3ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7d18cb347dcd9a765fc12c0934b0d8c8fa658bf541e85e6bb1ef8ad4c6d421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8703a04faa89b9912987dc84d1e346bb040b15f02bfa930abf1935b6b003f4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddaa2fe4abc0ddc829f8efc988c70750542e3e04ec0443237b98254a44a95b0e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570a8a05da5f90d307b9a03f726daab02aa2c2e04e60864a33b82c5dcf501283(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc76873f2f2810573080e83394fe3e759a5a8c6164afb0620318526e3283143(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    distribution: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistribution, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063fe33d9c39316dff8b54de0719c1dec2fc26039350935e8e43e3741b280658(
    *,
    region: builtins.str,
    ami_distribution_configuration: typing.Optional[typing.Union[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    container_distribution_configuration: typing.Optional[typing.Union[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    fast_launch_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    launch_template_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    license_configuration_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_export_configuration: typing.Optional[typing.Union[ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ssm_parameter_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365930475a46fc709e3b2fdff666353aca41b889eb89d9ab15ceb6a1044e59f5(
    *,
    ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    launch_permission: typing.Optional[typing.Union[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    target_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649cc94b30720e427a010c2d110b2cf51aea2f7506ff80d50a119f80dbc52dce(
    *,
    organizational_unit_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7beb0c7c43bebbf1a520d7e7f6afb6843962883412e2f2bad9f794b3caf8d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e11d4c3da7178c91a16edabfce4723f3b540252e91ea46e859674dadf4a01b0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07957831691fd971cdd1de101ce782822b0d4235317e348192d36d2de7af011d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ce50e9095128b22bfb091ae5cd3a750bca4648c754a8dda14605b8b4e24124(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f2d05899e119dab365f87c8b9b2dcc74fd8176eb20fd86fae5bff49a6426dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102ef4cb185b2963222ab648ec27c8cdfa5b4f43f5b6f115804de10f4066e326(
    value: typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfigurationLaunchPermission],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1b340b9880588a2f0fe5e1af85789842e828c4c023c8ccb0c5490362404ae5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142244f11b9a936fbc1d40f274710e5fa6b0c72605681f8ac1c637e85ade3c32(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9e8cf9f71dfc20f61c7d26c198c39d32fe611c67f842e0e1089fa6e5c5c82c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e30f4d813a6c6efe8c93349d2803463f471bf3ecde0d75531401b37c5ee87d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e784e489b03435f1e2675ba263bc5e1417bb28f4d781c94cb17dc06e5562a600(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1e1b99e71e08db2febf502294d0b77495417192be80a1613a5b399cc4c4811(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594909d63459343d637982896b5b65a7ea10e9a9588449a2ae4d23d0cfed7482(
    value: typing.Optional[ImagebuilderDistributionConfigurationDistributionAmiDistributionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983a12a8807613d8ff05848ced9ac9bec379efb096bf2d1667aa02a3189aa2c4(
    *,
    target_repository: typing.Union[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository, typing.Dict[builtins.str, typing.Any]],
    container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e39de7bda79297cf070936da34e3fa35945d6236a5c30c859a5a89d235c3c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdb495b0a41c8d5acf26415b39b6bfd0f29b12a17da9b1bbd96458a9d17eb53(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a8fe831060e6acc2857a92d8e72544aaf2ba70caeeacff4f7137fda454e5e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b52e75a2acf4fcb8b3bcc069ece64104d654e0e5f6de6774601b27b0b0e0be(
    value: typing.Optional[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14c50f36cbff43b702b3ec58f837ffe5dd6aa37bd9755821fdd63e8ed820c4b(
    *,
    repository_name: builtins.str,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e775d485e06580c54120b748d7d5519eb936d569ebe7c7bf0e7b392d7c754d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048c2e8632b731e31099fd7556fc32a7a14c168d1a0ad0ebaab9d1261e524fb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618cba5cb26aaee1fe08e8b6eb99be7d4572aa764f4f01d06f06c1d218d47bc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5961510166f1c58737edc47c347afc4337dc4026d7cb2c09cd6b09f60ff605a0(
    value: typing.Optional[ImagebuilderDistributionConfigurationDistributionContainerDistributionConfigurationTargetRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9631b846bf5147e575ffeab8f2d5d41588f113fb04467322489e6d6dbd0ba72f(
    *,
    account_id: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    launch_template: typing.Optional[typing.Union[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    max_parallel_launches: typing.Optional[jsii.Number] = None,
    snapshot_configuration: typing.Optional[typing.Union[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c1bd32bdbed69c91c6f5a6bac7bb05919ef655a8d87761282a614ba3a58ab1(
    *,
    launch_template_id: typing.Optional[builtins.str] = None,
    launch_template_name: typing.Optional[builtins.str] = None,
    launch_template_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7d364646f114de3bd1c8d6098bd017039e6d08f347ab62412e798ba8b28f6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea00c0183d92dd127c05573f8dfc5b1489bb3454cbf92ba4ec50a26bf180383b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e3d7ac810ee8cd9c10474e3b05bc5274816865470acf77feb3773daca17677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44765e87797161c1f2d75e3c5c12241ddcee58a7e5c82b572b0bac94491c9dd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc13d0fd0904b1ee87f589ad935e6e69187329ce6f2d1e0bf6cbc506877568a(
    value: typing.Optional[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationLaunchTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6dcfb9ed2f8835eb5da58e79956f289d0777d6d04a40d06bcc31cf7d8266e61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e669091db365379ae35abff9de44963d82daf3579921cb8744775d40776c65b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5bdbee20006b4e569df343fd3725380ef41fae04c9a24e02712ef92c52e7bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00cd41d8cdb4ca1a03bfd86f5ba48922eff85eedbd3582499d5bbaf56433b23(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fe44628814637164d8134b4012b5fe9066be08eb10e7439d4c460b2dfde795(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e97d7c9b39e659ed89edb133f9ac53b8ee4d0fb737a0f6cd9e4743cb5aa5413(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799d8b3dad552e5e5b9cd5e7eac8e271d4f203e031e2ef21e04c2d4875fca04d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc675ea73485ee3f0343eb9bc3bb0ec809d6b731ac8baa9e823bb30c8bdc001(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fceecdfee28c16678321dae14cc156e29dc233830e2a83544cfcccd5bf7b5d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761ee44f5acbe5ff217f83483efdef25fce8fddfb9adfd5e49ca696195a54921(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a752e7037573e976e20f764dbaf64f556e3b0e349686ca74af4bacce88ae372d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b159439eb1ac2229f816947ac4d7ad676bdfa94c9250f428a9271111b7a88d(
    *,
    target_resource_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d7164f7f9413e2ffdb3c8b805d6227f6b5d6fcc38945f3212dbf44c37ba7b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7acb9a5dd86295e63a099b86ed20fbab982107ed3f226b2ffdd4b4a6717c80a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f6f57c605be07a0c5ee4e0809dd6448d3b929511e63ddd8fa9e4aa5c90bc37(
    value: typing.Optional[ImagebuilderDistributionConfigurationDistributionFastLaunchConfigurationSnapshotConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7438538adf3e5bf300fa51dd296c1afbe826069dc0ef10fdcfebd50969f08ed(
    *,
    launch_template_id: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4b3063405766db74e279492f92a025610e13ccba65dabb7df66a747ec809b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d6ef585eaf28ccacab1f6f2aed6f30b1f64ad9dd1dfbc0fe582890465cd454(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0103186a1869a4626fd16a6ef177f23b1ea8899b9c83c748a885ecb2826d804c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8c9c7e8824990af4d37110efcb2caa32ec096601ea660759c70926f5426866(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e466bf7f5d98862d0021900eb57ea3965b9ca81212a1b01f74fff7135b7324a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b767f7ddcac0e71f1d1675132894a295f98320e2af663808997c25eef55cc160(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8726ab07313c941145e0c4606dbda8f83d9b31b3bfa4573a166bcce09b5a4ea4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3777acaf1eb94b3acc1e595408c2e6e8e906006fd4da96b7e0387bf4d569891(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61f513369839d16ef0dcade2ab6b1085e794d4806930de819bdcbcc204630f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a28c9375337e2c18565e24742ddfd3238afdde9604a96c22190536e2114cba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20103621cd5e1f44603e92fa995964e46ef20cdf7c6b684b91d760acef8a30d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f062a426493be6397d9ee2d0686a38c32bfa843819588428bf9473e16e64da33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8ba90d49c805e99a392170c64e6dca6228ba99f6b3650a9c4998a625f81012(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525f691c4d29d87bc99e2a24d6569470155b13fcaf77f56582b943f472ea2b05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de4e8ace12f8b11e501a3855f6c09d887c672eba369f54fb24a894d5a565fe1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee95e6e4b50b00abc50ef21f0145374ec04ab736a7d1a809a3583b6fd94c9713(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5f14ffeafd21e9324011af0d1c3785e9e77f828e39526c36009fe729863891(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistribution]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9f291a5b02ffe2d6124b9b234b7f6de84c7cc68f17f88cc0eb6b8ed8223358(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec99a14ec86003cc9b604e9570aea8dea2c9c95aadc765a98a481a981d37793(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistributionFastLaunchConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c04481dc822392440e4c7f05d57880cc3a4776efa5b165074bb3942645a6c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistributionLaunchTemplateConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfb8f277214e84d25bcab350eaa7ac096932eec3df17c60bcd5805382104d0a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1733359519129e79fa0922976189193b00b83bf9bcab1876ddec7a09b58504e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fafeee3d705286a511038b5583ecc936a4341d0fbc710b564ae4abae5861644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ce2ac20a5088a636c97dd1ecc2e0a8121cf7c0970506077ba6a3cbd59acb8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistribution]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db405fd4471d613bb5a55b59a8d7128b1b07219c24ed2eabaf18fb556c436277(
    *,
    disk_image_format: builtins.str,
    role_name: builtins.str,
    s3_bucket: builtins.str,
    s3_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae28a6ca719efb5e061134c996dc73ed65c6375a982cce78ca774ffc5e60b60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f4c2aa8343e20d843cd878b25af7f2c7479d2642bcc2429304e054962a7c00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdbaa223402a108138d432c3d581933d6ce453999bc98bd211feaee36eb356a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7117c9717732a34f0b6d9440ed62e6ed16a68fce19889928624c8b214cf3256(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab8fe5e3b009d8cc8518161104410833601178289e033a142b49d4235e17176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2288ced51012314e92ae57019a65f762c9ae9e009f82fd38b89e3961e27dc7df(
    value: typing.Optional[ImagebuilderDistributionConfigurationDistributionS3ExportConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827f2977d1f17d7099e6865eed3d82eb13723e4f48bde975c6b9a91f12234892(
    *,
    parameter_name: builtins.str,
    ami_account_id: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a884a23226cd533335420f0c513828e1fedba0c95bc469d676d909b79edce71d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca0c5d1221417a048cd96de64021e67f7bf26cee576798efc2a57a7fe9705a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9b951e0edd184fa2161093d1f48b21907cd455fb6f008e7dd27748fe3c8231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec72a1ea8a37382ac9c5d402e8ad525815cdd4c158248d0f86ec6643eb16f92(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9a2d57c62ed23aaca96782d9d9d9288cbfea64418a9a6a379f5e237f5d64f9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff00b8082c3b6674d781ff13b93545a9ddb35509051ef8a3a3ebc3ea6cdda42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6403fb444a60da08f850a5d405d0e302a6a55aa334291769b26a9351c7e5b69b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ad6d0956fb2cf43fe8ec94a6f89aee34c9bb2b642a5488b2d6096a1793296f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95954cbb2af363a0e899713c6715993b31a1575086724b7949994ded03422797(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986aba66f0f367fb3b3adf4f8ce1cf232deaef5828edf5b36ddf82b66cfa43ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb2913bb8246cfca33ce7d1ed5500e9eff5f1ec1b3553f4c33255a3be5d3738(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderDistributionConfigurationDistributionSsmParameterConfiguration]],
) -> None:
    """Type checking stubs"""
    pass
