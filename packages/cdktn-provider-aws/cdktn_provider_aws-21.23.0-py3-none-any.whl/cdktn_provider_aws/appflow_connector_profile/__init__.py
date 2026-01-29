r'''
# `aws_appflow_connector_profile`

Refer to the Terraform Registry for docs: [`aws_appflow_connector_profile`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile).
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


class AppflowConnectorProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile aws_appflow_connector_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_mode: builtins.str,
        connector_profile_config: typing.Union["AppflowConnectorProfileConnectorProfileConfig", typing.Dict[builtins.str, typing.Any]],
        connector_type: builtins.str,
        name: builtins.str,
        connector_label: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile aws_appflow_connector_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connection_mode AppflowConnectorProfile#connection_mode}.
        :param connector_profile_config: connector_profile_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_profile_config AppflowConnectorProfile#connector_profile_config}
        :param connector_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_type AppflowConnectorProfile#connector_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#name AppflowConnectorProfile#name}.
        :param connector_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_label AppflowConnectorProfile#connector_label}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#id AppflowConnectorProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#kms_arn AppflowConnectorProfile#kms_arn}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#region AppflowConnectorProfile#region}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7932c1b6772439701692dc70f9fddcd7e9ff721d12d8e17bfd7502fac31ee35)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppflowConnectorProfileConfig(
            connection_mode=connection_mode,
            connector_profile_config=connector_profile_config,
            connector_type=connector_type,
            name=name,
            connector_label=connector_label,
            id=id,
            kms_arn=kms_arn,
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
        '''Generates CDKTF code for importing a AppflowConnectorProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppflowConnectorProfile to import.
        :param import_from_id: The id of the existing AppflowConnectorProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppflowConnectorProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb318c99f54a3757432aa88de16ef354922b52b6f99f0a78de54d01034052a25)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConnectorProfileConfig")
    def put_connector_profile_config(
        self,
        *,
        connector_profile_credentials: typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials", typing.Dict[builtins.str, typing.Any]],
        connector_profile_properties: typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param connector_profile_credentials: connector_profile_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_profile_credentials AppflowConnectorProfile#connector_profile_credentials}
        :param connector_profile_properties: connector_profile_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_profile_properties AppflowConnectorProfile#connector_profile_properties}
        '''
        value = AppflowConnectorProfileConnectorProfileConfig(
            connector_profile_credentials=connector_profile_credentials,
            connector_profile_properties=connector_profile_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putConnectorProfileConfig", [value]))

    @jsii.member(jsii_name="resetConnectorLabel")
    def reset_connector_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorLabel", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsArn")
    def reset_kms_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsArn", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileConfig")
    def connector_profile_config(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigOutputReference", jsii.get(self, "connectorProfileConfig"))

    @builtins.property
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialsArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionModeInput")
    def connection_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorLabelInput")
    def connector_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileConfigInput")
    def connector_profile_config_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfig"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfig"], jsii.get(self, "connectorProfileConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorTypeInput")
    def connector_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsArnInput")
    def kms_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsArnInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionMode")
    def connection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionMode"))

    @connection_mode.setter
    def connection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9a8fefdf026dde94050def4ecfbcf5fd22da6a18844bb8b39865146e8da6c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorLabel")
    def connector_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorLabel"))

    @connector_label.setter
    def connector_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad5ae364b2e9ed147d7ea802b1ff6196865da3680cb6dba5576adb27ed54fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @connector_type.setter
    def connector_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a658560f8c79d578f7b2cebf8a5268921fd27b8578e42acfebcd204f0203e584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf4a5b8e74ebeeb9304c90bc374754c469b287c68a65c77d196f878b4970d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsArn")
    def kms_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsArn"))

    @kms_arn.setter
    def kms_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9627b23a7f3b815646dca371e037e66021d8e7bf0d23c9de80dd9fc00b0eb7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f9fcadf2afab16bf5f1abd9dc2e2fb784b396837e6361c6c15b349ce8be2c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758bf6ef5c6ec875cc2da666dade386b4e223fd401f327107aacef55fa85bae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "connection_mode": "connectionMode",
        "connector_profile_config": "connectorProfileConfig",
        "connector_type": "connectorType",
        "name": "name",
        "connector_label": "connectorLabel",
        "id": "id",
        "kms_arn": "kmsArn",
        "region": "region",
    },
)
class AppflowConnectorProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        connection_mode: builtins.str,
        connector_profile_config: typing.Union["AppflowConnectorProfileConnectorProfileConfig", typing.Dict[builtins.str, typing.Any]],
        connector_type: builtins.str,
        name: builtins.str,
        connector_label: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
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
        :param connection_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connection_mode AppflowConnectorProfile#connection_mode}.
        :param connector_profile_config: connector_profile_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_profile_config AppflowConnectorProfile#connector_profile_config}
        :param connector_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_type AppflowConnectorProfile#connector_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#name AppflowConnectorProfile#name}.
        :param connector_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_label AppflowConnectorProfile#connector_label}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#id AppflowConnectorProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#kms_arn AppflowConnectorProfile#kms_arn}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#region AppflowConnectorProfile#region}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(connector_profile_config, dict):
            connector_profile_config = AppflowConnectorProfileConnectorProfileConfig(**connector_profile_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76871d01a63facc0ba5a31b7fd2e0c7674b463828a372e85d4e9b1451ba8fc93)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument connection_mode", value=connection_mode, expected_type=type_hints["connection_mode"])
            check_type(argname="argument connector_profile_config", value=connector_profile_config, expected_type=type_hints["connector_profile_config"])
            check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument connector_label", value=connector_label, expected_type=type_hints["connector_label"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_mode": connection_mode,
            "connector_profile_config": connector_profile_config,
            "connector_type": connector_type,
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
        if connector_label is not None:
            self._values["connector_label"] = connector_label
        if id is not None:
            self._values["id"] = id
        if kms_arn is not None:
            self._values["kms_arn"] = kms_arn
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
    def connection_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connection_mode AppflowConnectorProfile#connection_mode}.'''
        result = self._values.get("connection_mode")
        assert result is not None, "Required property 'connection_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_profile_config(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfig":
        '''connector_profile_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_profile_config AppflowConnectorProfile#connector_profile_config}
        '''
        result = self._values.get("connector_profile_config")
        assert result is not None, "Required property 'connector_profile_config' is missing"
        return typing.cast("AppflowConnectorProfileConnectorProfileConfig", result)

    @builtins.property
    def connector_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_type AppflowConnectorProfile#connector_type}.'''
        result = self._values.get("connector_type")
        assert result is not None, "Required property 'connector_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#name AppflowConnectorProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_label AppflowConnectorProfile#connector_label}.'''
        result = self._values.get("connector_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#id AppflowConnectorProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#kms_arn AppflowConnectorProfile#kms_arn}.'''
        result = self._values.get("kms_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#region AppflowConnectorProfile#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connector_profile_credentials": "connectorProfileCredentials",
        "connector_profile_properties": "connectorProfileProperties",
    },
)
class AppflowConnectorProfileConnectorProfileConfig:
    def __init__(
        self,
        *,
        connector_profile_credentials: typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials", typing.Dict[builtins.str, typing.Any]],
        connector_profile_properties: typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param connector_profile_credentials: connector_profile_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_profile_credentials AppflowConnectorProfile#connector_profile_credentials}
        :param connector_profile_properties: connector_profile_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_profile_properties AppflowConnectorProfile#connector_profile_properties}
        '''
        if isinstance(connector_profile_credentials, dict):
            connector_profile_credentials = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials(**connector_profile_credentials)
        if isinstance(connector_profile_properties, dict):
            connector_profile_properties = AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties(**connector_profile_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86f40ab517f594cb0f99b4f4d1bf12e05f637d396c85805a7119c73a3e7b1d6)
            check_type(argname="argument connector_profile_credentials", value=connector_profile_credentials, expected_type=type_hints["connector_profile_credentials"])
            check_type(argname="argument connector_profile_properties", value=connector_profile_properties, expected_type=type_hints["connector_profile_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connector_profile_credentials": connector_profile_credentials,
            "connector_profile_properties": connector_profile_properties,
        }

    @builtins.property
    def connector_profile_credentials(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials":
        '''connector_profile_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_profile_credentials AppflowConnectorProfile#connector_profile_credentials}
        '''
        result = self._values.get("connector_profile_credentials")
        assert result is not None, "Required property 'connector_profile_credentials' is missing"
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials", result)

    @builtins.property
    def connector_profile_properties(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties":
        '''connector_profile_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#connector_profile_properties AppflowConnectorProfile#connector_profile_properties}
        '''
        result = self._values.get("connector_profile_properties")
        assert result is not None, "Required property 'connector_profile_properties' is missing"
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "amplitude": "amplitude",
        "custom_connector": "customConnector",
        "datadog": "datadog",
        "dynatrace": "dynatrace",
        "google_analytics": "googleAnalytics",
        "honeycode": "honeycode",
        "infor_nexus": "inforNexus",
        "marketo": "marketo",
        "redshift": "redshift",
        "salesforce": "salesforce",
        "sapo_data": "sapoData",
        "service_now": "serviceNow",
        "singular": "singular",
        "slack": "slack",
        "snowflake": "snowflake",
        "trendmicro": "trendmicro",
        "veeva": "veeva",
        "zendesk": "zendesk",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials:
    def __init__(
        self,
        *,
        amplitude: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace", typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode", typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus", typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce", typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack", typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake", typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro", typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva", typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        if isinstance(amplitude, dict):
            amplitude = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude(**amplitude)
        if isinstance(custom_connector, dict):
            custom_connector = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector(**custom_connector)
        if isinstance(datadog, dict):
            datadog = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog(**datadog)
        if isinstance(dynatrace, dict):
            dynatrace = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace(**dynatrace)
        if isinstance(google_analytics, dict):
            google_analytics = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics(**google_analytics)
        if isinstance(honeycode, dict):
            honeycode = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode(**honeycode)
        if isinstance(infor_nexus, dict):
            infor_nexus = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus(**infor_nexus)
        if isinstance(marketo, dict):
            marketo = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo(**marketo)
        if isinstance(redshift, dict):
            redshift = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift(**redshift)
        if isinstance(salesforce, dict):
            salesforce = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce(**salesforce)
        if isinstance(sapo_data, dict):
            sapo_data = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData(**sapo_data)
        if isinstance(service_now, dict):
            service_now = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow(**service_now)
        if isinstance(singular, dict):
            singular = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular(**singular)
        if isinstance(slack, dict):
            slack = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack(**slack)
        if isinstance(snowflake, dict):
            snowflake = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake(**snowflake)
        if isinstance(trendmicro, dict):
            trendmicro = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro(**trendmicro)
        if isinstance(veeva, dict):
            veeva = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva(**veeva)
        if isinstance(zendesk, dict):
            zendesk = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk(**zendesk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__087e7ac33bc41e8f2c913afe8a5b56be22933119fc2970d88275abb572ed5d25)
            check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
            check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
            check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
            check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
            check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
            check_type(argname="argument honeycode", value=honeycode, expected_type=type_hints["honeycode"])
            check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
            check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
            check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
            check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
            check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
            check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
            check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
            check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amplitude is not None:
            self._values["amplitude"] = amplitude
        if custom_connector is not None:
            self._values["custom_connector"] = custom_connector
        if datadog is not None:
            self._values["datadog"] = datadog
        if dynatrace is not None:
            self._values["dynatrace"] = dynatrace
        if google_analytics is not None:
            self._values["google_analytics"] = google_analytics
        if honeycode is not None:
            self._values["honeycode"] = honeycode
        if infor_nexus is not None:
            self._values["infor_nexus"] = infor_nexus
        if marketo is not None:
            self._values["marketo"] = marketo
        if redshift is not None:
            self._values["redshift"] = redshift
        if salesforce is not None:
            self._values["salesforce"] = salesforce
        if sapo_data is not None:
            self._values["sapo_data"] = sapo_data
        if service_now is not None:
            self._values["service_now"] = service_now
        if singular is not None:
            self._values["singular"] = singular
        if slack is not None:
            self._values["slack"] = slack
        if snowflake is not None:
            self._values["snowflake"] = snowflake
        if trendmicro is not None:
            self._values["trendmicro"] = trendmicro
        if veeva is not None:
            self._values["veeva"] = veeva
        if zendesk is not None:
            self._values["zendesk"] = zendesk

    @builtins.property
    def amplitude(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude"]:
        '''amplitude block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        '''
        result = self._values.get("amplitude")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude"], result)

    @builtins.property
    def custom_connector(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector"]:
        '''custom_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        '''
        result = self._values.get("custom_connector")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector"], result)

    @builtins.property
    def datadog(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog"]:
        '''datadog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        '''
        result = self._values.get("datadog")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog"], result)

    @builtins.property
    def dynatrace(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace"]:
        '''dynatrace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        '''
        result = self._values.get("dynatrace")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace"], result)

    @builtins.property
    def google_analytics(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics"]:
        '''google_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        '''
        result = self._values.get("google_analytics")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics"], result)

    @builtins.property
    def honeycode(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode"]:
        '''honeycode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        '''
        result = self._values.get("honeycode")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode"], result)

    @builtins.property
    def infor_nexus(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus"]:
        '''infor_nexus block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        '''
        result = self._values.get("infor_nexus")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus"], result)

    @builtins.property
    def marketo(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo"]:
        '''marketo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        '''
        result = self._values.get("marketo")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo"], result)

    @builtins.property
    def redshift(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift"]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift"], result)

    @builtins.property
    def salesforce(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce"]:
        '''salesforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        '''
        result = self._values.get("salesforce")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce"], result)

    @builtins.property
    def sapo_data(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData"]:
        '''sapo_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        '''
        result = self._values.get("sapo_data")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData"], result)

    @builtins.property
    def service_now(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow"]:
        '''service_now block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        '''
        result = self._values.get("service_now")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow"], result)

    @builtins.property
    def singular(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular"]:
        '''singular block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        '''
        result = self._values.get("singular")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular"], result)

    @builtins.property
    def slack(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack"]:
        '''slack block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        '''
        result = self._values.get("slack")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack"], result)

    @builtins.property
    def snowflake(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake"]:
        '''snowflake block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        '''
        result = self._values.get("snowflake")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake"], result)

    @builtins.property
    def trendmicro(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro"]:
        '''trendmicro block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        '''
        result = self._values.get("trendmicro")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro"], result)

    @builtins.property
    def veeva(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva"]:
        '''veeva block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        '''
        result = self._values.get("veeva")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva"], result)

    @builtins.property
    def zendesk(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk"]:
        '''zendesk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        result = self._values.get("zendesk")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude",
    jsii_struct_bases=[],
    name_mapping={"api_key": "apiKey", "secret_key": "secretKey"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude:
    def __init__(self, *, api_key: builtins.str, secret_key: builtins.str) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#secret_key AppflowConnectorProfile#secret_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daac45aff60f6e9f4da6be4f4e63968cf7921761437b03114aa7b6aa81879556)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "secret_key": secret_key,
        }

    @builtins.property
    def api_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#secret_key AppflowConnectorProfile#secret_key}.'''
        result = self._values.get("secret_key")
        assert result is not None, "Required property 'secret_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitudeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitudeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10f05f24951f2a6cb607117299afb5be1243d6b3cd43336eb07e27afa73eb000)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyInput")
    def secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f59d3d888beff92b0eccebf517b5615003bc565738b82e6d52500cbcce59607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07d486939cfa76635f7863457b3699cf2d2d0b7136e0434e7fb267751a222a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450d72b31da0645392ff50c58ff20634656e252187c739b2571e3ed5998b8182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "api_key": "apiKey",
        "basic": "basic",
        "custom": "custom",
        "oauth2": "oauth2",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector:
    def __init__(
        self,
        *,
        authentication_type: builtins.str,
        api_key: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey", typing.Dict[builtins.str, typing.Any]]] = None,
        basic: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        custom: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#authentication_type AppflowConnectorProfile#authentication_type}.
        :param api_key: api_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#basic AppflowConnectorProfile#basic}
        :param custom: custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom AppflowConnectorProfile#custom}
        :param oauth2: oauth2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2 AppflowConnectorProfile#oauth2}
        '''
        if isinstance(api_key, dict):
            api_key = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey(**api_key)
        if isinstance(basic, dict):
            basic = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic(**basic)
        if isinstance(custom, dict):
            custom = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom(**custom)
        if isinstance(oauth2, dict):
            oauth2 = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2(**oauth2)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9448c554587b89ed2fb94507a4f66f45bc8d272988793847a0415bd91e9257cb)
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument basic", value=basic, expected_type=type_hints["basic"])
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument oauth2", value=oauth2, expected_type=type_hints["oauth2"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_type": authentication_type,
        }
        if api_key is not None:
            self._values["api_key"] = api_key
        if basic is not None:
            self._values["basic"] = basic
        if custom is not None:
            self._values["custom"] = custom
        if oauth2 is not None:
            self._values["oauth2"] = oauth2

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#authentication_type AppflowConnectorProfile#authentication_type}.'''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey"]:
        '''api_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey"], result)

    @builtins.property
    def basic(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic"]:
        '''basic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#basic AppflowConnectorProfile#basic}
        '''
        result = self._values.get("basic")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic"], result)

    @builtins.property
    def custom(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom"]:
        '''custom block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom AppflowConnectorProfile#custom}
        '''
        result = self._values.get("custom")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom"], result)

    @builtins.property
    def oauth2(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2"]:
        '''oauth2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2 AppflowConnectorProfile#oauth2}
        '''
        result = self._values.get("oauth2")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey",
    jsii_struct_bases=[],
    name_mapping={"api_key": "apiKey", "api_secret_key": "apiSecretKey"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        api_secret_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param api_secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf74636ff5e98dfcf8307858d09bfb825f450a1330756406c2d9207a35e4c0f)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument api_secret_key", value=api_secret_key, expected_type=type_hints["api_secret_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
        }
        if api_secret_key is not None:
            self._values["api_secret_key"] = api_secret_key

    @builtins.property
    def api_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_secret_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.'''
        result = self._values.get("api_secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98104156c8720c1e9f5cd54347bc425d5620cc3b7c293f6f4b6a550bfa7c3cdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApiSecretKey")
    def reset_api_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiSecretKey", []))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSecretKeyInput")
    def api_secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiSecretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10033de67e5e1e4f112e66fcf57e411a508740126b4fd16167cc0d564dff24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiSecretKey")
    def api_secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiSecretKey"))

    @api_secret_key.setter
    def api_secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981183b29fca36db1061dfce2136d0693a459f6963361f8c13cbba263aaff2a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiSecretKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f677107723fe180afb4054261a6136aad936ee11684e537d52fe0450714f51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44ba35fe9999e0ff0886bd673900923d8da2024777719401e4287fd8710b055)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasicOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__896e2e8c68e38632af01d4b6bacce8ee3a4741fcf1b81b09d6b873c611fefd1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8216f68e1963552b2aa4fae3d7337f32813513180cdef98f138897fe700cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735ddcf38ab7465e1c3d23e08f2c1ec1e9bcddb16072aa7de1b720fe71a10056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5661da20cb807512e9944449afd85cd6c66b4ebe816d21e4618e5db03a67be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom",
    jsii_struct_bases=[],
    name_mapping={
        "custom_authentication_type": "customAuthenticationType",
        "credentials_map": "credentialsMap",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom:
    def __init__(
        self,
        *,
        custom_authentication_type: builtins.str,
        credentials_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param custom_authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom_authentication_type AppflowConnectorProfile#custom_authentication_type}.
        :param credentials_map: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#credentials_map AppflowConnectorProfile#credentials_map}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad5d934ade2f56f1ad79f32cc4c1e5b3c080581887debbf9c528e07ca3bb718)
            check_type(argname="argument custom_authentication_type", value=custom_authentication_type, expected_type=type_hints["custom_authentication_type"])
            check_type(argname="argument credentials_map", value=credentials_map, expected_type=type_hints["credentials_map"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_authentication_type": custom_authentication_type,
        }
        if credentials_map is not None:
            self._values["credentials_map"] = credentials_map

    @builtins.property
    def custom_authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom_authentication_type AppflowConnectorProfile#custom_authentication_type}.'''
        result = self._values.get("custom_authentication_type")
        assert result is not None, "Required property 'custom_authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials_map(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#credentials_map AppflowConnectorProfile#credentials_map}.'''
        result = self._values.get("credentials_map")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4b1c5c7c7ff7966a6582a78c184dd845db8078e4469c44db98c44642db1fefa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCredentialsMap")
    def reset_credentials_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialsMap", []))

    @builtins.property
    @jsii.member(jsii_name="credentialsMapInput")
    def credentials_map_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "credentialsMapInput"))

    @builtins.property
    @jsii.member(jsii_name="customAuthenticationTypeInput")
    def custom_authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customAuthenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsMap")
    def credentials_map(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "credentialsMap"))

    @credentials_map.setter
    def credentials_map(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05ef292512dec9b83fa18ecdd37b01a997708518d989b40e9dec04934eb005a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialsMap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customAuthenticationType")
    def custom_authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customAuthenticationType"))

    @custom_authentication_type.setter
    def custom_authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1a9165b433a1109aa25cd93d50e2f4618be3943496056e2a45f908e3d7f0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAuthenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d6baa86a33d6ef6076e2528949c24b7b58a90d93f78cf2fcf3ee324b9024a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "oauth_request": "oauthRequest",
        "refresh_token": "refreshToken",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243d7ce8fd12e2ef55063cab9bb5786cbfff044d5aad148b7d6deb49c53fdede)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest"], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bf702950685118540db345c0f2df5c85db6e84d77574b5eaaafbaffd9123f1)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4480fc1077329e9b43bfe00107b192bdb409633a7e37ec8027dc693c0f6283a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3fdbb4c4a48590839e3de9970bd05a6179984c8a578b0480f0ab88bc0734da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b40d435467a8538ab5a05f05621d3f3bc57166a685c73a6dc3f6c4ad337d3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811e313200558387a8abde090732025d47b897b3ce502624cc43d91cd2830a4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47f064bc3ae448ac52a762e5479066a7140c2235ee057c3028f3396026c76ff4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619ddd3d95929fd0b52c96644dcebe54a4824aa854bf580bc1d55df25d8f7dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9238859091ff40eec7dd849d6c8c14b9a976ee2b602f7abe2e88d5b74d2b9c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf06c31090ee62700d1ca310012c83573e16247239e9bcce97fd8b51c671976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__065b2dcf7d5968977ed0c405e9ebdbf13bb1c73e39bd6e5436ddf859544364fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7887ea11509af1b5e9fdbe3c9bbdd9cabe54826fbc45dde2f3784c324917700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3202e72ac941ebf04eccebb7adc2751f5240e57b70c1368f1c4dcb1f0fe58797)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiKey")
    def put_api_key(
        self,
        *,
        api_key: builtins.str,
        api_secret_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param api_secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey(
            api_key=api_key, api_secret_key=api_secret_key
        )

        return typing.cast(None, jsii.invoke(self, "putApiKey", [value]))

    @jsii.member(jsii_name="putBasic")
    def put_basic(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putBasic", [value]))

    @jsii.member(jsii_name="putCustom")
    def put_custom(
        self,
        *,
        custom_authentication_type: builtins.str,
        credentials_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param custom_authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom_authentication_type AppflowConnectorProfile#custom_authentication_type}.
        :param credentials_map: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#credentials_map AppflowConnectorProfile#credentials_map}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom(
            custom_authentication_type=custom_authentication_type,
            credentials_map=credentials_map,
        )

        return typing.cast(None, jsii.invoke(self, "putCustom", [value]))

    @jsii.member(jsii_name="putOauth2")
    def put_oauth2(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2(
            access_token=access_token,
            client_id=client_id,
            client_secret=client_secret,
            oauth_request=oauth_request,
            refresh_token=refresh_token,
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2", [value]))

    @jsii.member(jsii_name="resetApiKey")
    def reset_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKey", []))

    @jsii.member(jsii_name="resetBasic")
    def reset_basic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasic", []))

    @jsii.member(jsii_name="resetCustom")
    def reset_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustom", []))

    @jsii.member(jsii_name="resetOauth2")
    def reset_oauth2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2", []))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKeyOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKeyOutputReference, jsii.get(self, "apiKey"))

    @builtins.property
    @jsii.member(jsii_name="basic")
    def basic(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasicOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasicOutputReference, jsii.get(self, "basic"))

    @builtins.property
    @jsii.member(jsii_name="custom")
    def custom(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustomOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustomOutputReference, jsii.get(self, "custom"))

    @builtins.property
    @jsii.member(jsii_name="oauth2")
    def oauth2(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OutputReference, jsii.get(self, "oauth2"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypeInput")
    def authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="basicInput")
    def basic_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic], jsii.get(self, "basicInput"))

    @builtins.property
    @jsii.member(jsii_name="customInput")
    def custom_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom], jsii.get(self, "customInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2Input")
    def oauth2_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2], jsii.get(self, "oauth2Input"))

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fcb957063d1ecae44e2999059bbe4a34f20fe7e2c7d9a71e947a822b45cbd9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3abc58f02b032f0238baf04170563e7ad3cd24e3b2d8f44120566a0ba18ecf94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog",
    jsii_struct_bases=[],
    name_mapping={"api_key": "apiKey", "application_key": "applicationKey"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog:
    def __init__(self, *, api_key: builtins.str, application_key: builtins.str) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param application_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#application_key AppflowConnectorProfile#application_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8a81e80cef8b1b900975dd61a7fa9023ee2687e0d920f11042dad74efedf18)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument application_key", value=application_key, expected_type=type_hints["application_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "application_key": application_key,
        }

    @builtins.property
    def api_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#application_key AppflowConnectorProfile#application_key}.'''
        result = self._values.get("application_key")
        assert result is not None, "Required property 'application_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f08cc9fc21a4a3263d0579dd3efa82935e62b7d9af7c9ede5d4ed7b831ac93ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationKeyInput")
    def application_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11684cb7b8d8600d05a189ac7ed1cbb8bb40016fee064c3ab4fd70967d80c2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationKey")
    def application_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationKey"))

    @application_key.setter
    def application_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de4f7c4c1214b811eac14ccd68bae73ae43e0e3963103f4b81ea214bf024a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f6a7a81938e42866037fd060e14875a88ffe15969e915d3b8cf73f52539310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace",
    jsii_struct_bases=[],
    name_mapping={"api_token": "apiToken"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace:
    def __init__(self, *, api_token: builtins.str) -> None:
        '''
        :param api_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_token AppflowConnectorProfile#api_token}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea78e8c5adbdfcac93dcc101a164d402ab0b22e5d0912e43ceb00dae0e206ee)
            check_type(argname="argument api_token", value=api_token, expected_type=type_hints["api_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_token": api_token,
        }

    @builtins.property
    def api_token(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_token AppflowConnectorProfile#api_token}.'''
        result = self._values.get("api_token")
        assert result is not None, "Required property 'api_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatraceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatraceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cf567104fceb1bd90235a02ef4eeadd84294cbdcf35c5ff355966baacb31d59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiTokenInput")
    def api_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="apiToken")
    def api_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiToken"))

    @api_token.setter
    def api_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1600e3dcf3de16f2ad45630532b3cba7a07c502e19ad342f9718e8d2e20568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229239659af41080e0f03b2a56448b904fe7bb5cc5b156c127da5ec89e938f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
        "refresh_token": "refreshToken",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42892be567cf48a023cc79ca21f635438c5078227243c42e73be78bf311801a)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest"], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fd78ad6f72c6d8249533ac7c9d39b5245afb218129bbfcf5ba25003185a702)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae09ac3aea3e432a18bf78120a9bb21dd3f965dc2acbfb5c81d1a96f805b4cb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff12c4a1cdeab3b2397d9923a1f65d040c3df24e1ef6a3efbc34c0fba7a1dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe2445746a292b4c029f99e5c8563f159acf7f6f0dbc0e8e8909da87ea06c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102cb4fe41e1924617625174d23b27b16213fa98d7576c9b5a1e1a5fccc124d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a4866028faecc93f993a3e9e0e0a6423785ee8b9afab076fb574ac8563f9ced)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b7416f805809377e7b24c61ca9061c778c17f17631e9acea9aed36ab31abea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0f4e7f1cb644d5f93c6aa6bdb0bd5db540c6aad4ff655b167b23e496f418478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029b2d6970ac2a3d6fb805811856ffa526f3ab8084e028e3c72d2acd68eb563b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5a3d409adb2272425dcffc1c478da5a0cf3fdc7c0bfe0c793a54c1989c1ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2498869056caa004a5322d9a5abdd001bc56e6cca166a70d41ee27499d5a9f06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
        "refresh_token": "refreshToken",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b027a3ff48a7ccb985184b5a42e3de482d8fceb4802a513ad880a81d3447782)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest"], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5940623c76c905f519db4096b0066f6306a112b457ef35cc7d9f73b28c2758)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5cef275e4ebf9a424dcf5b1b88104bd6ffe6ab124895f9e353745b8d9f6deb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b50000d1500f702f4464bc246bdd96e92b3b4461d52ff02bae127d995475447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795011e872821007fb04aaeddc6af9b015800bb7e3d467c33fde0870f98ffdf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__379185ededf2f372455faf01bfe2904e42ab16ab47e54fae64e3d345f939d282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__342251015321e3fa509c97ae29babd27bc611039f131861d9961dbed239e190f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37853a7b6c645b59d011141853a846861319d9db12f40cce9e06841332cdff09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8561478a9e013d06a0eae187b84e0fbf7de18f73c12b1de78c729a3f927f067a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77b9ca12f8fac1d640e565f34fb42bb88bc1376e76c6b1fe65faaa4630be8f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "datakey": "datakey",
        "secret_access_key": "secretAccessKey",
        "user_id": "userId",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus:
    def __init__(
        self,
        *,
        access_key_id: builtins.str,
        datakey: builtins.str,
        secret_access_key: builtins.str,
        user_id: builtins.str,
    ) -> None:
        '''
        :param access_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_key_id AppflowConnectorProfile#access_key_id}.
        :param datakey: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#datakey AppflowConnectorProfile#datakey}.
        :param secret_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#secret_access_key AppflowConnectorProfile#secret_access_key}.
        :param user_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#user_id AppflowConnectorProfile#user_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f15d17b43e6419e2ef9888321c0773f693942e1f139e326bb5a341bdd3b75cb)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument datakey", value=datakey, expected_type=type_hints["datakey"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_key_id": access_key_id,
            "datakey": datakey,
            "secret_access_key": secret_access_key,
            "user_id": user_id,
        }

    @builtins.property
    def access_key_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_key_id AppflowConnectorProfile#access_key_id}.'''
        result = self._values.get("access_key_id")
        assert result is not None, "Required property 'access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datakey(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#datakey AppflowConnectorProfile#datakey}.'''
        result = self._values.get("datakey")
        assert result is not None, "Required property 'datakey' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_access_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#secret_access_key AppflowConnectorProfile#secret_access_key}.'''
        result = self._values.get("secret_access_key")
        assert result is not None, "Required property 'secret_access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#user_id AppflowConnectorProfile#user_id}.'''
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efe5b72a823f10e4c3ddd9a0f86d0728d968e5d2d2aa49d26a13be3bf28a2d49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="accessKeyIdInput")
    def access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datakeyInput")
    def datakey_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datakeyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyInput")
    def secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276d44539444a8a43220e7afc1550c69f16e59f10d0dbac6c996acbee1cdde0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datakey")
    def datakey(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datakey"))

    @datakey.setter
    def datakey(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38572042bcfe84f2b96b60041366efaf269d61cc727184554cc8eb77ed01feaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datakey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKey"))

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3befbbc2ce1877ac62d339b696241b29ffa49272fbc3b977a460c9b177933cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ba2a96d787caac1b7c2d88528adaa000f95f07e30fab0590d1b63be9bd21688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568ecd54ec04ba95c73f933c7a57b0372e285e91bfcff90b36b453ff2976d1c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ca600ee3c0c4b4ca2053e7f53b1de275af450e0528a5a565388f8152803911)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0a91ee2fb257b478659c1691fdaaba6d462aa1b2fe603af28ffd52dfcc7f9e)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aac9fa73e1d07fa7040660dcc72d1570ff0821afcfae816f46eb9fdfababb724)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbddf983eb956d5499d3e0cde84a17c10cda6c53455de01839c8152fcdcba7e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35849f0a3176884ab75dbbf3922ba3795307fd37aea575694de053464ebd4d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd0fddecf1e9936ebeb7efa2d3d92b9ecdd59fbc801b0bcaaeacf4ab5225787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a87737e88bcebf7a9dca5c777742325c6ad34de48dc4c6d746fce01e9c4047e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fa113b55b4686c0118f55647407ac2a03cad02255b51ff4a09586d8d3bab08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__124ea5466956be312de5bea91d3040249502de260baa8a323042797330d57689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1adc7a3160246d280bbd99335a994c14d55effffc852a3a3b2d0c8a69fd13a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c0250ddcef5ec0ffa485aed4ea57e677998d8412fabbc7c508ef1c5d60dc026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__820bc7b85817e0b2e7ca480c312e7c354726006f517a6cb1516c2fb97492628b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAmplitude")
    def put_amplitude(self, *, api_key: builtins.str, secret_key: builtins.str) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#secret_key AppflowConnectorProfile#secret_key}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude(
            api_key=api_key, secret_key=secret_key
        )

        return typing.cast(None, jsii.invoke(self, "putAmplitude", [value]))

    @jsii.member(jsii_name="putCustomConnector")
    def put_custom_connector(
        self,
        *,
        authentication_type: builtins.str,
        api_key: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey, typing.Dict[builtins.str, typing.Any]]] = None,
        basic: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic, typing.Dict[builtins.str, typing.Any]]] = None,
        custom: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom, typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#authentication_type AppflowConnectorProfile#authentication_type}.
        :param api_key: api_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#basic AppflowConnectorProfile#basic}
        :param custom: custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom AppflowConnectorProfile#custom}
        :param oauth2: oauth2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2 AppflowConnectorProfile#oauth2}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector(
            authentication_type=authentication_type,
            api_key=api_key,
            basic=basic,
            custom=custom,
            oauth2=oauth2,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConnector", [value]))

    @jsii.member(jsii_name="putDatadog")
    def put_datadog(
        self,
        *,
        api_key: builtins.str,
        application_key: builtins.str,
    ) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param application_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#application_key AppflowConnectorProfile#application_key}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog(
            api_key=api_key, application_key=application_key
        )

        return typing.cast(None, jsii.invoke(self, "putDatadog", [value]))

    @jsii.member(jsii_name="putDynatrace")
    def put_dynatrace(self, *, api_token: builtins.str) -> None:
        '''
        :param api_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_token AppflowConnectorProfile#api_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace(
            api_token=api_token
        )

        return typing.cast(None, jsii.invoke(self, "putDynatrace", [value]))

    @jsii.member(jsii_name="putGoogleAnalytics")
    def put_google_analytics(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            oauth_request=oauth_request,
            refresh_token=refresh_token,
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleAnalytics", [value]))

    @jsii.member(jsii_name="putHoneycode")
    def put_honeycode(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode(
            access_token=access_token,
            oauth_request=oauth_request,
            refresh_token=refresh_token,
        )

        return typing.cast(None, jsii.invoke(self, "putHoneycode", [value]))

    @jsii.member(jsii_name="putInforNexus")
    def put_infor_nexus(
        self,
        *,
        access_key_id: builtins.str,
        datakey: builtins.str,
        secret_access_key: builtins.str,
        user_id: builtins.str,
    ) -> None:
        '''
        :param access_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_key_id AppflowConnectorProfile#access_key_id}.
        :param datakey: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#datakey AppflowConnectorProfile#datakey}.
        :param secret_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#secret_access_key AppflowConnectorProfile#secret_access_key}.
        :param user_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#user_id AppflowConnectorProfile#user_id}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus(
            access_key_id=access_key_id,
            datakey=datakey,
            secret_access_key=secret_access_key,
            user_id=user_id,
        )

        return typing.cast(None, jsii.invoke(self, "putInforNexus", [value]))

    @jsii.member(jsii_name="putMarketo")
    def put_marketo(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            oauth_request=oauth_request,
        )

        return typing.cast(None, jsii.invoke(self, "putMarketo", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putSalesforce")
    def put_salesforce(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        client_credentials_arn: typing.Optional[builtins.str] = None,
        jwt_token: typing.Optional[builtins.str] = None,
        oauth2_grant_type: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param client_credentials_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_credentials_arn AppflowConnectorProfile#client_credentials_arn}.
        :param jwt_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#jwt_token AppflowConnectorProfile#jwt_token}.
        :param oauth2_grant_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce(
            access_token=access_token,
            client_credentials_arn=client_credentials_arn,
            jwt_token=jwt_token,
            oauth2_grant_type=oauth2_grant_type,
            oauth_request=oauth_request,
            refresh_token=refresh_token,
        )

        return typing.cast(None, jsii.invoke(self, "putSalesforce", [value]))

    @jsii.member(jsii_name="putSapoData")
    def put_sapo_data(
        self,
        *,
        basic_auth_credentials: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_credentials: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param basic_auth_credentials: basic_auth_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#basic_auth_credentials AppflowConnectorProfile#basic_auth_credentials}
        :param oauth_credentials: oauth_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_credentials AppflowConnectorProfile#oauth_credentials}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData(
            basic_auth_credentials=basic_auth_credentials,
            oauth_credentials=oauth_credentials,
        )

        return typing.cast(None, jsii.invoke(self, "putSapoData", [value]))

    @jsii.member(jsii_name="putServiceNow")
    def put_service_now(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putServiceNow", [value]))

    @jsii.member(jsii_name="putSingular")
    def put_singular(self, *, api_key: builtins.str) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular(
            api_key=api_key
        )

        return typing.cast(None, jsii.invoke(self, "putSingular", [value]))

    @jsii.member(jsii_name="putSlack")
    def put_slack(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            oauth_request=oauth_request,
        )

        return typing.cast(None, jsii.invoke(self, "putSlack", [value]))

    @jsii.member(jsii_name="putSnowflake")
    def put_snowflake(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putSnowflake", [value]))

    @jsii.member(jsii_name="putTrendmicro")
    def put_trendmicro(self, *, api_secret_key: builtins.str) -> None:
        '''
        :param api_secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro(
            api_secret_key=api_secret_key
        )

        return typing.cast(None, jsii.invoke(self, "putTrendmicro", [value]))

    @jsii.member(jsii_name="putVeeva")
    def put_veeva(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putVeeva", [value]))

    @jsii.member(jsii_name="putZendesk")
    def put_zendesk(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            oauth_request=oauth_request,
        )

        return typing.cast(None, jsii.invoke(self, "putZendesk", [value]))

    @jsii.member(jsii_name="resetAmplitude")
    def reset_amplitude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmplitude", []))

    @jsii.member(jsii_name="resetCustomConnector")
    def reset_custom_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConnector", []))

    @jsii.member(jsii_name="resetDatadog")
    def reset_datadog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadog", []))

    @jsii.member(jsii_name="resetDynatrace")
    def reset_dynatrace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynatrace", []))

    @jsii.member(jsii_name="resetGoogleAnalytics")
    def reset_google_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleAnalytics", []))

    @jsii.member(jsii_name="resetHoneycode")
    def reset_honeycode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHoneycode", []))

    @jsii.member(jsii_name="resetInforNexus")
    def reset_infor_nexus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInforNexus", []))

    @jsii.member(jsii_name="resetMarketo")
    def reset_marketo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketo", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetSalesforce")
    def reset_salesforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSalesforce", []))

    @jsii.member(jsii_name="resetSapoData")
    def reset_sapo_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSapoData", []))

    @jsii.member(jsii_name="resetServiceNow")
    def reset_service_now(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceNow", []))

    @jsii.member(jsii_name="resetSingular")
    def reset_singular(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingular", []))

    @jsii.member(jsii_name="resetSlack")
    def reset_slack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlack", []))

    @jsii.member(jsii_name="resetSnowflake")
    def reset_snowflake(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowflake", []))

    @jsii.member(jsii_name="resetTrendmicro")
    def reset_trendmicro(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrendmicro", []))

    @jsii.member(jsii_name="resetVeeva")
    def reset_veeva(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVeeva", []))

    @jsii.member(jsii_name="resetZendesk")
    def reset_zendesk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZendesk", []))

    @builtins.property
    @jsii.member(jsii_name="amplitude")
    def amplitude(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitudeOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitudeOutputReference, jsii.get(self, "amplitude"))

    @builtins.property
    @jsii.member(jsii_name="customConnector")
    def custom_connector(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOutputReference, jsii.get(self, "customConnector"))

    @builtins.property
    @jsii.member(jsii_name="datadog")
    def datadog(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadogOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadogOutputReference, jsii.get(self, "datadog"))

    @builtins.property
    @jsii.member(jsii_name="dynatrace")
    def dynatrace(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatraceOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatraceOutputReference, jsii.get(self, "dynatrace"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalytics")
    def google_analytics(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOutputReference, jsii.get(self, "googleAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="honeycode")
    def honeycode(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOutputReference, jsii.get(self, "honeycode"))

    @builtins.property
    @jsii.member(jsii_name="inforNexus")
    def infor_nexus(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexusOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexusOutputReference, jsii.get(self, "inforNexus"))

    @builtins.property
    @jsii.member(jsii_name="marketo")
    def marketo(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOutputReference, jsii.get(self, "marketo"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshiftOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshiftOutputReference", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="salesforce")
    def salesforce(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOutputReference", jsii.get(self, "salesforce"))

    @builtins.property
    @jsii.member(jsii_name="sapoData")
    def sapo_data(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOutputReference", jsii.get(self, "sapoData"))

    @builtins.property
    @jsii.member(jsii_name="serviceNow")
    def service_now(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNowOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNowOutputReference", jsii.get(self, "serviceNow"))

    @builtins.property
    @jsii.member(jsii_name="singular")
    def singular(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingularOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingularOutputReference", jsii.get(self, "singular"))

    @builtins.property
    @jsii.member(jsii_name="slack")
    def slack(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOutputReference", jsii.get(self, "slack"))

    @builtins.property
    @jsii.member(jsii_name="snowflake")
    def snowflake(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflakeOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflakeOutputReference", jsii.get(self, "snowflake"))

    @builtins.property
    @jsii.member(jsii_name="trendmicro")
    def trendmicro(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicroOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicroOutputReference", jsii.get(self, "trendmicro"))

    @builtins.property
    @jsii.member(jsii_name="veeva")
    def veeva(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeevaOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeevaOutputReference", jsii.get(self, "veeva"))

    @builtins.property
    @jsii.member(jsii_name="zendesk")
    def zendesk(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOutputReference", jsii.get(self, "zendesk"))

    @builtins.property
    @jsii.member(jsii_name="amplitudeInput")
    def amplitude_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude], jsii.get(self, "amplitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="customConnectorInput")
    def custom_connector_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector], jsii.get(self, "customConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogInput")
    def datadog_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog], jsii.get(self, "datadogInput"))

    @builtins.property
    @jsii.member(jsii_name="dynatraceInput")
    def dynatrace_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace], jsii.get(self, "dynatraceInput"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalyticsInput")
    def google_analytics_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics], jsii.get(self, "googleAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="honeycodeInput")
    def honeycode_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode], jsii.get(self, "honeycodeInput"))

    @builtins.property
    @jsii.member(jsii_name="inforNexusInput")
    def infor_nexus_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus], jsii.get(self, "inforNexusInput"))

    @builtins.property
    @jsii.member(jsii_name="marketoInput")
    def marketo_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo], jsii.get(self, "marketoInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift"], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="salesforceInput")
    def salesforce_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce"], jsii.get(self, "salesforceInput"))

    @builtins.property
    @jsii.member(jsii_name="sapoDataInput")
    def sapo_data_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData"], jsii.get(self, "sapoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNowInput")
    def service_now_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow"], jsii.get(self, "serviceNowInput"))

    @builtins.property
    @jsii.member(jsii_name="singularInput")
    def singular_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular"], jsii.get(self, "singularInput"))

    @builtins.property
    @jsii.member(jsii_name="slackInput")
    def slack_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack"], jsii.get(self, "slackInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeInput")
    def snowflake_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake"], jsii.get(self, "snowflakeInput"))

    @builtins.property
    @jsii.member(jsii_name="trendmicroInput")
    def trendmicro_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro"], jsii.get(self, "trendmicroInput"))

    @builtins.property
    @jsii.member(jsii_name="veevaInput")
    def veeva_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva"], jsii.get(self, "veevaInput"))

    @builtins.property
    @jsii.member(jsii_name="zendeskInput")
    def zendesk_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk"], jsii.get(self, "zendeskInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c01dec191c5a0e0670ad44ee6667b30a5416ee94386df46a515bbb259c5c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51afc302e6b7315882b2b954d4ae1e858be835009de80c281688950427a39f2a)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__272ea5a4cca340136c4ddc07617e6cd999bd0b90e78f94ce85641899e16eaa8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b067298c303ca6e87de9566a7a2ce972effbce3ae985427a0ee6696b4fc28b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95cc46577fd0865eae626ab4bfd9d7bf2605c9ca10d9d2f8a3c59f989c43f630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc138a8a681babfb715d09ce2246ecd29f786d97091419e50cc17f77c0b8983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "client_credentials_arn": "clientCredentialsArn",
        "jwt_token": "jwtToken",
        "oauth2_grant_type": "oauth2GrantType",
        "oauth_request": "oauthRequest",
        "refresh_token": "refreshToken",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        client_credentials_arn: typing.Optional[builtins.str] = None,
        jwt_token: typing.Optional[builtins.str] = None,
        oauth2_grant_type: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param client_credentials_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_credentials_arn AppflowConnectorProfile#client_credentials_arn}.
        :param jwt_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#jwt_token AppflowConnectorProfile#jwt_token}.
        :param oauth2_grant_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184c6fe339cce42a0485a6c9e71c227aab73762204285c04ebe9dded47e2d258)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument client_credentials_arn", value=client_credentials_arn, expected_type=type_hints["client_credentials_arn"])
            check_type(argname="argument jwt_token", value=jwt_token, expected_type=type_hints["jwt_token"])
            check_type(argname="argument oauth2_grant_type", value=oauth2_grant_type, expected_type=type_hints["oauth2_grant_type"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if client_credentials_arn is not None:
            self._values["client_credentials_arn"] = client_credentials_arn
        if jwt_token is not None:
            self._values["jwt_token"] = jwt_token
        if oauth2_grant_type is not None:
            self._values["oauth2_grant_type"] = oauth2_grant_type
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_credentials_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_credentials_arn AppflowConnectorProfile#client_credentials_arn}.'''
        result = self._values.get("client_credentials_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jwt_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#jwt_token AppflowConnectorProfile#jwt_token}.'''
        result = self._values.get("jwt_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth2_grant_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.'''
        result = self._values.get("oauth2_grant_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest"], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0de1e46bd3b966adb8f092d7ce3f65a3c8523d0c987dce1d216c0f258a412c7)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__591d66fd0656d7193a1d01e4436ebd2c0ee474cecd9a0f81ead0a50d25030ee5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9215ea439b80ff177e8cb71cd00945935e49c99c9d7332c02a986ff71e39d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4924de2bdd011779ab7d099122be086890b28f81799fdf095a73554fc06d9188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ea2b7981ae621dedaf6c8b825ee311a7e04f619d5f77f92d1cc304510690ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fb4e59e28bd37bc9c05ce53d6012080054725e63f408c6ce67e3c484e6eeecc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetClientCredentialsArn")
    def reset_client_credentials_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCredentialsArn", []))

    @jsii.member(jsii_name="resetJwtToken")
    def reset_jwt_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtToken", []))

    @jsii.member(jsii_name="resetOauth2GrantType")
    def reset_oauth2_grant_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2GrantType", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCredentialsArnInput")
    def client_credentials_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCredentialsArnInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtTokenInput")
    def jwt_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jwtTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2GrantTypeInput")
    def oauth2_grant_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauth2GrantTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec0aa4ebb9efc27816aa30f98d226f54b6820afaf1f0565ed6f68b1cb376035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCredentialsArn")
    def client_credentials_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCredentialsArn"))

    @client_credentials_arn.setter
    def client_credentials_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834fac8fd8ecce049ba0232240c50c09cf92e84b7c2b4b8b497d82da710d240d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCredentialsArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwtToken")
    def jwt_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwtToken"))

    @jwt_token.setter
    def jwt_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c41318aa837e83a097b0e5d83a0bc7337e3d694e6966e686c183ea803adcb8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2GrantType")
    def oauth2_grant_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2GrantType"))

    @oauth2_grant_type.setter
    def oauth2_grant_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336afe147282279ac3dc4060243895355ed7a48e47f7f25f6dbc89b4126f31c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2GrantType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a1aab707b9fc9433cf7da8f244b824d5a78420f33570cfd8242b09a697d572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796faf572c6709abddf9f23323fc42f06d1f4fbb8230c4a1ebcad0a08a68ef7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData",
    jsii_struct_bases=[],
    name_mapping={
        "basic_auth_credentials": "basicAuthCredentials",
        "oauth_credentials": "oauthCredentials",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData:
    def __init__(
        self,
        *,
        basic_auth_credentials: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_credentials: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param basic_auth_credentials: basic_auth_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#basic_auth_credentials AppflowConnectorProfile#basic_auth_credentials}
        :param oauth_credentials: oauth_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_credentials AppflowConnectorProfile#oauth_credentials}
        '''
        if isinstance(basic_auth_credentials, dict):
            basic_auth_credentials = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials(**basic_auth_credentials)
        if isinstance(oauth_credentials, dict):
            oauth_credentials = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials(**oauth_credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33bde2c3b7138ba3a2f3723fb25aa44f3a5f40ed51527c822659698bd6eea5b5)
            check_type(argname="argument basic_auth_credentials", value=basic_auth_credentials, expected_type=type_hints["basic_auth_credentials"])
            check_type(argname="argument oauth_credentials", value=oauth_credentials, expected_type=type_hints["oauth_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic_auth_credentials is not None:
            self._values["basic_auth_credentials"] = basic_auth_credentials
        if oauth_credentials is not None:
            self._values["oauth_credentials"] = oauth_credentials

    @builtins.property
    def basic_auth_credentials(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials"]:
        '''basic_auth_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#basic_auth_credentials AppflowConnectorProfile#basic_auth_credentials}
        '''
        result = self._values.get("basic_auth_credentials")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials"], result)

    @builtins.property
    def oauth_credentials(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials"]:
        '''oauth_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_credentials AppflowConnectorProfile#oauth_credentials}
        '''
        result = self._values.get("oauth_credentials")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17765fe2ac10de1528c5d1d2816703bc20fe155d15f0e972728c0c5ae2e50dc)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b68d56fe8260979c500c5b1ae049a83c641bb946632b64e1222eefc5a200bb1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd86f45c4a908229c9ffba1a7b561cd6483bc29db8f4234616267aeb6dff1dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8a7301e8613fc311e27d7a3941394faaed9ac31286734c5d97c459a0fcfe5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8288e33b03561a92cf77bb158651cd002a31f29de9ced6327718614472b6bd51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
        "refresh_token": "refreshToken",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cbcd0732b5602cc0ebb01031fb99ecfec90f275bc0aa49d57d84184efa43a1)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest"], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b70fa768cee692a51a11607e9559a8eebd17380f07156e1257b7d5d2ed5e2f48)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bc55a8d83edb0218bf1e37708874d8e03df0312e755947a593898de5f8fc0b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6587acd564c661a0716becacbd4017ae188d34386b915f5903c13ef0716850d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4727aeda50ebc183ec4dc175fcfacad3c1be747a579e8b2e23921f74a829ab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84826935c439cd20e35142248c97474b388f642748db405dd7ef2774b7a52d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceaa1f253d892aa684549321d1d6878744107c212369180b4dd7e047ec60181b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a65e72796e2e7ed7aaaa35d3dd221eab3bf2805d3b23c67ddda3234235f437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ecb9cee757519061765bd064511fd51f402ad3c57a73c91c9878deb1acaad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c72c323805bacdaf34a78cf1c8a1c9ee797ccc080218f139034c89c83678bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430b2cccabba307094733525d2e93ee19e97733a780bfd95f77dafd341b5a031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8bef0a20e33a2b3f7f8075e784358afc0c665468d20aef5af1a1b3bfee29a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c10680288c1767fd4f108def5a464f38201d318aa06d8222c48abc210f0d313)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBasicAuthCredentials")
    def put_basic_auth_credentials(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putBasicAuthCredentials", [value]))

    @jsii.member(jsii_name="putOauthCredentials")
    def put_oauth_credentials(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            oauth_request=oauth_request,
            refresh_token=refresh_token,
        )

        return typing.cast(None, jsii.invoke(self, "putOauthCredentials", [value]))

    @jsii.member(jsii_name="resetBasicAuthCredentials")
    def reset_basic_auth_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuthCredentials", []))

    @jsii.member(jsii_name="resetOauthCredentials")
    def reset_oauth_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuthCredentials")
    def basic_auth_credentials(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentialsOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentialsOutputReference, jsii.get(self, "basicAuthCredentials"))

    @builtins.property
    @jsii.member(jsii_name="oauthCredentials")
    def oauth_credentials(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOutputReference, jsii.get(self, "oauthCredentials"))

    @builtins.property
    @jsii.member(jsii_name="basicAuthCredentialsInput")
    def basic_auth_credentials_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials], jsii.get(self, "basicAuthCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthCredentialsInput")
    def oauth_credentials_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials], jsii.get(self, "oauthCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5df427e6e40da103480903c8ef2bc234990cd67beb4c82bebc402dbbb4a823a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036efa852ad732250f352038cc32c37d38e5d4f3520320721702ed854d33100c)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__374a7ac1241dc04c4325fce225d4e0246b2d538c96998719b0b0ff093ae7dfb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308c89dff9e484c57356d39541b2bda651b99255b8d4bf1d750ce47d083d618c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281a05c0a0a9352b077465e125e9773087c00b07e411b6f212df07e8f8313c4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ddac264191d756d0c05f45771506145d08354a7e85091e428571fc3bb3725a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular",
    jsii_struct_bases=[],
    name_mapping={"api_key": "apiKey"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular:
    def __init__(self, *, api_key: builtins.str) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dba0dcbfc7b561902d6734b0cdfd56fd1d6039adaa41b8b96b399386c1c58b1)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
        }

    @builtins.property
    def api_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingularOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingularOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__297665aedaf1434aea0e8ce1e52ca0204941c06b1875c6c3e26ee1877007d452)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecf46edcf6b6765ae086b4935014368de8ad479c38f340a4397ac9b12cc0b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78af1965f36f01e1506439d3311b9d3d6c105a4d79905ba85c5bf77066052b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4726a79ca0c4868265c2512432032b05df8a158dcaba71aa0e899b6b424986f)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a0fb65150d4cd5fddce008793504ef6adbdade82b4565396e83c86f2546cbc)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__660a107ed4ed8cac0c2064d48b34fc90cf50fdf0f63a10abaef9632c57e3c932)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27eb1b71b92ae4cfbb940b8831d95b75de18cc3bb9a5ffc6fdc9cd17c8a5d0bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3f00e5a06404b7bdbc80d86ab4de2bae9340db4250986992a51a58fdf0f072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b78b5403775ab07409a5cce6907908ac0c2d0e9771600b93e231da0d306ae52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b1ce0c652e762c07d1a700239808de4829dcfeb734a2761e2903cb9619a3b82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe8f11a6652d66ea449c837eff813276d5336f6515560049bb3053742f6dace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a1fb8a01386286d3ecb439efcaa2002a31a07a566b36411eb3f29e03475b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0314991a6b75d682cdb1fa78f0a92539823b92c6a52258ae6daf14c939fffc87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7085110e5c19ed230cfa1b38a823ca4a4f6e69a15ed70c451e56a413f72158b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc11484766db602068b08a2680632fb5f9c1ac83aa03789d4be484540bd0e6d)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflakeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflakeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ceb4c964f4554ad1cb9a2bb49653f99f760c5a401b54d5e13e74569948b061e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737e922204be835acee08b51ba703fe541b3850ee6d7f347b679b098fa5ae3d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daae8b93a9220088880d0d51334904b2a2a744294402b6a2c53b507a3ab95eee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__092f5e18f5152bd4226e5291ddebbfe2925bbc23ae57b2c3419766bb2639f8ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro",
    jsii_struct_bases=[],
    name_mapping={"api_secret_key": "apiSecretKey"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro:
    def __init__(self, *, api_secret_key: builtins.str) -> None:
        '''
        :param api_secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4a8a468647c04d33600433740307a236f5e3e256392ebeed9fc73c96ee500f)
            check_type(argname="argument api_secret_key", value=api_secret_key, expected_type=type_hints["api_secret_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_secret_key": api_secret_key,
        }

    @builtins.property
    def api_secret_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.'''
        result = self._values.get("api_secret_key")
        assert result is not None, "Required property 'api_secret_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicroOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicroOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ea1b0590db77e32bb29761421cbd3f79860d577349b5819e5d03e600b19d655)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiSecretKeyInput")
    def api_secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiSecretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSecretKey")
    def api_secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiSecretKey"))

    @api_secret_key.setter
    def api_secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0455327144d9ba08f38f9793515d6d45d95306789d5e930dfa8fc9fe5094bc2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiSecretKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ef2893ad43417e0bd8067e08a483826d7216091f7715b6dfef6fbd5cd1bf9c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0786144dc59bbcbe2dcb842c6f22ce022b0f5b2ca46f19eb7c8d65e68eaa8e8f)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeevaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeevaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54b3c930b7cbb3ad77aeda10e88204b30030aaff60a30d1f6483148a97e587d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3e5be5c089317df62198a8ca2232fe2a1944c37df439c25bb4a44089a9241e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c3199daa4a71b1a999f90eed0de89968f86197dc5cf751b4914bfd56af2a537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b18964d025688c7265581cac569100d15da1646cddf5695948bcec747d09b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b573fe9b732bfc57b725a6c59128d288f922a480e46919a0b708ca351de9213f)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40004efd6419d0bc841659262ba83367885f0b1df6cbfb2a67ef9e791e238aa)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03d59ddc6735ebff542d5607dddfc8f0330fee54ec83fdef74358c0c72ca939c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79bf0609ab721fc733099bf108862b7ead22910036850eaec6ef25a8275588ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbff5c965be6b98547d94e70076c74708a56155f86e5532fbf58045fb1d68420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04848c498149d6e47e8403bd5f293fb0c31abe6f35d4f676370a05b2f435314a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e665721fb24be7ae5eb67894a11960d9bd2f75165771558e16e4b0e8fb45e292)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68576c6faec5601179f3c80f629321f8f5a6a3baa97afb3fc0c6d8b156a17d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0d307f172c7be60f25907d1ef0ec620e8bf1937fb32873b0f913ddc16d6c2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49dab2733e4525cdadcb29853a3bf3c70ffbda31ba9dd7e8167c5cd572f3f013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83499cd1661c7b700eca6f7d0b048a9ddbbca7f0f5a351ed0e0c8343a475e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties",
    jsii_struct_bases=[],
    name_mapping={
        "amplitude": "amplitude",
        "custom_connector": "customConnector",
        "datadog": "datadog",
        "dynatrace": "dynatrace",
        "google_analytics": "googleAnalytics",
        "honeycode": "honeycode",
        "infor_nexus": "inforNexus",
        "marketo": "marketo",
        "redshift": "redshift",
        "salesforce": "salesforce",
        "sapo_data": "sapoData",
        "service_now": "serviceNow",
        "singular": "singular",
        "slack": "slack",
        "snowflake": "snowflake",
        "trendmicro": "trendmicro",
        "veeva": "veeva",
        "zendesk": "zendesk",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties:
    def __init__(
        self,
        *,
        amplitude: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace", typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode", typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus", typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce", typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack", typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake", typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro", typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva", typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        if isinstance(amplitude, dict):
            amplitude = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude(**amplitude)
        if isinstance(custom_connector, dict):
            custom_connector = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector(**custom_connector)
        if isinstance(datadog, dict):
            datadog = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog(**datadog)
        if isinstance(dynatrace, dict):
            dynatrace = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace(**dynatrace)
        if isinstance(google_analytics, dict):
            google_analytics = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics(**google_analytics)
        if isinstance(honeycode, dict):
            honeycode = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode(**honeycode)
        if isinstance(infor_nexus, dict):
            infor_nexus = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus(**infor_nexus)
        if isinstance(marketo, dict):
            marketo = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo(**marketo)
        if isinstance(redshift, dict):
            redshift = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift(**redshift)
        if isinstance(salesforce, dict):
            salesforce = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce(**salesforce)
        if isinstance(sapo_data, dict):
            sapo_data = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData(**sapo_data)
        if isinstance(service_now, dict):
            service_now = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow(**service_now)
        if isinstance(singular, dict):
            singular = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular(**singular)
        if isinstance(slack, dict):
            slack = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack(**slack)
        if isinstance(snowflake, dict):
            snowflake = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake(**snowflake)
        if isinstance(trendmicro, dict):
            trendmicro = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro(**trendmicro)
        if isinstance(veeva, dict):
            veeva = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva(**veeva)
        if isinstance(zendesk, dict):
            zendesk = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk(**zendesk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4e5d400c720b79aefb9b39b08feabb212b0a1fb37891556965a2b2ec2adaab)
            check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
            check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
            check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
            check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
            check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
            check_type(argname="argument honeycode", value=honeycode, expected_type=type_hints["honeycode"])
            check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
            check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
            check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
            check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
            check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
            check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
            check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
            check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amplitude is not None:
            self._values["amplitude"] = amplitude
        if custom_connector is not None:
            self._values["custom_connector"] = custom_connector
        if datadog is not None:
            self._values["datadog"] = datadog
        if dynatrace is not None:
            self._values["dynatrace"] = dynatrace
        if google_analytics is not None:
            self._values["google_analytics"] = google_analytics
        if honeycode is not None:
            self._values["honeycode"] = honeycode
        if infor_nexus is not None:
            self._values["infor_nexus"] = infor_nexus
        if marketo is not None:
            self._values["marketo"] = marketo
        if redshift is not None:
            self._values["redshift"] = redshift
        if salesforce is not None:
            self._values["salesforce"] = salesforce
        if sapo_data is not None:
            self._values["sapo_data"] = sapo_data
        if service_now is not None:
            self._values["service_now"] = service_now
        if singular is not None:
            self._values["singular"] = singular
        if slack is not None:
            self._values["slack"] = slack
        if snowflake is not None:
            self._values["snowflake"] = snowflake
        if trendmicro is not None:
            self._values["trendmicro"] = trendmicro
        if veeva is not None:
            self._values["veeva"] = veeva
        if zendesk is not None:
            self._values["zendesk"] = zendesk

    @builtins.property
    def amplitude(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude"]:
        '''amplitude block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        '''
        result = self._values.get("amplitude")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude"], result)

    @builtins.property
    def custom_connector(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector"]:
        '''custom_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        '''
        result = self._values.get("custom_connector")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector"], result)

    @builtins.property
    def datadog(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog"]:
        '''datadog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        '''
        result = self._values.get("datadog")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog"], result)

    @builtins.property
    def dynatrace(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace"]:
        '''dynatrace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        '''
        result = self._values.get("dynatrace")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace"], result)

    @builtins.property
    def google_analytics(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics"]:
        '''google_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        '''
        result = self._values.get("google_analytics")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics"], result)

    @builtins.property
    def honeycode(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode"]:
        '''honeycode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        '''
        result = self._values.get("honeycode")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode"], result)

    @builtins.property
    def infor_nexus(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus"]:
        '''infor_nexus block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        '''
        result = self._values.get("infor_nexus")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus"], result)

    @builtins.property
    def marketo(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo"]:
        '''marketo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        '''
        result = self._values.get("marketo")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo"], result)

    @builtins.property
    def redshift(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift"]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift"], result)

    @builtins.property
    def salesforce(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce"]:
        '''salesforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        '''
        result = self._values.get("salesforce")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce"], result)

    @builtins.property
    def sapo_data(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData"]:
        '''sapo_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        '''
        result = self._values.get("sapo_data")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData"], result)

    @builtins.property
    def service_now(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow"]:
        '''service_now block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        '''
        result = self._values.get("service_now")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow"], result)

    @builtins.property
    def singular(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular"]:
        '''singular block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        '''
        result = self._values.get("singular")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular"], result)

    @builtins.property
    def slack(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack"]:
        '''slack block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        '''
        result = self._values.get("slack")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack"], result)

    @builtins.property
    def snowflake(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake"]:
        '''snowflake block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        '''
        result = self._values.get("snowflake")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake"], result)

    @builtins.property
    def trendmicro(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro"]:
        '''trendmicro block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        '''
        result = self._values.get("trendmicro")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro"], result)

    @builtins.property
    def veeva(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva"]:
        '''veeva block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        '''
        result = self._values.get("veeva")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva"], result)

    @builtins.property
    def zendesk(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk"]:
        '''zendesk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        result = self._values.get("zendesk")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitudeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitudeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9497b9e495174b3c0a065d6bef1f6ee0561f7aac88da82a3c88d78a1816520e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fae2d2a47e02b9a1af4e95be92377051e71be39602d6b8e17f51ea172e5da72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector",
    jsii_struct_bases=[],
    name_mapping={
        "oauth2_properties": "oauth2Properties",
        "profile_properties": "profileProperties",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector:
    def __init__(
        self,
        *,
        oauth2_properties: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties", typing.Dict[builtins.str, typing.Any]]] = None,
        profile_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2_properties: oauth2_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2_properties AppflowConnectorProfile#oauth2_properties}
        :param profile_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#profile_properties AppflowConnectorProfile#profile_properties}.
        '''
        if isinstance(oauth2_properties, dict):
            oauth2_properties = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties(**oauth2_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf9a42a115d28ad3fd920d399a4f8c1a27b393aca3309868fd4260cc290ff74)
            check_type(argname="argument oauth2_properties", value=oauth2_properties, expected_type=type_hints["oauth2_properties"])
            check_type(argname="argument profile_properties", value=profile_properties, expected_type=type_hints["profile_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if oauth2_properties is not None:
            self._values["oauth2_properties"] = oauth2_properties
        if profile_properties is not None:
            self._values["profile_properties"] = profile_properties

    @builtins.property
    def oauth2_properties(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties"]:
        '''oauth2_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2_properties AppflowConnectorProfile#oauth2_properties}
        '''
        result = self._values.get("oauth2_properties")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties"], result)

    @builtins.property
    def profile_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#profile_properties AppflowConnectorProfile#profile_properties}.'''
        result = self._values.get("profile_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties",
    jsii_struct_bases=[],
    name_mapping={
        "oauth2_grant_type": "oauth2GrantType",
        "token_url": "tokenUrl",
        "token_url_custom_properties": "tokenUrlCustomProperties",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties:
    def __init__(
        self,
        *,
        oauth2_grant_type: builtins.str,
        token_url: builtins.str,
        token_url_custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2_grant_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.
        :param token_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.
        :param token_url_custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#token_url_custom_properties AppflowConnectorProfile#token_url_custom_properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c506516a35c699cf61b0ca3ed264366da733e84cb1f5fc180ce029e76b3927b1)
            check_type(argname="argument oauth2_grant_type", value=oauth2_grant_type, expected_type=type_hints["oauth2_grant_type"])
            check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
            check_type(argname="argument token_url_custom_properties", value=token_url_custom_properties, expected_type=type_hints["token_url_custom_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth2_grant_type": oauth2_grant_type,
            "token_url": token_url,
        }
        if token_url_custom_properties is not None:
            self._values["token_url_custom_properties"] = token_url_custom_properties

    @builtins.property
    def oauth2_grant_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.'''
        result = self._values.get("oauth2_grant_type")
        assert result is not None, "Required property 'oauth2_grant_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.'''
        result = self._values.get("token_url")
        assert result is not None, "Required property 'token_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_url_custom_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#token_url_custom_properties AppflowConnectorProfile#token_url_custom_properties}.'''
        result = self._values.get("token_url_custom_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2PropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2PropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bddee0000f9b94ecff201a9b48e73fc85e0618603d5ba0eb606adffeaadb6955)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTokenUrlCustomProperties")
    def reset_token_url_custom_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenUrlCustomProperties", []))

    @builtins.property
    @jsii.member(jsii_name="oauth2GrantTypeInput")
    def oauth2_grant_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauth2GrantTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrlCustomPropertiesInput")
    def token_url_custom_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tokenUrlCustomPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrlInput")
    def token_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2GrantType")
    def oauth2_grant_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2GrantType"))

    @oauth2_grant_type.setter
    def oauth2_grant_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01423bd838ec06c2434c57f3992e41e4d7deb170948b8a6ed4c83201e251315a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2GrantType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

    @token_url.setter
    def token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561500396444bc69b710f202d8ac082dcaffb6f31b3bb8df1cdb5b52614db18a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenUrlCustomProperties")
    def token_url_custom_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tokenUrlCustomProperties"))

    @token_url_custom_properties.setter
    def token_url_custom_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23c0ea652084eea5550bbd07d839b22dc935a6c7efe76386e12d0410307802a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrlCustomProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92346172df64a83f6bcc27570eed72290af9bb290685ef850723ca22ca09ec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42aa3bb900a30675bf00e36c9d4aba2cbceb2277ce74c9f05c218381d179dbc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauth2Properties")
    def put_oauth2_properties(
        self,
        *,
        oauth2_grant_type: builtins.str,
        token_url: builtins.str,
        token_url_custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2_grant_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.
        :param token_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.
        :param token_url_custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#token_url_custom_properties AppflowConnectorProfile#token_url_custom_properties}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties(
            oauth2_grant_type=oauth2_grant_type,
            token_url=token_url,
            token_url_custom_properties=token_url_custom_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2Properties", [value]))

    @jsii.member(jsii_name="resetOauth2Properties")
    def reset_oauth2_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2Properties", []))

    @jsii.member(jsii_name="resetProfileProperties")
    def reset_profile_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileProperties", []))

    @builtins.property
    @jsii.member(jsii_name="oauth2Properties")
    def oauth2_properties(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2PropertiesOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2PropertiesOutputReference, jsii.get(self, "oauth2Properties"))

    @builtins.property
    @jsii.member(jsii_name="oauth2PropertiesInput")
    def oauth2_properties_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties], jsii.get(self, "oauth2PropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="profilePropertiesInput")
    def profile_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "profilePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="profileProperties")
    def profile_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "profileProperties"))

    @profile_properties.setter
    def profile_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f7b8678e85a95f1f3f44bb2d1879ed9132832f16e9a356f04614348369d485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3aa9ac7926e657329fb778fa241c0a689f1766690538942ec409155f46bedf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed1de928579847c9ae24703355f2414417b5938e5a3c00b57bae26197dbdcdf)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04c289c9a7c16c27eee0ed8a6b5bae346787f0e727e745f78f4895631e566e98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43f6250bbed1c5e1f8f8d2016329db5f5e9dfda02b244a5b227140e2af4fa06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3ecf5a5ce8d0a6e6f7c984017bc99a4e942dd322bcf887e13a95526e559f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de26e619fdb15c1ffabc1b125166c32d73636eb449e9d19d969232cc7596e179)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatraceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatraceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9228b3ce7ed3100b00e3902b0cd8294596b1ccf4e5330b998068cd67a88a5d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a9eef18acad32308490a81492f816263210743c9dfdb0d743b45c05d2825a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25dd0cc1e421623a940db53f5783dbf34b754b35408e8623872bcaebd4739d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85541698bb1150674451ff334ad7a374d1794cf29bb4bb44350195ae8f2c885e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc0bdeb661cb0d08d39f29cd3c8a0e085c0ca2661dc5bcd38788de12e02db79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87a78e43c4d989d9a927b01c2f9ba7d846f50d4f58ca9581054d666e26c7cbfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9981b313b275b6a2271485fa8520a033d14a82dfe7f06bbd3c034dc6a67d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6345f6d9531ac5c8f0571e1330b7554f9f93b2cd784c4d054e57e6d6f5feee33)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efb9aa6523905d4eb571c506df888dd018fa62c839b3037506f86c1ba90da36a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238b9221a545467b8dd646b7a9037e2cc505ea175a4e824a3b45eeb86cff28e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c303aa8c6546886333b3d1cbb71fab38f14182a86e061fe695da0cd5d52e416a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca12e1672af0e16129e71ed2592685ae5c6f92af6c3b10879a87d51537bf6e3f)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6710d7b26a9af468f7a0f075dc198135ea571ff32faeffac4d410ce5bb3ab2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fac749e8bc6e0abaa54ecfd11f230547d5a0f84daf21171e8cb939084be3f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c1d837c87c419f25ced8ccd9d631ae44600394c91046df6ba8216a39f6e804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6acf8b6c1af69e6dfd6c391c94589aac49af1e1cdc978547e31876139740154d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAmplitude")
    def put_amplitude(self) -> None:
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude()

        return typing.cast(None, jsii.invoke(self, "putAmplitude", [value]))

    @jsii.member(jsii_name="putCustomConnector")
    def put_custom_connector(
        self,
        *,
        oauth2_properties: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties, typing.Dict[builtins.str, typing.Any]]] = None,
        profile_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2_properties: oauth2_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth2_properties AppflowConnectorProfile#oauth2_properties}
        :param profile_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#profile_properties AppflowConnectorProfile#profile_properties}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector(
            oauth2_properties=oauth2_properties, profile_properties=profile_properties
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConnector", [value]))

    @jsii.member(jsii_name="putDatadog")
    def put_datadog(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putDatadog", [value]))

    @jsii.member(jsii_name="putDynatrace")
    def put_dynatrace(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putDynatrace", [value]))

    @jsii.member(jsii_name="putGoogleAnalytics")
    def put_google_analytics(self) -> None:
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics()

        return typing.cast(None, jsii.invoke(self, "putGoogleAnalytics", [value]))

    @jsii.member(jsii_name="putHoneycode")
    def put_honeycode(self) -> None:
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode()

        return typing.cast(None, jsii.invoke(self, "putHoneycode", [value]))

    @jsii.member(jsii_name="putInforNexus")
    def put_infor_nexus(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putInforNexus", [value]))

    @jsii.member(jsii_name="putMarketo")
    def put_marketo(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putMarketo", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(
        self,
        *,
        bucket_name: builtins.str,
        role_arn: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        data_api_role_arn: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        database_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#role_arn AppflowConnectorProfile#role_arn}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.
        :param cluster_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#cluster_identifier AppflowConnectorProfile#cluster_identifier}.
        :param data_api_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#data_api_role_arn AppflowConnectorProfile#data_api_role_arn}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#database_name AppflowConnectorProfile#database_name}.
        :param database_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#database_url AppflowConnectorProfile#database_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift(
            bucket_name=bucket_name,
            role_arn=role_arn,
            bucket_prefix=bucket_prefix,
            cluster_identifier=cluster_identifier,
            data_api_role_arn=data_api_role_arn,
            database_name=database_name,
            database_url=database_url,
        )

        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putSalesforce")
    def put_salesforce(
        self,
        *,
        instance_url: typing.Optional[builtins.str] = None,
        is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_privatelink_for_metadata_and_authorization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        :param is_sandbox_environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#is_sandbox_environment AppflowConnectorProfile#is_sandbox_environment}.
        :param use_privatelink_for_metadata_and_authorization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#use_privatelink_for_metadata_and_authorization AppflowConnectorProfile#use_privatelink_for_metadata_and_authorization}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce(
            instance_url=instance_url,
            is_sandbox_environment=is_sandbox_environment,
            use_privatelink_for_metadata_and_authorization=use_privatelink_for_metadata_and_authorization,
        )

        return typing.cast(None, jsii.invoke(self, "putSalesforce", [value]))

    @jsii.member(jsii_name="putSapoData")
    def put_sapo_data(
        self,
        *,
        application_host_url: builtins.str,
        application_service_path: builtins.str,
        client_number: builtins.str,
        port_number: jsii.Number,
        logon_language: typing.Optional[builtins.str] = None,
        oauth_properties: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param application_host_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#application_host_url AppflowConnectorProfile#application_host_url}.
        :param application_service_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#application_service_path AppflowConnectorProfile#application_service_path}.
        :param client_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_number AppflowConnectorProfile#client_number}.
        :param port_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#port_number AppflowConnectorProfile#port_number}.
        :param logon_language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#logon_language AppflowConnectorProfile#logon_language}.
        :param oauth_properties: oauth_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_properties AppflowConnectorProfile#oauth_properties}
        :param private_link_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData(
            application_host_url=application_host_url,
            application_service_path=application_service_path,
            client_number=client_number,
            port_number=port_number,
            logon_language=logon_language,
            oauth_properties=oauth_properties,
            private_link_service_name=private_link_service_name,
        )

        return typing.cast(None, jsii.invoke(self, "putSapoData", [value]))

    @jsii.member(jsii_name="putServiceNow")
    def put_service_now(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putServiceNow", [value]))

    @jsii.member(jsii_name="putSingular")
    def put_singular(self) -> None:
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular()

        return typing.cast(None, jsii.invoke(self, "putSingular", [value]))

    @jsii.member(jsii_name="putSlack")
    def put_slack(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putSlack", [value]))

    @jsii.member(jsii_name="putSnowflake")
    def put_snowflake(
        self,
        *,
        bucket_name: builtins.str,
        stage: builtins.str,
        warehouse: builtins.str,
        account_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        private_link_service_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.
        :param stage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#stage AppflowConnectorProfile#stage}.
        :param warehouse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#warehouse AppflowConnectorProfile#warehouse}.
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#account_name AppflowConnectorProfile#account_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.
        :param private_link_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#region AppflowConnectorProfile#region}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake(
            bucket_name=bucket_name,
            stage=stage,
            warehouse=warehouse,
            account_name=account_name,
            bucket_prefix=bucket_prefix,
            private_link_service_name=private_link_service_name,
            region=region,
        )

        return typing.cast(None, jsii.invoke(self, "putSnowflake", [value]))

    @jsii.member(jsii_name="putTrendmicro")
    def put_trendmicro(self) -> None:
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro()

        return typing.cast(None, jsii.invoke(self, "putTrendmicro", [value]))

    @jsii.member(jsii_name="putVeeva")
    def put_veeva(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putVeeva", [value]))

    @jsii.member(jsii_name="putZendesk")
    def put_zendesk(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putZendesk", [value]))

    @jsii.member(jsii_name="resetAmplitude")
    def reset_amplitude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmplitude", []))

    @jsii.member(jsii_name="resetCustomConnector")
    def reset_custom_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConnector", []))

    @jsii.member(jsii_name="resetDatadog")
    def reset_datadog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadog", []))

    @jsii.member(jsii_name="resetDynatrace")
    def reset_dynatrace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynatrace", []))

    @jsii.member(jsii_name="resetGoogleAnalytics")
    def reset_google_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleAnalytics", []))

    @jsii.member(jsii_name="resetHoneycode")
    def reset_honeycode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHoneycode", []))

    @jsii.member(jsii_name="resetInforNexus")
    def reset_infor_nexus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInforNexus", []))

    @jsii.member(jsii_name="resetMarketo")
    def reset_marketo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketo", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetSalesforce")
    def reset_salesforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSalesforce", []))

    @jsii.member(jsii_name="resetSapoData")
    def reset_sapo_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSapoData", []))

    @jsii.member(jsii_name="resetServiceNow")
    def reset_service_now(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceNow", []))

    @jsii.member(jsii_name="resetSingular")
    def reset_singular(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingular", []))

    @jsii.member(jsii_name="resetSlack")
    def reset_slack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlack", []))

    @jsii.member(jsii_name="resetSnowflake")
    def reset_snowflake(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowflake", []))

    @jsii.member(jsii_name="resetTrendmicro")
    def reset_trendmicro(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrendmicro", []))

    @jsii.member(jsii_name="resetVeeva")
    def reset_veeva(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVeeva", []))

    @jsii.member(jsii_name="resetZendesk")
    def reset_zendesk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZendesk", []))

    @builtins.property
    @jsii.member(jsii_name="amplitude")
    def amplitude(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitudeOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitudeOutputReference, jsii.get(self, "amplitude"))

    @builtins.property
    @jsii.member(jsii_name="customConnector")
    def custom_connector(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOutputReference, jsii.get(self, "customConnector"))

    @builtins.property
    @jsii.member(jsii_name="datadog")
    def datadog(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadogOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadogOutputReference, jsii.get(self, "datadog"))

    @builtins.property
    @jsii.member(jsii_name="dynatrace")
    def dynatrace(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatraceOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatraceOutputReference, jsii.get(self, "dynatrace"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalytics")
    def google_analytics(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalyticsOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalyticsOutputReference, jsii.get(self, "googleAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="honeycode")
    def honeycode(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycodeOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycodeOutputReference, jsii.get(self, "honeycode"))

    @builtins.property
    @jsii.member(jsii_name="inforNexus")
    def infor_nexus(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexusOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexusOutputReference, jsii.get(self, "inforNexus"))

    @builtins.property
    @jsii.member(jsii_name="marketo")
    def marketo(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketoOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketoOutputReference, jsii.get(self, "marketo"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshiftOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshiftOutputReference", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="salesforce")
    def salesforce(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforceOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforceOutputReference", jsii.get(self, "salesforce"))

    @builtins.property
    @jsii.member(jsii_name="sapoData")
    def sapo_data(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOutputReference", jsii.get(self, "sapoData"))

    @builtins.property
    @jsii.member(jsii_name="serviceNow")
    def service_now(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNowOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNowOutputReference", jsii.get(self, "serviceNow"))

    @builtins.property
    @jsii.member(jsii_name="singular")
    def singular(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingularOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingularOutputReference", jsii.get(self, "singular"))

    @builtins.property
    @jsii.member(jsii_name="slack")
    def slack(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlackOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlackOutputReference", jsii.get(self, "slack"))

    @builtins.property
    @jsii.member(jsii_name="snowflake")
    def snowflake(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflakeOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflakeOutputReference", jsii.get(self, "snowflake"))

    @builtins.property
    @jsii.member(jsii_name="trendmicro")
    def trendmicro(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicroOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicroOutputReference", jsii.get(self, "trendmicro"))

    @builtins.property
    @jsii.member(jsii_name="veeva")
    def veeva(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeevaOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeevaOutputReference", jsii.get(self, "veeva"))

    @builtins.property
    @jsii.member(jsii_name="zendesk")
    def zendesk(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendeskOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendeskOutputReference", jsii.get(self, "zendesk"))

    @builtins.property
    @jsii.member(jsii_name="amplitudeInput")
    def amplitude_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude], jsii.get(self, "amplitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="customConnectorInput")
    def custom_connector_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector], jsii.get(self, "customConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogInput")
    def datadog_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog], jsii.get(self, "datadogInput"))

    @builtins.property
    @jsii.member(jsii_name="dynatraceInput")
    def dynatrace_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace], jsii.get(self, "dynatraceInput"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalyticsInput")
    def google_analytics_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics], jsii.get(self, "googleAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="honeycodeInput")
    def honeycode_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode], jsii.get(self, "honeycodeInput"))

    @builtins.property
    @jsii.member(jsii_name="inforNexusInput")
    def infor_nexus_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus], jsii.get(self, "inforNexusInput"))

    @builtins.property
    @jsii.member(jsii_name="marketoInput")
    def marketo_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo], jsii.get(self, "marketoInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift"], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="salesforceInput")
    def salesforce_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce"], jsii.get(self, "salesforceInput"))

    @builtins.property
    @jsii.member(jsii_name="sapoDataInput")
    def sapo_data_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData"], jsii.get(self, "sapoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNowInput")
    def service_now_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow"], jsii.get(self, "serviceNowInput"))

    @builtins.property
    @jsii.member(jsii_name="singularInput")
    def singular_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular"], jsii.get(self, "singularInput"))

    @builtins.property
    @jsii.member(jsii_name="slackInput")
    def slack_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack"], jsii.get(self, "slackInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeInput")
    def snowflake_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake"], jsii.get(self, "snowflakeInput"))

    @builtins.property
    @jsii.member(jsii_name="trendmicroInput")
    def trendmicro_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro"], jsii.get(self, "trendmicroInput"))

    @builtins.property
    @jsii.member(jsii_name="veevaInput")
    def veeva_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva"], jsii.get(self, "veevaInput"))

    @builtins.property
    @jsii.member(jsii_name="zendeskInput")
    def zendesk_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk"], jsii.get(self, "zendeskInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c33009615600cbbc908da9dd73ac08cf53ef3b26a95fc38f64cef7401632976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "role_arn": "roleArn",
        "bucket_prefix": "bucketPrefix",
        "cluster_identifier": "clusterIdentifier",
        "data_api_role_arn": "dataApiRoleArn",
        "database_name": "databaseName",
        "database_url": "databaseUrl",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        role_arn: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        data_api_role_arn: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        database_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#role_arn AppflowConnectorProfile#role_arn}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.
        :param cluster_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#cluster_identifier AppflowConnectorProfile#cluster_identifier}.
        :param data_api_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#data_api_role_arn AppflowConnectorProfile#data_api_role_arn}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#database_name AppflowConnectorProfile#database_name}.
        :param database_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#database_url AppflowConnectorProfile#database_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba56e7832ef3f079572d94516ec0e7930f237df3af971ad05b4d444ea9e9993)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
            check_type(argname="argument data_api_role_arn", value=data_api_role_arn, expected_type=type_hints["data_api_role_arn"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument database_url", value=database_url, expected_type=type_hints["database_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "role_arn": role_arn,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if cluster_identifier is not None:
            self._values["cluster_identifier"] = cluster_identifier
        if data_api_role_arn is not None:
            self._values["data_api_role_arn"] = data_api_role_arn
        if database_name is not None:
            self._values["database_name"] = database_name
        if database_url is not None:
            self._values["database_url"] = database_url

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#role_arn AppflowConnectorProfile#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#cluster_identifier AppflowConnectorProfile#cluster_identifier}.'''
        result = self._values.get("cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_api_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#data_api_role_arn AppflowConnectorProfile#data_api_role_arn}.'''
        result = self._values.get("data_api_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#database_name AppflowConnectorProfile#database_name}.'''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#database_url AppflowConnectorProfile#database_url}.'''
        result = self._values.get("database_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c7c473b51a4cbbcac49a340fb86dc9a00d0de9bb71afe2a3f6f0d71c31216b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetClusterIdentifier")
    def reset_cluster_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterIdentifier", []))

    @jsii.member(jsii_name="resetDataApiRoleArn")
    def reset_data_api_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataApiRoleArn", []))

    @jsii.member(jsii_name="resetDatabaseName")
    def reset_database_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseName", []))

    @jsii.member(jsii_name="resetDatabaseUrl")
    def reset_database_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseUrl", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifierInput")
    def cluster_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="dataApiRoleArnInput")
    def data_api_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataApiRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseUrlInput")
    def database_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99b9dcb137993b5c08c9ecb8777a33a91532d9d267f73bc40e2e3a63a3349d7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d38e8ed6e7fe3101686afff6fab888748aeae6548c58588c90e0ec7094da600d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @cluster_identifier.setter
    def cluster_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9589a4040a575d51f2cf39cb694d2daa156831e5d5062dc1f5d042c414ca1db5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataApiRoleArn")
    def data_api_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataApiRoleArn"))

    @data_api_role_arn.setter
    def data_api_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ad97da85fecc1b68ea50b4de22cc203b91ebeab1d01d2da4b44220d6579498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataApiRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee41bcd1bd4cecee3d98f7de3485ca4430294dbf596b24d7cd765b98494f1a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseUrl")
    def database_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseUrl"))

    @database_url.setter
    def database_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095eee0116b1c70929161bbbe387836be5c802f7377ad2a6c625bee3f53d9f05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818d8fad887ff7592127dd8ab93511a1e3721423b7119d88a9d8d13898922f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10f232fc4e7bc7959aa81749e33d7a36cfeb772123eec887d546672297e93e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce",
    jsii_struct_bases=[],
    name_mapping={
        "instance_url": "instanceUrl",
        "is_sandbox_environment": "isSandboxEnvironment",
        "use_privatelink_for_metadata_and_authorization": "usePrivatelinkForMetadataAndAuthorization",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce:
    def __init__(
        self,
        *,
        instance_url: typing.Optional[builtins.str] = None,
        is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_privatelink_for_metadata_and_authorization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        :param is_sandbox_environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#is_sandbox_environment AppflowConnectorProfile#is_sandbox_environment}.
        :param use_privatelink_for_metadata_and_authorization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#use_privatelink_for_metadata_and_authorization AppflowConnectorProfile#use_privatelink_for_metadata_and_authorization}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d835ad017372d7074864a69fa58b4b1db91271ece95ef68a3882fa01b2186178)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            check_type(argname="argument is_sandbox_environment", value=is_sandbox_environment, expected_type=type_hints["is_sandbox_environment"])
            check_type(argname="argument use_privatelink_for_metadata_and_authorization", value=use_privatelink_for_metadata_and_authorization, expected_type=type_hints["use_privatelink_for_metadata_and_authorization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_url is not None:
            self._values["instance_url"] = instance_url
        if is_sandbox_environment is not None:
            self._values["is_sandbox_environment"] = is_sandbox_environment
        if use_privatelink_for_metadata_and_authorization is not None:
            self._values["use_privatelink_for_metadata_and_authorization"] = use_privatelink_for_metadata_and_authorization

    @builtins.property
    def instance_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_sandbox_environment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#is_sandbox_environment AppflowConnectorProfile#is_sandbox_environment}.'''
        result = self._values.get("is_sandbox_environment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_privatelink_for_metadata_and_authorization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#use_privatelink_for_metadata_and_authorization AppflowConnectorProfile#use_privatelink_for_metadata_and_authorization}.'''
        result = self._values.get("use_privatelink_for_metadata_and_authorization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7693b8cb15aee7d0fcc11572737749adde16aaa2fcd5a34acc8024fc155ad82e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceUrl")
    def reset_instance_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceUrl", []))

    @jsii.member(jsii_name="resetIsSandboxEnvironment")
    def reset_is_sandbox_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSandboxEnvironment", []))

    @jsii.member(jsii_name="resetUsePrivatelinkForMetadataAndAuthorization")
    def reset_use_privatelink_for_metadata_and_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsePrivatelinkForMetadataAndAuthorization", []))

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="isSandboxEnvironmentInput")
    def is_sandbox_environment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSandboxEnvironmentInput"))

    @builtins.property
    @jsii.member(jsii_name="usePrivatelinkForMetadataAndAuthorizationInput")
    def use_privatelink_for_metadata_and_authorization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "usePrivatelinkForMetadataAndAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2ecb07d943cac2f8d9f9aca90d68480b61ef79d4a610a7ca139e2301cc76ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSandboxEnvironment")
    def is_sandbox_environment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSandboxEnvironment"))

    @is_sandbox_environment.setter
    def is_sandbox_environment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda3b8b450caf6e76ee0a73856cd6a8243bd73df20d20fa07459ab675db6be0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSandboxEnvironment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usePrivatelinkForMetadataAndAuthorization")
    def use_privatelink_for_metadata_and_authorization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "usePrivatelinkForMetadataAndAuthorization"))

    @use_privatelink_for_metadata_and_authorization.setter
    def use_privatelink_for_metadata_and_authorization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e806d3d37e277abbe26852dad8d184daa8cd3c4ab5cff5f023257fe7f99d292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usePrivatelinkForMetadataAndAuthorization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8615968fe1065dc346cf7da61b4a757e0ce4a7276579952931236dfbfd680f87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData",
    jsii_struct_bases=[],
    name_mapping={
        "application_host_url": "applicationHostUrl",
        "application_service_path": "applicationServicePath",
        "client_number": "clientNumber",
        "port_number": "portNumber",
        "logon_language": "logonLanguage",
        "oauth_properties": "oauthProperties",
        "private_link_service_name": "privateLinkServiceName",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData:
    def __init__(
        self,
        *,
        application_host_url: builtins.str,
        application_service_path: builtins.str,
        client_number: builtins.str,
        port_number: jsii.Number,
        logon_language: typing.Optional[builtins.str] = None,
        oauth_properties: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param application_host_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#application_host_url AppflowConnectorProfile#application_host_url}.
        :param application_service_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#application_service_path AppflowConnectorProfile#application_service_path}.
        :param client_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_number AppflowConnectorProfile#client_number}.
        :param port_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#port_number AppflowConnectorProfile#port_number}.
        :param logon_language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#logon_language AppflowConnectorProfile#logon_language}.
        :param oauth_properties: oauth_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_properties AppflowConnectorProfile#oauth_properties}
        :param private_link_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.
        '''
        if isinstance(oauth_properties, dict):
            oauth_properties = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties(**oauth_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdaa4135056120302752c4c1ddf20108c046aa87f221406d215b28e9462e9dd7)
            check_type(argname="argument application_host_url", value=application_host_url, expected_type=type_hints["application_host_url"])
            check_type(argname="argument application_service_path", value=application_service_path, expected_type=type_hints["application_service_path"])
            check_type(argname="argument client_number", value=client_number, expected_type=type_hints["client_number"])
            check_type(argname="argument port_number", value=port_number, expected_type=type_hints["port_number"])
            check_type(argname="argument logon_language", value=logon_language, expected_type=type_hints["logon_language"])
            check_type(argname="argument oauth_properties", value=oauth_properties, expected_type=type_hints["oauth_properties"])
            check_type(argname="argument private_link_service_name", value=private_link_service_name, expected_type=type_hints["private_link_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_host_url": application_host_url,
            "application_service_path": application_service_path,
            "client_number": client_number,
            "port_number": port_number,
        }
        if logon_language is not None:
            self._values["logon_language"] = logon_language
        if oauth_properties is not None:
            self._values["oauth_properties"] = oauth_properties
        if private_link_service_name is not None:
            self._values["private_link_service_name"] = private_link_service_name

    @builtins.property
    def application_host_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#application_host_url AppflowConnectorProfile#application_host_url}.'''
        result = self._values.get("application_host_url")
        assert result is not None, "Required property 'application_host_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_service_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#application_service_path AppflowConnectorProfile#application_service_path}.'''
        result = self._values.get("application_service_path")
        assert result is not None, "Required property 'application_service_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_number(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#client_number AppflowConnectorProfile#client_number}.'''
        result = self._values.get("client_number")
        assert result is not None, "Required property 'client_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port_number(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#port_number AppflowConnectorProfile#port_number}.'''
        result = self._values.get("port_number")
        assert result is not None, "Required property 'port_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def logon_language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#logon_language AppflowConnectorProfile#logon_language}.'''
        result = self._values.get("logon_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_properties(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties"]:
        '''oauth_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_properties AppflowConnectorProfile#oauth_properties}
        '''
        result = self._values.get("oauth_properties")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties"], result)

    @builtins.property
    def private_link_service_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.'''
        result = self._values.get("private_link_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties",
    jsii_struct_bases=[],
    name_mapping={
        "auth_code_url": "authCodeUrl",
        "oauth_scopes": "oauthScopes",
        "token_url": "tokenUrl",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties:
    def __init__(
        self,
        *,
        auth_code_url: builtins.str,
        oauth_scopes: typing.Sequence[builtins.str],
        token_url: builtins.str,
    ) -> None:
        '''
        :param auth_code_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code_url AppflowConnectorProfile#auth_code_url}.
        :param oauth_scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_scopes AppflowConnectorProfile#oauth_scopes}.
        :param token_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03891904b42202a9191faec3434cceae775f328196eb56954bd275b0e142c450)
            check_type(argname="argument auth_code_url", value=auth_code_url, expected_type=type_hints["auth_code_url"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
            check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_code_url": auth_code_url,
            "oauth_scopes": oauth_scopes,
            "token_url": token_url,
        }

    @builtins.property
    def auth_code_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code_url AppflowConnectorProfile#auth_code_url}.'''
        result = self._values.get("auth_code_url")
        assert result is not None, "Required property 'auth_code_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_scopes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_scopes AppflowConnectorProfile#oauth_scopes}.'''
        result = self._values.get("oauth_scopes")
        assert result is not None, "Required property 'oauth_scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def token_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.'''
        result = self._values.get("token_url")
        assert result is not None, "Required property 'token_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97f04e0b8a76bf3a442f273a152c28518e0d58bd699e2ad4dd37831209e2fe9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="authCodeUrlInput")
    def auth_code_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrlInput")
    def token_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="authCodeUrl")
    def auth_code_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCodeUrl"))

    @auth_code_url.setter
    def auth_code_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300666d35f9324429440cd87f1cdfb97cf15ee8a47a6baf3b4e98a2128a48ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCodeUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e5b319bef4b7836ba59dc4867afc08bfd6f9da5ef64fce2fe2eaf5997db8b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

    @token_url.setter
    def token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdaa9ea62d58ac8f8afce18b37fb13d2e43a56e644557a83f33b19e8478025c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e349939836a96aee263a1f951f36983ff3da8b36f26cebbe9ff66644b1247bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3e91263efb7939138067c0c2344b92ecf0e8f1839f8abdc07fdc4e0cb94fc35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthProperties")
    def put_oauth_properties(
        self,
        *,
        auth_code_url: builtins.str,
        oauth_scopes: typing.Sequence[builtins.str],
        token_url: builtins.str,
    ) -> None:
        '''
        :param auth_code_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#auth_code_url AppflowConnectorProfile#auth_code_url}.
        :param oauth_scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#oauth_scopes AppflowConnectorProfile#oauth_scopes}.
        :param token_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties(
            auth_code_url=auth_code_url, oauth_scopes=oauth_scopes, token_url=token_url
        )

        return typing.cast(None, jsii.invoke(self, "putOauthProperties", [value]))

    @jsii.member(jsii_name="resetLogonLanguage")
    def reset_logon_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogonLanguage", []))

    @jsii.member(jsii_name="resetOauthProperties")
    def reset_oauth_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthProperties", []))

    @jsii.member(jsii_name="resetPrivateLinkServiceName")
    def reset_private_link_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateLinkServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="oauthProperties")
    def oauth_properties(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthPropertiesOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthPropertiesOutputReference, jsii.get(self, "oauthProperties"))

    @builtins.property
    @jsii.member(jsii_name="applicationHostUrlInput")
    def application_host_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationHostUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationServicePathInput")
    def application_service_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationServicePathInput"))

    @builtins.property
    @jsii.member(jsii_name="clientNumberInput")
    def client_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="logonLanguageInput")
    def logon_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logonLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthPropertiesInput")
    def oauth_properties_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties], jsii.get(self, "oauthPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="portNumberInput")
    def port_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkServiceNameInput")
    def private_link_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateLinkServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationHostUrl")
    def application_host_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationHostUrl"))

    @application_host_url.setter
    def application_host_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f2451a40db127908855be19552fd96e156620cef80e27db8297dcf88252248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationHostUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationServicePath")
    def application_service_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationServicePath"))

    @application_service_path.setter
    def application_service_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4a00c3363d4272ea6331bb808ca35e0c25be5250e6f9b2200834fdd369c1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationServicePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientNumber")
    def client_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientNumber"))

    @client_number.setter
    def client_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9614302c3b105e7b1b26938ab6aff6ca4cdc8e660ab0f58a5c5cc48d46a6483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logonLanguage")
    def logon_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logonLanguage"))

    @logon_language.setter
    def logon_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865bdf783a9c906b41fcb0ef5880093c17c654974f463214c8725d4d1ee04e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logonLanguage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portNumber")
    def port_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "portNumber"))

    @port_number.setter
    def port_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd6bcbd9442faef142f55f5fb44f7d9864df84e9cb40795ceec3b1d754bdd57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateLinkServiceName")
    def private_link_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateLinkServiceName"))

    @private_link_service_name.setter
    def private_link_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcebf5eaa7708aabf743f169b1e9a96664ee99430603c40d84890b02108ae04e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateLinkServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e312df27b6e6aea47b71bd09c59dbb4fdfecc26bfc38edad17ae36a1d08744e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f230275cad2652c74b622cf917e7c02de77ddc176618a0ac2ee942e21af84678)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9482348613bdfe1d3c9612926cdacf7082316951c8c0c95475316a64b0a14b28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3d6848af7ca00621cb507904a1d38086b43a49a45b10afedc0de7fa97045fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8556af2be76b4e3755be79889f6f006b351a12a67df2a0e28a230a5ef727eee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingularOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingularOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e2c26cc51570cc4b4cf6b849533ac8dce0f602fa62617522132485a2f832ff2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7675605b7bc9e673c961c1611cb9ba516405b00aa4150919d97480ae1df159c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ebe0efe52d0edcac46a36d9f7895c68ccfbaf0461c2f16b9747142ccdfbfd41)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlackOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4f33aeb9e8653cc205ce0d83a1900d19fd3a4d811b452ca49671a6cae9ee17e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c93b0e0d24a47364e9a8ff6b63b876b5fa70a471d0c808d9ca71292a2d60c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55bc3ac607f108c4c7526dbb055d13c134c2ba1d62bd46cc79a306feb7b941bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "stage": "stage",
        "warehouse": "warehouse",
        "account_name": "accountName",
        "bucket_prefix": "bucketPrefix",
        "private_link_service_name": "privateLinkServiceName",
        "region": "region",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        stage: builtins.str,
        warehouse: builtins.str,
        account_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        private_link_service_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.
        :param stage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#stage AppflowConnectorProfile#stage}.
        :param warehouse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#warehouse AppflowConnectorProfile#warehouse}.
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#account_name AppflowConnectorProfile#account_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.
        :param private_link_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#region AppflowConnectorProfile#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe532941e05f415265a2813d1514942f49903800c6c5103550cf5f0d2ba9976e)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument warehouse", value=warehouse, expected_type=type_hints["warehouse"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument private_link_service_name", value=private_link_service_name, expected_type=type_hints["private_link_service_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "stage": stage,
            "warehouse": warehouse,
        }
        if account_name is not None:
            self._values["account_name"] = account_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if private_link_service_name is not None:
            self._values["private_link_service_name"] = private_link_service_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#stage AppflowConnectorProfile#stage}.'''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def warehouse(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#warehouse AppflowConnectorProfile#warehouse}.'''
        result = self._values.get("warehouse")
        assert result is not None, "Required property 'warehouse' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#account_name AppflowConnectorProfile#account_name}.'''
        result = self._values.get("account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_link_service_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.'''
        result = self._values.get("private_link_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#region AppflowConnectorProfile#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflakeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflakeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04ecdb0a27361a5c465d50e0dc01f352e6b38b8a3d12151f781c5ae6bb80979d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccountName")
    def reset_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetPrivateLinkServiceName")
    def reset_private_link_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateLinkServiceName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkServiceNameInput")
    def private_link_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateLinkServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="stageInput")
    def stage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stageInput"))

    @builtins.property
    @jsii.member(jsii_name="warehouseInput")
    def warehouse_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warehouseInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd1e91da1203b4f49db8831d43d597c1a7c9cf4410fdbd6a00b6c1e731b72c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89faf10037d208b0f51cafd3987724a069db28864dfc253edab709fd1e2a8e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20da9646053c98f6e295604f473df1af5c6a0c3e2d341dd00146ea66e1c9f4ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateLinkServiceName")
    def private_link_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateLinkServiceName"))

    @private_link_service_name.setter
    def private_link_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4460213380fe716920b96a39caacfa1c5a5894779ef20b1a13a8267f6d378b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateLinkServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb72a80bb703ab2e3bad541735319d1cb9a88693266444972f4dc75f0be3246d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stage"))

    @stage.setter
    def stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f838c0abaac1d03053962302ddc7fe3937a561c20b663e29d973b99f9f11af0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warehouse")
    def warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouse"))

    @warehouse.setter
    def warehouse(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bcb5b216e5d868ed204989086680398fb5d02bd66ae3ad85744aabd6cf4c1e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warehouse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c396075dcfcab9980aecfb9990ba2d10c63b491a116fcd5ddf4e22045a2e3d7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicroOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicroOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba61a1d0c0e109cb8b56a93d580a05e7b7fab4d9258a90784b9cd23ef4df7bba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33460545fc3ec40f74c009d18e9423e84149f7d974059e0411ef8a7f05e3c60f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b297be5eea6f88815e6bb1563ad669698f04788007149e035e4f9f1c23bf94ec)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeevaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeevaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da04dc4639c895ebf48fe3e9812d4bf0d0e7d75ce49029c3132360257fdf13f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babec7f4991f2c7cda1a0047e47a4d7d71b7483fa51cb86716597e6a12e0bbe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68f37cea9d05ab4480e04ae325c88e51a540ef7ce4719f22efda2662ca6a617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1861e56e6d8c60c5f05fcdea64e199637121015049ce58d5f9bb011a3ccb9ee5)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendeskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendeskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de4328bb6d49ddcdf36c8bc1054ee2faac8a943ca5665655ceb4e6676b41b9d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3f14f3dcf50af15dc3860359ac26819cc114db41c603994bed3e29afa11e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2bf55123232670938f3d86d03e18ba72af33750bd88d6eb112139bd0e3a93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34e06b370ed8bda16e5663b704e2bd4769889f53b41d4911191f04b5bc43a2ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConnectorProfileCredentials")
    def put_connector_profile_credentials(
        self,
        *,
        amplitude: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace, typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus, typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular, typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack, typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro, typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva, typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials(
            amplitude=amplitude,
            custom_connector=custom_connector,
            datadog=datadog,
            dynatrace=dynatrace,
            google_analytics=google_analytics,
            honeycode=honeycode,
            infor_nexus=infor_nexus,
            marketo=marketo,
            redshift=redshift,
            salesforce=salesforce,
            sapo_data=sapo_data,
            service_now=service_now,
            singular=singular,
            slack=slack,
            snowflake=snowflake,
            trendmicro=trendmicro,
            veeva=veeva,
            zendesk=zendesk,
        )

        return typing.cast(None, jsii.invoke(self, "putConnectorProfileCredentials", [value]))

    @jsii.member(jsii_name="putConnectorProfileProperties")
    def put_connector_profile_properties(
        self,
        *,
        amplitude: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace, typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus, typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular, typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack, typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro, typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva, typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties(
            amplitude=amplitude,
            custom_connector=custom_connector,
            datadog=datadog,
            dynatrace=dynatrace,
            google_analytics=google_analytics,
            honeycode=honeycode,
            infor_nexus=infor_nexus,
            marketo=marketo,
            redshift=redshift,
            salesforce=salesforce,
            sapo_data=sapo_data,
            service_now=service_now,
            singular=singular,
            slack=slack,
            snowflake=snowflake,
            trendmicro=trendmicro,
            veeva=veeva,
            zendesk=zendesk,
        )

        return typing.cast(None, jsii.invoke(self, "putConnectorProfileProperties", [value]))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileCredentials")
    def connector_profile_credentials(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsOutputReference, jsii.get(self, "connectorProfileCredentials"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileProperties")
    def connector_profile_properties(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesOutputReference, jsii.get(self, "connectorProfileProperties"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileCredentialsInput")
    def connector_profile_credentials_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials], jsii.get(self, "connectorProfileCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfilePropertiesInput")
    def connector_profile_properties_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties], jsii.get(self, "connectorProfilePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfig]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce6275f5d36eec9e8eac78591573ac6a29ced4f9a80c6c3ea5c48c7ce4fbcb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppflowConnectorProfile",
    "AppflowConnectorProfileConfig",
    "AppflowConnectorProfileConnectorProfileConfig",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitudeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKeyOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasicOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustomOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadogOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatraceOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexusOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshiftOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentialsOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNowOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingularOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflakeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicroOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeevaOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitudeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2PropertiesOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadogOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatraceOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalyticsOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycodeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexusOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketoOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshiftOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforceOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthPropertiesOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNowOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingularOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlackOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflakeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicroOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeevaOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendeskOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigOutputReference",
]

publication.publish()

def _typecheckingstub__d7932c1b6772439701692dc70f9fddcd7e9ff721d12d8e17bfd7502fac31ee35(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_mode: builtins.str,
    connector_profile_config: typing.Union[AppflowConnectorProfileConnectorProfileConfig, typing.Dict[builtins.str, typing.Any]],
    connector_type: builtins.str,
    name: builtins.str,
    connector_label: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__eb318c99f54a3757432aa88de16ef354922b52b6f99f0a78de54d01034052a25(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9a8fefdf026dde94050def4ecfbcf5fd22da6a18844bb8b39865146e8da6c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad5ae364b2e9ed147d7ea802b1ff6196865da3680cb6dba5576adb27ed54fc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a658560f8c79d578f7b2cebf8a5268921fd27b8578e42acfebcd204f0203e584(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf4a5b8e74ebeeb9304c90bc374754c469b287c68a65c77d196f878b4970d8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9627b23a7f3b815646dca371e037e66021d8e7bf0d23c9de80dd9fc00b0eb7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f9fcadf2afab16bf5f1abd9dc2e2fb784b396837e6361c6c15b349ce8be2c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758bf6ef5c6ec875cc2da666dade386b4e223fd401f327107aacef55fa85bae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76871d01a63facc0ba5a31b7fd2e0c7674b463828a372e85d4e9b1451ba8fc93(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_mode: builtins.str,
    connector_profile_config: typing.Union[AppflowConnectorProfileConnectorProfileConfig, typing.Dict[builtins.str, typing.Any]],
    connector_type: builtins.str,
    name: builtins.str,
    connector_label: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86f40ab517f594cb0f99b4f4d1bf12e05f637d396c85805a7119c73a3e7b1d6(
    *,
    connector_profile_credentials: typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials, typing.Dict[builtins.str, typing.Any]],
    connector_profile_properties: typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087e7ac33bc41e8f2c913afe8a5b56be22933119fc2970d88275abb572ed5d25(
    *,
    amplitude: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_connector: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    datadog: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
    dynatrace: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace, typing.Dict[builtins.str, typing.Any]]] = None,
    google_analytics: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    honeycode: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
    infor_nexus: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus, typing.Dict[builtins.str, typing.Any]]] = None,
    marketo: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
    salesforce: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
    sapo_data: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
    service_now: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
    singular: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular, typing.Dict[builtins.str, typing.Any]]] = None,
    slack: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack, typing.Dict[builtins.str, typing.Any]]] = None,
    snowflake: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
    trendmicro: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro, typing.Dict[builtins.str, typing.Any]]] = None,
    veeva: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva, typing.Dict[builtins.str, typing.Any]]] = None,
    zendesk: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daac45aff60f6e9f4da6be4f4e63968cf7921761437b03114aa7b6aa81879556(
    *,
    api_key: builtins.str,
    secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f05f24951f2a6cb607117299afb5be1243d6b3cd43336eb07e27afa73eb000(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f59d3d888beff92b0eccebf517b5615003bc565738b82e6d52500cbcce59607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07d486939cfa76635f7863457b3699cf2d2d0b7136e0434e7fb267751a222a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450d72b31da0645392ff50c58ff20634656e252187c739b2571e3ed5998b8182(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9448c554587b89ed2fb94507a4f66f45bc8d272988793847a0415bd91e9257cb(
    *,
    authentication_type: builtins.str,
    api_key: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey, typing.Dict[builtins.str, typing.Any]]] = None,
    basic: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    custom: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf74636ff5e98dfcf8307858d09bfb825f450a1330756406c2d9207a35e4c0f(
    *,
    api_key: builtins.str,
    api_secret_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98104156c8720c1e9f5cd54347bc425d5620cc3b7c293f6f4b6a550bfa7c3cdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10033de67e5e1e4f112e66fcf57e411a508740126b4fd16167cc0d564dff24f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981183b29fca36db1061dfce2136d0693a459f6963361f8c13cbba263aaff2a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f677107723fe180afb4054261a6136aad936ee11684e537d52fe0450714f51c(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44ba35fe9999e0ff0886bd673900923d8da2024777719401e4287fd8710b055(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896e2e8c68e38632af01d4b6bacce8ee3a4741fcf1b81b09d6b873c611fefd1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8216f68e1963552b2aa4fae3d7337f32813513180cdef98f138897fe700cc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735ddcf38ab7465e1c3d23e08f2c1ec1e9bcddb16072aa7de1b720fe71a10056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5661da20cb807512e9944449afd85cd6c66b4ebe816d21e4618e5db03a67be0(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad5d934ade2f56f1ad79f32cc4c1e5b3c080581887debbf9c528e07ca3bb718(
    *,
    custom_authentication_type: builtins.str,
    credentials_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b1c5c7c7ff7966a6582a78c184dd845db8078e4469c44db98c44642db1fefa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05ef292512dec9b83fa18ecdd37b01a997708518d989b40e9dec04934eb005a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1a9165b433a1109aa25cd93d50e2f4618be3943496056e2a45f908e3d7f0de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d6baa86a33d6ef6076e2528949c24b7b58a90d93f78cf2fcf3ee324b9024a4(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243d7ce8fd12e2ef55063cab9bb5786cbfff044d5aad148b7d6deb49c53fdede(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bf702950685118540db345c0f2df5c85db6e84d77574b5eaaafbaffd9123f1(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4480fc1077329e9b43bfe00107b192bdb409633a7e37ec8027dc693c0f6283a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3fdbb4c4a48590839e3de9970bd05a6179984c8a578b0480f0ab88bc0734da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b40d435467a8538ab5a05f05621d3f3bc57166a685c73a6dc3f6c4ad337d3c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811e313200558387a8abde090732025d47b897b3ce502624cc43d91cd2830a4d(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f064bc3ae448ac52a762e5479066a7140c2235ee057c3028f3396026c76ff4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619ddd3d95929fd0b52c96644dcebe54a4824aa854bf580bc1d55df25d8f7dad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9238859091ff40eec7dd849d6c8c14b9a976ee2b602f7abe2e88d5b74d2b9c7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf06c31090ee62700d1ca310012c83573e16247239e9bcce97fd8b51c671976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065b2dcf7d5968977ed0c405e9ebdbf13bb1c73e39bd6e5436ddf859544364fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7887ea11509af1b5e9fdbe3c9bbdd9cabe54826fbc45dde2f3784c324917700(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3202e72ac941ebf04eccebb7adc2751f5240e57b70c1368f1c4dcb1f0fe58797(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fcb957063d1ecae44e2999059bbe4a34f20fe7e2c7d9a71e947a822b45cbd9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abc58f02b032f0238baf04170563e7ad3cd24e3b2d8f44120566a0ba18ecf94(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8a81e80cef8b1b900975dd61a7fa9023ee2687e0d920f11042dad74efedf18(
    *,
    api_key: builtins.str,
    application_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08cc9fc21a4a3263d0579dd3efa82935e62b7d9af7c9ede5d4ed7b831ac93ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11684cb7b8d8600d05a189ac7ed1cbb8bb40016fee064c3ab4fd70967d80c2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de4f7c4c1214b811eac14ccd68bae73ae43e0e3963103f4b81ea214bf024a6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f6a7a81938e42866037fd060e14875a88ffe15969e915d3b8cf73f52539310(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea78e8c5adbdfcac93dcc101a164d402ab0b22e5d0912e43ceb00dae0e206ee(
    *,
    api_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf567104fceb1bd90235a02ef4eeadd84294cbdcf35c5ff355966baacb31d59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1600e3dcf3de16f2ad45630532b3cba7a07c502e19ad342f9718e8d2e20568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229239659af41080e0f03b2a56448b904fe7bb5cc5b156c127da5ec89e938f3a(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42892be567cf48a023cc79ca21f635438c5078227243c42e73be78bf311801a(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fd78ad6f72c6d8249533ac7c9d39b5245afb218129bbfcf5ba25003185a702(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae09ac3aea3e432a18bf78120a9bb21dd3f965dc2acbfb5c81d1a96f805b4cb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff12c4a1cdeab3b2397d9923a1f65d040c3df24e1ef6a3efbc34c0fba7a1dd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe2445746a292b4c029f99e5c8563f159acf7f6f0dbc0e8e8909da87ea06c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102cb4fe41e1924617625174d23b27b16213fa98d7576c9b5a1e1a5fccc124d5(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4866028faecc93f993a3e9e0e0a6423785ee8b9afab076fb574ac8563f9ced(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b7416f805809377e7b24c61ca9061c778c17f17631e9acea9aed36ab31abea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f4e7f1cb644d5f93c6aa6bdb0bd5db540c6aad4ff655b167b23e496f418478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029b2d6970ac2a3d6fb805811856ffa526f3ab8084e028e3c72d2acd68eb563b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5a3d409adb2272425dcffc1c478da5a0cf3fdc7c0bfe0c793a54c1989c1ce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2498869056caa004a5322d9a5abdd001bc56e6cca166a70d41ee27499d5a9f06(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b027a3ff48a7ccb985184b5a42e3de482d8fceb4802a513ad880a81d3447782(
    *,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5940623c76c905f519db4096b0066f6306a112b457ef35cc7d9f73b28c2758(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cef275e4ebf9a424dcf5b1b88104bd6ffe6ab124895f9e353745b8d9f6deb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b50000d1500f702f4464bc246bdd96e92b3b4461d52ff02bae127d995475447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795011e872821007fb04aaeddc6af9b015800bb7e3d467c33fde0870f98ffdf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379185ededf2f372455faf01bfe2904e42ab16ab47e54fae64e3d345f939d282(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342251015321e3fa509c97ae29babd27bc611039f131861d9961dbed239e190f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37853a7b6c645b59d011141853a846861319d9db12f40cce9e06841332cdff09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8561478a9e013d06a0eae187b84e0fbf7de18f73c12b1de78c729a3f927f067a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77b9ca12f8fac1d640e565f34fb42bb88bc1376e76c6b1fe65faaa4630be8f6(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f15d17b43e6419e2ef9888321c0773f693942e1f139e326bb5a341bdd3b75cb(
    *,
    access_key_id: builtins.str,
    datakey: builtins.str,
    secret_access_key: builtins.str,
    user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe5b72a823f10e4c3ddd9a0f86d0728d968e5d2d2aa49d26a13be3bf28a2d49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276d44539444a8a43220e7afc1550c69f16e59f10d0dbac6c996acbee1cdde0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38572042bcfe84f2b96b60041366efaf269d61cc727184554cc8eb77ed01feaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3befbbc2ce1877ac62d339b696241b29ffa49272fbc3b977a460c9b177933cc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba2a96d787caac1b7c2d88528adaa000f95f07e30fab0590d1b63be9bd21688(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568ecd54ec04ba95c73f933c7a57b0372e285e91bfcff90b36b453ff2976d1c5(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ca600ee3c0c4b4ca2053e7f53b1de275af450e0528a5a565388f8152803911(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0a91ee2fb257b478659c1691fdaaba6d462aa1b2fe603af28ffd52dfcc7f9e(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac9fa73e1d07fa7040660dcc72d1570ff0821afcfae816f46eb9fdfababb724(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbddf983eb956d5499d3e0cde84a17c10cda6c53455de01839c8152fcdcba7e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35849f0a3176884ab75dbbf3922ba3795307fd37aea575694de053464ebd4d28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd0fddecf1e9936ebeb7efa2d3d92b9ecdd59fbc801b0bcaaeacf4ab5225787(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87737e88bcebf7a9dca5c777742325c6ad34de48dc4c6d746fce01e9c4047e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fa113b55b4686c0118f55647407ac2a03cad02255b51ff4a09586d8d3bab08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124ea5466956be312de5bea91d3040249502de260baa8a323042797330d57689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1adc7a3160246d280bbd99335a994c14d55effffc852a3a3b2d0c8a69fd13a80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0250ddcef5ec0ffa485aed4ea57e677998d8412fabbc7c508ef1c5d60dc026(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820bc7b85817e0b2e7ca480c312e7c354726006f517a6cb1516c2fb97492628b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c01dec191c5a0e0670ad44ee6667b30a5416ee94386df46a515bbb259c5c76(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51afc302e6b7315882b2b954d4ae1e858be835009de80c281688950427a39f2a(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272ea5a4cca340136c4ddc07617e6cd999bd0b90e78f94ce85641899e16eaa8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b067298c303ca6e87de9566a7a2ce972effbce3ae985427a0ee6696b4fc28b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95cc46577fd0865eae626ab4bfd9d7bf2605c9ca10d9d2f8a3c59f989c43f630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc138a8a681babfb715d09ce2246ecd29f786d97091419e50cc17f77c0b8983(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184c6fe339cce42a0485a6c9e71c227aab73762204285c04ebe9dded47e2d258(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_credentials_arn: typing.Optional[builtins.str] = None,
    jwt_token: typing.Optional[builtins.str] = None,
    oauth2_grant_type: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0de1e46bd3b966adb8f092d7ce3f65a3c8523d0c987dce1d216c0f258a412c7(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591d66fd0656d7193a1d01e4436ebd2c0ee474cecd9a0f81ead0a50d25030ee5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9215ea439b80ff177e8cb71cd00945935e49c99c9d7332c02a986ff71e39d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4924de2bdd011779ab7d099122be086890b28f81799fdf095a73554fc06d9188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ea2b7981ae621dedaf6c8b825ee311a7e04f619d5f77f92d1cc304510690ae(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb4e59e28bd37bc9c05ce53d6012080054725e63f408c6ce67e3c484e6eeecc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec0aa4ebb9efc27816aa30f98d226f54b6820afaf1f0565ed6f68b1cb376035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834fac8fd8ecce049ba0232240c50c09cf92e84b7c2b4b8b497d82da710d240d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c41318aa837e83a097b0e5d83a0bc7337e3d694e6966e686c183ea803adcb8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336afe147282279ac3dc4060243895355ed7a48e47f7f25f6dbc89b4126f31c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a1aab707b9fc9433cf7da8f244b824d5a78420f33570cfd8242b09a697d572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796faf572c6709abddf9f23323fc42f06d1f4fbb8230c4a1ebcad0a08a68ef7d(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bde2c3b7138ba3a2f3723fb25aa44f3a5f40ed51527c822659698bd6eea5b5(
    *,
    basic_auth_credentials: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth_credentials: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17765fe2ac10de1528c5d1d2816703bc20fe155d15f0e972728c0c5ae2e50dc(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68d56fe8260979c500c5b1ae049a83c641bb946632b64e1222eefc5a200bb1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd86f45c4a908229c9ffba1a7b561cd6483bc29db8f4234616267aeb6dff1dca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8a7301e8613fc311e27d7a3941394faaed9ac31286734c5d97c459a0fcfe5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8288e33b03561a92cf77bb158651cd002a31f29de9ced6327718614472b6bd51(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cbcd0732b5602cc0ebb01031fb99ecfec90f275bc0aa49d57d84184efa43a1(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70fa768cee692a51a11607e9559a8eebd17380f07156e1257b7d5d2ed5e2f48(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc55a8d83edb0218bf1e37708874d8e03df0312e755947a593898de5f8fc0b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6587acd564c661a0716becacbd4017ae188d34386b915f5903c13ef0716850d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4727aeda50ebc183ec4dc175fcfacad3c1be747a579e8b2e23921f74a829ab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84826935c439cd20e35142248c97474b388f642748db405dd7ef2774b7a52d19(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceaa1f253d892aa684549321d1d6878744107c212369180b4dd7e047ec60181b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a65e72796e2e7ed7aaaa35d3dd221eab3bf2805d3b23c67ddda3234235f437(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ecb9cee757519061765bd064511fd51f402ad3c57a73c91c9878deb1acaad7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c72c323805bacdaf34a78cf1c8a1c9ee797ccc080218f139034c89c83678bf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430b2cccabba307094733525d2e93ee19e97733a780bfd95f77dafd341b5a031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8bef0a20e33a2b3f7f8075e784358afc0c665468d20aef5af1a1b3bfee29a2(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c10680288c1767fd4f108def5a464f38201d318aa06d8222c48abc210f0d313(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5df427e6e40da103480903c8ef2bc234990cd67beb4c82bebc402dbbb4a823a(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036efa852ad732250f352038cc32c37d38e5d4f3520320721702ed854d33100c(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374a7ac1241dc04c4325fce225d4e0246b2d538c96998719b0b0ff093ae7dfb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308c89dff9e484c57356d39541b2bda651b99255b8d4bf1d750ce47d083d618c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281a05c0a0a9352b077465e125e9773087c00b07e411b6f212df07e8f8313c4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ddac264191d756d0c05f45771506145d08354a7e85091e428571fc3bb3725a(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dba0dcbfc7b561902d6734b0cdfd56fd1d6039adaa41b8b96b399386c1c58b1(
    *,
    api_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297665aedaf1434aea0e8ce1e52ca0204941c06b1875c6c3e26ee1877007d452(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecf46edcf6b6765ae086b4935014368de8ad479c38f340a4397ac9b12cc0b13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78af1965f36f01e1506439d3311b9d3d6c105a4d79905ba85c5bf77066052b0c(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4726a79ca0c4868265c2512432032b05df8a158dcaba71aa0e899b6b424986f(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a0fb65150d4cd5fddce008793504ef6adbdade82b4565396e83c86f2546cbc(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660a107ed4ed8cac0c2064d48b34fc90cf50fdf0f63a10abaef9632c57e3c932(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27eb1b71b92ae4cfbb940b8831d95b75de18cc3bb9a5ffc6fdc9cd17c8a5d0bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3f00e5a06404b7bdbc80d86ab4de2bae9340db4250986992a51a58fdf0f072(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b78b5403775ab07409a5cce6907908ac0c2d0e9771600b93e231da0d306ae52(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1ce0c652e762c07d1a700239808de4829dcfeb734a2761e2903cb9619a3b82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe8f11a6652d66ea449c837eff813276d5336f6515560049bb3053742f6dace(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a1fb8a01386286d3ecb439efcaa2002a31a07a566b36411eb3f29e03475b92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0314991a6b75d682cdb1fa78f0a92539823b92c6a52258ae6daf14c939fffc87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7085110e5c19ed230cfa1b38a823ca4a4f6e69a15ed70c451e56a413f72158b(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc11484766db602068b08a2680632fb5f9c1ac83aa03789d4be484540bd0e6d(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ceb4c964f4554ad1cb9a2bb49653f99f760c5a401b54d5e13e74569948b061e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737e922204be835acee08b51ba703fe541b3850ee6d7f347b679b098fa5ae3d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daae8b93a9220088880d0d51334904b2a2a744294402b6a2c53b507a3ab95eee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__092f5e18f5152bd4226e5291ddebbfe2925bbc23ae57b2c3419766bb2639f8ae(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4a8a468647c04d33600433740307a236f5e3e256392ebeed9fc73c96ee500f(
    *,
    api_secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea1b0590db77e32bb29761421cbd3f79860d577349b5819e5d03e600b19d655(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0455327144d9ba08f38f9793515d6d45d95306789d5e930dfa8fc9fe5094bc2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef2893ad43417e0bd8067e08a483826d7216091f7715b6dfef6fbd5cd1bf9c5(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0786144dc59bbcbe2dcb842c6f22ce022b0f5b2ca46f19eb7c8d65e68eaa8e8f(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b3c930b7cbb3ad77aeda10e88204b30030aaff60a30d1f6483148a97e587d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3e5be5c089317df62198a8ca2232fe2a1944c37df439c25bb4a44089a9241e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3199daa4a71b1a999f90eed0de89968f86197dc5cf751b4914bfd56af2a537(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b18964d025688c7265581cac569100d15da1646cddf5695948bcec747d09b0(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b573fe9b732bfc57b725a6c59128d288f922a480e46919a0b708ca351de9213f(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40004efd6419d0bc841659262ba83367885f0b1df6cbfb2a67ef9e791e238aa(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d59ddc6735ebff542d5607dddfc8f0330fee54ec83fdef74358c0c72ca939c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79bf0609ab721fc733099bf108862b7ead22910036850eaec6ef25a8275588ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbff5c965be6b98547d94e70076c74708a56155f86e5532fbf58045fb1d68420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04848c498149d6e47e8403bd5f293fb0c31abe6f35d4f676370a05b2f435314a(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e665721fb24be7ae5eb67894a11960d9bd2f75165771558e16e4b0e8fb45e292(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68576c6faec5601179f3c80f629321f8f5a6a3baa97afb3fc0c6d8b156a17d84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0d307f172c7be60f25907d1ef0ec620e8bf1937fb32873b0f913ddc16d6c2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49dab2733e4525cdadcb29853a3bf3c70ffbda31ba9dd7e8167c5cd572f3f013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83499cd1661c7b700eca6f7d0b048a9ddbbca7f0f5a351ed0e0c8343a475e17(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4e5d400c720b79aefb9b39b08feabb212b0a1fb37891556965a2b2ec2adaab(
    *,
    amplitude: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_connector: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    datadog: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
    dynatrace: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace, typing.Dict[builtins.str, typing.Any]]] = None,
    google_analytics: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    honeycode: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
    infor_nexus: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus, typing.Dict[builtins.str, typing.Any]]] = None,
    marketo: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
    salesforce: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
    sapo_data: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
    service_now: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
    singular: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular, typing.Dict[builtins.str, typing.Any]]] = None,
    slack: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack, typing.Dict[builtins.str, typing.Any]]] = None,
    snowflake: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
    trendmicro: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro, typing.Dict[builtins.str, typing.Any]]] = None,
    veeva: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva, typing.Dict[builtins.str, typing.Any]]] = None,
    zendesk: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9497b9e495174b3c0a065d6bef1f6ee0561f7aac88da82a3c88d78a1816520e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fae2d2a47e02b9a1af4e95be92377051e71be39602d6b8e17f51ea172e5da72(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf9a42a115d28ad3fd920d399a4f8c1a27b393aca3309868fd4260cc290ff74(
    *,
    oauth2_properties: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties, typing.Dict[builtins.str, typing.Any]]] = None,
    profile_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c506516a35c699cf61b0ca3ed264366da733e84cb1f5fc180ce029e76b3927b1(
    *,
    oauth2_grant_type: builtins.str,
    token_url: builtins.str,
    token_url_custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddee0000f9b94ecff201a9b48e73fc85e0618603d5ba0eb606adffeaadb6955(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01423bd838ec06c2434c57f3992e41e4d7deb170948b8a6ed4c83201e251315a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561500396444bc69b710f202d8ac082dcaffb6f31b3bb8df1cdb5b52614db18a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23c0ea652084eea5550bbd07d839b22dc935a6c7efe76386e12d0410307802a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92346172df64a83f6bcc27570eed72290af9bb290685ef850723ca22ca09ec8(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42aa3bb900a30675bf00e36c9d4aba2cbceb2277ce74c9f05c218381d179dbc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f7b8678e85a95f1f3f44bb2d1879ed9132832f16e9a356f04614348369d485(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3aa9ac7926e657329fb778fa241c0a689f1766690538942ec409155f46bedf(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed1de928579847c9ae24703355f2414417b5938e5a3c00b57bae26197dbdcdf(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c289c9a7c16c27eee0ed8a6b5bae346787f0e727e745f78f4895631e566e98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43f6250bbed1c5e1f8f8d2016329db5f5e9dfda02b244a5b227140e2af4fa06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3ecf5a5ce8d0a6e6f7c984017bc99a4e942dd322bcf887e13a95526e559f90(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de26e619fdb15c1ffabc1b125166c32d73636eb449e9d19d969232cc7596e179(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9228b3ce7ed3100b00e3902b0cd8294596b1ccf4e5330b998068cd67a88a5d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a9eef18acad32308490a81492f816263210743c9dfdb0d743b45c05d2825a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25dd0cc1e421623a940db53f5783dbf34b754b35408e8623872bcaebd4739d4b(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85541698bb1150674451ff334ad7a374d1794cf29bb4bb44350195ae8f2c885e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc0bdeb661cb0d08d39f29cd3c8a0e085c0ca2661dc5bcd38788de12e02db79(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a78e43c4d989d9a927b01c2f9ba7d846f50d4f58ca9581054d666e26c7cbfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9981b313b275b6a2271485fa8520a033d14a82dfe7f06bbd3c034dc6a67d17(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6345f6d9531ac5c8f0571e1330b7554f9f93b2cd784c4d054e57e6d6f5feee33(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb9aa6523905d4eb571c506df888dd018fa62c839b3037506f86c1ba90da36a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238b9221a545467b8dd646b7a9037e2cc505ea175a4e824a3b45eeb86cff28e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c303aa8c6546886333b3d1cbb71fab38f14182a86e061fe695da0cd5d52e416a(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca12e1672af0e16129e71ed2592685ae5c6f92af6c3b10879a87d51537bf6e3f(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6710d7b26a9af468f7a0f075dc198135ea571ff32faeffac4d410ce5bb3ab2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fac749e8bc6e0abaa54ecfd11f230547d5a0f84daf21171e8cb939084be3f93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c1d837c87c419f25ced8ccd9d631ae44600394c91046df6ba8216a39f6e804(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acf8b6c1af69e6dfd6c391c94589aac49af1e1cdc978547e31876139740154d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c33009615600cbbc908da9dd73ac08cf53ef3b26a95fc38f64cef7401632976(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba56e7832ef3f079572d94516ec0e7930f237df3af971ad05b4d444ea9e9993(
    *,
    bucket_name: builtins.str,
    role_arn: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    cluster_identifier: typing.Optional[builtins.str] = None,
    data_api_role_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    database_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7c473b51a4cbbcac49a340fb86dc9a00d0de9bb71afe2a3f6f0d71c31216b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b9dcb137993b5c08c9ecb8777a33a91532d9d267f73bc40e2e3a63a3349d7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38e8ed6e7fe3101686afff6fab888748aeae6548c58588c90e0ec7094da600d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9589a4040a575d51f2cf39cb694d2daa156831e5d5062dc1f5d042c414ca1db5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ad97da85fecc1b68ea50b4de22cc203b91ebeab1d01d2da4b44220d6579498(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee41bcd1bd4cecee3d98f7de3485ca4430294dbf596b24d7cd765b98494f1a5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095eee0116b1c70929161bbbe387836be5c802f7377ad2a6c625bee3f53d9f05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818d8fad887ff7592127dd8ab93511a1e3721423b7119d88a9d8d13898922f63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10f232fc4e7bc7959aa81749e33d7a36cfeb772123eec887d546672297e93e0(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d835ad017372d7074864a69fa58b4b1db91271ece95ef68a3882fa01b2186178(
    *,
    instance_url: typing.Optional[builtins.str] = None,
    is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_privatelink_for_metadata_and_authorization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7693b8cb15aee7d0fcc11572737749adde16aaa2fcd5a34acc8024fc155ad82e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2ecb07d943cac2f8d9f9aca90d68480b61ef79d4a610a7ca139e2301cc76ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda3b8b450caf6e76ee0a73856cd6a8243bd73df20d20fa07459ab675db6be0f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e806d3d37e277abbe26852dad8d184daa8cd3c4ab5cff5f023257fe7f99d292(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8615968fe1065dc346cf7da61b4a757e0ce4a7276579952931236dfbfd680f87(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdaa4135056120302752c4c1ddf20108c046aa87f221406d215b28e9462e9dd7(
    *,
    application_host_url: builtins.str,
    application_service_path: builtins.str,
    client_number: builtins.str,
    port_number: jsii.Number,
    logon_language: typing.Optional[builtins.str] = None,
    oauth_properties: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03891904b42202a9191faec3434cceae775f328196eb56954bd275b0e142c450(
    *,
    auth_code_url: builtins.str,
    oauth_scopes: typing.Sequence[builtins.str],
    token_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f04e0b8a76bf3a442f273a152c28518e0d58bd699e2ad4dd37831209e2fe9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300666d35f9324429440cd87f1cdfb97cf15ee8a47a6baf3b4e98a2128a48ba7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5b319bef4b7836ba59dc4867afc08bfd6f9da5ef64fce2fe2eaf5997db8b38(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdaa9ea62d58ac8f8afce18b37fb13d2e43a56e644557a83f33b19e8478025c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e349939836a96aee263a1f951f36983ff3da8b36f26cebbe9ff66644b1247bf(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e91263efb7939138067c0c2344b92ecf0e8f1839f8abdc07fdc4e0cb94fc35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f2451a40db127908855be19552fd96e156620cef80e27db8297dcf88252248(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4a00c3363d4272ea6331bb808ca35e0c25be5250e6f9b2200834fdd369c1a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9614302c3b105e7b1b26938ab6aff6ca4cdc8e660ab0f58a5c5cc48d46a6483(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865bdf783a9c906b41fcb0ef5880093c17c654974f463214c8725d4d1ee04e34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd6bcbd9442faef142f55f5fb44f7d9864df84e9cb40795ceec3b1d754bdd57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcebf5eaa7708aabf743f169b1e9a96664ee99430603c40d84890b02108ae04e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e312df27b6e6aea47b71bd09c59dbb4fdfecc26bfc38edad17ae36a1d08744e(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f230275cad2652c74b622cf917e7c02de77ddc176618a0ac2ee942e21af84678(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9482348613bdfe1d3c9612926cdacf7082316951c8c0c95475316a64b0a14b28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3d6848af7ca00621cb507904a1d38086b43a49a45b10afedc0de7fa97045fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8556af2be76b4e3755be79889f6f006b351a12a67df2a0e28a230a5ef727eee4(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2c26cc51570cc4b4cf6b849533ac8dce0f602fa62617522132485a2f832ff2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7675605b7bc9e673c961c1611cb9ba516405b00aa4150919d97480ae1df159c4(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebe0efe52d0edcac46a36d9f7895c68ccfbaf0461c2f16b9747142ccdfbfd41(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f33aeb9e8653cc205ce0d83a1900d19fd3a4d811b452ca49671a6cae9ee17e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c93b0e0d24a47364e9a8ff6b63b876b5fa70a471d0c808d9ca71292a2d60c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bc3ac607f108c4c7526dbb055d13c134c2ba1d62bd46cc79a306feb7b941bf(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe532941e05f415265a2813d1514942f49903800c6c5103550cf5f0d2ba9976e(
    *,
    bucket_name: builtins.str,
    stage: builtins.str,
    warehouse: builtins.str,
    account_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    private_link_service_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ecdb0a27361a5c465d50e0dc01f352e6b38b8a3d12151f781c5ae6bb80979d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd1e91da1203b4f49db8831d43d597c1a7c9cf4410fdbd6a00b6c1e731b72c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89faf10037d208b0f51cafd3987724a069db28864dfc253edab709fd1e2a8e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20da9646053c98f6e295604f473df1af5c6a0c3e2d341dd00146ea66e1c9f4ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4460213380fe716920b96a39caacfa1c5a5894779ef20b1a13a8267f6d378b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb72a80bb703ab2e3bad541735319d1cb9a88693266444972f4dc75f0be3246d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f838c0abaac1d03053962302ddc7fe3937a561c20b663e29d973b99f9f11af0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bcb5b216e5d868ed204989086680398fb5d02bd66ae3ad85744aabd6cf4c1e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c396075dcfcab9980aecfb9990ba2d10c63b491a116fcd5ddf4e22045a2e3d7e(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba61a1d0c0e109cb8b56a93d580a05e7b7fab4d9258a90784b9cd23ef4df7bba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33460545fc3ec40f74c009d18e9423e84149f7d974059e0411ef8a7f05e3c60f(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b297be5eea6f88815e6bb1563ad669698f04788007149e035e4f9f1c23bf94ec(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da04dc4639c895ebf48fe3e9812d4bf0d0e7d75ce49029c3132360257fdf13f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babec7f4991f2c7cda1a0047e47a4d7d71b7483fa51cb86716597e6a12e0bbe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68f37cea9d05ab4480e04ae325c88e51a540ef7ce4719f22efda2662ca6a617(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1861e56e6d8c60c5f05fcdea64e199637121015049ce58d5f9bb011a3ccb9ee5(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4328bb6d49ddcdf36c8bc1054ee2faac8a943ca5665655ceb4e6676b41b9d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3f14f3dcf50af15dc3860359ac26819cc114db41c603994bed3e29afa11e7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2bf55123232670938f3d86d03e18ba72af33750bd88d6eb112139bd0e3a93f(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e06b370ed8bda16e5663b704e2bd4769889f53b41d4911191f04b5bc43a2ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce6275f5d36eec9e8eac78591573ac6a29ced4f9a80c6c3ea5c48c7ce4fbcb8(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfig],
) -> None:
    """Type checking stubs"""
    pass
