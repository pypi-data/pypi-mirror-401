r'''
# `aws_lexv2models_slot_type`

Refer to the Terraform Registry for docs: [`aws_lexv2models_slot_type`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type).
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


class Lexv2ModelsSlotType(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotType",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type aws_lexv2models_slot_type}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bot_id: builtins.str,
        bot_version: builtins.str,
        locale_id: builtins.str,
        name: builtins.str,
        composite_slot_type_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeCompositeSlotTypeSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        external_source_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeExternalSourceSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parent_slot_type_signature: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        slot_type_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeSlotTypeValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["Lexv2ModelsSlotTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_selection_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeValueSelectionSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type aws_lexv2models_slot_type} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bot_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#bot_id Lexv2ModelsSlotType#bot_id}.
        :param bot_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#bot_version Lexv2ModelsSlotType#bot_version}.
        :param locale_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#locale_id Lexv2ModelsSlotType#locale_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#name Lexv2ModelsSlotType#name}.
        :param composite_slot_type_setting: composite_slot_type_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#composite_slot_type_setting Lexv2ModelsSlotType#composite_slot_type_setting}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#description Lexv2ModelsSlotType#description}.
        :param external_source_setting: external_source_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#external_source_setting Lexv2ModelsSlotType#external_source_setting}
        :param parent_slot_type_signature: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#parent_slot_type_signature Lexv2ModelsSlotType#parent_slot_type_signature}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#region Lexv2ModelsSlotType#region}
        :param slot_type_values: slot_type_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#slot_type_values Lexv2ModelsSlotType#slot_type_values}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#timeouts Lexv2ModelsSlotType#timeouts}
        :param value_selection_setting: value_selection_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#value_selection_setting Lexv2ModelsSlotType#value_selection_setting}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c527731b8c902f223e1183669fc92e1c3b675052577fbd05ada06b4c49805c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = Lexv2ModelsSlotTypeConfig(
            bot_id=bot_id,
            bot_version=bot_version,
            locale_id=locale_id,
            name=name,
            composite_slot_type_setting=composite_slot_type_setting,
            description=description,
            external_source_setting=external_source_setting,
            parent_slot_type_signature=parent_slot_type_signature,
            region=region,
            slot_type_values=slot_type_values,
            timeouts=timeouts,
            value_selection_setting=value_selection_setting,
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
        '''Generates CDKTF code for importing a Lexv2ModelsSlotType resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Lexv2ModelsSlotType to import.
        :param import_from_id: The id of the existing Lexv2ModelsSlotType that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Lexv2ModelsSlotType to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92054681081560fc4572940c885916e8010ccbb7089fe532fba721435a56b0eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCompositeSlotTypeSetting")
    def put_composite_slot_type_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeCompositeSlotTypeSetting", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d023da18b9dfcf57f79a157296c64add2325d65bceddd13b91e281cc0c1564e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCompositeSlotTypeSetting", [value]))

    @jsii.member(jsii_name="putExternalSourceSetting")
    def put_external_source_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeExternalSourceSetting", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b82f8aec1570349fa09f881d9b94b7ebdbce3acfbb20aad3618aa1a70e6a46a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExternalSourceSetting", [value]))

    @jsii.member(jsii_name="putSlotTypeValues")
    def put_slot_type_values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeSlotTypeValues", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d54047e60f2d0e05613e367170c1e5e756dbd224a50667a7d7f342e5f0bfee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSlotTypeValues", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#create Lexv2ModelsSlotType#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#delete Lexv2ModelsSlotType#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#update Lexv2ModelsSlotType#update}
        '''
        value = Lexv2ModelsSlotTypeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putValueSelectionSetting")
    def put_value_selection_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeValueSelectionSetting", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe9e04992f84fc637ed929b2e0c601d5c04f3530545141ec171a206a3c487ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putValueSelectionSetting", [value]))

    @jsii.member(jsii_name="resetCompositeSlotTypeSetting")
    def reset_composite_slot_type_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompositeSlotTypeSetting", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExternalSourceSetting")
    def reset_external_source_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalSourceSetting", []))

    @jsii.member(jsii_name="resetParentSlotTypeSignature")
    def reset_parent_slot_type_signature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentSlotTypeSignature", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSlotTypeValues")
    def reset_slot_type_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlotTypeValues", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetValueSelectionSetting")
    def reset_value_selection_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueSelectionSetting", []))

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
    @jsii.member(jsii_name="compositeSlotTypeSetting")
    def composite_slot_type_setting(
        self,
    ) -> "Lexv2ModelsSlotTypeCompositeSlotTypeSettingList":
        return typing.cast("Lexv2ModelsSlotTypeCompositeSlotTypeSettingList", jsii.get(self, "compositeSlotTypeSetting"))

    @builtins.property
    @jsii.member(jsii_name="externalSourceSetting")
    def external_source_setting(self) -> "Lexv2ModelsSlotTypeExternalSourceSettingList":
        return typing.cast("Lexv2ModelsSlotTypeExternalSourceSettingList", jsii.get(self, "externalSourceSetting"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="slotTypeId")
    def slot_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slotTypeId"))

    @builtins.property
    @jsii.member(jsii_name="slotTypeValues")
    def slot_type_values(self) -> "Lexv2ModelsSlotTypeSlotTypeValuesList":
        return typing.cast("Lexv2ModelsSlotTypeSlotTypeValuesList", jsii.get(self, "slotTypeValues"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "Lexv2ModelsSlotTypeTimeoutsOutputReference":
        return typing.cast("Lexv2ModelsSlotTypeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="valueSelectionSetting")
    def value_selection_setting(self) -> "Lexv2ModelsSlotTypeValueSelectionSettingList":
        return typing.cast("Lexv2ModelsSlotTypeValueSelectionSettingList", jsii.get(self, "valueSelectionSetting"))

    @builtins.property
    @jsii.member(jsii_name="botIdInput")
    def bot_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "botIdInput"))

    @builtins.property
    @jsii.member(jsii_name="botVersionInput")
    def bot_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "botVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="compositeSlotTypeSettingInput")
    def composite_slot_type_setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeCompositeSlotTypeSetting"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeCompositeSlotTypeSetting"]]], jsii.get(self, "compositeSlotTypeSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="externalSourceSettingInput")
    def external_source_setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeExternalSourceSetting"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeExternalSourceSetting"]]], jsii.get(self, "externalSourceSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="localeIdInput")
    def locale_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentSlotTypeSignatureInput")
    def parent_slot_type_signature_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentSlotTypeSignatureInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="slotTypeValuesInput")
    def slot_type_values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValues"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValues"]]], jsii.get(self, "slotTypeValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Lexv2ModelsSlotTypeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Lexv2ModelsSlotTypeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="valueSelectionSettingInput")
    def value_selection_setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeValueSelectionSetting"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeValueSelectionSetting"]]], jsii.get(self, "valueSelectionSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="botId")
    def bot_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "botId"))

    @bot_id.setter
    def bot_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f615eacceb6885be7723bfbd29a63b948e6dc1b060343c4b35ca21703c93c5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="botVersion")
    def bot_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "botVersion"))

    @bot_version.setter
    def bot_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a0ac2eb2c994523864f082b664275108a78baae5d254c8933696b3899a307c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c1d5411b98771d35e7a54f19e85ad3d8ffe9dc7af29f9c09fcd5844f32d49a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localeId")
    def locale_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localeId"))

    @locale_id.setter
    def locale_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8650deeb56abcd9e5b0a8883880051054798c1341db3a8d8bd04df3eecafd97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f1258133610e58a3ff9dd51fba44ca354d6914defcb62baedd430b3369cf51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentSlotTypeSignature")
    def parent_slot_type_signature(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentSlotTypeSignature"))

    @parent_slot_type_signature.setter
    def parent_slot_type_signature(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b39bac19c9b134e0d3a3aba6422541434a7f8429f96aa483e0c459bd3763971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentSlotTypeSignature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8fd52f885b84e7d3113db46be3d9f5a7abc1fc33bc971bcccc6bd6f93814c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeCompositeSlotTypeSetting",
    jsii_struct_bases=[],
    name_mapping={"sub_slots": "subSlots"},
)
class Lexv2ModelsSlotTypeCompositeSlotTypeSetting:
    def __init__(
        self,
        *,
        sub_slots: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param sub_slots: sub_slots block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#sub_slots Lexv2ModelsSlotType#sub_slots}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c36699cfa1b1b6fab1ef1f0e57c71fd23cb1fff722139bfdad0783f8e4507d)
            check_type(argname="argument sub_slots", value=sub_slots, expected_type=type_hints["sub_slots"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sub_slots is not None:
            self._values["sub_slots"] = sub_slots

    @builtins.property
    def sub_slots(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots"]]]:
        '''sub_slots block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#sub_slots Lexv2ModelsSlotType#sub_slots}
        '''
        result = self._values.get("sub_slots")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeCompositeSlotTypeSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lexv2ModelsSlotTypeCompositeSlotTypeSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeCompositeSlotTypeSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d07f01b8dbd7ed1ed6cafcf1f933539d6fe4ade1a7cec7392e2aa3e2d9e8671)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeCompositeSlotTypeSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e8084ecaef12b095a10dc14814a509a22a564681c3c0bbb5b4ea682021869f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeCompositeSlotTypeSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e2d8e0ebabf8c709cac54ae00d2667f793914cad288e2ada553231bc30d5d45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04b0311b91d969bf9a6cebef16bb28059beea2008fff135bf394dccb60f88ce3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9a296513f5c02320000d9b659d6ac455bbe53fd4bd02c776c8ac34444607f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeCompositeSlotTypeSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeCompositeSlotTypeSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeCompositeSlotTypeSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305cf7c72e81344fc2e79b1dcbc87d4c5a818f55bc10a53dceed0f03f4c77980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeCompositeSlotTypeSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeCompositeSlotTypeSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1ce2efa2630c87971b4fd79a73b0f511430d202ebd3bc7b8520617fd6cb6922)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSubSlots")
    def put_sub_slots(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67fd09917399b7f0e9101ac583ab9824928406b013b3b2938cd8077bcdda1b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubSlots", [value]))

    @jsii.member(jsii_name="resetSubSlots")
    def reset_sub_slots(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubSlots", []))

    @builtins.property
    @jsii.member(jsii_name="subSlots")
    def sub_slots(self) -> "Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlotsList":
        return typing.cast("Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlotsList", jsii.get(self, "subSlots"))

    @builtins.property
    @jsii.member(jsii_name="subSlotsInput")
    def sub_slots_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots"]]], jsii.get(self, "subSlotsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeCompositeSlotTypeSetting]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeCompositeSlotTypeSetting]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeCompositeSlotTypeSetting]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331a8a475e446f43361423c7a097e3d4db18438bcee89e7cd58d3292752b3792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "slot_type_id": "slotTypeId"},
)
class Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots:
    def __init__(self, *, name: builtins.str, slot_type_id: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#name Lexv2ModelsSlotType#name}.
        :param slot_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#slot_type_id Lexv2ModelsSlotType#slot_type_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f1a178ef6d37c508e8c7d9524e2a41c987a84a1be29b05d3f8aca6aa798f722)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument slot_type_id", value=slot_type_id, expected_type=type_hints["slot_type_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "slot_type_id": slot_type_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#name Lexv2ModelsSlotType#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slot_type_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#slot_type_id Lexv2ModelsSlotType#slot_type_id}.'''
        result = self._values.get("slot_type_id")
        assert result is not None, "Required property 'slot_type_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlotsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlotsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d8494995f9defde22c82bfbc7714f7c046c00b9a93654894945cf461f142f31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlotsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653a8ebdd3af400d0f5fb6f130e1e800208d185668dae76947f01966cc95a515)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlotsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11066ac3a279fb68a5dd007591b8c4c216d72cbba85dbbd884a828d86ca6f42c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50eba8a0c60112e1134775094d199c14f2ae98a5a8bef042bd4b69a622096778)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8360f5c09d1581761ac36bc90f3e8fed6943eb629adcd359056613e2eee44c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b83d2bdcceff2e0bbacb69146764fd8824c7de8886ca07ab063712190b0c77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlotsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlotsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e568e623cab87391d84f607018a27c5bca56c39d502b1600440d7cf5b755d9ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="slotTypeIdInput")
    def slot_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slotTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cca1484e32debc3734beaccd27b14b36c15847d93898a87d2cbb3bdbf9a7ffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slotTypeId")
    def slot_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slotTypeId"))

    @slot_type_id.setter
    def slot_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5eb457bfa77cc813afb1e4d9bc92800cd127d152d3af4fa6f6b306d8870c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slotTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d864e418b080e318ca4f71f701145460d29de738fd077dbe68796d3076bf755a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bot_id": "botId",
        "bot_version": "botVersion",
        "locale_id": "localeId",
        "name": "name",
        "composite_slot_type_setting": "compositeSlotTypeSetting",
        "description": "description",
        "external_source_setting": "externalSourceSetting",
        "parent_slot_type_signature": "parentSlotTypeSignature",
        "region": "region",
        "slot_type_values": "slotTypeValues",
        "timeouts": "timeouts",
        "value_selection_setting": "valueSelectionSetting",
    },
)
class Lexv2ModelsSlotTypeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bot_id: builtins.str,
        bot_version: builtins.str,
        locale_id: builtins.str,
        name: builtins.str,
        composite_slot_type_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeCompositeSlotTypeSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        external_source_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeExternalSourceSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parent_slot_type_signature: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        slot_type_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeSlotTypeValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["Lexv2ModelsSlotTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_selection_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeValueSelectionSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bot_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#bot_id Lexv2ModelsSlotType#bot_id}.
        :param bot_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#bot_version Lexv2ModelsSlotType#bot_version}.
        :param locale_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#locale_id Lexv2ModelsSlotType#locale_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#name Lexv2ModelsSlotType#name}.
        :param composite_slot_type_setting: composite_slot_type_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#composite_slot_type_setting Lexv2ModelsSlotType#composite_slot_type_setting}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#description Lexv2ModelsSlotType#description}.
        :param external_source_setting: external_source_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#external_source_setting Lexv2ModelsSlotType#external_source_setting}
        :param parent_slot_type_signature: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#parent_slot_type_signature Lexv2ModelsSlotType#parent_slot_type_signature}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#region Lexv2ModelsSlotType#region}
        :param slot_type_values: slot_type_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#slot_type_values Lexv2ModelsSlotType#slot_type_values}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#timeouts Lexv2ModelsSlotType#timeouts}
        :param value_selection_setting: value_selection_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#value_selection_setting Lexv2ModelsSlotType#value_selection_setting}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = Lexv2ModelsSlotTypeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34456d357f474658467a160a3bd7498eb760535d920b990caea1b162e214a6ef)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bot_id", value=bot_id, expected_type=type_hints["bot_id"])
            check_type(argname="argument bot_version", value=bot_version, expected_type=type_hints["bot_version"])
            check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument composite_slot_type_setting", value=composite_slot_type_setting, expected_type=type_hints["composite_slot_type_setting"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_source_setting", value=external_source_setting, expected_type=type_hints["external_source_setting"])
            check_type(argname="argument parent_slot_type_signature", value=parent_slot_type_signature, expected_type=type_hints["parent_slot_type_signature"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument slot_type_values", value=slot_type_values, expected_type=type_hints["slot_type_values"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument value_selection_setting", value=value_selection_setting, expected_type=type_hints["value_selection_setting"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bot_id": bot_id,
            "bot_version": bot_version,
            "locale_id": locale_id,
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
        if composite_slot_type_setting is not None:
            self._values["composite_slot_type_setting"] = composite_slot_type_setting
        if description is not None:
            self._values["description"] = description
        if external_source_setting is not None:
            self._values["external_source_setting"] = external_source_setting
        if parent_slot_type_signature is not None:
            self._values["parent_slot_type_signature"] = parent_slot_type_signature
        if region is not None:
            self._values["region"] = region
        if slot_type_values is not None:
            self._values["slot_type_values"] = slot_type_values
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if value_selection_setting is not None:
            self._values["value_selection_setting"] = value_selection_setting

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
    def bot_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#bot_id Lexv2ModelsSlotType#bot_id}.'''
        result = self._values.get("bot_id")
        assert result is not None, "Required property 'bot_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bot_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#bot_version Lexv2ModelsSlotType#bot_version}.'''
        result = self._values.get("bot_version")
        assert result is not None, "Required property 'bot_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def locale_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#locale_id Lexv2ModelsSlotType#locale_id}.'''
        result = self._values.get("locale_id")
        assert result is not None, "Required property 'locale_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#name Lexv2ModelsSlotType#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def composite_slot_type_setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeCompositeSlotTypeSetting]]]:
        '''composite_slot_type_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#composite_slot_type_setting Lexv2ModelsSlotType#composite_slot_type_setting}
        '''
        result = self._values.get("composite_slot_type_setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeCompositeSlotTypeSetting]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#description Lexv2ModelsSlotType#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_source_setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeExternalSourceSetting"]]]:
        '''external_source_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#external_source_setting Lexv2ModelsSlotType#external_source_setting}
        '''
        result = self._values.get("external_source_setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeExternalSourceSetting"]]], result)

    @builtins.property
    def parent_slot_type_signature(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#parent_slot_type_signature Lexv2ModelsSlotType#parent_slot_type_signature}.'''
        result = self._values.get("parent_slot_type_signature")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#region Lexv2ModelsSlotType#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slot_type_values(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValues"]]]:
        '''slot_type_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#slot_type_values Lexv2ModelsSlotType#slot_type_values}
        '''
        result = self._values.get("slot_type_values")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValues"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["Lexv2ModelsSlotTypeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#timeouts Lexv2ModelsSlotType#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["Lexv2ModelsSlotTypeTimeouts"], result)

    @builtins.property
    def value_selection_setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeValueSelectionSetting"]]]:
        '''value_selection_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#value_selection_setting Lexv2ModelsSlotType#value_selection_setting}
        '''
        result = self._values.get("value_selection_setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeValueSelectionSetting"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeExternalSourceSetting",
    jsii_struct_bases=[],
    name_mapping={"grammar_slot_type_setting": "grammarSlotTypeSetting"},
)
class Lexv2ModelsSlotTypeExternalSourceSetting:
    def __init__(
        self,
        *,
        grammar_slot_type_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param grammar_slot_type_setting: grammar_slot_type_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#grammar_slot_type_setting Lexv2ModelsSlotType#grammar_slot_type_setting}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a0423d21f6209d675b3ea7c4219d38fc26c08459532467198aad0510b25d24)
            check_type(argname="argument grammar_slot_type_setting", value=grammar_slot_type_setting, expected_type=type_hints["grammar_slot_type_setting"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grammar_slot_type_setting is not None:
            self._values["grammar_slot_type_setting"] = grammar_slot_type_setting

    @builtins.property
    def grammar_slot_type_setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting"]]]:
        '''grammar_slot_type_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#grammar_slot_type_setting Lexv2ModelsSlotType#grammar_slot_type_setting}
        '''
        result = self._values.get("grammar_slot_type_setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeExternalSourceSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting",
    jsii_struct_bases=[],
    name_mapping={"source": "source"},
)
class Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting:
    def __init__(
        self,
        *,
        source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#source Lexv2ModelsSlotType#source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0a4a7426cd56d7c2a94a4244d3a1868ea52f3582b14a12a0572da56eb53d5d)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource"]]]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#source Lexv2ModelsSlotType#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57c5e0711083a32c6a2d5052e3cce5b947c38ff9747bc6e6c430400b830f6d23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0bd805f98b485f76ddaf692c1b4f466708276f67a00da14ab505226e0934c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23bd5f648546faa9b6d9d984eb26c9ac24a9561af23f2b25e4d319aa3aed7e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06e87f6be1a4ecd4a2f2e585fafdf07e97537120fdb4c24177f834e88e820361)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3846711be2496fa6cce5ddcdab855ec335a30bc83ab2112c428441b46c29424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ddde37daa7751b60e084180d64fb4ac7d04379a39133e5cf65bd9c60fa81230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43f5ca9c51c4f30b6195000a1c5815d1288c9593bc8e07efff801eca4a587cca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df224657ee73c9e7aa8cff336d08c72e3df50b8f05c9448849654e20b97e2123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(
        self,
    ) -> "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSourceList":
        return typing.cast("Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSourceList", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource"]]], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5251ac0f36caa32f7424630569ee5dee6ca2206f24a99cbd0af6f0e6ffd8e120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_arn": "kmsKeyArn",
        "s3_bucket_name": "s3BucketName",
        "s3_object_key": "s3ObjectKey",
    },
)
class Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource:
    def __init__(
        self,
        *,
        kms_key_arn: builtins.str,
        s3_bucket_name: builtins.str,
        s3_object_key: builtins.str,
    ) -> None:
        '''
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#kms_key_arn Lexv2ModelsSlotType#kms_key_arn}.
        :param s3_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#s3_bucket_name Lexv2ModelsSlotType#s3_bucket_name}.
        :param s3_object_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#s3_object_key Lexv2ModelsSlotType#s3_object_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed708a42fbff2fd301e305296b7f82505ea92861c450980b6182b8547b33c0d)
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument s3_object_key", value=s3_object_key, expected_type=type_hints["s3_object_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_arn": kms_key_arn,
            "s3_bucket_name": s3_bucket_name,
            "s3_object_key": s3_object_key,
        }

    @builtins.property
    def kms_key_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#kms_key_arn Lexv2ModelsSlotType#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        assert result is not None, "Required property 'kms_key_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#s3_bucket_name Lexv2ModelsSlotType#s3_bucket_name}.'''
        result = self._values.get("s3_bucket_name")
        assert result is not None, "Required property 's3_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_object_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#s3_object_key Lexv2ModelsSlotType#s3_object_key}.'''
        result = self._values.get("s3_object_key")
        assert result is not None, "Required property 's3_object_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48b2a6af7fd5916a0331888ccf895cf23a4e6bc937eb410979a66672d7291450)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1794ad872ec0df4ff262bab9b3ac186cf133c8ff99d01e1d36a9c198957dc810)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3d47d6a423b5b02d7bd80da7107f0654bf68114b9c3e6dd8f9ba8a9d058b09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfefce33ab3c99f811c19e2da2921a21b7fefc90704b74accce9c2f4aeda2566)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16a127626a5017cc15c4403d35d014aed18fd259fbe70fedcf5b2d6dd52bedb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752d562f86d1f7777cd41a4fceaacbed68a35bcccb65c27a14ceedfb35deda48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9de8ec8387a4645397a9e9f47b01db4639701138678c4bb177ca12359b1d0af0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketNameInput")
    def s3_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3ObjectKeyInput")
    def s3_object_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3ObjectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4206e49835b6301d0419e4e35a16e114a713b9119671b864df3bac88356a399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketName"))

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2718f37930f610827861ff4e85d63c400574ad46b704a347b603f21dab9975a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3ObjectKey")
    def s3_object_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3ObjectKey"))

    @s3_object_key.setter
    def s3_object_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7ca5d4fe374846217fc31d78e1bcf8af847cf5fdb5bd1a3de1c5aabaac67d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3ObjectKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e888cf03608166784e05ca0fe1fec6d7ef7b52dcc38005efc4f1894947085fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeExternalSourceSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeExternalSourceSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d34e9aefb108986a1f7004fd21c6fac12f1885d61ad3ce8bae444a66797cd52b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeExternalSourceSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ba3a45c8289a988d1176e386c59d39975156499521fc9a27febd1c36dbfb817)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeExternalSourceSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38969c13ca05f3e67fb2315745a5636b92f3c2a6ad550fda080e3591534dcb5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__122f30662592a81dca0d1e6a18ce0e530998612c896d06cc5e04ff55ede72bf9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77b9fcd232548012fdaedf5e8af6775454232473ed2d629695f71990113b9791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44b71f65af013a2fc8e7b8f4c9a7c25f34382800ee61ab7310e435087fe6f146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeExternalSourceSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeExternalSourceSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__884a04803d9b0c6211533cb16a80774556d32461730682cc5f31464acb656dc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGrammarSlotTypeSetting")
    def put_grammar_slot_type_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134260f7e05c33a6fab9d193e833f576d85b5c3dd861e3403eded697586b480e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGrammarSlotTypeSetting", [value]))

    @jsii.member(jsii_name="resetGrammarSlotTypeSetting")
    def reset_grammar_slot_type_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrammarSlotTypeSetting", []))

    @builtins.property
    @jsii.member(jsii_name="grammarSlotTypeSetting")
    def grammar_slot_type_setting(
        self,
    ) -> Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingList:
        return typing.cast(Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingList, jsii.get(self, "grammarSlotTypeSetting"))

    @builtins.property
    @jsii.member(jsii_name="grammarSlotTypeSettingInput")
    def grammar_slot_type_setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting]]], jsii.get(self, "grammarSlotTypeSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSetting]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSetting]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSetting]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344fcb7524e5481405c2631b20ed763b71a74700d0b909de16f5e40d9cba9942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeSlotTypeValues",
    jsii_struct_bases=[],
    name_mapping={"sample_value": "sampleValue", "synonyms": "synonyms"},
)
class Lexv2ModelsSlotTypeSlotTypeValues:
    def __init__(
        self,
        *,
        sample_value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeSlotTypeValuesSampleValue", typing.Dict[builtins.str, typing.Any]]]]] = None,
        synonyms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeSlotTypeValuesSynonyms", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param sample_value: sample_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#sample_value Lexv2ModelsSlotType#sample_value}
        :param synonyms: synonyms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#synonyms Lexv2ModelsSlotType#synonyms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dba38f9dbd5ecfb4c77339bace2e24ebfc9242ea1a6ed9697ed1c24f05f2b15)
            check_type(argname="argument sample_value", value=sample_value, expected_type=type_hints["sample_value"])
            check_type(argname="argument synonyms", value=synonyms, expected_type=type_hints["synonyms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sample_value is not None:
            self._values["sample_value"] = sample_value
        if synonyms is not None:
            self._values["synonyms"] = synonyms

    @builtins.property
    def sample_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValuesSampleValue"]]]:
        '''sample_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#sample_value Lexv2ModelsSlotType#sample_value}
        '''
        result = self._values.get("sample_value")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValuesSampleValue"]]], result)

    @builtins.property
    def synonyms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValuesSynonyms"]]]:
        '''synonyms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#synonyms Lexv2ModelsSlotType#synonyms}
        '''
        result = self._values.get("synonyms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValuesSynonyms"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeSlotTypeValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lexv2ModelsSlotTypeSlotTypeValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeSlotTypeValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9141c3fac6e3d561ff4163a736bc3ecc0285b730ccaa438e6b3b8088ca31ded3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeSlotTypeValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c756873efe91d49b594e6ee1bf2c63762650a6d65349d75b05c48e579c6cfc9a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeSlotTypeValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafa4df371829c2ff8b641196099a9189f035bc5fb135aba77916bcbce44c117)
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
            type_hints = typing.get_type_hints(_typecheckingstub__355b9785e44de136832ad29cb5487f5085195dc7910462eabb03dfcf709d22be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__938759843b8fe9c86f552ecefda59254f0641e6455a00f91665fc4f56341d1cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValues]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValues]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233397831cce6939250ed32c034e90523a249098b4144021141c62b4f884d949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeSlotTypeValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeSlotTypeValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0478b71b5f77a294159ddcad276fe1f2fea7a1d84a834b2d2d3db28247b6246)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSampleValue")
    def put_sample_value(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeSlotTypeValuesSampleValue", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6c17ea2bdd7e6dad1e08978f6325b62223fc56314fb47548a42589b31578a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSampleValue", [value]))

    @jsii.member(jsii_name="putSynonyms")
    def put_synonyms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeSlotTypeValuesSynonyms", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0ad8bf9e6ecac6b5344e398ec72ef34b1a2e5900b92b721b96c16814ed0593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSynonyms", [value]))

    @jsii.member(jsii_name="resetSampleValue")
    def reset_sample_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleValue", []))

    @jsii.member(jsii_name="resetSynonyms")
    def reset_synonyms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSynonyms", []))

    @builtins.property
    @jsii.member(jsii_name="sampleValue")
    def sample_value(self) -> "Lexv2ModelsSlotTypeSlotTypeValuesSampleValueList":
        return typing.cast("Lexv2ModelsSlotTypeSlotTypeValuesSampleValueList", jsii.get(self, "sampleValue"))

    @builtins.property
    @jsii.member(jsii_name="synonyms")
    def synonyms(self) -> "Lexv2ModelsSlotTypeSlotTypeValuesSynonymsList":
        return typing.cast("Lexv2ModelsSlotTypeSlotTypeValuesSynonymsList", jsii.get(self, "synonyms"))

    @builtins.property
    @jsii.member(jsii_name="sampleValueInput")
    def sample_value_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValuesSampleValue"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValuesSampleValue"]]], jsii.get(self, "sampleValueInput"))

    @builtins.property
    @jsii.member(jsii_name="synonymsInput")
    def synonyms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValuesSynonyms"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeSlotTypeValuesSynonyms"]]], jsii.get(self, "synonymsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValues]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValues]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValues]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5f3c97baeb68f890de1794a2ad85c6ff5bf8ba4c45cb9ec4709fbdfd471990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeSlotTypeValuesSampleValue",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class Lexv2ModelsSlotTypeSlotTypeValuesSampleValue:
    def __init__(self, *, value: builtins.str) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#value Lexv2ModelsSlotType#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744dfb77752862b365db9eeb7ef6dc56ad47389c01e899474e2303b6a1de00fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#value Lexv2ModelsSlotType#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeSlotTypeValuesSampleValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lexv2ModelsSlotTypeSlotTypeValuesSampleValueList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeSlotTypeValuesSampleValueList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73161aab4f02b681af8d9ceee57133884394097ab662891d7cbbb6414e5b27d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeSlotTypeValuesSampleValueOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205f99277ec1c9892b248b4faea2e6f6e63281c54e1cac72b13838dc611e1c65)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeSlotTypeValuesSampleValueOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1cb05e3213ed667d61789de4d0608d50a6526ed7b76259d483ecce36e7451d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14d85c93d4b6448a1fb7d0a2ba2ec8599ace168704a37819604da75273c42791)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ad9d6788b3139e2d1ba8ff4e346189c2a7ad31c779b936245aad89fc4d34d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValuesSampleValue]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValuesSampleValue]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValuesSampleValue]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a46a3188aee3870953167d1261d441fbd5a050bcbc85bf1ed7f85bdb37db40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeSlotTypeValuesSampleValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeSlotTypeValuesSampleValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8a1ab3591755c60f9e9d2831baf47d518076b1baef4eb55048f69bf7421bcfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519e462ca3a067999cd0bcbf810bd96e36f356068a28885e29d07c37046de3fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValuesSampleValue]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValuesSampleValue]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValuesSampleValue]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db2ea8be665cad11f2b5a1d89a5c8eba4b05ceb4fa41f3543d3ad957bba8db20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeSlotTypeValuesSynonyms",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class Lexv2ModelsSlotTypeSlotTypeValuesSynonyms:
    def __init__(self, *, value: builtins.str) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#value Lexv2ModelsSlotType#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a080967b82bc94787fe9ada8d3003864001b21f67909b29b351f7515222860d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#value Lexv2ModelsSlotType#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeSlotTypeValuesSynonyms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lexv2ModelsSlotTypeSlotTypeValuesSynonymsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeSlotTypeValuesSynonymsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72abaf4f2ce1c0983711693441409154abe05c73a20e3ab2a4975a3d31ceca83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeSlotTypeValuesSynonymsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee4c2b69f93002a9995eebc3accaf86476d60601a8f45b8ac5d0e5fb266a3e8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeSlotTypeValuesSynonymsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d328be2f5cf775007324e5de67a5521cf69ba598835f6ddfa153a8c5d553f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d29a94d20e92b1fe1b2f25d8612c40711a2d56725e5b5a69e65f82f06b39c520)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47bf42c49d8d01af04ffd50ebd9ff76f62bbae8d9d64af8d7bcc70e0489c186c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValuesSynonyms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValuesSynonyms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValuesSynonyms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6a4bc79a051a070d31f14583d15fd79f85c5be7a88387c1543330f9e5538de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeSlotTypeValuesSynonymsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeSlotTypeValuesSynonymsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ec91d69ba55228256fe5b3bfdaae67bf7692291402a07950c0843892a193e42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08157bd320a18c3189467317edaf18928a09410c729e6e525d9d426acd10a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValuesSynonyms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValuesSynonyms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValuesSynonyms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2136ad8231db4b356ebdb897b31bc7000e00afe914d57ba226ecbb7fbcdfa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class Lexv2ModelsSlotTypeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#create Lexv2ModelsSlotType#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#delete Lexv2ModelsSlotType#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#update Lexv2ModelsSlotType#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56eddce81d76fccf9462d87679eefa23e62f6f9e2d1b9627f582ed73f390125)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#create Lexv2ModelsSlotType#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#delete Lexv2ModelsSlotType#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#update Lexv2ModelsSlotType#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lexv2ModelsSlotTypeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f1a4bcd725857dcfc99cadfdc678c1d22623f222b420a2069428ea6d5a76dcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4bc7ce0c9a1ea5eca657d3b7d90d137a75bdbdd87cb7c12bf7eb40cc5be9062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e946977893b3f4a9a5a38fce271e65ac4e8499acdac928cba1417ac5dfe7c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90916a8c17e804b260d2a178da4f47b2834ce06a42ffb68e65c145a99dfbd907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793534bf792087cb31622736c2f2bf7ba5ea67440328135b01caaaeee6f4dcb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeValueSelectionSetting",
    jsii_struct_bases=[],
    name_mapping={
        "resolution_strategy": "resolutionStrategy",
        "advanced_recognition_setting": "advancedRecognitionSetting",
        "regex_filter": "regexFilter",
    },
)
class Lexv2ModelsSlotTypeValueSelectionSetting:
    def __init__(
        self,
        *,
        resolution_strategy: builtins.str,
        advanced_recognition_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        regex_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param resolution_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#resolution_strategy Lexv2ModelsSlotType#resolution_strategy}.
        :param advanced_recognition_setting: advanced_recognition_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#advanced_recognition_setting Lexv2ModelsSlotType#advanced_recognition_setting}
        :param regex_filter: regex_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#regex_filter Lexv2ModelsSlotType#regex_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53dad959b9c9248319123213fe623f1c96353a2ddc9f2c5765092464d1d12f7)
            check_type(argname="argument resolution_strategy", value=resolution_strategy, expected_type=type_hints["resolution_strategy"])
            check_type(argname="argument advanced_recognition_setting", value=advanced_recognition_setting, expected_type=type_hints["advanced_recognition_setting"])
            check_type(argname="argument regex_filter", value=regex_filter, expected_type=type_hints["regex_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resolution_strategy": resolution_strategy,
        }
        if advanced_recognition_setting is not None:
            self._values["advanced_recognition_setting"] = advanced_recognition_setting
        if regex_filter is not None:
            self._values["regex_filter"] = regex_filter

    @builtins.property
    def resolution_strategy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#resolution_strategy Lexv2ModelsSlotType#resolution_strategy}.'''
        result = self._values.get("resolution_strategy")
        assert result is not None, "Required property 'resolution_strategy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_recognition_setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting"]]]:
        '''advanced_recognition_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#advanced_recognition_setting Lexv2ModelsSlotType#advanced_recognition_setting}
        '''
        result = self._values.get("advanced_recognition_setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting"]]], result)

    @builtins.property
    def regex_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter"]]]:
        '''regex_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#regex_filter Lexv2ModelsSlotType#regex_filter}
        '''
        result = self._values.get("regex_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeValueSelectionSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting",
    jsii_struct_bases=[],
    name_mapping={"audio_recognition_strategy": "audioRecognitionStrategy"},
)
class Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting:
    def __init__(
        self,
        *,
        audio_recognition_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audio_recognition_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#audio_recognition_strategy Lexv2ModelsSlotType#audio_recognition_strategy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd530d20085d6364ef0b67459ad5b09eaf4a93c236dcafaf136fc5013b7432b8)
            check_type(argname="argument audio_recognition_strategy", value=audio_recognition_strategy, expected_type=type_hints["audio_recognition_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audio_recognition_strategy is not None:
            self._values["audio_recognition_strategy"] = audio_recognition_strategy

    @builtins.property
    def audio_recognition_strategy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#audio_recognition_strategy Lexv2ModelsSlotType#audio_recognition_strategy}.'''
        result = self._values.get("audio_recognition_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__379b44275690483acdb5579e311a09c26c4a28cb3dbb57e5a0f9efb32999c7a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9dad57bb7f415f1451255169754985942bd574fec68f1f4fcaf2ee5cd5c5f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f960c701487a15e47e64c199cd051484b00ebfd3beca400d48219963c4980b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f29a71f92ce87cea84843c0183ddff57343a78f47e38258eee9b0356f62a96c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc6327a6c11b8e752df987e8c701ef7238cd0541fd2918c30d3ce867fe9e3795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e31c839ed1808123427882206ca3ab960460ee69ee651016c554532fbf00d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e3d7d8114668130d5f80ca8efefa6160796ca3a62cc70fff3cdafeb3f06358e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAudioRecognitionStrategy")
    def reset_audio_recognition_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioRecognitionStrategy", []))

    @builtins.property
    @jsii.member(jsii_name="audioRecognitionStrategyInput")
    def audio_recognition_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioRecognitionStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="audioRecognitionStrategy")
    def audio_recognition_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioRecognitionStrategy"))

    @audio_recognition_strategy.setter
    def audio_recognition_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ed9e2fc111e4a738043e457a9d5e73cfcb7539f0f211e367071f046e5f12b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioRecognitionStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b2263a1b52ee691902de9c1fa25ec6eda2e83cf48449a65e77f09bca6e1825c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeValueSelectionSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeValueSelectionSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecb0a6ec7ed7908857783f95855c1601d3a122a3a1effac63a25e1ace0bafd90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeValueSelectionSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9dcba786b4023b1de4ac9fc27a825a83475420b697240a9aa8b70b33a09de5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeValueSelectionSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f882e4376d06e3493690042fb909fead11a28d51b9e0227d40aaaecc980e24f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ad79076436f0e57c3d276f675ae72a77be2efcf8f864f7940ecb2b7db66eca2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f28a0a8534e6f835dc22c917afcdbb88f892fa0c3cf33d7bcb3293724f2b4063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a423b61e85804061719a5d03147bd4c9dc446b8382652ea28cee96c3b355ecc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeValueSelectionSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeValueSelectionSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a4ce24ad22a79fb63a4fdbe5af97019667ce76464f8f4a5fd8dbd0d8109d01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAdvancedRecognitionSetting")
    def put_advanced_recognition_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60f4bfcfd8bb4349c8bb1b06cc786df54aeaff4801d68c8bc48aee1605ab49e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdvancedRecognitionSetting", [value]))

    @jsii.member(jsii_name="putRegexFilter")
    def put_regex_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94c97a9795c1f2d8273019dd876a366fe7cd8f104ac96f844b6c5c69d1976be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegexFilter", [value]))

    @jsii.member(jsii_name="resetAdvancedRecognitionSetting")
    def reset_advanced_recognition_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedRecognitionSetting", []))

    @jsii.member(jsii_name="resetRegexFilter")
    def reset_regex_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegexFilter", []))

    @builtins.property
    @jsii.member(jsii_name="advancedRecognitionSetting")
    def advanced_recognition_setting(
        self,
    ) -> Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSettingList:
        return typing.cast(Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSettingList, jsii.get(self, "advancedRecognitionSetting"))

    @builtins.property
    @jsii.member(jsii_name="regexFilter")
    def regex_filter(self) -> "Lexv2ModelsSlotTypeValueSelectionSettingRegexFilterList":
        return typing.cast("Lexv2ModelsSlotTypeValueSelectionSettingRegexFilterList", jsii.get(self, "regexFilter"))

    @builtins.property
    @jsii.member(jsii_name="advancedRecognitionSettingInput")
    def advanced_recognition_setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting]]], jsii.get(self, "advancedRecognitionSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="regexFilterInput")
    def regex_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter"]]], jsii.get(self, "regexFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="resolutionStrategyInput")
    def resolution_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resolutionStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="resolutionStrategy")
    def resolution_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resolutionStrategy"))

    @resolution_strategy.setter
    def resolution_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f4bc3d8e35f375997b060324e549d174df68bd12e01e39de68b5bc10268a32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolutionStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSetting]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSetting]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSetting]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f232c09841efce27db0f3969ee6bf4fd2ba1f8590eeb5df5df3afc9acf9bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern"},
)
class Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter:
    def __init__(self, *, pattern: builtins.str) -> None:
        '''
        :param pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#pattern Lexv2ModelsSlotType#pattern}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__419523e35f00ff1ccbb4d5e0b76e870f442334893afcadfe42af93bd203ac468)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
        }

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lexv2models_slot_type#pattern Lexv2ModelsSlotType#pattern}.'''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lexv2ModelsSlotTypeValueSelectionSettingRegexFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeValueSelectionSettingRegexFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1d6946757772169f7ded3e085b3c75fcfb4263b80e2a2a94c1f83a37d0459c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Lexv2ModelsSlotTypeValueSelectionSettingRegexFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0f7ccbfad70bb28b1066688f2911c2f11c0cd29f4c37d281fff6ad00d66306)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Lexv2ModelsSlotTypeValueSelectionSettingRegexFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eabbd50b36763a4ef4160f953240fdb4dad18ed5f36345c469f5a14dcae7af38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fac00b074c630301ed4130a436f2b6da46a5bb898761239b00c9f160e3ea3a1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__424079cdd8b56050aadf372fe5f882a941cba63a1c73d9459ff1ac3bd5fcfc92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c077bffffd1a6d8e5b0f9df426263d319c9dc15a955c0fe5c9ec67c412ab56e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Lexv2ModelsSlotTypeValueSelectionSettingRegexFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lexv2ModelsSlotType.Lexv2ModelsSlotTypeValueSelectionSettingRegexFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd6adc47bc810c546cd0b5e07f8fa47883e37dcb93b2819134ea96ac80046938)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b5d388ed1b5f4dfa1816d0cd7bb0b70e09f7648231841493583d33c08aa2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2b9c11798a60694574202f4d38ec4c8690195ef012bac4ed816be656b229cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Lexv2ModelsSlotType",
    "Lexv2ModelsSlotTypeCompositeSlotTypeSetting",
    "Lexv2ModelsSlotTypeCompositeSlotTypeSettingList",
    "Lexv2ModelsSlotTypeCompositeSlotTypeSettingOutputReference",
    "Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots",
    "Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlotsList",
    "Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlotsOutputReference",
    "Lexv2ModelsSlotTypeConfig",
    "Lexv2ModelsSlotTypeExternalSourceSetting",
    "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting",
    "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingList",
    "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingOutputReference",
    "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource",
    "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSourceList",
    "Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSourceOutputReference",
    "Lexv2ModelsSlotTypeExternalSourceSettingList",
    "Lexv2ModelsSlotTypeExternalSourceSettingOutputReference",
    "Lexv2ModelsSlotTypeSlotTypeValues",
    "Lexv2ModelsSlotTypeSlotTypeValuesList",
    "Lexv2ModelsSlotTypeSlotTypeValuesOutputReference",
    "Lexv2ModelsSlotTypeSlotTypeValuesSampleValue",
    "Lexv2ModelsSlotTypeSlotTypeValuesSampleValueList",
    "Lexv2ModelsSlotTypeSlotTypeValuesSampleValueOutputReference",
    "Lexv2ModelsSlotTypeSlotTypeValuesSynonyms",
    "Lexv2ModelsSlotTypeSlotTypeValuesSynonymsList",
    "Lexv2ModelsSlotTypeSlotTypeValuesSynonymsOutputReference",
    "Lexv2ModelsSlotTypeTimeouts",
    "Lexv2ModelsSlotTypeTimeoutsOutputReference",
    "Lexv2ModelsSlotTypeValueSelectionSetting",
    "Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting",
    "Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSettingList",
    "Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSettingOutputReference",
    "Lexv2ModelsSlotTypeValueSelectionSettingList",
    "Lexv2ModelsSlotTypeValueSelectionSettingOutputReference",
    "Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter",
    "Lexv2ModelsSlotTypeValueSelectionSettingRegexFilterList",
    "Lexv2ModelsSlotTypeValueSelectionSettingRegexFilterOutputReference",
]

