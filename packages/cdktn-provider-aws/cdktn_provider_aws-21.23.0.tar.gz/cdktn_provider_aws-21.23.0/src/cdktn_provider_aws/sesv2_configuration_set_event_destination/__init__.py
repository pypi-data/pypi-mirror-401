r'''
# `aws_sesv2_configuration_set_event_destination`

Refer to the Terraform Registry for docs: [`aws_sesv2_configuration_set_event_destination`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination).
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


class Sesv2ConfigurationSetEventDestination(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestination",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination aws_sesv2_configuration_set_event_destination}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        configuration_set_name: builtins.str,
        event_destination: typing.Union["Sesv2ConfigurationSetEventDestinationEventDestination", typing.Dict[builtins.str, typing.Any]],
        event_destination_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination aws_sesv2_configuration_set_event_destination} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param configuration_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#configuration_set_name Sesv2ConfigurationSetEventDestination#configuration_set_name}.
        :param event_destination: event_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_destination Sesv2ConfigurationSetEventDestination#event_destination}
        :param event_destination_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_destination_name Sesv2ConfigurationSetEventDestination#event_destination_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#id Sesv2ConfigurationSetEventDestination#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#region Sesv2ConfigurationSetEventDestination#region}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba9571935ba81567ad122a3573d40c80d951a0eaa34b4e1e003460718f3fc4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Sesv2ConfigurationSetEventDestinationConfig(
            configuration_set_name=configuration_set_name,
            event_destination=event_destination,
            event_destination_name=event_destination_name,
            id=id,
            region=region,
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
        '''Generates CDKTF code for importing a Sesv2ConfigurationSetEventDestination resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Sesv2ConfigurationSetEventDestination to import.
        :param import_from_id: The id of the existing Sesv2ConfigurationSetEventDestination that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Sesv2ConfigurationSetEventDestination to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18cc084f635ec99383b6e90d0dd1e4f1b40790fa9064a8da4059f4c3884abd67)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEventDestination")
    def put_event_destination(
        self,
        *,
        matching_event_types: typing.Sequence[builtins.str],
        cloud_watch_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_bridge_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_firehose_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        pinpoint_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        sns_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_event_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#matching_event_types Sesv2ConfigurationSetEventDestination#matching_event_types}.
        :param cloud_watch_destination: cloud_watch_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#cloud_watch_destination Sesv2ConfigurationSetEventDestination#cloud_watch_destination}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#enabled Sesv2ConfigurationSetEventDestination#enabled}.
        :param event_bridge_destination: event_bridge_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_bridge_destination Sesv2ConfigurationSetEventDestination#event_bridge_destination}
        :param kinesis_firehose_destination: kinesis_firehose_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#kinesis_firehose_destination Sesv2ConfigurationSetEventDestination#kinesis_firehose_destination}
        :param pinpoint_destination: pinpoint_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#pinpoint_destination Sesv2ConfigurationSetEventDestination#pinpoint_destination}
        :param sns_destination: sns_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#sns_destination Sesv2ConfigurationSetEventDestination#sns_destination}
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestination(
            matching_event_types=matching_event_types,
            cloud_watch_destination=cloud_watch_destination,
            enabled=enabled,
            event_bridge_destination=event_bridge_destination,
            kinesis_firehose_destination=kinesis_firehose_destination,
            pinpoint_destination=pinpoint_destination,
            sns_destination=sns_destination,
        )

        return typing.cast(None, jsii.invoke(self, "putEventDestination", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="eventDestination")
    def event_destination(
        self,
    ) -> "Sesv2ConfigurationSetEventDestinationEventDestinationOutputReference":
        return typing.cast("Sesv2ConfigurationSetEventDestinationEventDestinationOutputReference", jsii.get(self, "eventDestination"))

    @builtins.property
    @jsii.member(jsii_name="configurationSetNameInput")
    def configuration_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventDestinationInput")
    def event_destination_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestination"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestination"], jsii.get(self, "eventDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="eventDestinationNameInput")
    def event_destination_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventDestinationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationSetName")
    def configuration_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configurationSetName"))

    @configuration_set_name.setter
    def configuration_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864994a98b1da8eaef7793562265dade3bc9b048c6542aa2eabd7732863594cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventDestinationName")
    def event_destination_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventDestinationName"))

    @event_destination_name.setter
    def event_destination_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7af5d6353585d5bb2a70b28647af5a5f14fd51db0614cd37ea65440f748dc74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventDestinationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90b6553dce5880113a8437a40e5319ea7189232d90c15a0397b928a5a0c6b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf1cd6c5727f30c35c22933f84d5e80449547a3696d306fb590f1862d32e8cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "configuration_set_name": "configurationSetName",
        "event_destination": "eventDestination",
        "event_destination_name": "eventDestinationName",
        "id": "id",
        "region": "region",
    },
)
class Sesv2ConfigurationSetEventDestinationConfig(
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
        configuration_set_name: builtins.str,
        event_destination: typing.Union["Sesv2ConfigurationSetEventDestinationEventDestination", typing.Dict[builtins.str, typing.Any]],
        event_destination_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param configuration_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#configuration_set_name Sesv2ConfigurationSetEventDestination#configuration_set_name}.
        :param event_destination: event_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_destination Sesv2ConfigurationSetEventDestination#event_destination}
        :param event_destination_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_destination_name Sesv2ConfigurationSetEventDestination#event_destination_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#id Sesv2ConfigurationSetEventDestination#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#region Sesv2ConfigurationSetEventDestination#region}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(event_destination, dict):
            event_destination = Sesv2ConfigurationSetEventDestinationEventDestination(**event_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fcc56d077b366fd417f958ea3d41093b6f11ca7523e1c94bcac482896ec1ca6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument configuration_set_name", value=configuration_set_name, expected_type=type_hints["configuration_set_name"])
            check_type(argname="argument event_destination", value=event_destination, expected_type=type_hints["event_destination"])
            check_type(argname="argument event_destination_name", value=event_destination_name, expected_type=type_hints["event_destination_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_set_name": configuration_set_name,
            "event_destination": event_destination,
            "event_destination_name": event_destination_name,
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
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region

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
    def configuration_set_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#configuration_set_name Sesv2ConfigurationSetEventDestination#configuration_set_name}.'''
        result = self._values.get("configuration_set_name")
        assert result is not None, "Required property 'configuration_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_destination(
        self,
    ) -> "Sesv2ConfigurationSetEventDestinationEventDestination":
        '''event_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_destination Sesv2ConfigurationSetEventDestination#event_destination}
        '''
        result = self._values.get("event_destination")
        assert result is not None, "Required property 'event_destination' is missing"
        return typing.cast("Sesv2ConfigurationSetEventDestinationEventDestination", result)

    @builtins.property
    def event_destination_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_destination_name Sesv2ConfigurationSetEventDestination#event_destination_name}.'''
        result = self._values.get("event_destination_name")
        assert result is not None, "Required property 'event_destination_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#id Sesv2ConfigurationSetEventDestination#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#region Sesv2ConfigurationSetEventDestination#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestination",
    jsii_struct_bases=[],
    name_mapping={
        "matching_event_types": "matchingEventTypes",
        "cloud_watch_destination": "cloudWatchDestination",
        "enabled": "enabled",
        "event_bridge_destination": "eventBridgeDestination",
        "kinesis_firehose_destination": "kinesisFirehoseDestination",
        "pinpoint_destination": "pinpointDestination",
        "sns_destination": "snsDestination",
    },
)
class Sesv2ConfigurationSetEventDestinationEventDestination:
    def __init__(
        self,
        *,
        matching_event_types: typing.Sequence[builtins.str],
        cloud_watch_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_bridge_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_firehose_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        pinpoint_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        sns_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_event_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#matching_event_types Sesv2ConfigurationSetEventDestination#matching_event_types}.
        :param cloud_watch_destination: cloud_watch_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#cloud_watch_destination Sesv2ConfigurationSetEventDestination#cloud_watch_destination}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#enabled Sesv2ConfigurationSetEventDestination#enabled}.
        :param event_bridge_destination: event_bridge_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_bridge_destination Sesv2ConfigurationSetEventDestination#event_bridge_destination}
        :param kinesis_firehose_destination: kinesis_firehose_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#kinesis_firehose_destination Sesv2ConfigurationSetEventDestination#kinesis_firehose_destination}
        :param pinpoint_destination: pinpoint_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#pinpoint_destination Sesv2ConfigurationSetEventDestination#pinpoint_destination}
        :param sns_destination: sns_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#sns_destination Sesv2ConfigurationSetEventDestination#sns_destination}
        '''
        if isinstance(cloud_watch_destination, dict):
            cloud_watch_destination = Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination(**cloud_watch_destination)
        if isinstance(event_bridge_destination, dict):
            event_bridge_destination = Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination(**event_bridge_destination)
        if isinstance(kinesis_firehose_destination, dict):
            kinesis_firehose_destination = Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination(**kinesis_firehose_destination)
        if isinstance(pinpoint_destination, dict):
            pinpoint_destination = Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination(**pinpoint_destination)
        if isinstance(sns_destination, dict):
            sns_destination = Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination(**sns_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d058a1a80bb6baead3e2a59cb88d5b9bf5b3273d22f251216ef38176042d95)
            check_type(argname="argument matching_event_types", value=matching_event_types, expected_type=type_hints["matching_event_types"])
            check_type(argname="argument cloud_watch_destination", value=cloud_watch_destination, expected_type=type_hints["cloud_watch_destination"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_bridge_destination", value=event_bridge_destination, expected_type=type_hints["event_bridge_destination"])
            check_type(argname="argument kinesis_firehose_destination", value=kinesis_firehose_destination, expected_type=type_hints["kinesis_firehose_destination"])
            check_type(argname="argument pinpoint_destination", value=pinpoint_destination, expected_type=type_hints["pinpoint_destination"])
            check_type(argname="argument sns_destination", value=sns_destination, expected_type=type_hints["sns_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "matching_event_types": matching_event_types,
        }
        if cloud_watch_destination is not None:
            self._values["cloud_watch_destination"] = cloud_watch_destination
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_bridge_destination is not None:
            self._values["event_bridge_destination"] = event_bridge_destination
        if kinesis_firehose_destination is not None:
            self._values["kinesis_firehose_destination"] = kinesis_firehose_destination
        if pinpoint_destination is not None:
            self._values["pinpoint_destination"] = pinpoint_destination
        if sns_destination is not None:
            self._values["sns_destination"] = sns_destination

    @builtins.property
    def matching_event_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#matching_event_types Sesv2ConfigurationSetEventDestination#matching_event_types}.'''
        result = self._values.get("matching_event_types")
        assert result is not None, "Required property 'matching_event_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cloud_watch_destination(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination"]:
        '''cloud_watch_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#cloud_watch_destination Sesv2ConfigurationSetEventDestination#cloud_watch_destination}
        '''
        result = self._values.get("cloud_watch_destination")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#enabled Sesv2ConfigurationSetEventDestination#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def event_bridge_destination(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination"]:
        '''event_bridge_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_bridge_destination Sesv2ConfigurationSetEventDestination#event_bridge_destination}
        '''
        result = self._values.get("event_bridge_destination")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination"], result)

    @builtins.property
    def kinesis_firehose_destination(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination"]:
        '''kinesis_firehose_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#kinesis_firehose_destination Sesv2ConfigurationSetEventDestination#kinesis_firehose_destination}
        '''
        result = self._values.get("kinesis_firehose_destination")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination"], result)

    @builtins.property
    def pinpoint_destination(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination"]:
        '''pinpoint_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#pinpoint_destination Sesv2ConfigurationSetEventDestination#pinpoint_destination}
        '''
        result = self._values.get("pinpoint_destination")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination"], result)

    @builtins.property
    def sns_destination(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination"]:
        '''sns_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#sns_destination Sesv2ConfigurationSetEventDestination#sns_destination}
        '''
        result = self._values.get("sns_destination")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination",
    jsii_struct_bases=[],
    name_mapping={"dimension_configuration": "dimensionConfiguration"},
)
class Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination:
    def __init__(
        self,
        *,
        dimension_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param dimension_configuration: dimension_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#dimension_configuration Sesv2ConfigurationSetEventDestination#dimension_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc59a641938e01ee222ee44b6a384337db0d882762181f20eb0e36e780df483)
            check_type(argname="argument dimension_configuration", value=dimension_configuration, expected_type=type_hints["dimension_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dimension_configuration": dimension_configuration,
        }

    @builtins.property
    def dimension_configuration(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration"]]:
        '''dimension_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#dimension_configuration Sesv2ConfigurationSetEventDestination#dimension_configuration}
        '''
        result = self._values.get("dimension_configuration")
        assert result is not None, "Required property 'dimension_configuration' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "default_dimension_value": "defaultDimensionValue",
        "dimension_name": "dimensionName",
        "dimension_value_source": "dimensionValueSource",
    },
)
class Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration:
    def __init__(
        self,
        *,
        default_dimension_value: builtins.str,
        dimension_name: builtins.str,
        dimension_value_source: builtins.str,
    ) -> None:
        '''
        :param default_dimension_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#default_dimension_value Sesv2ConfigurationSetEventDestination#default_dimension_value}.
        :param dimension_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#dimension_name Sesv2ConfigurationSetEventDestination#dimension_name}.
        :param dimension_value_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#dimension_value_source Sesv2ConfigurationSetEventDestination#dimension_value_source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49dad6cec884bced6d563a2f7f6999fba74d0cfb70da86408792531c5ca8284)
            check_type(argname="argument default_dimension_value", value=default_dimension_value, expected_type=type_hints["default_dimension_value"])
            check_type(argname="argument dimension_name", value=dimension_name, expected_type=type_hints["dimension_name"])
            check_type(argname="argument dimension_value_source", value=dimension_value_source, expected_type=type_hints["dimension_value_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_dimension_value": default_dimension_value,
            "dimension_name": dimension_name,
            "dimension_value_source": dimension_value_source,
        }

    @builtins.property
    def default_dimension_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#default_dimension_value Sesv2ConfigurationSetEventDestination#default_dimension_value}.'''
        result = self._values.get("default_dimension_value")
        assert result is not None, "Required property 'default_dimension_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#dimension_name Sesv2ConfigurationSetEventDestination#dimension_name}.'''
        result = self._values.get("dimension_name")
        assert result is not None, "Required property 'dimension_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension_value_source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#dimension_value_source Sesv2ConfigurationSetEventDestination#dimension_value_source}.'''
        result = self._values.get("dimension_value_source")
        assert result is not None, "Required property 'dimension_value_source' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2f1137469cfbd416f01f93599f5be1f9af6ed5918c9ba262b06d10a64e69fe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1d2abf56e02b22df827431a26daa2ba5cdf407190127b75a96e8ed2da024b1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5372219ddd2f143b33b42e22038fedd1bc8b678789664c0720049632dc77c36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6eb5dd8352d5904afcaed82030a2ec6ebdd07d390e60d86f135ef57117a30ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36c875813ed1803482750c62af03137afd7e11b143ef0aec3dcdc847bec4f567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd42b76d53e5eab93fc0c3cd9ddb2e263c7076e359bf51dff7c66784aaf160d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__767ff91c152dee6dba30de8bc4b0ffac848e99b0dd16bc7e250c12fe520ac92f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="defaultDimensionValueInput")
    def default_dimension_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDimensionValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionNameInput")
    def dimension_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionValueSourceInput")
    def dimension_value_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionValueSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDimensionValue")
    def default_dimension_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDimensionValue"))

    @default_dimension_value.setter
    def default_dimension_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8e1924d4bd322c7c045bac14846271862bf2b9a9defd3da25040e233a40ab4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDimensionValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimensionName")
    def dimension_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimensionName"))

    @dimension_name.setter
    def dimension_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ef5e8625c87c80066448b18909c8a7f803d9e5d064ec21c5f6f466228e91a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimensionValueSource")
    def dimension_value_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimensionValueSource"))

    @dimension_value_source.setter
    def dimension_value_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ec3714e0e49331b29515ac895b865c369812559b9d21fe84c3d4b0987f2209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensionValueSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e92c1af2f4ea97facdf61e3a41ccb6b0df6b931876fe2cca0b7d868850af01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2430434915c070c707d62a88b95b7af4402955c1f602b767c5730d1f510cbca0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDimensionConfiguration")
    def put_dimension_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ca21ad90741b8de7c13d9ff0ed661084885acc14dbd7faaca2488e4f9c04f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimensionConfiguration", [value]))

    @builtins.property
    @jsii.member(jsii_name="dimensionConfiguration")
    def dimension_configuration(
        self,
    ) -> Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationList:
        return typing.cast(Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationList, jsii.get(self, "dimensionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="dimensionConfigurationInput")
    def dimension_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]], jsii.get(self, "dimensionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0241b5d750926eb7b4544d2f6ff1920110c173935dc7e60b7f2bee31c49ca2f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination",
    jsii_struct_bases=[],
    name_mapping={"event_bus_arn": "eventBusArn"},
)
class Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination:
    def __init__(self, *, event_bus_arn: builtins.str) -> None:
        '''
        :param event_bus_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_bus_arn Sesv2ConfigurationSetEventDestination#event_bus_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e710828a111e0f9058f4a754f0278a4bd4c81d342553a22a9fc30e6b5ce069ec)
            check_type(argname="argument event_bus_arn", value=event_bus_arn, expected_type=type_hints["event_bus_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_bus_arn": event_bus_arn,
        }

    @builtins.property
    def event_bus_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_bus_arn Sesv2ConfigurationSetEventDestination#event_bus_arn}.'''
        result = self._values.get("event_bus_arn")
        assert result is not None, "Required property 'event_bus_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06fd12bcaa5daa4dccd910623ffaec0c79d4c4cdceff0b9703f098fbf455fd90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventBusArnInput")
    def event_bus_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventBusArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventBusArn"))

    @event_bus_arn.setter
    def event_bus_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f7215e30e5f41414d3d5c1cfe603deb08268c3abcf504c2a64a0956e3788f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventBusArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8479cf60a75e3a5296dcb5b85987d0d35e4d8b678f29bf5c0ec8394cefd3fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_stream_arn": "deliveryStreamArn",
        "iam_role_arn": "iamRoleArn",
    },
)
class Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination:
    def __init__(
        self,
        *,
        delivery_stream_arn: builtins.str,
        iam_role_arn: builtins.str,
    ) -> None:
        '''
        :param delivery_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#delivery_stream_arn Sesv2ConfigurationSetEventDestination#delivery_stream_arn}.
        :param iam_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#iam_role_arn Sesv2ConfigurationSetEventDestination#iam_role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9464100907ff32861741db7de541615d83d9676598c494b0029bb8fc9d7771a)
            check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delivery_stream_arn": delivery_stream_arn,
            "iam_role_arn": iam_role_arn,
        }

    @builtins.property
    def delivery_stream_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#delivery_stream_arn Sesv2ConfigurationSetEventDestination#delivery_stream_arn}.'''
        result = self._values.get("delivery_stream_arn")
        assert result is not None, "Required property 'delivery_stream_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def iam_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#iam_role_arn Sesv2ConfigurationSetEventDestination#iam_role_arn}.'''
        result = self._values.get("iam_role_arn")
        assert result is not None, "Required property 'iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b57d560b44d6d646dd28522489083923edf27e705bd65d27d43b770beaca8849)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArnInput")
    def delivery_stream_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryStreamArnInput"))

    @builtins.property
    @jsii.member(jsii_name="iamRoleArnInput")
    def iam_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamArn"))

    @delivery_stream_arn.setter
    def delivery_stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb6245129e723b43b8db51d60ed1eb19fbcf579b50371e096cad80dadfe83e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryStreamArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209b04100de526d0bf6193a5e9f10f707c9387abfa04e73528eab136c1a49ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e3bbf36336b31a6949ca6266ca5b36f8c8b1e4a726f293f335062e1d8df116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Sesv2ConfigurationSetEventDestinationEventDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61ccddf8342f0ff828ff247c181a374e6b16655a1bcae8f00ad9b218627f92de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudWatchDestination")
    def put_cloud_watch_destination(
        self,
        *,
        dimension_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param dimension_configuration: dimension_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#dimension_configuration Sesv2ConfigurationSetEventDestination#dimension_configuration}
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination(
            dimension_configuration=dimension_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putCloudWatchDestination", [value]))

    @jsii.member(jsii_name="putEventBridgeDestination")
    def put_event_bridge_destination(self, *, event_bus_arn: builtins.str) -> None:
        '''
        :param event_bus_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#event_bus_arn Sesv2ConfigurationSetEventDestination#event_bus_arn}.
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination(
            event_bus_arn=event_bus_arn
        )

        return typing.cast(None, jsii.invoke(self, "putEventBridgeDestination", [value]))

    @jsii.member(jsii_name="putKinesisFirehoseDestination")
    def put_kinesis_firehose_destination(
        self,
        *,
        delivery_stream_arn: builtins.str,
        iam_role_arn: builtins.str,
    ) -> None:
        '''
        :param delivery_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#delivery_stream_arn Sesv2ConfigurationSetEventDestination#delivery_stream_arn}.
        :param iam_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#iam_role_arn Sesv2ConfigurationSetEventDestination#iam_role_arn}.
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination(
            delivery_stream_arn=delivery_stream_arn, iam_role_arn=iam_role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisFirehoseDestination", [value]))

    @jsii.member(jsii_name="putPinpointDestination")
    def put_pinpoint_destination(self, *, application_arn: builtins.str) -> None:
        '''
        :param application_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#application_arn Sesv2ConfigurationSetEventDestination#application_arn}.
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination(
            application_arn=application_arn
        )

        return typing.cast(None, jsii.invoke(self, "putPinpointDestination", [value]))

    @jsii.member(jsii_name="putSnsDestination")
    def put_sns_destination(self, *, topic_arn: builtins.str) -> None:
        '''
        :param topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#topic_arn Sesv2ConfigurationSetEventDestination#topic_arn}.
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination(
            topic_arn=topic_arn
        )

        return typing.cast(None, jsii.invoke(self, "putSnsDestination", [value]))

    @jsii.member(jsii_name="resetCloudWatchDestination")
    def reset_cloud_watch_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudWatchDestination", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEventBridgeDestination")
    def reset_event_bridge_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventBridgeDestination", []))

    @jsii.member(jsii_name="resetKinesisFirehoseDestination")
    def reset_kinesis_firehose_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisFirehoseDestination", []))

    @jsii.member(jsii_name="resetPinpointDestination")
    def reset_pinpoint_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPinpointDestination", []))

    @jsii.member(jsii_name="resetSnsDestination")
    def reset_sns_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnsDestination", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchDestination")
    def cloud_watch_destination(
        self,
    ) -> Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationOutputReference:
        return typing.cast(Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationOutputReference, jsii.get(self, "cloudWatchDestination"))

    @builtins.property
    @jsii.member(jsii_name="eventBridgeDestination")
    def event_bridge_destination(
        self,
    ) -> Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestinationOutputReference:
        return typing.cast(Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestinationOutputReference, jsii.get(self, "eventBridgeDestination"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseDestination")
    def kinesis_firehose_destination(
        self,
    ) -> Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationOutputReference:
        return typing.cast(Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationOutputReference, jsii.get(self, "kinesisFirehoseDestination"))

    @builtins.property
    @jsii.member(jsii_name="pinpointDestination")
    def pinpoint_destination(
        self,
    ) -> "Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestinationOutputReference":
        return typing.cast("Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestinationOutputReference", jsii.get(self, "pinpointDestination"))

    @builtins.property
    @jsii.member(jsii_name="snsDestination")
    def sns_destination(
        self,
    ) -> "Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestinationOutputReference":
        return typing.cast("Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestinationOutputReference", jsii.get(self, "snsDestination"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchDestinationInput")
    def cloud_watch_destination_input(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination], jsii.get(self, "cloudWatchDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventBridgeDestinationInput")
    def event_bridge_destination_input(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination], jsii.get(self, "eventBridgeDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseDestinationInput")
    def kinesis_firehose_destination_input(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination], jsii.get(self, "kinesisFirehoseDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingEventTypesInput")
    def matching_event_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchingEventTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="pinpointDestinationInput")
    def pinpoint_destination_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination"], jsii.get(self, "pinpointDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="snsDestinationInput")
    def sns_destination_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination"], jsii.get(self, "snsDestinationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a9b6ad68ed3c85f9a5886e9d01108e6182b2d6dd4c90e0224bed27d4eae0cd71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchingEventTypes")
    def matching_event_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchingEventTypes"))

    @matching_event_types.setter
    def matching_event_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5875f609d044669b02c070f47e22abce7cf9db0e2887d348b46186cc2a838b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchingEventTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4e7d0cab8a750cdeef635c9bacd7c968ced9ef7fa78afe02f18ea2dd4b32ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination",
    jsii_struct_bases=[],
    name_mapping={"application_arn": "applicationArn"},
)
class Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination:
    def __init__(self, *, application_arn: builtins.str) -> None:
        '''
        :param application_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#application_arn Sesv2ConfigurationSetEventDestination#application_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__412f9c43745f0a9786d6d82c14521835f37588d61f38ec3468740ea96580728b)
            check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_arn": application_arn,
        }

    @builtins.property
    def application_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#application_arn Sesv2ConfigurationSetEventDestination#application_arn}.'''
        result = self._values.get("application_arn")
        assert result is not None, "Required property 'application_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58bede87b0929c817ca1211d84f5549733d2a3ad8ce538301e471f80adcf2ff5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="applicationArnInput")
    def application_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @application_arn.setter
    def application_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb80b33aead48ac6788ec33b33308ac0ab0d435e8258e8cbc496101d5a0cc275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b005a8572bf38b769c8668d171b63c60e560e19f137de0de1d66fd95e2cb9920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination",
    jsii_struct_bases=[],
    name_mapping={"topic_arn": "topicArn"},
)
class Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination:
    def __init__(self, *, topic_arn: builtins.str) -> None:
        '''
        :param topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#topic_arn Sesv2ConfigurationSetEventDestination#topic_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa0f560a4e522b84fe5a0289f3f4bb33ccc5edf89ed4f4b3dedd6441734c5a3)
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic_arn": topic_arn,
        }

    @builtins.property
    def topic_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set_event_destination#topic_arn Sesv2ConfigurationSetEventDestination#topic_arn}.'''
        result = self._values.get("topic_arn")
        assert result is not None, "Required property 'topic_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__494b51b7584520492f8ed32fd90eb1480ab0ca318bea0aa7e55fa64b43598716)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="topicArnInput")
    def topic_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicArnInput"))

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicArn"))

    @topic_arn.setter
    def topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835420a6ac218b1a7df730fd0a531f879fe31901794a2590d44106335c9048ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba197b68bc908e079f6e9906e5a070759a50f1dceb43c62005e56424b668ef77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Sesv2ConfigurationSetEventDestination",
    "Sesv2ConfigurationSetEventDestinationConfig",
    "Sesv2ConfigurationSetEventDestinationEventDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration",
    "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationList",
    "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestinationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestinationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestinationOutputReference",
]

publication.publish()

def _typecheckingstub__5ba9571935ba81567ad122a3573d40c80d951a0eaa34b4e1e003460718f3fc4e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    configuration_set_name: builtins.str,
    event_destination: typing.Union[Sesv2ConfigurationSetEventDestinationEventDestination, typing.Dict[builtins.str, typing.Any]],
    event_destination_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__18cc084f635ec99383b6e90d0dd1e4f1b40790fa9064a8da4059f4c3884abd67(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864994a98b1da8eaef7793562265dade3bc9b048c6542aa2eabd7732863594cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7af5d6353585d5bb2a70b28647af5a5f14fd51db0614cd37ea65440f748dc74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90b6553dce5880113a8437a40e5319ea7189232d90c15a0397b928a5a0c6b63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf1cd6c5727f30c35c22933f84d5e80449547a3696d306fb590f1862d32e8cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fcc56d077b366fd417f958ea3d41093b6f11ca7523e1c94bcac482896ec1ca6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    configuration_set_name: builtins.str,
    event_destination: typing.Union[Sesv2ConfigurationSetEventDestinationEventDestination, typing.Dict[builtins.str, typing.Any]],
    event_destination_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d058a1a80bb6baead3e2a59cb88d5b9bf5b3273d22f251216ef38176042d95(
    *,
    matching_event_types: typing.Sequence[builtins.str],
    cloud_watch_destination: typing.Optional[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_bridge_destination: typing.Optional[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_firehose_destination: typing.Optional[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    pinpoint_destination: typing.Optional[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    sns_destination: typing.Optional[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc59a641938e01ee222ee44b6a384337db0d882762181f20eb0e36e780df483(
    *,
    dimension_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49dad6cec884bced6d563a2f7f6999fba74d0cfb70da86408792531c5ca8284(
    *,
    default_dimension_value: builtins.str,
    dimension_name: builtins.str,
    dimension_value_source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f1137469cfbd416f01f93599f5be1f9af6ed5918c9ba262b06d10a64e69fe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1d2abf56e02b22df827431a26daa2ba5cdf407190127b75a96e8ed2da024b1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5372219ddd2f143b33b42e22038fedd1bc8b678789664c0720049632dc77c36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6eb5dd8352d5904afcaed82030a2ec6ebdd07d390e60d86f135ef57117a30ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c875813ed1803482750c62af03137afd7e11b143ef0aec3dcdc847bec4f567(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd42b76d53e5eab93fc0c3cd9ddb2e263c7076e359bf51dff7c66784aaf160d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767ff91c152dee6dba30de8bc4b0ffac848e99b0dd16bc7e250c12fe520ac92f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8e1924d4bd322c7c045bac14846271862bf2b9a9defd3da25040e233a40ab4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ef5e8625c87c80066448b18909c8a7f803d9e5d064ec21c5f6f466228e91a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ec3714e0e49331b29515ac895b865c369812559b9d21fe84c3d4b0987f2209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e92c1af2f4ea97facdf61e3a41ccb6b0df6b931876fe2cca0b7d868850af01(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2430434915c070c707d62a88b95b7af4402955c1f602b767c5730d1f510cbca0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ca21ad90741b8de7c13d9ff0ed661084885acc14dbd7faaca2488e4f9c04f7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0241b5d750926eb7b4544d2f6ff1920110c173935dc7e60b7f2bee31c49ca2f7(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e710828a111e0f9058f4a754f0278a4bd4c81d342553a22a9fc30e6b5ce069ec(
    *,
    event_bus_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06fd12bcaa5daa4dccd910623ffaec0c79d4c4cdceff0b9703f098fbf455fd90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f7215e30e5f41414d3d5c1cfe603deb08268c3abcf504c2a64a0956e3788f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8479cf60a75e3a5296dcb5b85987d0d35e4d8b678f29bf5c0ec8394cefd3fa(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9464100907ff32861741db7de541615d83d9676598c494b0029bb8fc9d7771a(
    *,
    delivery_stream_arn: builtins.str,
    iam_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57d560b44d6d646dd28522489083923edf27e705bd65d27d43b770beaca8849(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb6245129e723b43b8db51d60ed1eb19fbcf579b50371e096cad80dadfe83e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209b04100de526d0bf6193a5e9f10f707c9387abfa04e73528eab136c1a49ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e3bbf36336b31a6949ca6266ca5b36f8c8b1e4a726f293f335062e1d8df116(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ccddf8342f0ff828ff247c181a374e6b16655a1bcae8f00ad9b218627f92de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b6ad68ed3c85f9a5886e9d01108e6182b2d6dd4c90e0224bed27d4eae0cd71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5875f609d044669b02c070f47e22abce7cf9db0e2887d348b46186cc2a838b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4e7d0cab8a750cdeef635c9bacd7c968ced9ef7fa78afe02f18ea2dd4b32ff(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412f9c43745f0a9786d6d82c14521835f37588d61f38ec3468740ea96580728b(
    *,
    application_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bede87b0929c817ca1211d84f5549733d2a3ad8ce538301e471f80adcf2ff5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb80b33aead48ac6788ec33b33308ac0ab0d435e8258e8cbc496101d5a0cc275(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b005a8572bf38b769c8668d171b63c60e560e19f137de0de1d66fd95e2cb9920(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa0f560a4e522b84fe5a0289f3f4bb33ccc5edf89ed4f4b3dedd6441734c5a3(
    *,
    topic_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494b51b7584520492f8ed32fd90eb1480ab0ca318bea0aa7e55fa64b43598716(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835420a6ac218b1a7df730fd0a531f879fe31901794a2590d44106335c9048ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba197b68bc908e079f6e9906e5a070759a50f1dceb43c62005e56424b668ef77(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination],
) -> None:
    """Type checking stubs"""
    pass
