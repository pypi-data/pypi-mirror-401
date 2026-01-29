r'''
# `aws_iot_indexing_configuration`

Refer to the Terraform Registry for docs: [`aws_iot_indexing_configuration`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration).
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


class IotIndexingConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration aws_iot_indexing_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        thing_group_indexing_configuration: typing.Optional[typing.Union["IotIndexingConfigurationThingGroupIndexingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        thing_indexing_configuration: typing.Optional[typing.Union["IotIndexingConfigurationThingIndexingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration aws_iot_indexing_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#id IotIndexingConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#region IotIndexingConfiguration#region}
        :param thing_group_indexing_configuration: thing_group_indexing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_group_indexing_configuration IotIndexingConfiguration#thing_group_indexing_configuration}
        :param thing_indexing_configuration: thing_indexing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_indexing_configuration IotIndexingConfiguration#thing_indexing_configuration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4bb7478324957bcc0486b05ebfe509a5312d7f196bb4645121b92b22dccccd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IotIndexingConfigurationConfig(
            id=id,
            region=region,
            thing_group_indexing_configuration=thing_group_indexing_configuration,
            thing_indexing_configuration=thing_indexing_configuration,
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
        '''Generates CDKTF code for importing a IotIndexingConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IotIndexingConfiguration to import.
        :param import_from_id: The id of the existing IotIndexingConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IotIndexingConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35918e075fa147014f0f47f51e674229da9a1f68c2f732cf87ddecd4d1a6b6c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putThingGroupIndexingConfiguration")
    def put_thing_group_indexing_configuration(
        self,
        *,
        thing_group_indexing_mode: builtins.str,
        custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingGroupIndexingConfigurationCustomField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingGroupIndexingConfigurationManagedField", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param thing_group_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_group_indexing_mode IotIndexingConfiguration#thing_group_indexing_mode}.
        :param custom_field: custom_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        :param managed_field: managed_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        '''
        value = IotIndexingConfigurationThingGroupIndexingConfiguration(
            thing_group_indexing_mode=thing_group_indexing_mode,
            custom_field=custom_field,
            managed_field=managed_field,
        )

        return typing.cast(None, jsii.invoke(self, "putThingGroupIndexingConfiguration", [value]))

    @jsii.member(jsii_name="putThingIndexingConfiguration")
    def put_thing_indexing_configuration(
        self,
        *,
        thing_indexing_mode: builtins.str,
        custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingIndexingConfigurationCustomField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        device_defender_indexing_mode: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["IotIndexingConfigurationThingIndexingConfigurationFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingIndexingConfigurationManagedField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        named_shadow_indexing_mode: typing.Optional[builtins.str] = None,
        thing_connectivity_indexing_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param thing_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_indexing_mode IotIndexingConfiguration#thing_indexing_mode}.
        :param custom_field: custom_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        :param device_defender_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#device_defender_indexing_mode IotIndexingConfiguration#device_defender_indexing_mode}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#filter IotIndexingConfiguration#filter}
        :param managed_field: managed_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        :param named_shadow_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#named_shadow_indexing_mode IotIndexingConfiguration#named_shadow_indexing_mode}.
        :param thing_connectivity_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_connectivity_indexing_mode IotIndexingConfiguration#thing_connectivity_indexing_mode}.
        '''
        value = IotIndexingConfigurationThingIndexingConfiguration(
            thing_indexing_mode=thing_indexing_mode,
            custom_field=custom_field,
            device_defender_indexing_mode=device_defender_indexing_mode,
            filter=filter,
            managed_field=managed_field,
            named_shadow_indexing_mode=named_shadow_indexing_mode,
            thing_connectivity_indexing_mode=thing_connectivity_indexing_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putThingIndexingConfiguration", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetThingGroupIndexingConfiguration")
    def reset_thing_group_indexing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThingGroupIndexingConfiguration", []))

    @jsii.member(jsii_name="resetThingIndexingConfiguration")
    def reset_thing_indexing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThingIndexingConfiguration", []))

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
    @jsii.member(jsii_name="thingGroupIndexingConfiguration")
    def thing_group_indexing_configuration(
        self,
    ) -> "IotIndexingConfigurationThingGroupIndexingConfigurationOutputReference":
        return typing.cast("IotIndexingConfigurationThingGroupIndexingConfigurationOutputReference", jsii.get(self, "thingGroupIndexingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="thingIndexingConfiguration")
    def thing_indexing_configuration(
        self,
    ) -> "IotIndexingConfigurationThingIndexingConfigurationOutputReference":
        return typing.cast("IotIndexingConfigurationThingIndexingConfigurationOutputReference", jsii.get(self, "thingIndexingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="thingGroupIndexingConfigurationInput")
    def thing_group_indexing_configuration_input(
        self,
    ) -> typing.Optional["IotIndexingConfigurationThingGroupIndexingConfiguration"]:
        return typing.cast(typing.Optional["IotIndexingConfigurationThingGroupIndexingConfiguration"], jsii.get(self, "thingGroupIndexingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="thingIndexingConfigurationInput")
    def thing_indexing_configuration_input(
        self,
    ) -> typing.Optional["IotIndexingConfigurationThingIndexingConfiguration"]:
        return typing.cast(typing.Optional["IotIndexingConfigurationThingIndexingConfiguration"], jsii.get(self, "thingIndexingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6d063481b366ee0493bda43a1a1e8fa39ea205261f045166c7d95763f1c2a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b8f57056cbcf2578318b4efaa1b156e2cfbddf95f834bbdc85fe2a293e0f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "region": "region",
        "thing_group_indexing_configuration": "thingGroupIndexingConfiguration",
        "thing_indexing_configuration": "thingIndexingConfiguration",
    },
)
class IotIndexingConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        thing_group_indexing_configuration: typing.Optional[typing.Union["IotIndexingConfigurationThingGroupIndexingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        thing_indexing_configuration: typing.Optional[typing.Union["IotIndexingConfigurationThingIndexingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#id IotIndexingConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#region IotIndexingConfiguration#region}
        :param thing_group_indexing_configuration: thing_group_indexing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_group_indexing_configuration IotIndexingConfiguration#thing_group_indexing_configuration}
        :param thing_indexing_configuration: thing_indexing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_indexing_configuration IotIndexingConfiguration#thing_indexing_configuration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(thing_group_indexing_configuration, dict):
            thing_group_indexing_configuration = IotIndexingConfigurationThingGroupIndexingConfiguration(**thing_group_indexing_configuration)
        if isinstance(thing_indexing_configuration, dict):
            thing_indexing_configuration = IotIndexingConfigurationThingIndexingConfiguration(**thing_indexing_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a1382a1da4dfb1e14031629e48cb070458443889ea743413744cb266c4a6bd8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument thing_group_indexing_configuration", value=thing_group_indexing_configuration, expected_type=type_hints["thing_group_indexing_configuration"])
            check_type(argname="argument thing_indexing_configuration", value=thing_indexing_configuration, expected_type=type_hints["thing_indexing_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if thing_group_indexing_configuration is not None:
            self._values["thing_group_indexing_configuration"] = thing_group_indexing_configuration
        if thing_indexing_configuration is not None:
            self._values["thing_indexing_configuration"] = thing_indexing_configuration

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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#id IotIndexingConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#region IotIndexingConfiguration#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thing_group_indexing_configuration(
        self,
    ) -> typing.Optional["IotIndexingConfigurationThingGroupIndexingConfiguration"]:
        '''thing_group_indexing_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_group_indexing_configuration IotIndexingConfiguration#thing_group_indexing_configuration}
        '''
        result = self._values.get("thing_group_indexing_configuration")
        return typing.cast(typing.Optional["IotIndexingConfigurationThingGroupIndexingConfiguration"], result)

    @builtins.property
    def thing_indexing_configuration(
        self,
    ) -> typing.Optional["IotIndexingConfigurationThingIndexingConfiguration"]:
        '''thing_indexing_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_indexing_configuration IotIndexingConfiguration#thing_indexing_configuration}
        '''
        result = self._values.get("thing_indexing_configuration")
        return typing.cast(typing.Optional["IotIndexingConfigurationThingIndexingConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "thing_group_indexing_mode": "thingGroupIndexingMode",
        "custom_field": "customField",
        "managed_field": "managedField",
    },
)
class IotIndexingConfigurationThingGroupIndexingConfiguration:
    def __init__(
        self,
        *,
        thing_group_indexing_mode: builtins.str,
        custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingGroupIndexingConfigurationCustomField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingGroupIndexingConfigurationManagedField", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param thing_group_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_group_indexing_mode IotIndexingConfiguration#thing_group_indexing_mode}.
        :param custom_field: custom_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        :param managed_field: managed_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a974ef1c9b5f792c6f69abb3cc7239b411752676e67161906c9c85a396320c)
            check_type(argname="argument thing_group_indexing_mode", value=thing_group_indexing_mode, expected_type=type_hints["thing_group_indexing_mode"])
            check_type(argname="argument custom_field", value=custom_field, expected_type=type_hints["custom_field"])
            check_type(argname="argument managed_field", value=managed_field, expected_type=type_hints["managed_field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "thing_group_indexing_mode": thing_group_indexing_mode,
        }
        if custom_field is not None:
            self._values["custom_field"] = custom_field
        if managed_field is not None:
            self._values["managed_field"] = managed_field

    @builtins.property
    def thing_group_indexing_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_group_indexing_mode IotIndexingConfiguration#thing_group_indexing_mode}.'''
        result = self._values.get("thing_group_indexing_mode")
        assert result is not None, "Required property 'thing_group_indexing_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingGroupIndexingConfigurationCustomField"]]]:
        '''custom_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        '''
        result = self._values.get("custom_field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingGroupIndexingConfigurationCustomField"]]], result)

    @builtins.property
    def managed_field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingGroupIndexingConfigurationManagedField"]]]:
        '''managed_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        '''
        result = self._values.get("managed_field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingGroupIndexingConfigurationManagedField"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingGroupIndexingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationCustomField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class IotIndexingConfigurationThingGroupIndexingConfigurationCustomField:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7c82256ad06a0e51e82e6ba9b27367a1456ed6b65c00a9075d2e9d89e2c849)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingGroupIndexingConfigurationCustomField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc7366e923e16851cb296aaa5d30099e4971be9a4685a9657c40dece3d0f3b68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14fdc0d2874fc8c46a521aba581202fe5762920bd09aca0ec0a4b3f6818c6222)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1551c6f5d8ef38101ab2b9957d8f562f3d5a010ca4249a736c89e5053da0ef2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4af2aecabc363025fc8e34ccf78bb2bd7e29b645850a121de38ed7c3d7b37132)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1b9d82315e9e78239260433da11adf2b01a10b54d265b2ef35d55716adbef18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03492294e9d758e8e6df98de721ace6e6f4ae6bbe9ba30733c1226378ce790e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66009ed3250f87634f5dd823a5cd99449cbc84cb2a1556b147a1d75e2faa40ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d253aad5f22d306c6950704f6b540d5cbfecc28c33d70c44d6f85992e9848c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518347e1c3250b5d7efbab0efc99208e0b80505388b84d9256b095af33d4fbb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54453b9419e5dfa3807a05f5f069b334efc151fa6a7a6bc23b4187578079af7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationManagedField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class IotIndexingConfigurationThingGroupIndexingConfigurationManagedField:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63213a2c51f8963e6691faa1a4d280d265cb359ba3413dece02ee004c6538362)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingGroupIndexingConfigurationManagedField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fbd69f1dd56e1b97ea7d7620b429a514db4f4d03fb4d5b0c48c4ef502d810e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb7871608b60192f62cb496046c135f4febdd725312d316d634a04f9bd7e5ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58507f667d6a3b072baf7e23401c1ecf9ec842fbe2543179132f62349659296)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cdc67947808325491ff082fa3833d680dae235cfd1993258732b12d621ebac3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a10a961502d6f607a8b0cf1b04403392e3e7c8c53327e5a78966b0135bfab5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea934dcf9b1b36511e3ba89a6d81b37aa75cc32b281aec7ff6516071253e48d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c1deb44b152f2f18a372521824fd968239f05ef54992163421ec367e402e10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c293c27c3fd05888ed617221585d403f58946a0608e2e6d16a6b25d87edac6e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06370f95d2fa24ddc5c0b9a0e9b43766b2bd23a900f8bd5fd16cd45988c6b751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e591f7526ddf9dcea4e01ad000b0f82413674a938deb1c1fa472b0d48162439f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingGroupIndexingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingGroupIndexingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b3963cafba85a95913b09058508aba6ead2e5aa368528da137f18a8df24beb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomField")
    def put_custom_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bbb4104a9aa32dbef851fa79e53e621e3eea05ae46b2e767b7c74fbbc8b151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomField", [value]))

    @jsii.member(jsii_name="putManagedField")
    def put_managed_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f208eabbac55c54ce63ac16ae9791895095d2ad84080da9cc9e9ce98b202c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedField", [value]))

    @jsii.member(jsii_name="resetCustomField")
    def reset_custom_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomField", []))

    @jsii.member(jsii_name="resetManagedField")
    def reset_managed_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedField", []))

    @builtins.property
    @jsii.member(jsii_name="customField")
    def custom_field(
        self,
    ) -> IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldList:
        return typing.cast(IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldList, jsii.get(self, "customField"))

    @builtins.property
    @jsii.member(jsii_name="managedField")
    def managed_field(
        self,
    ) -> IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldList:
        return typing.cast(IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldList, jsii.get(self, "managedField"))

    @builtins.property
    @jsii.member(jsii_name="customFieldInput")
    def custom_field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]], jsii.get(self, "customFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="managedFieldInput")
    def managed_field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]], jsii.get(self, "managedFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="thingGroupIndexingModeInput")
    def thing_group_indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thingGroupIndexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="thingGroupIndexingMode")
    def thing_group_indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thingGroupIndexingMode"))

    @thing_group_indexing_mode.setter
    def thing_group_indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07e0a8a498873e40facc3242c7ea7ca8b3eceaa8dc8297ad257511e17de27d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thingGroupIndexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotIndexingConfigurationThingGroupIndexingConfiguration]:
        return typing.cast(typing.Optional[IotIndexingConfigurationThingGroupIndexingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotIndexingConfigurationThingGroupIndexingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b1620dbdea94c081de016ebb0368df293845a980ce064ba55b8eefbe4432dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "thing_indexing_mode": "thingIndexingMode",
        "custom_field": "customField",
        "device_defender_indexing_mode": "deviceDefenderIndexingMode",
        "filter": "filter",
        "managed_field": "managedField",
        "named_shadow_indexing_mode": "namedShadowIndexingMode",
        "thing_connectivity_indexing_mode": "thingConnectivityIndexingMode",
    },
)
class IotIndexingConfigurationThingIndexingConfiguration:
    def __init__(
        self,
        *,
        thing_indexing_mode: builtins.str,
        custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingIndexingConfigurationCustomField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        device_defender_indexing_mode: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["IotIndexingConfigurationThingIndexingConfigurationFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotIndexingConfigurationThingIndexingConfigurationManagedField", typing.Dict[builtins.str, typing.Any]]]]] = None,
        named_shadow_indexing_mode: typing.Optional[builtins.str] = None,
        thing_connectivity_indexing_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param thing_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_indexing_mode IotIndexingConfiguration#thing_indexing_mode}.
        :param custom_field: custom_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        :param device_defender_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#device_defender_indexing_mode IotIndexingConfiguration#device_defender_indexing_mode}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#filter IotIndexingConfiguration#filter}
        :param managed_field: managed_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        :param named_shadow_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#named_shadow_indexing_mode IotIndexingConfiguration#named_shadow_indexing_mode}.
        :param thing_connectivity_indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_connectivity_indexing_mode IotIndexingConfiguration#thing_connectivity_indexing_mode}.
        '''
        if isinstance(filter, dict):
            filter = IotIndexingConfigurationThingIndexingConfigurationFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98651ae576fbe554ad2c8495a65ab72e4e6169ececbc964312260863eb68dd2)
            check_type(argname="argument thing_indexing_mode", value=thing_indexing_mode, expected_type=type_hints["thing_indexing_mode"])
            check_type(argname="argument custom_field", value=custom_field, expected_type=type_hints["custom_field"])
            check_type(argname="argument device_defender_indexing_mode", value=device_defender_indexing_mode, expected_type=type_hints["device_defender_indexing_mode"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument managed_field", value=managed_field, expected_type=type_hints["managed_field"])
            check_type(argname="argument named_shadow_indexing_mode", value=named_shadow_indexing_mode, expected_type=type_hints["named_shadow_indexing_mode"])
            check_type(argname="argument thing_connectivity_indexing_mode", value=thing_connectivity_indexing_mode, expected_type=type_hints["thing_connectivity_indexing_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "thing_indexing_mode": thing_indexing_mode,
        }
        if custom_field is not None:
            self._values["custom_field"] = custom_field
        if device_defender_indexing_mode is not None:
            self._values["device_defender_indexing_mode"] = device_defender_indexing_mode
        if filter is not None:
            self._values["filter"] = filter
        if managed_field is not None:
            self._values["managed_field"] = managed_field
        if named_shadow_indexing_mode is not None:
            self._values["named_shadow_indexing_mode"] = named_shadow_indexing_mode
        if thing_connectivity_indexing_mode is not None:
            self._values["thing_connectivity_indexing_mode"] = thing_connectivity_indexing_mode

    @builtins.property
    def thing_indexing_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_indexing_mode IotIndexingConfiguration#thing_indexing_mode}.'''
        result = self._values.get("thing_indexing_mode")
        assert result is not None, "Required property 'thing_indexing_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingIndexingConfigurationCustomField"]]]:
        '''custom_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#custom_field IotIndexingConfiguration#custom_field}
        '''
        result = self._values.get("custom_field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingIndexingConfigurationCustomField"]]], result)

    @builtins.property
    def device_defender_indexing_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#device_defender_indexing_mode IotIndexingConfiguration#device_defender_indexing_mode}.'''
        result = self._values.get("device_defender_indexing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional["IotIndexingConfigurationThingIndexingConfigurationFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#filter IotIndexingConfiguration#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["IotIndexingConfigurationThingIndexingConfigurationFilter"], result)

    @builtins.property
    def managed_field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingIndexingConfigurationManagedField"]]]:
        '''managed_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#managed_field IotIndexingConfiguration#managed_field}
        '''
        result = self._values.get("managed_field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotIndexingConfigurationThingIndexingConfigurationManagedField"]]], result)

    @builtins.property
    def named_shadow_indexing_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#named_shadow_indexing_mode IotIndexingConfiguration#named_shadow_indexing_mode}.'''
        result = self._values.get("named_shadow_indexing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thing_connectivity_indexing_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#thing_connectivity_indexing_mode IotIndexingConfiguration#thing_connectivity_indexing_mode}.'''
        result = self._values.get("thing_connectivity_indexing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingIndexingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationCustomField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class IotIndexingConfigurationThingIndexingConfigurationCustomField:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca10ca6cfe9befe524a038ed8e4889863794693f92b61f630fababb2f56d9db)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingIndexingConfigurationCustomField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotIndexingConfigurationThingIndexingConfigurationCustomFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationCustomFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6f64abcd4e191da8a89327a63ef69d31f1c8442e366ee5d7f4d215a2615fe53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotIndexingConfigurationThingIndexingConfigurationCustomFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e806a1dc39c0f001d932dab7c858b650ce9aae08b25294ddebb2e4d893e1161)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotIndexingConfigurationThingIndexingConfigurationCustomFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0578322e798d865c4d2875e83af177b459e634820099af8221d054f812a1d635)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eefa70072bb6c4abb093862f8c987a7383f95aa6f0e10bc9b125ce4c366f1be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8df13d040ebd1b60ff8f4c6e2f219d8e53e8ce161d13799245669089ed175677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef598ea45ed8f4aaa2e2e9ee226cce5628860a98491b9bfd08d02555f30d443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingIndexingConfigurationCustomFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationCustomFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b0e7fa082544442780f497c97404b6d4d3719fb4cb18a92530aa84821c1a73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa43d972a2811f4281757bc1ac3129d5bec4830c0522d828742940e9159d153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c76f5205d59238f84f241b9548313057af1a74b297899cfc89a0859088be884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationCustomField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationCustomField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationCustomField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e430d0be026b408388a8b9f9993bb0f6f3a1bbc1f87acfccb9f17c803a4686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationFilter",
    jsii_struct_bases=[],
    name_mapping={"named_shadow_names": "namedShadowNames"},
)
class IotIndexingConfigurationThingIndexingConfigurationFilter:
    def __init__(
        self,
        *,
        named_shadow_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param named_shadow_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#named_shadow_names IotIndexingConfiguration#named_shadow_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6cbb21a36a74d4684fa0d55d2fd3f73c2bb21aa92e8c2a0fbf1c5ae519c704)
            check_type(argname="argument named_shadow_names", value=named_shadow_names, expected_type=type_hints["named_shadow_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if named_shadow_names is not None:
            self._values["named_shadow_names"] = named_shadow_names

    @builtins.property
    def named_shadow_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#named_shadow_names IotIndexingConfiguration#named_shadow_names}.'''
        result = self._values.get("named_shadow_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingIndexingConfigurationFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotIndexingConfigurationThingIndexingConfigurationFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6e8b4df0319e1b43966e9edd7aefaf18dba6aa96f56e00bc8ea35b5df1dc6cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNamedShadowNames")
    def reset_named_shadow_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamedShadowNames", []))

    @builtins.property
    @jsii.member(jsii_name="namedShadowNamesInput")
    def named_shadow_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namedShadowNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="namedShadowNames")
    def named_shadow_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "namedShadowNames"))

    @named_shadow_names.setter
    def named_shadow_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bab3b56f5ae8053c8deadeab65d075ebcbf97358c6de4f8a2921b5c494170b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namedShadowNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter]:
        return typing.cast(typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013abf5f3a1bd930c688dbe5e2c32efd0ece863c905d1ed2f60cbb6a3d3f572b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationManagedField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class IotIndexingConfigurationThingIndexingConfigurationManagedField:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922cb527b520bf6d9918f2dc7aba58e0f35b1e61b80c8055afedb360182f8683)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#name IotIndexingConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#type IotIndexingConfiguration#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotIndexingConfigurationThingIndexingConfigurationManagedField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotIndexingConfigurationThingIndexingConfigurationManagedFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationManagedFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8ec519934844c7a9e515cd9ad3dd3010bb225c6716e5de97707840488d874ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotIndexingConfigurationThingIndexingConfigurationManagedFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__994ffde2180d4aa07e8b631a10d28fc22a248faef53e6f45b71e0bfe95aaa301)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotIndexingConfigurationThingIndexingConfigurationManagedFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bddeb7089bb267f75acde7c0e65a72a2a5ada101dabc69ba6144a5009145ce67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8eab660afa2f2749bf196757751b84316e77a9af2f41b151ee18f4c8042c2ec4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad3487c4d09ec553389c7e97b7ea2998339573be75de827ac0ae168084025205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c195506a0fde313b31ff000fb52ce5f6e63a35cd35d38298a5de155d1c8dcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingIndexingConfigurationManagedFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationManagedFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__447cb7be017630625f23d6e3af613e7d7cb5393fa634f885b3c617d9e9bf4b91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd14b44bf1b4850fdd36a664cf9fee6b46a99336dae5ac039ed01972de28582f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd4320e4b5ebfe95c40e901159ffcd09c55e626f7e66703713ee22c5d3e9cba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationManagedField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationManagedField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationManagedField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642dc2dd0e2d113a26228fd55417eaee0420fe5505f625a8ba29d7bfe4bfc131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotIndexingConfigurationThingIndexingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotIndexingConfiguration.IotIndexingConfigurationThingIndexingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80900a06e7d994566231c1b42df6fadc1db0a67f2d982081ab63cca06af555a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomField")
    def put_custom_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0542b043c40c5110d0e6a3748eba840045da6282703a0a1b918eff2b1f7ed48a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomField", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        named_shadow_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param named_shadow_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_indexing_configuration#named_shadow_names IotIndexingConfiguration#named_shadow_names}.
        '''
        value = IotIndexingConfigurationThingIndexingConfigurationFilter(
            named_shadow_names=named_shadow_names
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putManagedField")
    def put_managed_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c33e2ef1bcff1e896078c3b24c3dfce5200f605e43f0716ee7af2cc6c699875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedField", [value]))

    @jsii.member(jsii_name="resetCustomField")
    def reset_custom_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomField", []))

    @jsii.member(jsii_name="resetDeviceDefenderIndexingMode")
    def reset_device_defender_indexing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceDefenderIndexingMode", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetManagedField")
    def reset_managed_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedField", []))

    @jsii.member(jsii_name="resetNamedShadowIndexingMode")
    def reset_named_shadow_indexing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamedShadowIndexingMode", []))

    @jsii.member(jsii_name="resetThingConnectivityIndexingMode")
    def reset_thing_connectivity_indexing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThingConnectivityIndexingMode", []))

    @builtins.property
    @jsii.member(jsii_name="customField")
    def custom_field(
        self,
    ) -> IotIndexingConfigurationThingIndexingConfigurationCustomFieldList:
        return typing.cast(IotIndexingConfigurationThingIndexingConfigurationCustomFieldList, jsii.get(self, "customField"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> IotIndexingConfigurationThingIndexingConfigurationFilterOutputReference:
        return typing.cast(IotIndexingConfigurationThingIndexingConfigurationFilterOutputReference, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="managedField")
    def managed_field(
        self,
    ) -> IotIndexingConfigurationThingIndexingConfigurationManagedFieldList:
        return typing.cast(IotIndexingConfigurationThingIndexingConfigurationManagedFieldList, jsii.get(self, "managedField"))

    @builtins.property
    @jsii.member(jsii_name="customFieldInput")
    def custom_field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]], jsii.get(self, "customFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceDefenderIndexingModeInput")
    def device_defender_indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceDefenderIndexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter]:
        return typing.cast(typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="managedFieldInput")
    def managed_field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]], jsii.get(self, "managedFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="namedShadowIndexingModeInput")
    def named_shadow_indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namedShadowIndexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="thingConnectivityIndexingModeInput")
    def thing_connectivity_indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thingConnectivityIndexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="thingIndexingModeInput")
    def thing_indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thingIndexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceDefenderIndexingMode")
    def device_defender_indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceDefenderIndexingMode"))

    @device_defender_indexing_mode.setter
    def device_defender_indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69056d655abad9e55f7171d5291af9cb385fabdf35dacefe1be5beef25d9f0cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceDefenderIndexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namedShadowIndexingMode")
    def named_shadow_indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namedShadowIndexingMode"))

    @named_shadow_indexing_mode.setter
    def named_shadow_indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691b77ca17d7a047171a810a67f9e539d3fe12f99dea609bd4f8bb276fb0959f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namedShadowIndexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thingConnectivityIndexingMode")
    def thing_connectivity_indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thingConnectivityIndexingMode"))

    @thing_connectivity_indexing_mode.setter
    def thing_connectivity_indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7400625395144c258d68cba0b682fb41fe2fd41e5fefe49d8fda6b89042e6fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thingConnectivityIndexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thingIndexingMode")
    def thing_indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thingIndexingMode"))

    @thing_indexing_mode.setter
    def thing_indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864d4bb0ec6824d5a1b57b9089912c5cfdad433f5e36ab51c1951ddfdee4d06b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thingIndexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotIndexingConfigurationThingIndexingConfiguration]:
        return typing.cast(typing.Optional[IotIndexingConfigurationThingIndexingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotIndexingConfigurationThingIndexingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cd33a1c05cb1b5be499132e06869866cc424e7fc9af4a09f8900d5e960eb5aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IotIndexingConfiguration",
    "IotIndexingConfigurationConfig",
    "IotIndexingConfigurationThingGroupIndexingConfiguration",
    "IotIndexingConfigurationThingGroupIndexingConfigurationCustomField",
    "IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldList",
    "IotIndexingConfigurationThingGroupIndexingConfigurationCustomFieldOutputReference",
    "IotIndexingConfigurationThingGroupIndexingConfigurationManagedField",
    "IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldList",
    "IotIndexingConfigurationThingGroupIndexingConfigurationManagedFieldOutputReference",
    "IotIndexingConfigurationThingGroupIndexingConfigurationOutputReference",
    "IotIndexingConfigurationThingIndexingConfiguration",
    "IotIndexingConfigurationThingIndexingConfigurationCustomField",
    "IotIndexingConfigurationThingIndexingConfigurationCustomFieldList",
    "IotIndexingConfigurationThingIndexingConfigurationCustomFieldOutputReference",
    "IotIndexingConfigurationThingIndexingConfigurationFilter",
    "IotIndexingConfigurationThingIndexingConfigurationFilterOutputReference",
    "IotIndexingConfigurationThingIndexingConfigurationManagedField",
    "IotIndexingConfigurationThingIndexingConfigurationManagedFieldList",
    "IotIndexingConfigurationThingIndexingConfigurationManagedFieldOutputReference",
    "IotIndexingConfigurationThingIndexingConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__8f4bb7478324957bcc0486b05ebfe509a5312d7f196bb4645121b92b22dccccd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    thing_group_indexing_configuration: typing.Optional[typing.Union[IotIndexingConfigurationThingGroupIndexingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    thing_indexing_configuration: typing.Optional[typing.Union[IotIndexingConfigurationThingIndexingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__35918e075fa147014f0f47f51e674229da9a1f68c2f732cf87ddecd4d1a6b6c5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6d063481b366ee0493bda43a1a1e8fa39ea205261f045166c7d95763f1c2a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b8f57056cbcf2578318b4efaa1b156e2cfbddf95f834bbdc85fe2a293e0f9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1382a1da4dfb1e14031629e48cb070458443889ea743413744cb266c4a6bd8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    thing_group_indexing_configuration: typing.Optional[typing.Union[IotIndexingConfigurationThingGroupIndexingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    thing_indexing_configuration: typing.Optional[typing.Union[IotIndexingConfigurationThingIndexingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a974ef1c9b5f792c6f69abb3cc7239b411752676e67161906c9c85a396320c(
    *,
    thing_group_indexing_mode: builtins.str,
    custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]]] = None,
    managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7c82256ad06a0e51e82e6ba9b27367a1456ed6b65c00a9075d2e9d89e2c849(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7366e923e16851cb296aaa5d30099e4971be9a4685a9657c40dece3d0f3b68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14fdc0d2874fc8c46a521aba581202fe5762920bd09aca0ec0a4b3f6818c6222(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1551c6f5d8ef38101ab2b9957d8f562f3d5a010ca4249a736c89e5053da0ef2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af2aecabc363025fc8e34ccf78bb2bd7e29b645850a121de38ed7c3d7b37132(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b9d82315e9e78239260433da11adf2b01a10b54d265b2ef35d55716adbef18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03492294e9d758e8e6df98de721ace6e6f4ae6bbe9ba30733c1226378ce790e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66009ed3250f87634f5dd823a5cd99449cbc84cb2a1556b147a1d75e2faa40ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d253aad5f22d306c6950704f6b540d5cbfecc28c33d70c44d6f85992e9848c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518347e1c3250b5d7efbab0efc99208e0b80505388b84d9256b095af33d4fbb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54453b9419e5dfa3807a05f5f069b334efc151fa6a7a6bc23b4187578079af7a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationCustomField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63213a2c51f8963e6691faa1a4d280d265cb359ba3413dece02ee004c6538362(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fbd69f1dd56e1b97ea7d7620b429a514db4f4d03fb4d5b0c48c4ef502d810e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb7871608b60192f62cb496046c135f4febdd725312d316d634a04f9bd7e5ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58507f667d6a3b072baf7e23401c1ecf9ec842fbe2543179132f62349659296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdc67947808325491ff082fa3833d680dae235cfd1993258732b12d621ebac3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a10a961502d6f607a8b0cf1b04403392e3e7c8c53327e5a78966b0135bfab5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea934dcf9b1b36511e3ba89a6d81b37aa75cc32b281aec7ff6516071253e48d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c1deb44b152f2f18a372521824fd968239f05ef54992163421ec367e402e10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c293c27c3fd05888ed617221585d403f58946a0608e2e6d16a6b25d87edac6e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06370f95d2fa24ddc5c0b9a0e9b43766b2bd23a900f8bd5fd16cd45988c6b751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e591f7526ddf9dcea4e01ad000b0f82413674a938deb1c1fa472b0d48162439f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingGroupIndexingConfigurationManagedField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3963cafba85a95913b09058508aba6ead2e5aa368528da137f18a8df24beb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bbb4104a9aa32dbef851fa79e53e621e3eea05ae46b2e767b7c74fbbc8b151(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f208eabbac55c54ce63ac16ae9791895095d2ad84080da9cc9e9ce98b202c6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingGroupIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07e0a8a498873e40facc3242c7ea7ca8b3eceaa8dc8297ad257511e17de27d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b1620dbdea94c081de016ebb0368df293845a980ce064ba55b8eefbe4432dc(
    value: typing.Optional[IotIndexingConfigurationThingGroupIndexingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98651ae576fbe554ad2c8495a65ab72e4e6169ececbc964312260863eb68dd2(
    *,
    thing_indexing_mode: builtins.str,
    custom_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]]] = None,
    device_defender_indexing_mode: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[IotIndexingConfigurationThingIndexingConfigurationFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]]] = None,
    named_shadow_indexing_mode: typing.Optional[builtins.str] = None,
    thing_connectivity_indexing_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca10ca6cfe9befe524a038ed8e4889863794693f92b61f630fababb2f56d9db(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f64abcd4e191da8a89327a63ef69d31f1c8442e366ee5d7f4d215a2615fe53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e806a1dc39c0f001d932dab7c858b650ce9aae08b25294ddebb2e4d893e1161(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0578322e798d865c4d2875e83af177b459e634820099af8221d054f812a1d635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eefa70072bb6c4abb093862f8c987a7383f95aa6f0e10bc9b125ce4c366f1be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df13d040ebd1b60ff8f4c6e2f219d8e53e8ce161d13799245669089ed175677(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef598ea45ed8f4aaa2e2e9ee226cce5628860a98491b9bfd08d02555f30d443(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationCustomField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b0e7fa082544442780f497c97404b6d4d3719fb4cb18a92530aa84821c1a73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa43d972a2811f4281757bc1ac3129d5bec4830c0522d828742940e9159d153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c76f5205d59238f84f241b9548313057af1a74b297899cfc89a0859088be884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e430d0be026b408388a8b9f9993bb0f6f3a1bbc1f87acfccb9f17c803a4686(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationCustomField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6cbb21a36a74d4684fa0d55d2fd3f73c2bb21aa92e8c2a0fbf1c5ae519c704(
    *,
    named_shadow_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e8b4df0319e1b43966e9edd7aefaf18dba6aa96f56e00bc8ea35b5df1dc6cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bab3b56f5ae8053c8deadeab65d075ebcbf97358c6de4f8a2921b5c494170b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013abf5f3a1bd930c688dbe5e2c32efd0ece863c905d1ed2f60cbb6a3d3f572b(
    value: typing.Optional[IotIndexingConfigurationThingIndexingConfigurationFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922cb527b520bf6d9918f2dc7aba58e0f35b1e61b80c8055afedb360182f8683(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ec519934844c7a9e515cd9ad3dd3010bb225c6716e5de97707840488d874ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994ffde2180d4aa07e8b631a10d28fc22a248faef53e6f45b71e0bfe95aaa301(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddeb7089bb267f75acde7c0e65a72a2a5ada101dabc69ba6144a5009145ce67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eab660afa2f2749bf196757751b84316e77a9af2f41b151ee18f4c8042c2ec4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3487c4d09ec553389c7e97b7ea2998339573be75de827ac0ae168084025205(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c195506a0fde313b31ff000fb52ce5f6e63a35cd35d38298a5de155d1c8dcd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotIndexingConfigurationThingIndexingConfigurationManagedField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447cb7be017630625f23d6e3af613e7d7cb5393fa634f885b3c617d9e9bf4b91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd14b44bf1b4850fdd36a664cf9fee6b46a99336dae5ac039ed01972de28582f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd4320e4b5ebfe95c40e901159ffcd09c55e626f7e66703713ee22c5d3e9cba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642dc2dd0e2d113a26228fd55417eaee0420fe5505f625a8ba29d7bfe4bfc131(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotIndexingConfigurationThingIndexingConfigurationManagedField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80900a06e7d994566231c1b42df6fadc1db0a67f2d982081ab63cca06af555a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0542b043c40c5110d0e6a3748eba840045da6282703a0a1b918eff2b1f7ed48a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationCustomField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c33e2ef1bcff1e896078c3b24c3dfce5200f605e43f0716ee7af2cc6c699875(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotIndexingConfigurationThingIndexingConfigurationManagedField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69056d655abad9e55f7171d5291af9cb385fabdf35dacefe1be5beef25d9f0cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691b77ca17d7a047171a810a67f9e539d3fe12f99dea609bd4f8bb276fb0959f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7400625395144c258d68cba0b682fb41fe2fd41e5fefe49d8fda6b89042e6fef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864d4bb0ec6824d5a1b57b9089912c5cfdad433f5e36ab51c1951ddfdee4d06b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd33a1c05cb1b5be499132e06869866cc424e7fc9af4a09f8900d5e960eb5aa(
    value: typing.Optional[IotIndexingConfigurationThingIndexingConfiguration],
) -> None:
    """Type checking stubs"""
    pass
