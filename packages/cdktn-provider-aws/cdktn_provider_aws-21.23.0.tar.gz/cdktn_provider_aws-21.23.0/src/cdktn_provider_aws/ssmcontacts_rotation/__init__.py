r'''
# `aws_ssmcontacts_rotation`

Refer to the Terraform Registry for docs: [`aws_ssmcontacts_rotation`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation).
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


class SsmcontactsRotation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotation",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation aws_ssmcontacts_rotation}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        contact_ids: typing.Sequence[builtins.str],
        name: builtins.str,
        time_zone_id: builtins.str,
        recurrence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrence", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation aws_ssmcontacts_rotation} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param contact_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#contact_ids SsmcontactsRotation#contact_ids}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#name SsmcontactsRotation#name}.
        :param time_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#time_zone_id SsmcontactsRotation#time_zone_id}.
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#recurrence SsmcontactsRotation#recurrence}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#region SsmcontactsRotation#region}
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#start_time SsmcontactsRotation#start_time}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#tags SsmcontactsRotation#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a619bf70d3102c23c0bdce132265c13a86a91d5374a96d4163f725020297b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = SsmcontactsRotationConfig(
            contact_ids=contact_ids,
            name=name,
            time_zone_id=time_zone_id,
            recurrence=recurrence,
            region=region,
            start_time=start_time,
            tags=tags,
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
        '''Generates CDKTF code for importing a SsmcontactsRotation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SsmcontactsRotation to import.
        :param import_from_id: The id of the existing SsmcontactsRotation that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SsmcontactsRotation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f0ce6f7ac782fd4e7d1febc422ff713edb52ba286938038caf8eb7ab3844b1b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrence", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73b4b4da2484f6ede368447a16c6f77b576b6c28e1fedad7d04bb44fe1b2e46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRecurrence", [value]))

    @jsii.member(jsii_name="resetRecurrence")
    def reset_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrence", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(self) -> "SsmcontactsRotationRecurrenceList":
        return typing.cast("SsmcontactsRotationRecurrenceList", jsii.get(self, "recurrence"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="contactIdsInput")
    def contact_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contactIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrence"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrence"]]], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneIdInput")
    def time_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="contactIds")
    def contact_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contactIds"))

    @contact_ids.setter
    def contact_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855bfff10eaa99c8b831c6946374071619f5c627ea6b0c676b81802307070bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8370ea75c60531b4eace7c96b3e8febeef19833bd70eda92dabeb21091d952c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8317778257ff2cb291fba90deeebbf04ce0b21751525916af547cf9597d63628)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad031a51902b45e4ad30142ebedd214025668707a1ee7903d06138e0d9dca67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381fd7ee3a50793616560db99533e8f1505e9ceef22416c016a981d9ec93ca3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZoneId")
    def time_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZoneId"))

    @time_zone_id.setter
    def time_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772502010ba84bc589dc9b32cb8c49214965a0cdfea2f456d64584bc60e81ad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZoneId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "contact_ids": "contactIds",
        "name": "name",
        "time_zone_id": "timeZoneId",
        "recurrence": "recurrence",
        "region": "region",
        "start_time": "startTime",
        "tags": "tags",
    },
)
class SsmcontactsRotationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        contact_ids: typing.Sequence[builtins.str],
        name: builtins.str,
        time_zone_id: builtins.str,
        recurrence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrence", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param contact_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#contact_ids SsmcontactsRotation#contact_ids}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#name SsmcontactsRotation#name}.
        :param time_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#time_zone_id SsmcontactsRotation#time_zone_id}.
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#recurrence SsmcontactsRotation#recurrence}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#region SsmcontactsRotation#region}
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#start_time SsmcontactsRotation#start_time}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#tags SsmcontactsRotation#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e39a3d3fd896dcaa3db3070622570d9feca3b4dabe4f9613523141ed9a55a75)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument contact_ids", value=contact_ids, expected_type=type_hints["contact_ids"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument time_zone_id", value=time_zone_id, expected_type=type_hints["time_zone_id"])
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contact_ids": contact_ids,
            "name": name,
            "time_zone_id": time_zone_id,
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
        if recurrence is not None:
            self._values["recurrence"] = recurrence
        if region is not None:
            self._values["region"] = region
        if start_time is not None:
            self._values["start_time"] = start_time
        if tags is not None:
            self._values["tags"] = tags

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
    def contact_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#contact_ids SsmcontactsRotation#contact_ids}.'''
        result = self._values.get("contact_ids")
        assert result is not None, "Required property 'contact_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#name SsmcontactsRotation#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#time_zone_id SsmcontactsRotation#time_zone_id}.'''
        result = self._values.get("time_zone_id")
        assert result is not None, "Required property 'time_zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recurrence(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrence"]]]:
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#recurrence SsmcontactsRotation#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrence"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#region SsmcontactsRotation#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#start_time SsmcontactsRotation#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#tags SsmcontactsRotation#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrence",
    jsii_struct_bases=[],
    name_mapping={
        "number_of_on_calls": "numberOfOnCalls",
        "recurrence_multiplier": "recurrenceMultiplier",
        "daily_settings": "dailySettings",
        "monthly_settings": "monthlySettings",
        "shift_coverages": "shiftCoverages",
        "weekly_settings": "weeklySettings",
    },
)
class SsmcontactsRotationRecurrence:
    def __init__(
        self,
        *,
        number_of_on_calls: jsii.Number,
        recurrence_multiplier: jsii.Number,
        daily_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceDailySettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        monthly_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceMonthlySettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        shift_coverages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceShiftCoverages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weekly_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceWeeklySettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param number_of_on_calls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#number_of_on_calls SsmcontactsRotation#number_of_on_calls}.
        :param recurrence_multiplier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#recurrence_multiplier SsmcontactsRotation#recurrence_multiplier}.
        :param daily_settings: daily_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#daily_settings SsmcontactsRotation#daily_settings}
        :param monthly_settings: monthly_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#monthly_settings SsmcontactsRotation#monthly_settings}
        :param shift_coverages: shift_coverages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#shift_coverages SsmcontactsRotation#shift_coverages}
        :param weekly_settings: weekly_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#weekly_settings SsmcontactsRotation#weekly_settings}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70657ddcc8f49189015540937d1641e4d5c8dac76fef62565159a88340843f57)
            check_type(argname="argument number_of_on_calls", value=number_of_on_calls, expected_type=type_hints["number_of_on_calls"])
            check_type(argname="argument recurrence_multiplier", value=recurrence_multiplier, expected_type=type_hints["recurrence_multiplier"])
            check_type(argname="argument daily_settings", value=daily_settings, expected_type=type_hints["daily_settings"])
            check_type(argname="argument monthly_settings", value=monthly_settings, expected_type=type_hints["monthly_settings"])
            check_type(argname="argument shift_coverages", value=shift_coverages, expected_type=type_hints["shift_coverages"])
            check_type(argname="argument weekly_settings", value=weekly_settings, expected_type=type_hints["weekly_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "number_of_on_calls": number_of_on_calls,
            "recurrence_multiplier": recurrence_multiplier,
        }
        if daily_settings is not None:
            self._values["daily_settings"] = daily_settings
        if monthly_settings is not None:
            self._values["monthly_settings"] = monthly_settings
        if shift_coverages is not None:
            self._values["shift_coverages"] = shift_coverages
        if weekly_settings is not None:
            self._values["weekly_settings"] = weekly_settings

    @builtins.property
    def number_of_on_calls(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#number_of_on_calls SsmcontactsRotation#number_of_on_calls}.'''
        result = self._values.get("number_of_on_calls")
        assert result is not None, "Required property 'number_of_on_calls' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def recurrence_multiplier(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#recurrence_multiplier SsmcontactsRotation#recurrence_multiplier}.'''
        result = self._values.get("recurrence_multiplier")
        assert result is not None, "Required property 'recurrence_multiplier' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def daily_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceDailySettings"]]]:
        '''daily_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#daily_settings SsmcontactsRotation#daily_settings}
        '''
        result = self._values.get("daily_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceDailySettings"]]], result)

    @builtins.property
    def monthly_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceMonthlySettings"]]]:
        '''monthly_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#monthly_settings SsmcontactsRotation#monthly_settings}
        '''
        result = self._values.get("monthly_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceMonthlySettings"]]], result)

    @builtins.property
    def shift_coverages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoverages"]]]:
        '''shift_coverages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#shift_coverages SsmcontactsRotation#shift_coverages}
        '''
        result = self._values.get("shift_coverages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoverages"]]], result)

    @builtins.property
    def weekly_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceWeeklySettings"]]]:
        '''weekly_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#weekly_settings SsmcontactsRotation#weekly_settings}
        '''
        result = self._values.get("weekly_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceWeeklySettings"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceDailySettings",
    jsii_struct_bases=[],
    name_mapping={"hour_of_day": "hourOfDay", "minute_of_hour": "minuteOfHour"},
)
class SsmcontactsRotationRecurrenceDailySettings:
    def __init__(
        self,
        *,
        hour_of_day: jsii.Number,
        minute_of_hour: jsii.Number,
    ) -> None:
        '''
        :param hour_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hour_of_day SsmcontactsRotation#hour_of_day}.
        :param minute_of_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#minute_of_hour SsmcontactsRotation#minute_of_hour}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3097b14ef1edd9636edc91f0fa3ee23fb422b98c4762c8560f64f0c52b6632)
            check_type(argname="argument hour_of_day", value=hour_of_day, expected_type=type_hints["hour_of_day"])
            check_type(argname="argument minute_of_hour", value=minute_of_hour, expected_type=type_hints["minute_of_hour"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hour_of_day": hour_of_day,
            "minute_of_hour": minute_of_hour,
        }

    @builtins.property
    def hour_of_day(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hour_of_day SsmcontactsRotation#hour_of_day}.'''
        result = self._values.get("hour_of_day")
        assert result is not None, "Required property 'hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minute_of_hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#minute_of_hour SsmcontactsRotation#minute_of_hour}.'''
        result = self._values.get("minute_of_hour")
        assert result is not None, "Required property 'minute_of_hour' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationRecurrenceDailySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmcontactsRotationRecurrenceDailySettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceDailySettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dee43f49eacf047931f0327cc5d3f3f3da4f6196397bfc38a9a269dd23fa23ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmcontactsRotationRecurrenceDailySettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57fd168b8f9d70e11ddab1524780f4776fe15a2959111fe0a4ee1432cc4f6d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmcontactsRotationRecurrenceDailySettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e5f6c430ac19587de879f991f9785f2ff37449be13d128ea28f96990ab5157)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7082e584fba58959216a478471ce0b7a5c04679d6a025971caadb48563f227a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc816bf826fbcac5a1ac4d3048161b3fdbef8a46a7bf1dc0ca4b38d260123764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceDailySettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceDailySettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceDailySettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e38bbf0f71fec9c070561667cb5572cb27b0ddb032f2f32f32e3fa36e880a9da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceDailySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceDailySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff568291b82c55b09589f1b99eea9117334d04cad4f5d2fdd5a88f81feec84e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hourOfDayInput")
    def hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteOfHourInput")
    def minute_of_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteOfHourInput"))

    @builtins.property
    @jsii.member(jsii_name="hourOfDay")
    def hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourOfDay"))

    @hour_of_day.setter
    def hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62bed95afd1d481482fb5530d9e14797b528388b41a66ae4592802bc13aee00f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minuteOfHour")
    def minute_of_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minuteOfHour"))

    @minute_of_hour.setter
    def minute_of_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8362f0791e504b869322f6b21e39b3bd37774e366a5b6388048fa8aad97b262e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minuteOfHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceDailySettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceDailySettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceDailySettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df56082473f61363bcb2521da2a0405a25e72748f514b252654a60a29da0c9e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__752168ec08942694a03eac69b8767b81aee8c8f55b892c18933ac1890d01bcbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SsmcontactsRotationRecurrenceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d084a7f0c48dc03889d0bb9b137b169dc3e30aa7280d242c17c328177588d2be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmcontactsRotationRecurrenceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d83598a9207c356be79e72dbcae641b90f66261f5470753ad595b6735d2bff7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de2431bc18ec7b80bda3d01270a2ce3689cbe6ad6231446470d92731d28cc36e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06c989d09a5863512c9add60f9b5573cbb9e6f02549b9d50a743563319541189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrence]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrence]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrence]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f73739bffc5f15dc613915010b0aa8f5154f9df2a0f118a9bbc281e6620e782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceMonthlySettings",
    jsii_struct_bases=[],
    name_mapping={"day_of_month": "dayOfMonth", "hand_off_time": "handOffTime"},
)
class SsmcontactsRotationRecurrenceMonthlySettings:
    def __init__(
        self,
        *,
        day_of_month: jsii.Number,
        hand_off_time: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param day_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#day_of_month SsmcontactsRotation#day_of_month}.
        :param hand_off_time: hand_off_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hand_off_time SsmcontactsRotation#hand_off_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6c91fd8a85ab35bde2a6056e92dbe3ccc54c3581f3bf8c682f7ff4e610259f)
            check_type(argname="argument day_of_month", value=day_of_month, expected_type=type_hints["day_of_month"])
            check_type(argname="argument hand_off_time", value=hand_off_time, expected_type=type_hints["hand_off_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_month": day_of_month,
        }
        if hand_off_time is not None:
            self._values["hand_off_time"] = hand_off_time

    @builtins.property
    def day_of_month(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#day_of_month SsmcontactsRotation#day_of_month}.'''
        result = self._values.get("day_of_month")
        assert result is not None, "Required property 'day_of_month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def hand_off_time(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime"]]]:
        '''hand_off_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hand_off_time SsmcontactsRotation#hand_off_time}
        '''
        result = self._values.get("hand_off_time")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationRecurrenceMonthlySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime",
    jsii_struct_bases=[],
    name_mapping={"hour_of_day": "hourOfDay", "minute_of_hour": "minuteOfHour"},
)
class SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime:
    def __init__(
        self,
        *,
        hour_of_day: jsii.Number,
        minute_of_hour: jsii.Number,
    ) -> None:
        '''
        :param hour_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hour_of_day SsmcontactsRotation#hour_of_day}.
        :param minute_of_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#minute_of_hour SsmcontactsRotation#minute_of_hour}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4384597393f23777afca9b019f36fe30af55579dc3eaa06d808ba0a4bca92fa)
            check_type(argname="argument hour_of_day", value=hour_of_day, expected_type=type_hints["hour_of_day"])
            check_type(argname="argument minute_of_hour", value=minute_of_hour, expected_type=type_hints["minute_of_hour"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hour_of_day": hour_of_day,
            "minute_of_hour": minute_of_hour,
        }

    @builtins.property
    def hour_of_day(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hour_of_day SsmcontactsRotation#hour_of_day}.'''
        result = self._values.get("hour_of_day")
        assert result is not None, "Required property 'hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minute_of_hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#minute_of_hour SsmcontactsRotation#minute_of_hour}.'''
        result = self._values.get("minute_of_hour")
        assert result is not None, "Required property 'minute_of_hour' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmcontactsRotationRecurrenceMonthlySettingsHandOffTimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceMonthlySettingsHandOffTimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46b1c252dca022fa12c91b4ff0d557ca8951ae0320f8fbcab4abc916946fff78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmcontactsRotationRecurrenceMonthlySettingsHandOffTimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296668a4470be6a322b121ca1eeb90abcb18ebc92b9c40d91f8f7c05c203941a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmcontactsRotationRecurrenceMonthlySettingsHandOffTimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9781e2bfb5e0d396311d36206b03228ab2a02b3b2afeded6231a11c532ab44cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cafe036321fe8b3acd7a1f7455b008c741793b6775a3b9940e2afe32e5be8ef0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c8a6f366d259ae4fa4b61913c75ec647bd4660a06c5721b1293f65cc21595ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443ce1f6cf489ec136697b68295ffd3ceaae6a48949fa3b1ea84fe53d9462d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceMonthlySettingsHandOffTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceMonthlySettingsHandOffTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a4e348d927d087faa38027e67f6aea9f8a27e17c7f1ab0883a3de22fd7b2491)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hourOfDayInput")
    def hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteOfHourInput")
    def minute_of_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteOfHourInput"))

    @builtins.property
    @jsii.member(jsii_name="hourOfDay")
    def hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourOfDay"))

    @hour_of_day.setter
    def hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a2477e113f9f3b121f547b2ff8fed61c35cf6f91cb7302e6cf220b6d25d1d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minuteOfHour")
    def minute_of_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minuteOfHour"))

    @minute_of_hour.setter
    def minute_of_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da9237980801719f78430c23a8655ba8b586a8b0d7b8101022dfe274e2d16a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minuteOfHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec35a67f0e12a617f40283dcec540c027ee0747cdc57d7d4410078e3226ba31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceMonthlySettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceMonthlySettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8ba8b6345704cdbcbd4b8d65cb1b891f055a57aa5d6b4c30c3918f9f4e32d7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmcontactsRotationRecurrenceMonthlySettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614aaf351d0dbfc5f5dbdcb61f028ca0ec33123829b51bc8573eb0ecbf972fc5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmcontactsRotationRecurrenceMonthlySettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8754c0e3bac33592b7ec8ce2d1789c6d2ea5d6fe5686dd4df6bcb3c0a0abc4c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a796cf728961e231300ac8ceff0fe33c99eaf759f79a53dcc35f80d53d2e0b5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cb956fa7abe6d76245463eb981090e1d2fcae31745bdad1d5824c4f58bcaa86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8f2f77df4ee40a41f209530be349eca5ccafdfc7cf89c2fb40435ecc8fcf04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceMonthlySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceMonthlySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__051a83228c25e9c216ff5aa0918652fb3f92442f602ddb5658d084dd9d199406)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHandOffTime")
    def put_hand_off_time(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d96fcbc2742499a2fc91d367a4503c5d877fe2a319edd465d1c163ef1fc2ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHandOffTime", [value]))

    @jsii.member(jsii_name="resetHandOffTime")
    def reset_hand_off_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHandOffTime", []))

    @builtins.property
    @jsii.member(jsii_name="handOffTime")
    def hand_off_time(
        self,
    ) -> SsmcontactsRotationRecurrenceMonthlySettingsHandOffTimeList:
        return typing.cast(SsmcontactsRotationRecurrenceMonthlySettingsHandOffTimeList, jsii.get(self, "handOffTime"))

    @builtins.property
    @jsii.member(jsii_name="dayOfMonthInput")
    def day_of_month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="handOffTimeInput")
    def hand_off_time_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime]]], jsii.get(self, "handOffTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfMonth")
    def day_of_month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dayOfMonth"))

    @day_of_month.setter
    def day_of_month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00be986e7ae326b550ce0d63e629969f7e6b71e7fd91840ffa47f9cfc07effcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceMonthlySettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceMonthlySettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceMonthlySettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492fe4678f31a913516653b13b419d1dae56b3c87063b76625d0b62842fa7484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f79ea237cdd2f3acbaf8b834c75b7ad7077336ff7ca100f3a52890c9dbe5a979)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDailySettings")
    def put_daily_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceDailySettings, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392799422c3ee27954589ecbe4709ef5bf9a842c81576ddb99851861cab4574f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDailySettings", [value]))

    @jsii.member(jsii_name="putMonthlySettings")
    def put_monthly_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceMonthlySettings, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151f74e97cb5a74163685dc1ef2e7961ebd0afe13461dc54023c3a8952928157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMonthlySettings", [value]))

    @jsii.member(jsii_name="putShiftCoverages")
    def put_shift_coverages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceShiftCoverages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e368e859cacbcf4221ad0952dc367fd23ab218997a4e26d0fef2ab099a99b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putShiftCoverages", [value]))

    @jsii.member(jsii_name="putWeeklySettings")
    def put_weekly_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceWeeklySettings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72eef68969de6d5f3e384f61c77856dc7b83a26ceda786f0ab9a0dfe1d6067bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeeklySettings", [value]))

    @jsii.member(jsii_name="resetDailySettings")
    def reset_daily_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailySettings", []))

    @jsii.member(jsii_name="resetMonthlySettings")
    def reset_monthly_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthlySettings", []))

    @jsii.member(jsii_name="resetShiftCoverages")
    def reset_shift_coverages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShiftCoverages", []))

    @jsii.member(jsii_name="resetWeeklySettings")
    def reset_weekly_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklySettings", []))

    @builtins.property
    @jsii.member(jsii_name="dailySettings")
    def daily_settings(self) -> SsmcontactsRotationRecurrenceDailySettingsList:
        return typing.cast(SsmcontactsRotationRecurrenceDailySettingsList, jsii.get(self, "dailySettings"))

    @builtins.property
    @jsii.member(jsii_name="monthlySettings")
    def monthly_settings(self) -> SsmcontactsRotationRecurrenceMonthlySettingsList:
        return typing.cast(SsmcontactsRotationRecurrenceMonthlySettingsList, jsii.get(self, "monthlySettings"))

    @builtins.property
    @jsii.member(jsii_name="shiftCoverages")
    def shift_coverages(self) -> "SsmcontactsRotationRecurrenceShiftCoveragesList":
        return typing.cast("SsmcontactsRotationRecurrenceShiftCoveragesList", jsii.get(self, "shiftCoverages"))

    @builtins.property
    @jsii.member(jsii_name="weeklySettings")
    def weekly_settings(self) -> "SsmcontactsRotationRecurrenceWeeklySettingsList":
        return typing.cast("SsmcontactsRotationRecurrenceWeeklySettingsList", jsii.get(self, "weeklySettings"))

    @builtins.property
    @jsii.member(jsii_name="dailySettingsInput")
    def daily_settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceDailySettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceDailySettings]]], jsii.get(self, "dailySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlySettingsInput")
    def monthly_settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettings]]], jsii.get(self, "monthlySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfOnCallsInput")
    def number_of_on_calls_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfOnCallsInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceMultiplierInput")
    def recurrence_multiplier_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "recurrenceMultiplierInput"))

    @builtins.property
    @jsii.member(jsii_name="shiftCoveragesInput")
    def shift_coverages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoverages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoverages"]]], jsii.get(self, "shiftCoveragesInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklySettingsInput")
    def weekly_settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceWeeklySettings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceWeeklySettings"]]], jsii.get(self, "weeklySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfOnCalls")
    def number_of_on_calls(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfOnCalls"))

    @number_of_on_calls.setter
    def number_of_on_calls(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada07ae43e5065c832ca10b80595827fd8958e28cc4385e02ca5a4ef7b9cd141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfOnCalls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrenceMultiplier")
    def recurrence_multiplier(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "recurrenceMultiplier"))

    @recurrence_multiplier.setter
    def recurrence_multiplier(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db5d5b90eb3f357afa793b225beeaadf4c44c726aac0a5205eda78b77697ff9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceMultiplier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrence]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrence]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrence]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b3edc12c526f53b37a05c535bc043928935953b9a3848ece3caf7727c4b73b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoverages",
    jsii_struct_bases=[],
    name_mapping={"map_block_key": "mapBlockKey", "coverage_times": "coverageTimes"},
)
class SsmcontactsRotationRecurrenceShiftCoverages:
    def __init__(
        self,
        *,
        map_block_key: builtins.str,
        coverage_times: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param map_block_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#map_block_key SsmcontactsRotation#map_block_key}.
        :param coverage_times: coverage_times block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#coverage_times SsmcontactsRotation#coverage_times}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cfbf479907fd8f797f72762770866d18903265efe804f0e3ae86e6060a78211)
            check_type(argname="argument map_block_key", value=map_block_key, expected_type=type_hints["map_block_key"])
            check_type(argname="argument coverage_times", value=coverage_times, expected_type=type_hints["coverage_times"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "map_block_key": map_block_key,
        }
        if coverage_times is not None:
            self._values["coverage_times"] = coverage_times

    @builtins.property
    def map_block_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#map_block_key SsmcontactsRotation#map_block_key}.'''
        result = self._values.get("map_block_key")
        assert result is not None, "Required property 'map_block_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def coverage_times(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes"]]]:
        '''coverage_times block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#coverage_times SsmcontactsRotation#coverage_times}
        '''
        result = self._values.get("coverage_times")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationRecurrenceShiftCoverages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes:
    def __init__(
        self,
        *,
        end: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
        start: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param end: end block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#end SsmcontactsRotation#end}
        :param start: start block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#start SsmcontactsRotation#start}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ea4056f337c82e5874037e55c2d4b1980f360966429e3c1149367e14533688)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if end is not None:
            self._values["end"] = end
        if start is not None:
            self._values["start"] = start

    @builtins.property
    def end(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd"]]]:
        '''end block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#end SsmcontactsRotation#end}
        '''
        result = self._values.get("end")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd"]]], result)

    @builtins.property
    def start(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart"]]]:
        '''start block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#start SsmcontactsRotation#start}
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd",
    jsii_struct_bases=[],
    name_mapping={"hour_of_day": "hourOfDay", "minute_of_hour": "minuteOfHour"},
)
class SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd:
    def __init__(
        self,
        *,
        hour_of_day: jsii.Number,
        minute_of_hour: jsii.Number,
    ) -> None:
        '''
        :param hour_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hour_of_day SsmcontactsRotation#hour_of_day}.
        :param minute_of_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#minute_of_hour SsmcontactsRotation#minute_of_hour}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2c7fb0ebe6374f8e246203e6b422fb6e2e018f97a9b454fcc02d8dee3ccce9)
            check_type(argname="argument hour_of_day", value=hour_of_day, expected_type=type_hints["hour_of_day"])
            check_type(argname="argument minute_of_hour", value=minute_of_hour, expected_type=type_hints["minute_of_hour"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hour_of_day": hour_of_day,
            "minute_of_hour": minute_of_hour,
        }

    @builtins.property
    def hour_of_day(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hour_of_day SsmcontactsRotation#hour_of_day}.'''
        result = self._values.get("hour_of_day")
        assert result is not None, "Required property 'hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minute_of_hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#minute_of_hour SsmcontactsRotation#minute_of_hour}.'''
        result = self._values.get("minute_of_hour")
        assert result is not None, "Required property 'minute_of_hour' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEndList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEndList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1904cbc4a7d808795c3e15e293396044020aeed1a99bd150b49b9c49d57986ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEndOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01c15b9292808604434600038280da86a52586fb9d703f873679b7d3c3bc439)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEndOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628d122f52aeb9b41af55605e1b353395ec4e83554a0d8bbdf96d65707936977)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7eeb4e07920cdd26d8a61d94373ff14668ce70ed154233956d2ca58b29cf55b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__977c1acec4f8ac1c5cf09e045ed6a92c4d5441a9761d8c4e1364ccae8e46ec56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec4f621614f6a3875566d9d5cb35bafcb4d2932402745ee829e53744094a79a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEndOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEndOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ff8bf4cfea2684c8655abdc6314c6c913844e191ae58d3ad74307e6dbe04115)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hourOfDayInput")
    def hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteOfHourInput")
    def minute_of_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteOfHourInput"))

    @builtins.property
    @jsii.member(jsii_name="hourOfDay")
    def hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourOfDay"))

    @hour_of_day.setter
    def hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b9c037c8eff030634c2d868d389aaf0497ecd7f817cbe971f8e38d7f4dc329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minuteOfHour")
    def minute_of_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minuteOfHour"))

    @minute_of_hour.setter
    def minute_of_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce30add72eea28a2f80e49a04c1da6b5ef49932dd7912b304e912923ff5c260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minuteOfHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488a2943b7ef441b6432a48af19d6b06a0c46f889e66bd9c7bc0c6e0a73a82d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67ecfd1c36100a6c1b7a9929cadc727680ac436094b9495068f34e818fe7353c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd965b3b131cc7814110019945f376708daee037f8277c3f487a619a1431450e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6c6d29932503c88b9a285ca3c542e807e22360b981310811c30e5a28980020)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e117149d98302fac36506aa0a927af5bf39f36b10424d70cc49398543948e9b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07fecf510fd3a7ffb3abab4ea1339db153e25814aa90891dd7682da14eeebedc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b65b2d8cabdb1c4ec30f6609b2c9a0b2a37911000811f38d0ec323987e5e5d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afe561bd28e0d95abb3399f456bd41b3de35c4079a11a1df656dfd45732567cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnd")
    def put_end(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494bffa1c600cef1f6aa20f1c45a4252984423cb270b44bd87fd607b3059093d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnd", [value]))

    @jsii.member(jsii_name="putStart")
    def put_start(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d54566dfb0a54494052aae0cceae0f19ffbbc18737db9c9ad9ca03064079fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStart", [value]))

    @jsii.member(jsii_name="resetEnd")
    def reset_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnd", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEndList:
        return typing.cast(SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEndList, jsii.get(self, "end"))

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(
        self,
    ) -> "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStartList":
        return typing.cast("SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStartList", jsii.get(self, "start"))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd]]], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart"]]], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b558bb2dd8c4cba872c87c5ff83e6b1a00372bd1caa993e59a94567c295dbd5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart",
    jsii_struct_bases=[],
    name_mapping={"hour_of_day": "hourOfDay", "minute_of_hour": "minuteOfHour"},
)
class SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart:
    def __init__(
        self,
        *,
        hour_of_day: jsii.Number,
        minute_of_hour: jsii.Number,
    ) -> None:
        '''
        :param hour_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hour_of_day SsmcontactsRotation#hour_of_day}.
        :param minute_of_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#minute_of_hour SsmcontactsRotation#minute_of_hour}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a814e35b0d6d340d04eab9557323097c9172068b8f91dd289089c3a79020d58b)
            check_type(argname="argument hour_of_day", value=hour_of_day, expected_type=type_hints["hour_of_day"])
            check_type(argname="argument minute_of_hour", value=minute_of_hour, expected_type=type_hints["minute_of_hour"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hour_of_day": hour_of_day,
            "minute_of_hour": minute_of_hour,
        }

    @builtins.property
    def hour_of_day(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hour_of_day SsmcontactsRotation#hour_of_day}.'''
        result = self._values.get("hour_of_day")
        assert result is not None, "Required property 'hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minute_of_hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#minute_of_hour SsmcontactsRotation#minute_of_hour}.'''
        result = self._values.get("minute_of_hour")
        assert result is not None, "Required property 'minute_of_hour' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStartList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStartList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f58609585afcf6743740a0c943dee1202bc72a8f63e8eb3b870e7ab1b07bf14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c86a1da65dd5fbc61aaee17f17b080abff75284a765ac38d20e31179c2f056c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd03ef9eab7325a3641d058a42f50af834e47f5db437379460aea648d9aa7162)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a91c5d7d18c48789527dbc1dcc854122aadeeca281b6da5e97c8c5355e6b7cc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2963f22a66c70d0cf73b0b8e4daede13043984571aa3dcbfda14089bbd9f986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d97c43abbf30ee65ccfa0d094820298cd33bb02f0b5e072ac99bc255fc0c9ec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStartOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStartOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__990d7354b032d3b19dbf13f2b0ec9b4f99beb6a96ad24fc9b12e8e59cbf787fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hourOfDayInput")
    def hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteOfHourInput")
    def minute_of_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteOfHourInput"))

    @builtins.property
    @jsii.member(jsii_name="hourOfDay")
    def hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourOfDay"))

    @hour_of_day.setter
    def hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ffa0deb75dc86f068c2c6b6634fc983a8963c9e73deefa6d0ce705e856df8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minuteOfHour")
    def minute_of_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minuteOfHour"))

    @minute_of_hour.setter
    def minute_of_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da647da0e6595cc462c442dd7badbfbc7c10cafc6a91b21048d28eac5dd0968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minuteOfHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775bb434b86fa34cf6d1b1b1067998dbc11c345a93cec7f1036b03bead31791b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceShiftCoveragesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4866e6da9c78feab1dcaafc91a5637e8b970346b178a65275dfaeb6ef0d9bc93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmcontactsRotationRecurrenceShiftCoveragesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530ea96a2978f1e668883131d015ebadef9ed5b0395e507ede058f1b43fadf70)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmcontactsRotationRecurrenceShiftCoveragesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04df7d837bf34231b9958f4b11c68e85f163977264ee0a2c1ea47d8b9ce2b54d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a41f10ef4715202cde712cf7353b2b732ef5517218e5a78cd652ceabc436791f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2f2efa7d7faf4e5a0f175e2e793cfd799330d3ee9870b1d18191e52c84fee6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoverages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoverages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoverages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5855d183117215760a573d3945474ca130e3101b40a81a3a7afa03819137ebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceShiftCoveragesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceShiftCoveragesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__656c509c714bf2731c8fbe52e80b20f4d54cd4b25e2009bd8ada5e29f0087df0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCoverageTimes")
    def put_coverage_times(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf35c87d5c62661355e2b48c7a587605275e95fc94db76ca998efb5e76c4d80e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCoverageTimes", [value]))

    @jsii.member(jsii_name="resetCoverageTimes")
    def reset_coverage_times(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoverageTimes", []))

    @builtins.property
    @jsii.member(jsii_name="coverageTimes")
    def coverage_times(
        self,
    ) -> SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesList:
        return typing.cast(SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesList, jsii.get(self, "coverageTimes"))

    @builtins.property
    @jsii.member(jsii_name="coverageTimesInput")
    def coverage_times_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes]]], jsii.get(self, "coverageTimesInput"))

    @builtins.property
    @jsii.member(jsii_name="mapBlockKeyInput")
    def map_block_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mapBlockKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="mapBlockKey")
    def map_block_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mapBlockKey"))

    @map_block_key.setter
    def map_block_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f454a442fb046903e34f25573410199644560f7dc38ed7ed78e9976beee6ec5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapBlockKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoverages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoverages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoverages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe074be8aa684ddc6c5bd4067da230dc6fc26b70c68ccfddd49a0e8d6fc18bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceWeeklySettings",
    jsii_struct_bases=[],
    name_mapping={"day_of_week": "dayOfWeek", "hand_off_time": "handOffTime"},
)
class SsmcontactsRotationRecurrenceWeeklySettings:
    def __init__(
        self,
        *,
        day_of_week: builtins.str,
        hand_off_time: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#day_of_week SsmcontactsRotation#day_of_week}.
        :param hand_off_time: hand_off_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hand_off_time SsmcontactsRotation#hand_off_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b360953dc9221b89138813cdcc8d9eb7297643be9d06523ff764bf5e0e803ce0)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument hand_off_time", value=hand_off_time, expected_type=type_hints["hand_off_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
        }
        if hand_off_time is not None:
            self._values["hand_off_time"] = hand_off_time

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#day_of_week SsmcontactsRotation#day_of_week}.'''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hand_off_time(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime"]]]:
        '''hand_off_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hand_off_time SsmcontactsRotation#hand_off_time}
        '''
        result = self._values.get("hand_off_time")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationRecurrenceWeeklySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime",
    jsii_struct_bases=[],
    name_mapping={"hour_of_day": "hourOfDay", "minute_of_hour": "minuteOfHour"},
)
class SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime:
    def __init__(
        self,
        *,
        hour_of_day: jsii.Number,
        minute_of_hour: jsii.Number,
    ) -> None:
        '''
        :param hour_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hour_of_day SsmcontactsRotation#hour_of_day}.
        :param minute_of_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#minute_of_hour SsmcontactsRotation#minute_of_hour}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296a9cbe75caa96d399990965962ed0744f5eb3e5020613c58bacb3c89aee09e)
            check_type(argname="argument hour_of_day", value=hour_of_day, expected_type=type_hints["hour_of_day"])
            check_type(argname="argument minute_of_hour", value=minute_of_hour, expected_type=type_hints["minute_of_hour"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hour_of_day": hour_of_day,
            "minute_of_hour": minute_of_hour,
        }

    @builtins.property
    def hour_of_day(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#hour_of_day SsmcontactsRotation#hour_of_day}.'''
        result = self._values.get("hour_of_day")
        assert result is not None, "Required property 'hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minute_of_hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssmcontacts_rotation#minute_of_hour SsmcontactsRotation#minute_of_hour}.'''
        result = self._values.get("minute_of_hour")
        assert result is not None, "Required property 'minute_of_hour' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmcontactsRotationRecurrenceWeeklySettingsHandOffTimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceWeeklySettingsHandOffTimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__257cee91d078ae2e5870286794dda8c610ac6a9b886f5a826f30cf321e5241af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmcontactsRotationRecurrenceWeeklySettingsHandOffTimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c36d30c760efc9b82659c7cd793fd38527db12f35aa98efb9b814e37d13c73)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmcontactsRotationRecurrenceWeeklySettingsHandOffTimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826a56d9f072f59188cdf0cddd400937f0e8e18b04b202cca71f54fcffad7a2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0f67a48265e970da41cae9f413673881591b22d98fee8e0323855b10d6a167b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__318e4acc3d314ba4af64beb0fc21eefd84fb9296c0eb047202e8d41c8b98e9c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1a2fe5f487ad4e0bdcf667a90efe15c3bf5d129062432fcf7adc8ed0e2cb4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceWeeklySettingsHandOffTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceWeeklySettingsHandOffTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dfbbb7c0378a50f82c8904e4090f93b6600b7c1f8c71b40f67a9b88822d1e91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hourOfDayInput")
    def hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteOfHourInput")
    def minute_of_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteOfHourInput"))

    @builtins.property
    @jsii.member(jsii_name="hourOfDay")
    def hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourOfDay"))

    @hour_of_day.setter
    def hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b57d95c7513ff243478f476cc3ce5cc0b16ef639bc3227061eec5109f7747c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minuteOfHour")
    def minute_of_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minuteOfHour"))

    @minute_of_hour.setter
    def minute_of_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2099cc62316fb5005d577a48b86f011ecc86dee5de43a5b0c2609d8ce088b408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minuteOfHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f36e5c3234aa39a97b91a304b04b4839ade52fcb2e7443b0a754db985f6af8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceWeeklySettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceWeeklySettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f173f3928fdec66135f4666d4530909ac3a323288aec6d8611477d2749115f68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmcontactsRotationRecurrenceWeeklySettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6656ec440b1d384454f0498fcbc4b96dc985e99238cfd616fa8bfd3be9f460bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmcontactsRotationRecurrenceWeeklySettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4f7744e6c20abe795727f65ca0a64e0ac73f9a0fb308df00cbdcfda62eec7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1833498f39db0b31958f0d7d4767860e822c42e3b96cdcbbb4c28da4723bf50b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f0ac8be66d7d6e45eba9e9725c85dba20c0ad67bc590bac89ba0e8434c39ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceWeeklySettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceWeeklySettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceWeeklySettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44786c844bf74247141a35196ad4b6bcbab924dbac3c6fb077c6ab7b538cbb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmcontactsRotationRecurrenceWeeklySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmcontactsRotation.SsmcontactsRotationRecurrenceWeeklySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0f32392b0f6ae41c38b57b76502ea6664f4c9c2bf55360f1b4373eada7ea16b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHandOffTime")
    def put_hand_off_time(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046d754a21b797d725fdbf4c5e0e8c3158a581b93001eb8a271628c0b2e212c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHandOffTime", [value]))

    @jsii.member(jsii_name="resetHandOffTime")
    def reset_hand_off_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHandOffTime", []))

    @builtins.property
    @jsii.member(jsii_name="handOffTime")
    def hand_off_time(
        self,
    ) -> SsmcontactsRotationRecurrenceWeeklySettingsHandOffTimeList:
        return typing.cast(SsmcontactsRotationRecurrenceWeeklySettingsHandOffTimeList, jsii.get(self, "handOffTime"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="handOffTimeInput")
    def hand_off_time_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime]]], jsii.get(self, "handOffTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__116fd17b803a2fad1c4fdb739473d33c2d3818b7f7f74da5b1a5ca1dd7473e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceWeeklySettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceWeeklySettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceWeeklySettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33d8210e36e0bc128a841e556b0d05e8d6d8e6feaec71a10bab408dc063ad89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SsmcontactsRotation",
    "SsmcontactsRotationConfig",
    "SsmcontactsRotationRecurrence",
    "SsmcontactsRotationRecurrenceDailySettings",
    "SsmcontactsRotationRecurrenceDailySettingsList",
    "SsmcontactsRotationRecurrenceDailySettingsOutputReference",
    "SsmcontactsRotationRecurrenceList",
    "SsmcontactsRotationRecurrenceMonthlySettings",
    "SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime",
    "SsmcontactsRotationRecurrenceMonthlySettingsHandOffTimeList",
    "SsmcontactsRotationRecurrenceMonthlySettingsHandOffTimeOutputReference",
    "SsmcontactsRotationRecurrenceMonthlySettingsList",
    "SsmcontactsRotationRecurrenceMonthlySettingsOutputReference",
    "SsmcontactsRotationRecurrenceOutputReference",
    "SsmcontactsRotationRecurrenceShiftCoverages",
    "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes",
    "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd",
    "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEndList",
    "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEndOutputReference",
    "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesList",
    "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesOutputReference",
    "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart",
    "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStartList",
    "SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStartOutputReference",
    "SsmcontactsRotationRecurrenceShiftCoveragesList",
    "SsmcontactsRotationRecurrenceShiftCoveragesOutputReference",
    "SsmcontactsRotationRecurrenceWeeklySettings",
    "SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime",
    "SsmcontactsRotationRecurrenceWeeklySettingsHandOffTimeList",
    "SsmcontactsRotationRecurrenceWeeklySettingsHandOffTimeOutputReference",
    "SsmcontactsRotationRecurrenceWeeklySettingsList",
    "SsmcontactsRotationRecurrenceWeeklySettingsOutputReference",
]

