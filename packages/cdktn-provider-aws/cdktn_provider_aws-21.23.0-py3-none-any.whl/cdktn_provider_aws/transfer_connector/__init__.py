r'''
# `aws_transfer_connector`

Refer to the Terraform Registry for docs: [`aws_transfer_connector`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector).
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


class TransferConnector(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnector",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector aws_transfer_connector}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        access_role: builtins.str,
        as2_config: typing.Optional[typing.Union["TransferConnectorAs2Config", typing.Dict[builtins.str, typing.Any]]] = None,
        egress_config: typing.Optional[typing.Union["TransferConnectorEgressConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        sftp_config: typing.Optional[typing.Union["TransferConnectorSftpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["TransferConnectorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector aws_transfer_connector} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#access_role TransferConnector#access_role}.
        :param as2_config: as2_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#as2_config TransferConnector#as2_config}
        :param egress_config: egress_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#egress_config TransferConnector#egress_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#id TransferConnector#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#logging_role TransferConnector#logging_role}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#region TransferConnector#region}
        :param security_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#security_policy_name TransferConnector#security_policy_name}.
        :param sftp_config: sftp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#sftp_config TransferConnector#sftp_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#tags TransferConnector#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#tags_all TransferConnector#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#timeouts TransferConnector#timeouts}
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#url TransferConnector#url}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c37bc1afbc6700ba6c5df0076d7d15950015ab593dbecc9431ff15282b3835)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TransferConnectorConfig(
            access_role=access_role,
            as2_config=as2_config,
            egress_config=egress_config,
            id=id,
            logging_role=logging_role,
            region=region,
            security_policy_name=security_policy_name,
            sftp_config=sftp_config,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            url=url,
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
        '''Generates CDKTF code for importing a TransferConnector resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TransferConnector to import.
        :param import_from_id: The id of the existing TransferConnector that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TransferConnector to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682301e2023993dc5b1352c6ce35bb2a4da1b8469098487d0dbdb4e0f1135705)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAs2Config")
    def put_as2_config(
        self,
        *,
        compression: builtins.str,
        encryption_algorithm: builtins.str,
        local_profile_id: builtins.str,
        mdn_response: builtins.str,
        partner_profile_id: builtins.str,
        signing_algorithm: builtins.str,
        mdn_signing_algorithm: typing.Optional[builtins.str] = None,
        message_subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#compression TransferConnector#compression}.
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#encryption_algorithm TransferConnector#encryption_algorithm}.
        :param local_profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#local_profile_id TransferConnector#local_profile_id}.
        :param mdn_response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#mdn_response TransferConnector#mdn_response}.
        :param partner_profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#partner_profile_id TransferConnector#partner_profile_id}.
        :param signing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#signing_algorithm TransferConnector#signing_algorithm}.
        :param mdn_signing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#mdn_signing_algorithm TransferConnector#mdn_signing_algorithm}.
        :param message_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#message_subject TransferConnector#message_subject}.
        '''
        value = TransferConnectorAs2Config(
            compression=compression,
            encryption_algorithm=encryption_algorithm,
            local_profile_id=local_profile_id,
            mdn_response=mdn_response,
            partner_profile_id=partner_profile_id,
            signing_algorithm=signing_algorithm,
            mdn_signing_algorithm=mdn_signing_algorithm,
            message_subject=message_subject,
        )

        return typing.cast(None, jsii.invoke(self, "putAs2Config", [value]))

    @jsii.member(jsii_name="putEgressConfig")
    def put_egress_config(
        self,
        *,
        vpc_lattice: typing.Optional[typing.Union["TransferConnectorEgressConfigVpcLattice", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vpc_lattice: vpc_lattice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#vpc_lattice TransferConnector#vpc_lattice}
        '''
        value = TransferConnectorEgressConfig(vpc_lattice=vpc_lattice)

        return typing.cast(None, jsii.invoke(self, "putEgressConfig", [value]))

    @jsii.member(jsii_name="putSftpConfig")
    def put_sftp_config(
        self,
        *,
        trusted_host_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_secret_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param trusted_host_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#trusted_host_keys TransferConnector#trusted_host_keys}.
        :param user_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#user_secret_id TransferConnector#user_secret_id}.
        '''
        value = TransferConnectorSftpConfig(
            trusted_host_keys=trusted_host_keys, user_secret_id=user_secret_id
        )

        return typing.cast(None, jsii.invoke(self, "putSftpConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#create TransferConnector#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#delete TransferConnector#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#update TransferConnector#update}.
        '''
        value = TransferConnectorTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAs2Config")
    def reset_as2_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAs2Config", []))

    @jsii.member(jsii_name="resetEgressConfig")
    def reset_egress_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoggingRole")
    def reset_logging_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingRole", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecurityPolicyName")
    def reset_security_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityPolicyName", []))

    @jsii.member(jsii_name="resetSftpConfig")
    def reset_sftp_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSftpConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

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
    @jsii.member(jsii_name="as2Config")
    def as2_config(self) -> "TransferConnectorAs2ConfigOutputReference":
        return typing.cast("TransferConnectorAs2ConfigOutputReference", jsii.get(self, "as2Config"))

    @builtins.property
    @jsii.member(jsii_name="connectorId")
    def connector_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorId"))

    @builtins.property
    @jsii.member(jsii_name="egressConfig")
    def egress_config(self) -> "TransferConnectorEgressConfigOutputReference":
        return typing.cast("TransferConnectorEgressConfigOutputReference", jsii.get(self, "egressConfig"))

    @builtins.property
    @jsii.member(jsii_name="sftpConfig")
    def sftp_config(self) -> "TransferConnectorSftpConfigOutputReference":
        return typing.cast("TransferConnectorSftpConfigOutputReference", jsii.get(self, "sftpConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "TransferConnectorTimeoutsOutputReference":
        return typing.cast("TransferConnectorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessRoleInput")
    def access_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="as2ConfigInput")
    def as2_config_input(self) -> typing.Optional["TransferConnectorAs2Config"]:
        return typing.cast(typing.Optional["TransferConnectorAs2Config"], jsii.get(self, "as2ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="egressConfigInput")
    def egress_config_input(self) -> typing.Optional["TransferConnectorEgressConfig"]:
        return typing.cast(typing.Optional["TransferConnectorEgressConfig"], jsii.get(self, "egressConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingRoleInput")
    def logging_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPolicyNameInput")
    def security_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sftpConfigInput")
    def sftp_config_input(self) -> typing.Optional["TransferConnectorSftpConfig"]:
        return typing.cast(typing.Optional["TransferConnectorSftpConfig"], jsii.get(self, "sftpConfigInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TransferConnectorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TransferConnectorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="accessRole")
    def access_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessRole"))

    @access_role.setter
    def access_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40403db89dcd74329814a9d7c05b7113e82d4a3a0b3b4deb29c695061d557218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101fdccad9438463933f1fe095b84d52866d79393468905db9bc93153610e871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingRole")
    def logging_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loggingRole"))

    @logging_role.setter
    def logging_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc387cddc61fcf34e20ab402fac2e15c6b6b56b040c2c1e7b34632a261e248e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfe7b2256203be266c1dfc824384631e394d31e1b4a7d2a06ec60d9b0382080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityPolicyName")
    def security_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicyName"))

    @security_policy_name.setter
    def security_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6995827d82472ab14f5424274457b1364541669276a42c479ee7d4c5377e2a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b774730b0215a42d12856713d39763e1eaee89b05815d39b01feff3bcbac071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad0cf7b34c71139289289465fecf93a9e84bb6b4ee796fabf8f13543607d544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac92c740dd58dc5098eb16388c1b2093599b9738f585d4d5b066539bedba388a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorAs2Config",
    jsii_struct_bases=[],
    name_mapping={
        "compression": "compression",
        "encryption_algorithm": "encryptionAlgorithm",
        "local_profile_id": "localProfileId",
        "mdn_response": "mdnResponse",
        "partner_profile_id": "partnerProfileId",
        "signing_algorithm": "signingAlgorithm",
        "mdn_signing_algorithm": "mdnSigningAlgorithm",
        "message_subject": "messageSubject",
    },
)
class TransferConnectorAs2Config:
    def __init__(
        self,
        *,
        compression: builtins.str,
        encryption_algorithm: builtins.str,
        local_profile_id: builtins.str,
        mdn_response: builtins.str,
        partner_profile_id: builtins.str,
        signing_algorithm: builtins.str,
        mdn_signing_algorithm: typing.Optional[builtins.str] = None,
        message_subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#compression TransferConnector#compression}.
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#encryption_algorithm TransferConnector#encryption_algorithm}.
        :param local_profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#local_profile_id TransferConnector#local_profile_id}.
        :param mdn_response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#mdn_response TransferConnector#mdn_response}.
        :param partner_profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#partner_profile_id TransferConnector#partner_profile_id}.
        :param signing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#signing_algorithm TransferConnector#signing_algorithm}.
        :param mdn_signing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#mdn_signing_algorithm TransferConnector#mdn_signing_algorithm}.
        :param message_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#message_subject TransferConnector#message_subject}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f97f3a2bdd88bf322748355d26d7d7bf8ca92c77e106b1e18e454edd4faa08)
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument encryption_algorithm", value=encryption_algorithm, expected_type=type_hints["encryption_algorithm"])
            check_type(argname="argument local_profile_id", value=local_profile_id, expected_type=type_hints["local_profile_id"])
            check_type(argname="argument mdn_response", value=mdn_response, expected_type=type_hints["mdn_response"])
            check_type(argname="argument partner_profile_id", value=partner_profile_id, expected_type=type_hints["partner_profile_id"])
            check_type(argname="argument signing_algorithm", value=signing_algorithm, expected_type=type_hints["signing_algorithm"])
            check_type(argname="argument mdn_signing_algorithm", value=mdn_signing_algorithm, expected_type=type_hints["mdn_signing_algorithm"])
            check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compression": compression,
            "encryption_algorithm": encryption_algorithm,
            "local_profile_id": local_profile_id,
            "mdn_response": mdn_response,
            "partner_profile_id": partner_profile_id,
            "signing_algorithm": signing_algorithm,
        }
        if mdn_signing_algorithm is not None:
            self._values["mdn_signing_algorithm"] = mdn_signing_algorithm
        if message_subject is not None:
            self._values["message_subject"] = message_subject

    @builtins.property
    def compression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#compression TransferConnector#compression}.'''
        result = self._values.get("compression")
        assert result is not None, "Required property 'compression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#encryption_algorithm TransferConnector#encryption_algorithm}.'''
        result = self._values.get("encryption_algorithm")
        assert result is not None, "Required property 'encryption_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_profile_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#local_profile_id TransferConnector#local_profile_id}.'''
        result = self._values.get("local_profile_id")
        assert result is not None, "Required property 'local_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mdn_response(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#mdn_response TransferConnector#mdn_response}.'''
        result = self._values.get("mdn_response")
        assert result is not None, "Required property 'mdn_response' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partner_profile_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#partner_profile_id TransferConnector#partner_profile_id}.'''
        result = self._values.get("partner_profile_id")
        assert result is not None, "Required property 'partner_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#signing_algorithm TransferConnector#signing_algorithm}.'''
        result = self._values.get("signing_algorithm")
        assert result is not None, "Required property 'signing_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mdn_signing_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#mdn_signing_algorithm TransferConnector#mdn_signing_algorithm}.'''
        result = self._values.get("mdn_signing_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_subject(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#message_subject TransferConnector#message_subject}.'''
        result = self._values.get("message_subject")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferConnectorAs2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferConnectorAs2ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorAs2ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d31918238fc4afb346923b3404b30e28378305f1fd507f451829da8bc862246)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMdnSigningAlgorithm")
    def reset_mdn_signing_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMdnSigningAlgorithm", []))

    @jsii.member(jsii_name="resetMessageSubject")
    def reset_message_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageSubject", []))

    @builtins.property
    @jsii.member(jsii_name="compressionInput")
    def compression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithmInput")
    def encryption_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="localProfileIdInput")
    def local_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="mdnResponseInput")
    def mdn_response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mdnResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="mdnSigningAlgorithmInput")
    def mdn_signing_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mdnSigningAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="messageSubjectInput")
    def message_subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageSubjectInput"))

    @builtins.property
    @jsii.member(jsii_name="partnerProfileIdInput")
    def partner_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partnerProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="signingAlgorithmInput")
    def signing_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signingAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222d624540dc83d438d575901d708d932803e782318799ddffb2e5878b036749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithm")
    def encryption_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionAlgorithm"))

    @encryption_algorithm.setter
    def encryption_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d680d447cb80b0ed6de3549a908ddbff61a14fc32e9b68b3987dc201434035ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localProfileId")
    def local_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localProfileId"))

    @local_profile_id.setter
    def local_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd3f00f39838be12a7ab3aee27bf770a04c10d68c673ec5bd6252af503b2fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mdnResponse")
    def mdn_response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mdnResponse"))

    @mdn_response.setter
    def mdn_response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b593789577d28462079b7dc13797f216cb98f299fe14b8074e35e847605d4cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mdnResponse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mdnSigningAlgorithm")
    def mdn_signing_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mdnSigningAlgorithm"))

    @mdn_signing_algorithm.setter
    def mdn_signing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63342063fcd284e75d450f6b6d8db0d5fa4e91829a21e97468e9a5544755f56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mdnSigningAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageSubject")
    def message_subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageSubject"))

    @message_subject.setter
    def message_subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756cd59daada743d84714bf5825fd15110c4286cc6ef69b49323e26cd430b677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageSubject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partnerProfileId")
    def partner_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partnerProfileId"))

    @partner_profile_id.setter
    def partner_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91fe3ad33b772e2fc23e1f8355bbcfcd9448df4e8bf88f53392f211dff230bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partnerProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signingAlgorithm"))

    @signing_algorithm.setter
    def signing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f738b5fa976cc1b0248f03b9387a9a607f77b33dd5595c846e1402457a1d12f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signingAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferConnectorAs2Config]:
        return typing.cast(typing.Optional[TransferConnectorAs2Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferConnectorAs2Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff50a627b107296438a5291e63063ec98bfdbc91282896e02db0299a62e2f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "access_role": "accessRole",
        "as2_config": "as2Config",
        "egress_config": "egressConfig",
        "id": "id",
        "logging_role": "loggingRole",
        "region": "region",
        "security_policy_name": "securityPolicyName",
        "sftp_config": "sftpConfig",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "url": "url",
    },
)
class TransferConnectorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_role: builtins.str,
        as2_config: typing.Optional[typing.Union[TransferConnectorAs2Config, typing.Dict[builtins.str, typing.Any]]] = None,
        egress_config: typing.Optional[typing.Union["TransferConnectorEgressConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        sftp_config: typing.Optional[typing.Union["TransferConnectorSftpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["TransferConnectorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param access_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#access_role TransferConnector#access_role}.
        :param as2_config: as2_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#as2_config TransferConnector#as2_config}
        :param egress_config: egress_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#egress_config TransferConnector#egress_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#id TransferConnector#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#logging_role TransferConnector#logging_role}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#region TransferConnector#region}
        :param security_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#security_policy_name TransferConnector#security_policy_name}.
        :param sftp_config: sftp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#sftp_config TransferConnector#sftp_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#tags TransferConnector#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#tags_all TransferConnector#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#timeouts TransferConnector#timeouts}
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#url TransferConnector#url}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(as2_config, dict):
            as2_config = TransferConnectorAs2Config(**as2_config)
        if isinstance(egress_config, dict):
            egress_config = TransferConnectorEgressConfig(**egress_config)
        if isinstance(sftp_config, dict):
            sftp_config = TransferConnectorSftpConfig(**sftp_config)
        if isinstance(timeouts, dict):
            timeouts = TransferConnectorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c4b811b0de2e8b080cc5a60a97f92d9f15d247fef1294e76d12617ad0fd07c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument access_role", value=access_role, expected_type=type_hints["access_role"])
            check_type(argname="argument as2_config", value=as2_config, expected_type=type_hints["as2_config"])
            check_type(argname="argument egress_config", value=egress_config, expected_type=type_hints["egress_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging_role", value=logging_role, expected_type=type_hints["logging_role"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_policy_name", value=security_policy_name, expected_type=type_hints["security_policy_name"])
            check_type(argname="argument sftp_config", value=sftp_config, expected_type=type_hints["sftp_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_role": access_role,
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
        if as2_config is not None:
            self._values["as2_config"] = as2_config
        if egress_config is not None:
            self._values["egress_config"] = egress_config
        if id is not None:
            self._values["id"] = id
        if logging_role is not None:
            self._values["logging_role"] = logging_role
        if region is not None:
            self._values["region"] = region
        if security_policy_name is not None:
            self._values["security_policy_name"] = security_policy_name
        if sftp_config is not None:
            self._values["sftp_config"] = sftp_config
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if url is not None:
            self._values["url"] = url

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
    def access_role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#access_role TransferConnector#access_role}.'''
        result = self._values.get("access_role")
        assert result is not None, "Required property 'access_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def as2_config(self) -> typing.Optional[TransferConnectorAs2Config]:
        '''as2_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#as2_config TransferConnector#as2_config}
        '''
        result = self._values.get("as2_config")
        return typing.cast(typing.Optional[TransferConnectorAs2Config], result)

    @builtins.property
    def egress_config(self) -> typing.Optional["TransferConnectorEgressConfig"]:
        '''egress_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#egress_config TransferConnector#egress_config}
        '''
        result = self._values.get("egress_config")
        return typing.cast(typing.Optional["TransferConnectorEgressConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#id TransferConnector#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#logging_role TransferConnector#logging_role}.'''
        result = self._values.get("logging_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#region TransferConnector#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#security_policy_name TransferConnector#security_policy_name}.'''
        result = self._values.get("security_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sftp_config(self) -> typing.Optional["TransferConnectorSftpConfig"]:
        '''sftp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#sftp_config TransferConnector#sftp_config}
        '''
        result = self._values.get("sftp_config")
        return typing.cast(typing.Optional["TransferConnectorSftpConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#tags TransferConnector#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#tags_all TransferConnector#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["TransferConnectorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#timeouts TransferConnector#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["TransferConnectorTimeouts"], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#url TransferConnector#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferConnectorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorEgressConfig",
    jsii_struct_bases=[],
    name_mapping={"vpc_lattice": "vpcLattice"},
)
class TransferConnectorEgressConfig:
    def __init__(
        self,
        *,
        vpc_lattice: typing.Optional[typing.Union["TransferConnectorEgressConfigVpcLattice", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vpc_lattice: vpc_lattice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#vpc_lattice TransferConnector#vpc_lattice}
        '''
        if isinstance(vpc_lattice, dict):
            vpc_lattice = TransferConnectorEgressConfigVpcLattice(**vpc_lattice)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b21c6dfc683894803f408b54b5f7ef5d630438281a7abeb7e9bb49b8027f70)
            check_type(argname="argument vpc_lattice", value=vpc_lattice, expected_type=type_hints["vpc_lattice"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vpc_lattice is not None:
            self._values["vpc_lattice"] = vpc_lattice

    @builtins.property
    def vpc_lattice(self) -> typing.Optional["TransferConnectorEgressConfigVpcLattice"]:
        '''vpc_lattice block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#vpc_lattice TransferConnector#vpc_lattice}
        '''
        result = self._values.get("vpc_lattice")
        return typing.cast(typing.Optional["TransferConnectorEgressConfigVpcLattice"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferConnectorEgressConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferConnectorEgressConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorEgressConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b5e0fb5d64ad7301b99491a211f45093fdb5c8af272b8fe11e0f75e32d7dc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVpcLattice")
    def put_vpc_lattice(
        self,
        *,
        resource_configuration_arn: builtins.str,
        port_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param resource_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#resource_configuration_arn TransferConnector#resource_configuration_arn}.
        :param port_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#port_number TransferConnector#port_number}.
        '''
        value = TransferConnectorEgressConfigVpcLattice(
            resource_configuration_arn=resource_configuration_arn,
            port_number=port_number,
        )

        return typing.cast(None, jsii.invoke(self, "putVpcLattice", [value]))

    @jsii.member(jsii_name="resetVpcLattice")
    def reset_vpc_lattice(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcLattice", []))

    @builtins.property
    @jsii.member(jsii_name="vpcLattice")
    def vpc_lattice(self) -> "TransferConnectorEgressConfigVpcLatticeOutputReference":
        return typing.cast("TransferConnectorEgressConfigVpcLatticeOutputReference", jsii.get(self, "vpcLattice"))

    @builtins.property
    @jsii.member(jsii_name="vpcLatticeInput")
    def vpc_lattice_input(
        self,
    ) -> typing.Optional["TransferConnectorEgressConfigVpcLattice"]:
        return typing.cast(typing.Optional["TransferConnectorEgressConfigVpcLattice"], jsii.get(self, "vpcLatticeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferConnectorEgressConfig]:
        return typing.cast(typing.Optional[TransferConnectorEgressConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferConnectorEgressConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb3fb680ba219e14956fd1caf7c887112554628f55af5b5fa86e5389aca482c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorEgressConfigVpcLattice",
    jsii_struct_bases=[],
    name_mapping={
        "resource_configuration_arn": "resourceConfigurationArn",
        "port_number": "portNumber",
    },
)
class TransferConnectorEgressConfigVpcLattice:
    def __init__(
        self,
        *,
        resource_configuration_arn: builtins.str,
        port_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param resource_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#resource_configuration_arn TransferConnector#resource_configuration_arn}.
        :param port_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#port_number TransferConnector#port_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f29cb8d797c416a8f491ff8b54164a75a0f1f511dfec4bb3dcbaa1e2f2329a1)
            check_type(argname="argument resource_configuration_arn", value=resource_configuration_arn, expected_type=type_hints["resource_configuration_arn"])
            check_type(argname="argument port_number", value=port_number, expected_type=type_hints["port_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_configuration_arn": resource_configuration_arn,
        }
        if port_number is not None:
            self._values["port_number"] = port_number

    @builtins.property
    def resource_configuration_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#resource_configuration_arn TransferConnector#resource_configuration_arn}.'''
        result = self._values.get("resource_configuration_arn")
        assert result is not None, "Required property 'resource_configuration_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#port_number TransferConnector#port_number}.'''
        result = self._values.get("port_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferConnectorEgressConfigVpcLattice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferConnectorEgressConfigVpcLatticeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorEgressConfigVpcLatticeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ef4fda87811f1f5a421ed377179a0041d50c8f58aba5b011694c9fa14fd487a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPortNumber")
    def reset_port_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortNumber", []))

    @builtins.property
    @jsii.member(jsii_name="portNumberInput")
    def port_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceConfigurationArnInput")
    def resource_configuration_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceConfigurationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="portNumber")
    def port_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "portNumber"))

    @port_number.setter
    def port_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c6c0dd3a3bcba7fed40482695fdc034d3707b5ce940ae0a101de84a2392ab23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceConfigurationArn")
    def resource_configuration_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceConfigurationArn"))

    @resource_configuration_arn.setter
    def resource_configuration_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b11fdbcd9256677a9565b1250eaa62ca65e48a8eb68756a871519f2314e4432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceConfigurationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferConnectorEgressConfigVpcLattice]:
        return typing.cast(typing.Optional[TransferConnectorEgressConfigVpcLattice], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferConnectorEgressConfigVpcLattice],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894cf9112a4f9d2aece71afd640770f43e810f184d21603636f74255e11f64ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorSftpConfig",
    jsii_struct_bases=[],
    name_mapping={
        "trusted_host_keys": "trustedHostKeys",
        "user_secret_id": "userSecretId",
    },
)
class TransferConnectorSftpConfig:
    def __init__(
        self,
        *,
        trusted_host_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_secret_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param trusted_host_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#trusted_host_keys TransferConnector#trusted_host_keys}.
        :param user_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#user_secret_id TransferConnector#user_secret_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82154500d2d4fe85ffc44a258493534dee1474468540b7e642e4dce007b1c821)
            check_type(argname="argument trusted_host_keys", value=trusted_host_keys, expected_type=type_hints["trusted_host_keys"])
            check_type(argname="argument user_secret_id", value=user_secret_id, expected_type=type_hints["user_secret_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if trusted_host_keys is not None:
            self._values["trusted_host_keys"] = trusted_host_keys
        if user_secret_id is not None:
            self._values["user_secret_id"] = user_secret_id

    @builtins.property
    def trusted_host_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#trusted_host_keys TransferConnector#trusted_host_keys}.'''
        result = self._values.get("trusted_host_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_secret_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#user_secret_id TransferConnector#user_secret_id}.'''
        result = self._values.get("user_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferConnectorSftpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferConnectorSftpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorSftpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a14e99b11489fced6ca4e798d3252aeaf3d5c07659d1efe9d284e7ea5ec43ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTrustedHostKeys")
    def reset_trusted_host_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedHostKeys", []))

    @jsii.member(jsii_name="resetUserSecretId")
    def reset_user_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserSecretId", []))

    @builtins.property
    @jsii.member(jsii_name="trustedHostKeysInput")
    def trusted_host_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedHostKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="userSecretIdInput")
    def user_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedHostKeys")
    def trusted_host_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedHostKeys"))

    @trusted_host_keys.setter
    def trusted_host_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6cda6a8244bd90b82d7b0a9f12b797c5067dffaf885b980dfe3ee578fd2f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedHostKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userSecretId")
    def user_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userSecretId"))

    @user_secret_id.setter
    def user_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53226f3cc6b61bd842083f083291339df737062b89c66dd565b128c7509aa42a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferConnectorSftpConfig]:
        return typing.cast(typing.Optional[TransferConnectorSftpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferConnectorSftpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6899432eb4adb7e267656d9a4a3d336ea3e45076378d3dcb035e6016cc51c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class TransferConnectorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#create TransferConnector#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#delete TransferConnector#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#update TransferConnector#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06d4e147ea1a5c44fe21cb5e4dae4861deea6cf90e14c17158adb53ffc5e68c2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#create TransferConnector#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#delete TransferConnector#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_connector#update TransferConnector#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferConnectorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferConnectorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferConnector.TransferConnectorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd1b4bb69d71f1fbd0b3a9e355a50d61915087e94ce29f4961b09641c103d721)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19fcc76fc3851406d26b746dfb6c1c5f00a93031ca3b2bd4ab0f90cdfd94c409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7421a2463ec0344c3b0f1653c3aa7d94dcbdea4a2d5920fcc15cbc11ea0595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ccff9242e2fc134a277a0ddf8f0845e42117ef8d1e8be16b55211449284cff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferConnectorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferConnectorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferConnectorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab439346075987c56e30c67c0f1f849d8f259e35a24b7c9cb51aec253e3e09f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TransferConnector",
    "TransferConnectorAs2Config",
    "TransferConnectorAs2ConfigOutputReference",
    "TransferConnectorConfig",
    "TransferConnectorEgressConfig",
    "TransferConnectorEgressConfigOutputReference",
    "TransferConnectorEgressConfigVpcLattice",
    "TransferConnectorEgressConfigVpcLatticeOutputReference",
    "TransferConnectorSftpConfig",
    "TransferConnectorSftpConfigOutputReference",
    "TransferConnectorTimeouts",
    "TransferConnectorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__00c37bc1afbc6700ba6c5df0076d7d15950015ab593dbecc9431ff15282b3835(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    access_role: builtins.str,
    as2_config: typing.Optional[typing.Union[TransferConnectorAs2Config, typing.Dict[builtins.str, typing.Any]]] = None,
    egress_config: typing.Optional[typing.Union[TransferConnectorEgressConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging_role: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_policy_name: typing.Optional[builtins.str] = None,
    sftp_config: typing.Optional[typing.Union[TransferConnectorSftpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[TransferConnectorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__682301e2023993dc5b1352c6ce35bb2a4da1b8469098487d0dbdb4e0f1135705(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40403db89dcd74329814a9d7c05b7113e82d4a3a0b3b4deb29c695061d557218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101fdccad9438463933f1fe095b84d52866d79393468905db9bc93153610e871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc387cddc61fcf34e20ab402fac2e15c6b6b56b040c2c1e7b34632a261e248e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfe7b2256203be266c1dfc824384631e394d31e1b4a7d2a06ec60d9b0382080(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6995827d82472ab14f5424274457b1364541669276a42c479ee7d4c5377e2a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b774730b0215a42d12856713d39763e1eaee89b05815d39b01feff3bcbac071(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad0cf7b34c71139289289465fecf93a9e84bb6b4ee796fabf8f13543607d544(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac92c740dd58dc5098eb16388c1b2093599b9738f585d4d5b066539bedba388a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f97f3a2bdd88bf322748355d26d7d7bf8ca92c77e106b1e18e454edd4faa08(
    *,
    compression: builtins.str,
    encryption_algorithm: builtins.str,
    local_profile_id: builtins.str,
    mdn_response: builtins.str,
    partner_profile_id: builtins.str,
    signing_algorithm: builtins.str,
    mdn_signing_algorithm: typing.Optional[builtins.str] = None,
    message_subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d31918238fc4afb346923b3404b30e28378305f1fd507f451829da8bc862246(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222d624540dc83d438d575901d708d932803e782318799ddffb2e5878b036749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d680d447cb80b0ed6de3549a908ddbff61a14fc32e9b68b3987dc201434035ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd3f00f39838be12a7ab3aee27bf770a04c10d68c673ec5bd6252af503b2fcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b593789577d28462079b7dc13797f216cb98f299fe14b8074e35e847605d4cc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63342063fcd284e75d450f6b6d8db0d5fa4e91829a21e97468e9a5544755f56d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756cd59daada743d84714bf5825fd15110c4286cc6ef69b49323e26cd430b677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fe3ad33b772e2fc23e1f8355bbcfcd9448df4e8bf88f53392f211dff230bb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f738b5fa976cc1b0248f03b9387a9a607f77b33dd5595c846e1402457a1d12f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff50a627b107296438a5291e63063ec98bfdbc91282896e02db0299a62e2f13(
    value: typing.Optional[TransferConnectorAs2Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c4b811b0de2e8b080cc5a60a97f92d9f15d247fef1294e76d12617ad0fd07c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    access_role: builtins.str,
    as2_config: typing.Optional[typing.Union[TransferConnectorAs2Config, typing.Dict[builtins.str, typing.Any]]] = None,
    egress_config: typing.Optional[typing.Union[TransferConnectorEgressConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging_role: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_policy_name: typing.Optional[builtins.str] = None,
    sftp_config: typing.Optional[typing.Union[TransferConnectorSftpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[TransferConnectorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b21c6dfc683894803f408b54b5f7ef5d630438281a7abeb7e9bb49b8027f70(
    *,
    vpc_lattice: typing.Optional[typing.Union[TransferConnectorEgressConfigVpcLattice, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b5e0fb5d64ad7301b99491a211f45093fdb5c8af272b8fe11e0f75e32d7dc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb3fb680ba219e14956fd1caf7c887112554628f55af5b5fa86e5389aca482c(
    value: typing.Optional[TransferConnectorEgressConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f29cb8d797c416a8f491ff8b54164a75a0f1f511dfec4bb3dcbaa1e2f2329a1(
    *,
    resource_configuration_arn: builtins.str,
    port_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef4fda87811f1f5a421ed377179a0041d50c8f58aba5b011694c9fa14fd487a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c6c0dd3a3bcba7fed40482695fdc034d3707b5ce940ae0a101de84a2392ab23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b11fdbcd9256677a9565b1250eaa62ca65e48a8eb68756a871519f2314e4432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894cf9112a4f9d2aece71afd640770f43e810f184d21603636f74255e11f64ce(
    value: typing.Optional[TransferConnectorEgressConfigVpcLattice],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82154500d2d4fe85ffc44a258493534dee1474468540b7e642e4dce007b1c821(
    *,
    trusted_host_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a14e99b11489fced6ca4e798d3252aeaf3d5c07659d1efe9d284e7ea5ec43ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6cda6a8244bd90b82d7b0a9f12b797c5067dffaf885b980dfe3ee578fd2f7c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53226f3cc6b61bd842083f083291339df737062b89c66dd565b128c7509aa42a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6899432eb4adb7e267656d9a4a3d336ea3e45076378d3dcb035e6016cc51c98(
    value: typing.Optional[TransferConnectorSftpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d4e147ea1a5c44fe21cb5e4dae4861deea6cf90e14c17158adb53ffc5e68c2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1b4bb69d71f1fbd0b3a9e355a50d61915087e94ce29f4961b09641c103d721(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fcc76fc3851406d26b746dfb6c1c5f00a93031ca3b2bd4ab0f90cdfd94c409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7421a2463ec0344c3b0f1653c3aa7d94dcbdea4a2d5920fcc15cbc11ea0595(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ccff9242e2fc134a277a0ddf8f0845e42117ef8d1e8be16b55211449284cff4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab439346075987c56e30c67c0f1f849d8f259e35a24b7c9cb51aec253e3e09f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferConnectorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