publication.publish()

def _typecheckingstub__2c527731b8c902f223e1183669fc92e1c3b675052577fbd05ada06b4c49805c4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bot_id: builtins.str,
    bot_version: builtins.str,
    locale_id: builtins.str,
    name: builtins.str,
    composite_slot_type_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeCompositeSlotTypeSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    external_source_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeExternalSourceSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parent_slot_type_signature: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    slot_type_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeSlotTypeValues, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[Lexv2ModelsSlotTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_selection_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeValueSelectionSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__92054681081560fc4572940c885916e8010ccbb7089fe532fba721435a56b0eb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d023da18b9dfcf57f79a157296c64add2325d65bceddd13b91e281cc0c1564e7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeCompositeSlotTypeSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82f8aec1570349fa09f881d9b94b7ebdbce3acfbb20aad3618aa1a70e6a46a4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeExternalSourceSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d54047e60f2d0e05613e367170c1e5e756dbd224a50667a7d7f342e5f0bfee5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeSlotTypeValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe9e04992f84fc637ed929b2e0c601d5c04f3530545141ec171a206a3c487ab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeValueSelectionSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f615eacceb6885be7723bfbd29a63b948e6dc1b060343c4b35ca21703c93c5eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a0ac2eb2c994523864f082b664275108a78baae5d254c8933696b3899a307c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1d5411b98771d35e7a54f19e85ad3d8ffe9dc7af29f9c09fcd5844f32d49a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8650deeb56abcd9e5b0a8883880051054798c1341db3a8d8bd04df3eecafd97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f1258133610e58a3ff9dd51fba44ca354d6914defcb62baedd430b3369cf51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b39bac19c9b134e0d3a3aba6422541434a7f8429f96aa483e0c459bd3763971(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8fd52f885b84e7d3113db46be3d9f5a7abc1fc33bc971bcccc6bd6f93814c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c36699cfa1b1b6fab1ef1f0e57c71fd23cb1fff722139bfdad0783f8e4507d(
    *,
    sub_slots: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d07f01b8dbd7ed1ed6cafcf1f933539d6fe4ade1a7cec7392e2aa3e2d9e8671(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e8084ecaef12b095a10dc14814a509a22a564681c3c0bbb5b4ea682021869f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2d8e0ebabf8c709cac54ae00d2667f793914cad288e2ada553231bc30d5d45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b0311b91d969bf9a6cebef16bb28059beea2008fff135bf394dccb60f88ce3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a296513f5c02320000d9b659d6ac455bbe53fd4bd02c776c8ac34444607f8b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305cf7c72e81344fc2e79b1dcbc87d4c5a818f55bc10a53dceed0f03f4c77980(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeCompositeSlotTypeSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ce2efa2630c87971b4fd79a73b0f511430d202ebd3bc7b8520617fd6cb6922(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67fd09917399b7f0e9101ac583ab9824928406b013b3b2938cd8077bcdda1b6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331a8a475e446f43361423c7a097e3d4db18438bcee89e7cd58d3292752b3792(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeCompositeSlotTypeSetting]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1a178ef6d37c508e8c7d9524e2a41c987a84a1be29b05d3f8aca6aa798f722(
    *,
    name: builtins.str,
    slot_type_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8494995f9defde22c82bfbc7714f7c046c00b9a93654894945cf461f142f31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653a8ebdd3af400d0f5fb6f130e1e800208d185668dae76947f01966cc95a515(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11066ac3a279fb68a5dd007591b8c4c216d72cbba85dbbd884a828d86ca6f42c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50eba8a0c60112e1134775094d199c14f2ae98a5a8bef042bd4b69a622096778(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8360f5c09d1581761ac36bc90f3e8fed6943eb629adcd359056613e2eee44c96(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b83d2bdcceff2e0bbacb69146764fd8824c7de8886ca07ab063712190b0c77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e568e623cab87391d84f607018a27c5bca56c39d502b1600440d7cf5b755d9ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cca1484e32debc3734beaccd27b14b36c15847d93898a87d2cbb3bdbf9a7ffd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5eb457bfa77cc813afb1e4d9bc92800cd127d152d3af4fa6f6b306d8870c09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d864e418b080e318ca4f71f701145460d29de738fd077dbe68796d3076bf755a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeCompositeSlotTypeSettingSubSlots]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34456d357f474658467a160a3bd7498eb760535d920b990caea1b162e214a6ef(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bot_id: builtins.str,
    bot_version: builtins.str,
    locale_id: builtins.str,
    name: builtins.str,
    composite_slot_type_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeCompositeSlotTypeSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    external_source_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeExternalSourceSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parent_slot_type_signature: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    slot_type_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeSlotTypeValues, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[Lexv2ModelsSlotTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_selection_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeValueSelectionSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a0423d21f6209d675b3ea7c4219d38fc26c08459532467198aad0510b25d24(
    *,
    grammar_slot_type_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0a4a7426cd56d7c2a94a4244d3a1868ea52f3582b14a12a0572da56eb53d5d(
    *,
    source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c5e0711083a32c6a2d5052e3cce5b947c38ff9747bc6e6c430400b830f6d23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0bd805f98b485f76ddaf692c1b4f466708276f67a00da14ab505226e0934c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23bd5f648546faa9b6d9d984eb26c9ac24a9561af23f2b25e4d319aa3aed7e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e87f6be1a4ecd4a2f2e585fafdf07e97537120fdb4c24177f834e88e820361(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3846711be2496fa6cce5ddcdab855ec335a30bc83ab2112c428441b46c29424(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ddde37daa7751b60e084180d64fb4ac7d04379a39133e5cf65bd9c60fa81230(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f5ca9c51c4f30b6195000a1c5815d1288c9593bc8e07efff801eca4a587cca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df224657ee73c9e7aa8cff336d08c72e3df50b8f05c9448849654e20b97e2123(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5251ac0f36caa32f7424630569ee5dee6ca2206f24a99cbd0af6f0e6ffd8e120(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed708a42fbff2fd301e305296b7f82505ea92861c450980b6182b8547b33c0d(
    *,
    kms_key_arn: builtins.str,
    s3_bucket_name: builtins.str,
    s3_object_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b2a6af7fd5916a0331888ccf895cf23a4e6bc937eb410979a66672d7291450(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1794ad872ec0df4ff262bab9b3ac186cf133c8ff99d01e1d36a9c198957dc810(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3d47d6a423b5b02d7bd80da7107f0654bf68114b9c3e6dd8f9ba8a9d058b09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfefce33ab3c99f811c19e2da2921a21b7fefc90704b74accce9c2f4aeda2566(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a127626a5017cc15c4403d35d014aed18fd259fbe70fedcf5b2d6dd52bedb4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752d562f86d1f7777cd41a4fceaacbed68a35bcccb65c27a14ceedfb35deda48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de8ec8387a4645397a9e9f47b01db4639701138678c4bb177ca12359b1d0af0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4206e49835b6301d0419e4e35a16e114a713b9119671b864df3bac88356a399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2718f37930f610827861ff4e85d63c400574ad46b704a347b603f21dab9975a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7ca5d4fe374846217fc31d78e1bcf8af847cf5fdb5bd1a3de1c5aabaac67d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e888cf03608166784e05ca0fe1fec6d7ef7b52dcc38005efc4f1894947085fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSettingSource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34e9aefb108986a1f7004fd21c6fac12f1885d61ad3ce8bae444a66797cd52b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba3a45c8289a988d1176e386c59d39975156499521fc9a27febd1c36dbfb817(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38969c13ca05f3e67fb2315745a5636b92f3c2a6ad550fda080e3591534dcb5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122f30662592a81dca0d1e6a18ce0e530998612c896d06cc5e04ff55ede72bf9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b9fcd232548012fdaedf5e8af6775454232473ed2d629695f71990113b9791(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b71f65af013a2fc8e7b8f4c9a7c25f34382800ee61ab7310e435087fe6f146(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeExternalSourceSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__884a04803d9b0c6211533cb16a80774556d32461730682cc5f31464acb656dc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134260f7e05c33a6fab9d193e833f576d85b5c3dd861e3403eded697586b480e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeExternalSourceSettingGrammarSlotTypeSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344fcb7524e5481405c2631b20ed763b71a74700d0b909de16f5e40d9cba9942(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeExternalSourceSetting]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dba38f9dbd5ecfb4c77339bace2e24ebfc9242ea1a6ed9697ed1c24f05f2b15(
    *,
    sample_value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeSlotTypeValuesSampleValue, typing.Dict[builtins.str, typing.Any]]]]] = None,
    synonyms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeSlotTypeValuesSynonyms, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9141c3fac6e3d561ff4163a736bc3ecc0285b730ccaa438e6b3b8088ca31ded3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c756873efe91d49b594e6ee1bf2c63762650a6d65349d75b05c48e579c6cfc9a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafa4df371829c2ff8b641196099a9189f035bc5fb135aba77916bcbce44c117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355b9785e44de136832ad29cb5487f5085195dc7910462eabb03dfcf709d22be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938759843b8fe9c86f552ecefda59254f0641e6455a00f91665fc4f56341d1cb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233397831cce6939250ed32c034e90523a249098b4144021141c62b4f884d949(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValues]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0478b71b5f77a294159ddcad276fe1f2fea7a1d84a834b2d2d3db28247b6246(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6c17ea2bdd7e6dad1e08978f6325b62223fc56314fb47548a42589b31578a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeSlotTypeValuesSampleValue, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0ad8bf9e6ecac6b5344e398ec72ef34b1a2e5900b92b721b96c16814ed0593(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeSlotTypeValuesSynonyms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5f3c97baeb68f890de1794a2ad85c6ff5bf8ba4c45cb9ec4709fbdfd471990(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValues]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744dfb77752862b365db9eeb7ef6dc56ad47389c01e899474e2303b6a1de00fa(
    *,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73161aab4f02b681af8d9ceee57133884394097ab662891d7cbbb6414e5b27d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205f99277ec1c9892b248b4faea2e6f6e63281c54e1cac72b13838dc611e1c65(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1cb05e3213ed667d61789de4d0608d50a6526ed7b76259d483ecce36e7451d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d85c93d4b6448a1fb7d0a2ba2ec8599ace168704a37819604da75273c42791(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad9d6788b3139e2d1ba8ff4e346189c2a7ad31c779b936245aad89fc4d34d96(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a46a3188aee3870953167d1261d441fbd5a050bcbc85bf1ed7f85bdb37db40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValuesSampleValue]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a1ab3591755c60f9e9d2831baf47d518076b1baef4eb55048f69bf7421bcfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519e462ca3a067999cd0bcbf810bd96e36f356068a28885e29d07c37046de3fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2ea8be665cad11f2b5a1d89a5c8eba4b05ceb4fa41f3543d3ad957bba8db20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValuesSampleValue]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a080967b82bc94787fe9ada8d3003864001b21f67909b29b351f7515222860d(
    *,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72abaf4f2ce1c0983711693441409154abe05c73a20e3ab2a4975a3d31ceca83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee4c2b69f93002a9995eebc3accaf86476d60601a8f45b8ac5d0e5fb266a3e8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d328be2f5cf775007324e5de67a5521cf69ba598835f6ddfa153a8c5d553f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29a94d20e92b1fe1b2f25d8612c40711a2d56725e5b5a69e65f82f06b39c520(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47bf42c49d8d01af04ffd50ebd9ff76f62bbae8d9d64af8d7bcc70e0489c186c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6a4bc79a051a070d31f14583d15fd79f85c5be7a88387c1543330f9e5538de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeSlotTypeValuesSynonyms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec91d69ba55228256fe5b3bfdaae67bf7692291402a07950c0843892a193e42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08157bd320a18c3189467317edaf18928a09410c729e6e525d9d426acd10a66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2136ad8231db4b356ebdb897b31bc7000e00afe914d57ba226ecbb7fbcdfa2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeSlotTypeValuesSynonyms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56eddce81d76fccf9462d87679eefa23e62f6f9e2d1b9627f582ed73f390125(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1a4bcd725857dcfc99cadfdc678c1d22623f222b420a2069428ea6d5a76dcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bc7ce0c9a1ea5eca657d3b7d90d137a75bdbdd87cb7c12bf7eb40cc5be9062(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e946977893b3f4a9a5a38fce271e65ac4e8499acdac928cba1417ac5dfe7c3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90916a8c17e804b260d2a178da4f47b2834ce06a42ffb68e65c145a99dfbd907(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793534bf792087cb31622736c2f2bf7ba5ea67440328135b01caaaeee6f4dcb1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53dad959b9c9248319123213fe623f1c96353a2ddc9f2c5765092464d1d12f7(
    *,
    resolution_strategy: builtins.str,
    advanced_recognition_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    regex_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd530d20085d6364ef0b67459ad5b09eaf4a93c236dcafaf136fc5013b7432b8(
    *,
    audio_recognition_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379b44275690483acdb5579e311a09c26c4a28cb3dbb57e5a0f9efb32999c7a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9dad57bb7f415f1451255169754985942bd574fec68f1f4fcaf2ee5cd5c5f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f960c701487a15e47e64c199cd051484b00ebfd3beca400d48219963c4980b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f29a71f92ce87cea84843c0183ddff57343a78f47e38258eee9b0356f62a96c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6327a6c11b8e752df987e8c701ef7238cd0541fd2918c30d3ce867fe9e3795(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e31c839ed1808123427882206ca3ab960460ee69ee651016c554532fbf00d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3d7d8114668130d5f80ca8efefa6160796ca3a62cc70fff3cdafeb3f06358e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ed9e2fc111e4a738043e457a9d5e73cfcb7539f0f211e367071f046e5f12b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2263a1b52ee691902de9c1fa25ec6eda2e83cf48449a65e77f09bca6e1825c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb0a6ec7ed7908857783f95855c1601d3a122a3a1effac63a25e1ace0bafd90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9dcba786b4023b1de4ac9fc27a825a83475420b697240a9aa8b70b33a09de5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f882e4376d06e3493690042fb909fead11a28d51b9e0227d40aaaecc980e24f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad79076436f0e57c3d276f675ae72a77be2efcf8f864f7940ecb2b7db66eca2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28a0a8534e6f835dc22c917afcdbb88f892fa0c3cf33d7bcb3293724f2b4063(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a423b61e85804061719a5d03147bd4c9dc446b8382652ea28cee96c3b355ecc4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a4ce24ad22a79fb63a4fdbe5af97019667ce76464f8f4a5fd8dbd0d8109d01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60f4bfcfd8bb4349c8bb1b06cc786df54aeaff4801d68c8bc48aee1605ab49e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeValueSelectionSettingAdvancedRecognitionSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94c97a9795c1f2d8273019dd876a366fe7cd8f104ac96f844b6c5c69d1976be(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f4bc3d8e35f375997b060324e549d174df68bd12e01e39de68b5bc10268a32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f232c09841efce27db0f3969ee6bf4fd2ba1f8590eeb5df5df3afc9acf9bea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSetting]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419523e35f00ff1ccbb4d5e0b76e870f442334893afcadfe42af93bd203ac468(
    *,
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d6946757772169f7ded3e085b3c75fcfb4263b80e2a2a94c1f83a37d0459c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0f7ccbfad70bb28b1066688f2911c2f11c0cd29f4c37d281fff6ad00d66306(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eabbd50b36763a4ef4160f953240fdb4dad18ed5f36345c469f5a14dcae7af38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac00b074c630301ed4130a436f2b6da46a5bb898761239b00c9f160e3ea3a1e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424079cdd8b56050aadf372fe5f882a941cba63a1c73d9459ff1ac3bd5fcfc92(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c077bffffd1a6d8e5b0f9df426263d319c9dc15a955c0fe5c9ec67c412ab56e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6adc47bc810c546cd0b5e07f8fa47883e37dcb93b2819134ea96ac80046938(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b5d388ed1b5f4dfa1816d0cd7bb0b70e09f7648231841493583d33c08aa2c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2b9c11798a60694574202f4d38ec4c8690195ef012bac4ed816be656b229cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Lexv2ModelsSlotTypeValueSelectionSettingRegexFilter]],
) -> None:
    """Type checking stubs"""
    pass