publication.publish()

def _typecheckingstub__a1a619bf70d3102c23c0bdce132265c13a86a91d5374a96d4163f725020297b8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    contact_ids: typing.Sequence[builtins.str],
    name: builtins.str,
    time_zone_id: builtins.str,
    recurrence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrence, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__8f0ce6f7ac782fd4e7d1febc422ff713edb52ba286938038caf8eb7ab3844b1b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73b4b4da2484f6ede368447a16c6f77b576b6c28e1fedad7d04bb44fe1b2e46(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrence, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855bfff10eaa99c8b831c6946374071619f5c627ea6b0c676b81802307070bd4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8370ea75c60531b4eace7c96b3e8febeef19833bd70eda92dabeb21091d952c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8317778257ff2cb291fba90deeebbf04ce0b21751525916af547cf9597d63628(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad031a51902b45e4ad30142ebedd214025668707a1ee7903d06138e0d9dca67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381fd7ee3a50793616560db99533e8f1505e9ceef22416c016a981d9ec93ca3e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772502010ba84bc589dc9b32cb8c49214965a0cdfea2f456d64584bc60e81ad3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e39a3d3fd896dcaa3db3070622570d9feca3b4dabe4f9613523141ed9a55a75(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    contact_ids: typing.Sequence[builtins.str],
    name: builtins.str,
    time_zone_id: builtins.str,
    recurrence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrence, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70657ddcc8f49189015540937d1641e4d5c8dac76fef62565159a88340843f57(
    *,
    number_of_on_calls: jsii.Number,
    recurrence_multiplier: jsii.Number,
    daily_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceDailySettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    monthly_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceMonthlySettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    shift_coverages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceShiftCoverages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    weekly_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceWeeklySettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3097b14ef1edd9636edc91f0fa3ee23fb422b98c4762c8560f64f0c52b6632(
    *,
    hour_of_day: jsii.Number,
    minute_of_hour: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee43f49eacf047931f0327cc5d3f3f3da4f6196397bfc38a9a269dd23fa23ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57fd168b8f9d70e11ddab1524780f4776fe15a2959111fe0a4ee1432cc4f6d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e5f6c430ac19587de879f991f9785f2ff37449be13d128ea28f96990ab5157(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7082e584fba58959216a478471ce0b7a5c04679d6a025971caadb48563f227a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc816bf826fbcac5a1ac4d3048161b3fdbef8a46a7bf1dc0ca4b38d260123764(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e38bbf0f71fec9c070561667cb5572cb27b0ddb032f2f32f32e3fa36e880a9da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceDailySettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff568291b82c55b09589f1b99eea9117334d04cad4f5d2fdd5a88f81feec84e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62bed95afd1d481482fb5530d9e14797b528388b41a66ae4592802bc13aee00f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8362f0791e504b869322f6b21e39b3bd37774e366a5b6388048fa8aad97b262e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df56082473f61363bcb2521da2a0405a25e72748f514b252654a60a29da0c9e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceDailySettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752168ec08942694a03eac69b8767b81aee8c8f55b892c18933ac1890d01bcbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d084a7f0c48dc03889d0bb9b137b169dc3e30aa7280d242c17c328177588d2be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d83598a9207c356be79e72dbcae641b90f66261f5470753ad595b6735d2bff7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2431bc18ec7b80bda3d01270a2ce3689cbe6ad6231446470d92731d28cc36e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c989d09a5863512c9add60f9b5573cbb9e6f02549b9d50a743563319541189(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f73739bffc5f15dc613915010b0aa8f5154f9df2a0f118a9bbc281e6620e782(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrence]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6c91fd8a85ab35bde2a6056e92dbe3ccc54c3581f3bf8c682f7ff4e610259f(
    *,
    day_of_month: jsii.Number,
    hand_off_time: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4384597393f23777afca9b019f36fe30af55579dc3eaa06d808ba0a4bca92fa(
    *,
    hour_of_day: jsii.Number,
    minute_of_hour: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b1c252dca022fa12c91b4ff0d557ca8951ae0320f8fbcab4abc916946fff78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296668a4470be6a322b121ca1eeb90abcb18ebc92b9c40d91f8f7c05c203941a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9781e2bfb5e0d396311d36206b03228ab2a02b3b2afeded6231a11c532ab44cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafe036321fe8b3acd7a1f7455b008c741793b6775a3b9940e2afe32e5be8ef0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8a6f366d259ae4fa4b61913c75ec647bd4660a06c5721b1293f65cc21595ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443ce1f6cf489ec136697b68295ffd3ceaae6a48949fa3b1ea84fe53d9462d1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4e348d927d087faa38027e67f6aea9f8a27e17c7f1ab0883a3de22fd7b2491(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a2477e113f9f3b121f547b2ff8fed61c35cf6f91cb7302e6cf220b6d25d1d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da9237980801719f78430c23a8655ba8b586a8b0d7b8101022dfe274e2d16a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec35a67f0e12a617f40283dcec540c027ee0747cdc57d7d4410078e3226ba31(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ba8b6345704cdbcbd4b8d65cb1b891f055a57aa5d6b4c30c3918f9f4e32d7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614aaf351d0dbfc5f5dbdcb61f028ca0ec33123829b51bc8573eb0ecbf972fc5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8754c0e3bac33592b7ec8ce2d1789c6d2ea5d6fe5686dd4df6bcb3c0a0abc4c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a796cf728961e231300ac8ceff0fe33c99eaf759f79a53dcc35f80d53d2e0b5c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb956fa7abe6d76245463eb981090e1d2fcae31745bdad1d5824c4f58bcaa86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8f2f77df4ee40a41f209530be349eca5ccafdfc7cf89c2fb40435ecc8fcf04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceMonthlySettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051a83228c25e9c216ff5aa0918652fb3f92442f602ddb5658d084dd9d199406(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d96fcbc2742499a2fc91d367a4503c5d877fe2a319edd465d1c163ef1fc2ca3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceMonthlySettingsHandOffTime, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00be986e7ae326b550ce0d63e629969f7e6b71e7fd91840ffa47f9cfc07effcf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492fe4678f31a913516653b13b419d1dae56b3c87063b76625d0b62842fa7484(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceMonthlySettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79ea237cdd2f3acbaf8b834c75b7ad7077336ff7ca100f3a52890c9dbe5a979(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392799422c3ee27954589ecbe4709ef5bf9a842c81576ddb99851861cab4574f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceDailySettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151f74e97cb5a74163685dc1ef2e7961ebd0afe13461dc54023c3a8952928157(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceMonthlySettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e368e859cacbcf4221ad0952dc367fd23ab218997a4e26d0fef2ab099a99b9d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceShiftCoverages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72eef68969de6d5f3e384f61c77856dc7b83a26ceda786f0ab9a0dfe1d6067bb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceWeeklySettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada07ae43e5065c832ca10b80595827fd8958e28cc4385e02ca5a4ef7b9cd141(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5d5b90eb3f357afa793b225beeaadf4c44c726aac0a5205eda78b77697ff9f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b3edc12c526f53b37a05c535bc043928935953b9a3848ece3caf7727c4b73b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrence]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfbf479907fd8f797f72762770866d18903265efe804f0e3ae86e6060a78211(
    *,
    map_block_key: builtins.str,
    coverage_times: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ea4056f337c82e5874037e55c2d4b1980f360966429e3c1149367e14533688(
    *,
    end: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    start: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2c7fb0ebe6374f8e246203e6b422fb6e2e018f97a9b454fcc02d8dee3ccce9(
    *,
    hour_of_day: jsii.Number,
    minute_of_hour: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1904cbc4a7d808795c3e15e293396044020aeed1a99bd150b49b9c49d57986ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01c15b9292808604434600038280da86a52586fb9d703f873679b7d3c3bc439(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628d122f52aeb9b41af55605e1b353395ec4e83554a0d8bbdf96d65707936977(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eeb4e07920cdd26d8a61d94373ff14668ce70ed154233956d2ca58b29cf55b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977c1acec4f8ac1c5cf09e045ed6a92c4d5441a9761d8c4e1364ccae8e46ec56(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec4f621614f6a3875566d9d5cb35bafcb4d2932402745ee829e53744094a79a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff8bf4cfea2684c8655abdc6314c6c913844e191ae58d3ad74307e6dbe04115(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b9c037c8eff030634c2d868d389aaf0497ecd7f817cbe971f8e38d7f4dc329(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce30add72eea28a2f80e49a04c1da6b5ef49932dd7912b304e912923ff5c260(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488a2943b7ef441b6432a48af19d6b06a0c46f889e66bd9c7bc0c6e0a73a82d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ecfd1c36100a6c1b7a9929cadc727680ac436094b9495068f34e818fe7353c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd965b3b131cc7814110019945f376708daee037f8277c3f487a619a1431450e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6c6d29932503c88b9a285ca3c542e807e22360b981310811c30e5a28980020(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e117149d98302fac36506aa0a927af5bf39f36b10424d70cc49398543948e9b2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07fecf510fd3a7ffb3abab4ea1339db153e25814aa90891dd7682da14eeebedc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65b2d8cabdb1c4ec30f6609b2c9a0b2a37911000811f38d0ec323987e5e5d98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe561bd28e0d95abb3399f456bd41b3de35c4079a11a1df656dfd45732567cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494bffa1c600cef1f6aa20f1c45a4252984423cb270b44bd87fd607b3059093d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesEnd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d54566dfb0a54494052aae0cceae0f19ffbbc18737db9c9ad9ca03064079fc4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b558bb2dd8c4cba872c87c5ff83e6b1a00372bd1caa993e59a94567c295dbd5e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a814e35b0d6d340d04eab9557323097c9172068b8f91dd289089c3a79020d58b(
    *,
    hour_of_day: jsii.Number,
    minute_of_hour: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f58609585afcf6743740a0c943dee1202bc72a8f63e8eb3b870e7ab1b07bf14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c86a1da65dd5fbc61aaee17f17b080abff75284a765ac38d20e31179c2f056c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd03ef9eab7325a3641d058a42f50af834e47f5db437379460aea648d9aa7162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91c5d7d18c48789527dbc1dcc854122aadeeca281b6da5e97c8c5355e6b7cc5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2963f22a66c70d0cf73b0b8e4daede13043984571aa3dcbfda14089bbd9f986(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97c43abbf30ee65ccfa0d094820298cd33bb02f0b5e072ac99bc255fc0c9ec8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990d7354b032d3b19dbf13f2b0ec9b4f99beb6a96ad24fc9b12e8e59cbf787fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ffa0deb75dc86f068c2c6b6634fc983a8963c9e73deefa6d0ce705e856df8a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da647da0e6595cc462c442dd7badbfbc7c10cafc6a91b21048d28eac5dd0968(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775bb434b86fa34cf6d1b1b1067998dbc11c345a93cec7f1036b03bead31791b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimesStart]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4866e6da9c78feab1dcaafc91a5637e8b970346b178a65275dfaeb6ef0d9bc93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530ea96a2978f1e668883131d015ebadef9ed5b0395e507ede058f1b43fadf70(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04df7d837bf34231b9958f4b11c68e85f163977264ee0a2c1ea47d8b9ce2b54d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41f10ef4715202cde712cf7353b2b732ef5517218e5a78cd652ceabc436791f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f2efa7d7faf4e5a0f175e2e793cfd799330d3ee9870b1d18191e52c84fee6b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5855d183117215760a573d3945474ca130e3101b40a81a3a7afa03819137ebd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceShiftCoverages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656c509c714bf2731c8fbe52e80b20f4d54cd4b25e2009bd8ada5e29f0087df0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf35c87d5c62661355e2b48c7a587605275e95fc94db76ca998efb5e76c4d80e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceShiftCoveragesCoverageTimes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f454a442fb046903e34f25573410199644560f7dc38ed7ed78e9976beee6ec5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe074be8aa684ddc6c5bd4067da230dc6fc26b70c68ccfddd49a0e8d6fc18bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceShiftCoverages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b360953dc9221b89138813cdcc8d9eb7297643be9d06523ff764bf5e0e803ce0(
    *,
    day_of_week: builtins.str,
    hand_off_time: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296a9cbe75caa96d399990965962ed0744f5eb3e5020613c58bacb3c89aee09e(
    *,
    hour_of_day: jsii.Number,
    minute_of_hour: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257cee91d078ae2e5870286794dda8c610ac6a9b886f5a826f30cf321e5241af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c36d30c760efc9b82659c7cd793fd38527db12f35aa98efb9b814e37d13c73(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826a56d9f072f59188cdf0cddd400937f0e8e18b04b202cca71f54fcffad7a2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f67a48265e970da41cae9f413673881591b22d98fee8e0323855b10d6a167b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318e4acc3d314ba4af64beb0fc21eefd84fb9296c0eb047202e8d41c8b98e9c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1a2fe5f487ad4e0bdcf667a90efe15c3bf5d129062432fcf7adc8ed0e2cb4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfbbb7c0378a50f82c8904e4090f93b6600b7c1f8c71b40f67a9b88822d1e91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b57d95c7513ff243478f476cc3ce5cc0b16ef639bc3227061eec5109f7747c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2099cc62316fb5005d577a48b86f011ecc86dee5de43a5b0c2609d8ce088b408(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f36e5c3234aa39a97b91a304b04b4839ade52fcb2e7443b0a754db985f6af8c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f173f3928fdec66135f4666d4530909ac3a323288aec6d8611477d2749115f68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6656ec440b1d384454f0498fcbc4b96dc985e99238cfd616fa8bfd3be9f460bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4f7744e6c20abe795727f65ca0a64e0ac73f9a0fb308df00cbdcfda62eec7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1833498f39db0b31958f0d7d4767860e822c42e3b96cdcbbb4c28da4723bf50b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0ac8be66d7d6e45eba9e9725c85dba20c0ad67bc590bac89ba0e8434c39ed9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44786c844bf74247141a35196ad4b6bcbab924dbac3c6fb077c6ab7b538cbb6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmcontactsRotationRecurrenceWeeklySettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f32392b0f6ae41c38b57b76502ea6664f4c9c2bf55360f1b4373eada7ea16b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046d754a21b797d725fdbf4c5e0e8c3158a581b93001eb8a271628c0b2e212c0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmcontactsRotationRecurrenceWeeklySettingsHandOffTime, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116fd17b803a2fad1c4fdb739473d33c2d3818b7f7f74da5b1a5ca1dd7473e73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33d8210e36e0bc128a841e556b0d05e8d6d8e6feaec71a10bab408dc063ad89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmcontactsRotationRecurrenceWeeklySettings]],
) -> None:
    """Type checking stubs"""
    pass
