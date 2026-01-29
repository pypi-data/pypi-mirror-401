r'''
# `aws_guardduty_organization_configuration`

Refer to the Terraform Registry for docs: [`aws_guardduty_organization_configuration`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration).
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


class GuarddutyOrganizationConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration aws_guardduty_organization_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        auto_enable_organization_members: builtins.str,
        detector_id: builtins.str,
        datasources: typing.Optional[typing.Union["GuarddutyOrganizationConfigurationDatasources", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration aws_guardduty_organization_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auto_enable_organization_members: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#auto_enable_organization_members GuarddutyOrganizationConfiguration#auto_enable_organization_members}.
        :param detector_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#detector_id GuarddutyOrganizationConfiguration#detector_id}.
        :param datasources: datasources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#datasources GuarddutyOrganizationConfiguration#datasources}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#id GuarddutyOrganizationConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#region GuarddutyOrganizationConfiguration#region}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e03e79e38166a77fe655ad90984d69a542942f307877dbf2f822e13781af30a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GuarddutyOrganizationConfigurationConfig(
            auto_enable_organization_members=auto_enable_organization_members,
            detector_id=detector_id,
            datasources=datasources,
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
        '''Generates CDKTF code for importing a GuarddutyOrganizationConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GuarddutyOrganizationConfiguration to import.
        :param import_from_id: The id of the existing GuarddutyOrganizationConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GuarddutyOrganizationConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f1ea4d1239968615ba4bbe60793d58204f0e5efdb16885a00edc3dab3dcc8e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDatasources")
    def put_datasources(
        self,
        *,
        kubernetes: typing.Optional[typing.Union["GuarddutyOrganizationConfigurationDatasourcesKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
        malware_protection: typing.Optional[typing.Union["GuarddutyOrganizationConfigurationDatasourcesMalwareProtection", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_logs: typing.Optional[typing.Union["GuarddutyOrganizationConfigurationDatasourcesS3Logs", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kubernetes: kubernetes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#kubernetes GuarddutyOrganizationConfiguration#kubernetes}
        :param malware_protection: malware_protection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#malware_protection GuarddutyOrganizationConfiguration#malware_protection}
        :param s3_logs: s3_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#s3_logs GuarddutyOrganizationConfiguration#s3_logs}
        '''
        value = GuarddutyOrganizationConfigurationDatasources(
            kubernetes=kubernetes,
            malware_protection=malware_protection,
            s3_logs=s3_logs,
        )

        return typing.cast(None, jsii.invoke(self, "putDatasources", [value]))

    @jsii.member(jsii_name="resetDatasources")
    def reset_datasources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasources", []))

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
    @jsii.member(jsii_name="datasources")
    def datasources(
        self,
    ) -> "GuarddutyOrganizationConfigurationDatasourcesOutputReference":
        return typing.cast("GuarddutyOrganizationConfigurationDatasourcesOutputReference", jsii.get(self, "datasources"))

    @builtins.property
    @jsii.member(jsii_name="autoEnableOrganizationMembersInput")
    def auto_enable_organization_members_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoEnableOrganizationMembersInput"))

    @builtins.property
    @jsii.member(jsii_name="datasourcesInput")
    def datasources_input(
        self,
    ) -> typing.Optional["GuarddutyOrganizationConfigurationDatasources"]:
        return typing.cast(typing.Optional["GuarddutyOrganizationConfigurationDatasources"], jsii.get(self, "datasourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="detectorIdInput")
    def detector_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "detectorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="autoEnableOrganizationMembers")
    def auto_enable_organization_members(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoEnableOrganizationMembers"))

    @auto_enable_organization_members.setter
    def auto_enable_organization_members(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7837fb61216b88ccdd1229b4b2c867650ac073be9bb8d17f5a31f370c294cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoEnableOrganizationMembers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectorId")
    def detector_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detectorId"))

    @detector_id.setter
    def detector_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecdf0d730ef43d6f3f496ab2f9a3b5add6a3508ed5ec7d4a127758204709584d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbfa863bc71d0bc3d9652c5f975070e244999a109f66364acb98dfd04a7a8452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c0e74752f72919fd628ee804c155e9e73e5662c49d37d3aa6bd59bbd5fb6af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "auto_enable_organization_members": "autoEnableOrganizationMembers",
        "detector_id": "detectorId",
        "datasources": "datasources",
        "id": "id",
        "region": "region",
    },
)
class GuarddutyOrganizationConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auto_enable_organization_members: builtins.str,
        detector_id: builtins.str,
        datasources: typing.Optional[typing.Union["GuarddutyOrganizationConfigurationDatasources", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param auto_enable_organization_members: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#auto_enable_organization_members GuarddutyOrganizationConfiguration#auto_enable_organization_members}.
        :param detector_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#detector_id GuarddutyOrganizationConfiguration#detector_id}.
        :param datasources: datasources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#datasources GuarddutyOrganizationConfiguration#datasources}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#id GuarddutyOrganizationConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#region GuarddutyOrganizationConfiguration#region}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(datasources, dict):
            datasources = GuarddutyOrganizationConfigurationDatasources(**datasources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f03b901b9615701ffb5f525e26befa66b0e42d53e5bf7565e28e79217501e4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auto_enable_organization_members", value=auto_enable_organization_members, expected_type=type_hints["auto_enable_organization_members"])
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument datasources", value=datasources, expected_type=type_hints["datasources"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_enable_organization_members": auto_enable_organization_members,
            "detector_id": detector_id,
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
        if datasources is not None:
            self._values["datasources"] = datasources
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
    def auto_enable_organization_members(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#auto_enable_organization_members GuarddutyOrganizationConfiguration#auto_enable_organization_members}.'''
        result = self._values.get("auto_enable_organization_members")
        assert result is not None, "Required property 'auto_enable_organization_members' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def detector_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#detector_id GuarddutyOrganizationConfiguration#detector_id}.'''
        result = self._values.get("detector_id")
        assert result is not None, "Required property 'detector_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datasources(
        self,
    ) -> typing.Optional["GuarddutyOrganizationConfigurationDatasources"]:
        '''datasources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#datasources GuarddutyOrganizationConfiguration#datasources}
        '''
        result = self._values.get("datasources")
        return typing.cast(typing.Optional["GuarddutyOrganizationConfigurationDatasources"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#id GuarddutyOrganizationConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#region GuarddutyOrganizationConfiguration#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuarddutyOrganizationConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasources",
    jsii_struct_bases=[],
    name_mapping={
        "kubernetes": "kubernetes",
        "malware_protection": "malwareProtection",
        "s3_logs": "s3Logs",
    },
)
class GuarddutyOrganizationConfigurationDatasources:
    def __init__(
        self,
        *,
        kubernetes: typing.Optional[typing.Union["GuarddutyOrganizationConfigurationDatasourcesKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
        malware_protection: typing.Optional[typing.Union["GuarddutyOrganizationConfigurationDatasourcesMalwareProtection", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_logs: typing.Optional[typing.Union["GuarddutyOrganizationConfigurationDatasourcesS3Logs", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kubernetes: kubernetes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#kubernetes GuarddutyOrganizationConfiguration#kubernetes}
        :param malware_protection: malware_protection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#malware_protection GuarddutyOrganizationConfiguration#malware_protection}
        :param s3_logs: s3_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#s3_logs GuarddutyOrganizationConfiguration#s3_logs}
        '''
        if isinstance(kubernetes, dict):
            kubernetes = GuarddutyOrganizationConfigurationDatasourcesKubernetes(**kubernetes)
        if isinstance(malware_protection, dict):
            malware_protection = GuarddutyOrganizationConfigurationDatasourcesMalwareProtection(**malware_protection)
        if isinstance(s3_logs, dict):
            s3_logs = GuarddutyOrganizationConfigurationDatasourcesS3Logs(**s3_logs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4887cb2e1c373049b37a32d5856951d99ca683808509102037a6893c2787f15)
            check_type(argname="argument kubernetes", value=kubernetes, expected_type=type_hints["kubernetes"])
            check_type(argname="argument malware_protection", value=malware_protection, expected_type=type_hints["malware_protection"])
            check_type(argname="argument s3_logs", value=s3_logs, expected_type=type_hints["s3_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kubernetes is not None:
            self._values["kubernetes"] = kubernetes
        if malware_protection is not None:
            self._values["malware_protection"] = malware_protection
        if s3_logs is not None:
            self._values["s3_logs"] = s3_logs

    @builtins.property
    def kubernetes(
        self,
    ) -> typing.Optional["GuarddutyOrganizationConfigurationDatasourcesKubernetes"]:
        '''kubernetes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#kubernetes GuarddutyOrganizationConfiguration#kubernetes}
        '''
        result = self._values.get("kubernetes")
        return typing.cast(typing.Optional["GuarddutyOrganizationConfigurationDatasourcesKubernetes"], result)

    @builtins.property
    def malware_protection(
        self,
    ) -> typing.Optional["GuarddutyOrganizationConfigurationDatasourcesMalwareProtection"]:
        '''malware_protection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#malware_protection GuarddutyOrganizationConfiguration#malware_protection}
        '''
        result = self._values.get("malware_protection")
        return typing.cast(typing.Optional["GuarddutyOrganizationConfigurationDatasourcesMalwareProtection"], result)

    @builtins.property
    def s3_logs(
        self,
    ) -> typing.Optional["GuarddutyOrganizationConfigurationDatasourcesS3Logs"]:
        '''s3_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#s3_logs GuarddutyOrganizationConfiguration#s3_logs}
        '''
        result = self._values.get("s3_logs")
        return typing.cast(typing.Optional["GuarddutyOrganizationConfigurationDatasourcesS3Logs"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuarddutyOrganizationConfigurationDatasources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesKubernetes",
    jsii_struct_bases=[],
    name_mapping={"audit_logs": "auditLogs"},
)
class GuarddutyOrganizationConfigurationDatasourcesKubernetes:
    def __init__(
        self,
        *,
        audit_logs: typing.Union["GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param audit_logs: audit_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#audit_logs GuarddutyOrganizationConfiguration#audit_logs}
        '''
        if isinstance(audit_logs, dict):
            audit_logs = GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs(**audit_logs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4fa2cb9b0bf0dd4ccd5d1b73c181aad5b49cfcc03c49409699f0b350ac74243)
            check_type(argname="argument audit_logs", value=audit_logs, expected_type=type_hints["audit_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audit_logs": audit_logs,
        }

    @builtins.property
    def audit_logs(
        self,
    ) -> "GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs":
        '''audit_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#audit_logs GuarddutyOrganizationConfiguration#audit_logs}
        '''
        result = self._values.get("audit_logs")
        assert result is not None, "Required property 'audit_logs' is missing"
        return typing.cast("GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuarddutyOrganizationConfigurationDatasourcesKubernetes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs",
    jsii_struct_bases=[],
    name_mapping={"enable": "enable"},
)
class GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs:
    def __init__(
        self,
        *,
        enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#enable GuarddutyOrganizationConfiguration#enable}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d930d00b25e008cd260367bb96ff3d71d0296dfa3ee9d54d0d29b97b4bc680bd)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable": enable,
        }

    @builtins.property
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#enable GuarddutyOrganizationConfiguration#enable}.'''
        result = self._values.get("enable")
        assert result is not None, "Required property 'enable' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1fb149b50eddb7615f0d3857fe827aba644a264f35f8ff47bfde7698a0e0063)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2ffd3e542fc7038c3b307fb62a10491df69d1beb43b15b512384d8ba4000b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce56fba90afd82cfcf155391c380151d40145cea4fafefd77c1e5b0816a8259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GuarddutyOrganizationConfigurationDatasourcesKubernetesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesKubernetesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c64bd1170e69b867e6649f946254acb492b82ce0021a5be91bcec33d5a70859f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuditLogs")
    def put_audit_logs(
        self,
        *,
        enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#enable GuarddutyOrganizationConfiguration#enable}.
        '''
        value = GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs(
            enable=enable
        )

        return typing.cast(None, jsii.invoke(self, "putAuditLogs", [value]))

    @builtins.property
    @jsii.member(jsii_name="auditLogs")
    def audit_logs(
        self,
    ) -> GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogsOutputReference:
        return typing.cast(GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogsOutputReference, jsii.get(self, "auditLogs"))

    @builtins.property
    @jsii.member(jsii_name="auditLogsInput")
    def audit_logs_input(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs], jsii.get(self, "auditLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetes]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab760ef1127066e18adcf06811009099b01ce5ec4ba4829a9ad7885e1031074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesMalwareProtection",
    jsii_struct_bases=[],
    name_mapping={"scan_ec2_instance_with_findings": "scanEc2InstanceWithFindings"},
)
class GuarddutyOrganizationConfigurationDatasourcesMalwareProtection:
    def __init__(
        self,
        *,
        scan_ec2_instance_with_findings: typing.Union["GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param scan_ec2_instance_with_findings: scan_ec2_instance_with_findings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#scan_ec2_instance_with_findings GuarddutyOrganizationConfiguration#scan_ec2_instance_with_findings}
        '''
        if isinstance(scan_ec2_instance_with_findings, dict):
            scan_ec2_instance_with_findings = GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings(**scan_ec2_instance_with_findings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6cae0d9fac96db1f62e78f9cb859535e7a43d997eec2f78564e5a1638ff356)
            check_type(argname="argument scan_ec2_instance_with_findings", value=scan_ec2_instance_with_findings, expected_type=type_hints["scan_ec2_instance_with_findings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scan_ec2_instance_with_findings": scan_ec2_instance_with_findings,
        }

    @builtins.property
    def scan_ec2_instance_with_findings(
        self,
    ) -> "GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings":
        '''scan_ec2_instance_with_findings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#scan_ec2_instance_with_findings GuarddutyOrganizationConfiguration#scan_ec2_instance_with_findings}
        '''
        result = self._values.get("scan_ec2_instance_with_findings")
        assert result is not None, "Required property 'scan_ec2_instance_with_findings' is missing"
        return typing.cast("GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuarddutyOrganizationConfigurationDatasourcesMalwareProtection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__497f83d68a230546f1c5309a7206793a5c480cc916174026d66b621691a4ab30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScanEc2InstanceWithFindings")
    def put_scan_ec2_instance_with_findings(
        self,
        *,
        ebs_volumes: typing.Union["GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param ebs_volumes: ebs_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#ebs_volumes GuarddutyOrganizationConfiguration#ebs_volumes}
        '''
        value = GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings(
            ebs_volumes=ebs_volumes
        )

        return typing.cast(None, jsii.invoke(self, "putScanEc2InstanceWithFindings", [value]))

    @builtins.property
    @jsii.member(jsii_name="scanEc2InstanceWithFindings")
    def scan_ec2_instance_with_findings(
        self,
    ) -> "GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsOutputReference":
        return typing.cast("GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsOutputReference", jsii.get(self, "scanEc2InstanceWithFindings"))

    @builtins.property
    @jsii.member(jsii_name="scanEc2InstanceWithFindingsInput")
    def scan_ec2_instance_with_findings_input(
        self,
    ) -> typing.Optional["GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings"]:
        return typing.cast(typing.Optional["GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings"], jsii.get(self, "scanEc2InstanceWithFindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtection]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3579108b6ea7f716740e30f1869182add4e72e30a596eb9287092dd1893bfc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings",
    jsii_struct_bases=[],
    name_mapping={"ebs_volumes": "ebsVolumes"},
)
class GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings:
    def __init__(
        self,
        *,
        ebs_volumes: typing.Union["GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param ebs_volumes: ebs_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#ebs_volumes GuarddutyOrganizationConfiguration#ebs_volumes}
        '''
        if isinstance(ebs_volumes, dict):
            ebs_volumes = GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes(**ebs_volumes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ccc7cb0ef99afa0c1a3113c53812460fa95e6dedaf038b8d2d1d8dd2fa7c31)
            check_type(argname="argument ebs_volumes", value=ebs_volumes, expected_type=type_hints["ebs_volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ebs_volumes": ebs_volumes,
        }

    @builtins.property
    def ebs_volumes(
        self,
    ) -> "GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes":
        '''ebs_volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#ebs_volumes GuarddutyOrganizationConfiguration#ebs_volumes}
        '''
        result = self._values.get("ebs_volumes")
        assert result is not None, "Required property 'ebs_volumes' is missing"
        return typing.cast("GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes",
    jsii_struct_bases=[],
    name_mapping={"auto_enable": "autoEnable"},
)
class GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes:
    def __init__(
        self,
        *,
        auto_enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param auto_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#auto_enable GuarddutyOrganizationConfiguration#auto_enable}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525a46c6da512d0edcbd05d6348db25d0ed621742948f4148195a3bd80d087eb)
            check_type(argname="argument auto_enable", value=auto_enable, expected_type=type_hints["auto_enable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_enable": auto_enable,
        }

    @builtins.property
    def auto_enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#auto_enable GuarddutyOrganizationConfiguration#auto_enable}.'''
        result = self._values.get("auto_enable")
        assert result is not None, "Required property 'auto_enable' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2f6bb2daada30c622953e43f2f49de3340c3f2c50d05d518e1cd6dfb6c35676)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="autoEnableInput")
    def auto_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="autoEnable")
    def auto_enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoEnable"))

    @auto_enable.setter
    def auto_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba32f4355dd77341a94e7bcafa792fdd1b22e10e75c69d6e1d905e5365f68c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77ae6a0d198edd8cea2f40375b09408b9a439e4f0d8c5e69eef6abec31034f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e37555da54bb0056813631536867ace02cb5b1312a5114efb870b7acc79c07b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEbsVolumes")
    def put_ebs_volumes(
        self,
        *,
        auto_enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param auto_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#auto_enable GuarddutyOrganizationConfiguration#auto_enable}.
        '''
        value = GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes(
            auto_enable=auto_enable
        )

        return typing.cast(None, jsii.invoke(self, "putEbsVolumes", [value]))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumes")
    def ebs_volumes(
        self,
    ) -> GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesOutputReference:
        return typing.cast(GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesOutputReference, jsii.get(self, "ebsVolumes"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumesInput")
    def ebs_volumes_input(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes], jsii.get(self, "ebsVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98cf14c636b90de73eb83cb1111596559d12c48d2a4c3d6fe7e79dce714bdae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GuarddutyOrganizationConfigurationDatasourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbee17f0456c7d77d2df75ab04a0afc15d0fa0b3027b787fd8ed4eb539aaba98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKubernetes")
    def put_kubernetes(
        self,
        *,
        audit_logs: typing.Union[GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param audit_logs: audit_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#audit_logs GuarddutyOrganizationConfiguration#audit_logs}
        '''
        value = GuarddutyOrganizationConfigurationDatasourcesKubernetes(
            audit_logs=audit_logs
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetes", [value]))

    @jsii.member(jsii_name="putMalwareProtection")
    def put_malware_protection(
        self,
        *,
        scan_ec2_instance_with_findings: typing.Union[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param scan_ec2_instance_with_findings: scan_ec2_instance_with_findings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#scan_ec2_instance_with_findings GuarddutyOrganizationConfiguration#scan_ec2_instance_with_findings}
        '''
        value = GuarddutyOrganizationConfigurationDatasourcesMalwareProtection(
            scan_ec2_instance_with_findings=scan_ec2_instance_with_findings
        )

        return typing.cast(None, jsii.invoke(self, "putMalwareProtection", [value]))

    @jsii.member(jsii_name="putS3Logs")
    def put_s3_logs(
        self,
        *,
        auto_enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param auto_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#auto_enable GuarddutyOrganizationConfiguration#auto_enable}.
        '''
        value = GuarddutyOrganizationConfigurationDatasourcesS3Logs(
            auto_enable=auto_enable
        )

        return typing.cast(None, jsii.invoke(self, "putS3Logs", [value]))

    @jsii.member(jsii_name="resetKubernetes")
    def reset_kubernetes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetes", []))

    @jsii.member(jsii_name="resetMalwareProtection")
    def reset_malware_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMalwareProtection", []))

    @jsii.member(jsii_name="resetS3Logs")
    def reset_s3_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Logs", []))

    @builtins.property
    @jsii.member(jsii_name="kubernetes")
    def kubernetes(
        self,
    ) -> GuarddutyOrganizationConfigurationDatasourcesKubernetesOutputReference:
        return typing.cast(GuarddutyOrganizationConfigurationDatasourcesKubernetesOutputReference, jsii.get(self, "kubernetes"))

    @builtins.property
    @jsii.member(jsii_name="malwareProtection")
    def malware_protection(
        self,
    ) -> GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionOutputReference:
        return typing.cast(GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionOutputReference, jsii.get(self, "malwareProtection"))

    @builtins.property
    @jsii.member(jsii_name="s3Logs")
    def s3_logs(
        self,
    ) -> "GuarddutyOrganizationConfigurationDatasourcesS3LogsOutputReference":
        return typing.cast("GuarddutyOrganizationConfigurationDatasourcesS3LogsOutputReference", jsii.get(self, "s3Logs"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesInput")
    def kubernetes_input(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetes]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetes], jsii.get(self, "kubernetesInput"))

    @builtins.property
    @jsii.member(jsii_name="malwareProtectionInput")
    def malware_protection_input(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtection]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtection], jsii.get(self, "malwareProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="s3LogsInput")
    def s3_logs_input(
        self,
    ) -> typing.Optional["GuarddutyOrganizationConfigurationDatasourcesS3Logs"]:
        return typing.cast(typing.Optional["GuarddutyOrganizationConfigurationDatasourcesS3Logs"], jsii.get(self, "s3LogsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasources]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GuarddutyOrganizationConfigurationDatasources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce70fb0644f549925eb45d34349f9826391134367c351a4b3ca798bfcc48ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesS3Logs",
    jsii_struct_bases=[],
    name_mapping={"auto_enable": "autoEnable"},
)
class GuarddutyOrganizationConfigurationDatasourcesS3Logs:
    def __init__(
        self,
        *,
        auto_enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param auto_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#auto_enable GuarddutyOrganizationConfiguration#auto_enable}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d7d7b15bc0016a4cc90de5a79f72bf65dc7bba978c8f489a2a82e229686dff)
            check_type(argname="argument auto_enable", value=auto_enable, expected_type=type_hints["auto_enable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_enable": auto_enable,
        }

    @builtins.property
    def auto_enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/guardduty_organization_configuration#auto_enable GuarddutyOrganizationConfiguration#auto_enable}.'''
        result = self._values.get("auto_enable")
        assert result is not None, "Required property 'auto_enable' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuarddutyOrganizationConfigurationDatasourcesS3Logs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GuarddutyOrganizationConfigurationDatasourcesS3LogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.guarddutyOrganizationConfiguration.GuarddutyOrganizationConfigurationDatasourcesS3LogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbc7637826a1762d8eb757e707d83567d82559ee790267f9c302d9874c2de0f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="autoEnableInput")
    def auto_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="autoEnable")
    def auto_enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoEnable"))

    @auto_enable.setter
    def auto_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7386ff914661b2ee26ee24da4883d7dd8443d3e7490d0578922dae5ed5bf9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GuarddutyOrganizationConfigurationDatasourcesS3Logs]:
        return typing.cast(typing.Optional[GuarddutyOrganizationConfigurationDatasourcesS3Logs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesS3Logs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4653b3e56b64f70000af2f81fb1f6b727da786006e169e44bc0c7609dd9afc8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GuarddutyOrganizationConfiguration",
    "GuarddutyOrganizationConfigurationConfig",
    "GuarddutyOrganizationConfigurationDatasources",
    "GuarddutyOrganizationConfigurationDatasourcesKubernetes",
    "GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs",
    "GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogsOutputReference",
    "GuarddutyOrganizationConfigurationDatasourcesKubernetesOutputReference",
    "GuarddutyOrganizationConfigurationDatasourcesMalwareProtection",
    "GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionOutputReference",
    "GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings",
    "GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes",
    "GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesOutputReference",
    "GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsOutputReference",
    "GuarddutyOrganizationConfigurationDatasourcesOutputReference",
    "GuarddutyOrganizationConfigurationDatasourcesS3Logs",
    "GuarddutyOrganizationConfigurationDatasourcesS3LogsOutputReference",
]

publication.publish()

def _typecheckingstub__5e03e79e38166a77fe655ad90984d69a542942f307877dbf2f822e13781af30a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    auto_enable_organization_members: builtins.str,
    detector_id: builtins.str,
    datasources: typing.Optional[typing.Union[GuarddutyOrganizationConfigurationDatasources, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a4f1ea4d1239968615ba4bbe60793d58204f0e5efdb16885a00edc3dab3dcc8e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7837fb61216b88ccdd1229b4b2c867650ac073be9bb8d17f5a31f370c294cf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecdf0d730ef43d6f3f496ab2f9a3b5add6a3508ed5ec7d4a127758204709584d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbfa863bc71d0bc3d9652c5f975070e244999a109f66364acb98dfd04a7a8452(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c0e74752f72919fd628ee804c155e9e73e5662c49d37d3aa6bd59bbd5fb6af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f03b901b9615701ffb5f525e26befa66b0e42d53e5bf7565e28e79217501e4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auto_enable_organization_members: builtins.str,
    detector_id: builtins.str,
    datasources: typing.Optional[typing.Union[GuarddutyOrganizationConfigurationDatasources, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4887cb2e1c373049b37a32d5856951d99ca683808509102037a6893c2787f15(
    *,
    kubernetes: typing.Optional[typing.Union[GuarddutyOrganizationConfigurationDatasourcesKubernetes, typing.Dict[builtins.str, typing.Any]]] = None,
    malware_protection: typing.Optional[typing.Union[GuarddutyOrganizationConfigurationDatasourcesMalwareProtection, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_logs: typing.Optional[typing.Union[GuarddutyOrganizationConfigurationDatasourcesS3Logs, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4fa2cb9b0bf0dd4ccd5d1b73c181aad5b49cfcc03c49409699f0b350ac74243(
    *,
    audit_logs: typing.Union[GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d930d00b25e008cd260367bb96ff3d71d0296dfa3ee9d54d0d29b97b4bc680bd(
    *,
    enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fb149b50eddb7615f0d3857fe827aba644a264f35f8ff47bfde7698a0e0063(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2ffd3e542fc7038c3b307fb62a10491df69d1beb43b15b512384d8ba4000b9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce56fba90afd82cfcf155391c380151d40145cea4fafefd77c1e5b0816a8259(
    value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetesAuditLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64bd1170e69b867e6649f946254acb492b82ce0021a5be91bcec33d5a70859f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab760ef1127066e18adcf06811009099b01ce5ec4ba4829a9ad7885e1031074(
    value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesKubernetes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6cae0d9fac96db1f62e78f9cb859535e7a43d997eec2f78564e5a1638ff356(
    *,
    scan_ec2_instance_with_findings: typing.Union[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497f83d68a230546f1c5309a7206793a5c480cc916174026d66b621691a4ab30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3579108b6ea7f716740e30f1869182add4e72e30a596eb9287092dd1893bfc0(
    value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ccc7cb0ef99afa0c1a3113c53812460fa95e6dedaf038b8d2d1d8dd2fa7c31(
    *,
    ebs_volumes: typing.Union[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525a46c6da512d0edcbd05d6348db25d0ed621742948f4148195a3bd80d087eb(
    *,
    auto_enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f6bb2daada30c622953e43f2f49de3340c3f2c50d05d518e1cd6dfb6c35676(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba32f4355dd77341a94e7bcafa792fdd1b22e10e75c69d6e1d905e5365f68c69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77ae6a0d198edd8cea2f40375b09408b9a439e4f0d8c5e69eef6abec31034f8(
    value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e37555da54bb0056813631536867ace02cb5b1312a5114efb870b7acc79c07b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98cf14c636b90de73eb83cb1111596559d12c48d2a4c3d6fe7e79dce714bdae4(
    value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbee17f0456c7d77d2df75ab04a0afc15d0fa0b3027b787fd8ed4eb539aaba98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce70fb0644f549925eb45d34349f9826391134367c351a4b3ca798bfcc48ef6(
    value: typing.Optional[GuarddutyOrganizationConfigurationDatasources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d7d7b15bc0016a4cc90de5a79f72bf65dc7bba978c8f489a2a82e229686dff(
    *,
    auto_enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc7637826a1762d8eb757e707d83567d82559ee790267f9c302d9874c2de0f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7386ff914661b2ee26ee24da4883d7dd8443d3e7490d0578922dae5ed5bf9f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4653b3e56b64f70000af2f81fb1f6b727da786006e169e44bc0c7609dd9afc8c(
    value: typing.Optional[GuarddutyOrganizationConfigurationDatasourcesS3Logs],
) -> None:
    """Type checking stubs"""
    pass
