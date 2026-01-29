r'''
# `aws_acmpca_certificate_authority`

Refer to the Terraform Registry for docs: [`aws_acmpca_certificate_authority`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority).
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


class AcmpcaCertificateAuthority(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthority",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority aws_acmpca_certificate_authority}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        certificate_authority_configuration: typing.Union["AcmpcaCertificateAuthorityCertificateAuthorityConfiguration", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        key_storage_security_standard: typing.Optional[builtins.str] = None,
        permanent_deletion_time_in_days: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        revocation_configuration: typing.Optional[typing.Union["AcmpcaCertificateAuthorityRevocationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AcmpcaCertificateAuthorityTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        usage_mode: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority aws_acmpca_certificate_authority} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param certificate_authority_configuration: certificate_authority_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#certificate_authority_configuration AcmpcaCertificateAuthority#certificate_authority_configuration}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#enabled AcmpcaCertificateAuthority#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#id AcmpcaCertificateAuthority#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_storage_security_standard: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#key_storage_security_standard AcmpcaCertificateAuthority#key_storage_security_standard}.
        :param permanent_deletion_time_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#permanent_deletion_time_in_days AcmpcaCertificateAuthority#permanent_deletion_time_in_days}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#region AcmpcaCertificateAuthority#region}
        :param revocation_configuration: revocation_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#revocation_configuration AcmpcaCertificateAuthority#revocation_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#tags AcmpcaCertificateAuthority#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#tags_all AcmpcaCertificateAuthority#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#timeouts AcmpcaCertificateAuthority#timeouts}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#type AcmpcaCertificateAuthority#type}.
        :param usage_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#usage_mode AcmpcaCertificateAuthority#usage_mode}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b5d9592aa732802f225c1a82fdb1e9380fd3e2248baa492c38afe390676cb6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AcmpcaCertificateAuthorityConfig(
            certificate_authority_configuration=certificate_authority_configuration,
            enabled=enabled,
            id=id,
            key_storage_security_standard=key_storage_security_standard,
            permanent_deletion_time_in_days=permanent_deletion_time_in_days,
            region=region,
            revocation_configuration=revocation_configuration,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            type=type,
            usage_mode=usage_mode,
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
        '''Generates CDKTF code for importing a AcmpcaCertificateAuthority resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AcmpcaCertificateAuthority to import.
        :param import_from_id: The id of the existing AcmpcaCertificateAuthority that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AcmpcaCertificateAuthority to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10995fa79d98c0828e4db7e4a7ec4b560357bfeb7ebad805a7bea06727a5affb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCertificateAuthorityConfiguration")
    def put_certificate_authority_configuration(
        self,
        *,
        key_algorithm: builtins.str,
        signing_algorithm: builtins.str,
        subject: typing.Union["AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param key_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#key_algorithm AcmpcaCertificateAuthority#key_algorithm}.
        :param signing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#signing_algorithm AcmpcaCertificateAuthority#signing_algorithm}.
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#subject AcmpcaCertificateAuthority#subject}
        '''
        value = AcmpcaCertificateAuthorityCertificateAuthorityConfiguration(
            key_algorithm=key_algorithm,
            signing_algorithm=signing_algorithm,
            subject=subject,
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateAuthorityConfiguration", [value]))

    @jsii.member(jsii_name="putRevocationConfiguration")
    def put_revocation_configuration(
        self,
        *,
        crl_configuration: typing.Optional[typing.Union["AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        ocsp_configuration: typing.Optional[typing.Union["AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param crl_configuration: crl_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#crl_configuration AcmpcaCertificateAuthority#crl_configuration}
        :param ocsp_configuration: ocsp_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#ocsp_configuration AcmpcaCertificateAuthority#ocsp_configuration}
        '''
        value = AcmpcaCertificateAuthorityRevocationConfiguration(
            crl_configuration=crl_configuration, ocsp_configuration=ocsp_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putRevocationConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#create AcmpcaCertificateAuthority#create}.
        '''
        value = AcmpcaCertificateAuthorityTimeouts(create=create)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeyStorageSecurityStandard")
    def reset_key_storage_security_standard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyStorageSecurityStandard", []))

    @jsii.member(jsii_name="resetPermanentDeletionTimeInDays")
    def reset_permanent_deletion_time_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermanentDeletionTimeInDays", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRevocationConfiguration")
    def reset_revocation_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevocationConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUsageMode")
    def reset_usage_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsageMode", []))

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
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityConfiguration")
    def certificate_authority_configuration(
        self,
    ) -> "AcmpcaCertificateAuthorityCertificateAuthorityConfigurationOutputReference":
        return typing.cast("AcmpcaCertificateAuthorityCertificateAuthorityConfigurationOutputReference", jsii.get(self, "certificateAuthorityConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateChain"))

    @builtins.property
    @jsii.member(jsii_name="certificateSigningRequest")
    def certificate_signing_request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSigningRequest"))

    @builtins.property
    @jsii.member(jsii_name="notAfter")
    def not_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notAfter"))

    @builtins.property
    @jsii.member(jsii_name="notBefore")
    def not_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notBefore"))

    @builtins.property
    @jsii.member(jsii_name="revocationConfiguration")
    def revocation_configuration(
        self,
    ) -> "AcmpcaCertificateAuthorityRevocationConfigurationOutputReference":
        return typing.cast("AcmpcaCertificateAuthorityRevocationConfigurationOutputReference", jsii.get(self, "revocationConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="serial")
    def serial(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serial"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AcmpcaCertificateAuthorityTimeoutsOutputReference":
        return typing.cast("AcmpcaCertificateAuthorityTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityConfigurationInput")
    def certificate_authority_configuration_input(
        self,
    ) -> typing.Optional["AcmpcaCertificateAuthorityCertificateAuthorityConfiguration"]:
        return typing.cast(typing.Optional["AcmpcaCertificateAuthorityCertificateAuthorityConfiguration"], jsii.get(self, "certificateAuthorityConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyStorageSecurityStandardInput")
    def key_storage_security_standard_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyStorageSecurityStandardInput"))

    @builtins.property
    @jsii.member(jsii_name="permanentDeletionTimeInDaysInput")
    def permanent_deletion_time_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "permanentDeletionTimeInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="revocationConfigurationInput")
    def revocation_configuration_input(
        self,
    ) -> typing.Optional["AcmpcaCertificateAuthorityRevocationConfiguration"]:
        return typing.cast(typing.Optional["AcmpcaCertificateAuthorityRevocationConfiguration"], jsii.get(self, "revocationConfigurationInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AcmpcaCertificateAuthorityTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AcmpcaCertificateAuthorityTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="usageModeInput")
    def usage_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usageModeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f7fb8a38c615af55e12c0aca9523ceba527b64798f1db2a134b4ffb6db0dbc34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfccf4cce58a7bcc9ab0a6b23728434c31ae0677a75701163bef671dcdee3fe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyStorageSecurityStandard")
    def key_storage_security_standard(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyStorageSecurityStandard"))

    @key_storage_security_standard.setter
    def key_storage_security_standard(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963f01212c7aae6f728e8c9fb6382f6e147c356bf14f2936144f5c93a5a43dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyStorageSecurityStandard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permanentDeletionTimeInDays")
    def permanent_deletion_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "permanentDeletionTimeInDays"))

    @permanent_deletion_time_in_days.setter
    def permanent_deletion_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1e4f252113aa1a088ebe348dac25cbf6adcb55b7360862267bffac658daaa6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permanentDeletionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff956ed4175c0da1f7c928abe9744d65062378edfe13a5561b19123408b2ac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0ec898ae0d582648bf9ec9438af498cdd1c7cd7c7d96b042d635333261608c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fff978811265be6ef658e0d7ac2fce49e94c88966a30769b2d29a5c8946f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995cc072149cb7f7bfe8c55be8fe567a963f57e60966300f0646eedc34e14d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usageMode")
    def usage_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usageMode"))

    @usage_mode.setter
    def usage_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5ca4a5ef88a582a061a887d6ffc9e891e5153554929a2e4f8b673a013978d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usageMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityCertificateAuthorityConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "key_algorithm": "keyAlgorithm",
        "signing_algorithm": "signingAlgorithm",
        "subject": "subject",
    },
)
class AcmpcaCertificateAuthorityCertificateAuthorityConfiguration:
    def __init__(
        self,
        *,
        key_algorithm: builtins.str,
        signing_algorithm: builtins.str,
        subject: typing.Union["AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param key_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#key_algorithm AcmpcaCertificateAuthority#key_algorithm}.
        :param signing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#signing_algorithm AcmpcaCertificateAuthority#signing_algorithm}.
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#subject AcmpcaCertificateAuthority#subject}
        '''
        if isinstance(subject, dict):
            subject = AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject(**subject)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5b38a20068f231ce64482eb4b86ec57e26fc476978beee9591da5ee8cb48e6)
            check_type(argname="argument key_algorithm", value=key_algorithm, expected_type=type_hints["key_algorithm"])
            check_type(argname="argument signing_algorithm", value=signing_algorithm, expected_type=type_hints["signing_algorithm"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_algorithm": key_algorithm,
            "signing_algorithm": signing_algorithm,
            "subject": subject,
        }

    @builtins.property
    def key_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#key_algorithm AcmpcaCertificateAuthority#key_algorithm}.'''
        result = self._values.get("key_algorithm")
        assert result is not None, "Required property 'key_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#signing_algorithm AcmpcaCertificateAuthority#signing_algorithm}.'''
        result = self._values.get("signing_algorithm")
        assert result is not None, "Required property 'signing_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(
        self,
    ) -> "AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject":
        '''subject block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#subject AcmpcaCertificateAuthority#subject}
        '''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast("AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcmpcaCertificateAuthorityCertificateAuthorityConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AcmpcaCertificateAuthorityCertificateAuthorityConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityCertificateAuthorityConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5959cb0bd131623e643e9f8d1b51fb9653473d5b1813b1f7bd007bffd54d809c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubject")
    def put_subject(
        self,
        *,
        common_name: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        distinguished_name_qualifier: typing.Optional[builtins.str] = None,
        generation_qualifier: typing.Optional[builtins.str] = None,
        given_name: typing.Optional[builtins.str] = None,
        initials: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        pseudonym: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        surname: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#common_name AcmpcaCertificateAuthority#common_name}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#country AcmpcaCertificateAuthority#country}.
        :param distinguished_name_qualifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#distinguished_name_qualifier AcmpcaCertificateAuthority#distinguished_name_qualifier}.
        :param generation_qualifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#generation_qualifier AcmpcaCertificateAuthority#generation_qualifier}.
        :param given_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#given_name AcmpcaCertificateAuthority#given_name}.
        :param initials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#initials AcmpcaCertificateAuthority#initials}.
        :param locality: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#locality AcmpcaCertificateAuthority#locality}.
        :param organization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#organization AcmpcaCertificateAuthority#organization}.
        :param organizational_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#organizational_unit AcmpcaCertificateAuthority#organizational_unit}.
        :param pseudonym: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#pseudonym AcmpcaCertificateAuthority#pseudonym}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#state AcmpcaCertificateAuthority#state}.
        :param surname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#surname AcmpcaCertificateAuthority#surname}.
        :param title: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#title AcmpcaCertificateAuthority#title}.
        '''
        value = AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject(
            common_name=common_name,
            country=country,
            distinguished_name_qualifier=distinguished_name_qualifier,
            generation_qualifier=generation_qualifier,
            given_name=given_name,
            initials=initials,
            locality=locality,
            organization=organization,
            organizational_unit=organizational_unit,
            pseudonym=pseudonym,
            state=state,
            surname=surname,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putSubject", [value]))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(
        self,
    ) -> "AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubjectOutputReference":
        return typing.cast("AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubjectOutputReference", jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithmInput")
    def key_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="signingAlgorithmInput")
    def signing_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signingAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(
        self,
    ) -> typing.Optional["AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject"]:
        return typing.cast(typing.Optional["AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject"], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithm")
    def key_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyAlgorithm"))

    @key_algorithm.setter
    def key_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b03c3dae126b88b5c452feffaee0210769eaefb29aad5bfb10082231d2e7cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signingAlgorithm"))

    @signing_algorithm.setter
    def signing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a5ef5707fcc85230ac69e75f4bae9b58768baaefcb4045a56d071231ed0a0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signingAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AcmpcaCertificateAuthorityCertificateAuthorityConfiguration]:
        return typing.cast(typing.Optional[AcmpcaCertificateAuthorityCertificateAuthorityConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AcmpcaCertificateAuthorityCertificateAuthorityConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3b87dfc7aa3c50993987b85dbf51b78cdb18ccc222bf2eb4119f0d8d155b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject",
    jsii_struct_bases=[],
    name_mapping={
        "common_name": "commonName",
        "country": "country",
        "distinguished_name_qualifier": "distinguishedNameQualifier",
        "generation_qualifier": "generationQualifier",
        "given_name": "givenName",
        "initials": "initials",
        "locality": "locality",
        "organization": "organization",
        "organizational_unit": "organizationalUnit",
        "pseudonym": "pseudonym",
        "state": "state",
        "surname": "surname",
        "title": "title",
    },
)
class AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject:
    def __init__(
        self,
        *,
        common_name: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        distinguished_name_qualifier: typing.Optional[builtins.str] = None,
        generation_qualifier: typing.Optional[builtins.str] = None,
        given_name: typing.Optional[builtins.str] = None,
        initials: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        pseudonym: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        surname: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#common_name AcmpcaCertificateAuthority#common_name}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#country AcmpcaCertificateAuthority#country}.
        :param distinguished_name_qualifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#distinguished_name_qualifier AcmpcaCertificateAuthority#distinguished_name_qualifier}.
        :param generation_qualifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#generation_qualifier AcmpcaCertificateAuthority#generation_qualifier}.
        :param given_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#given_name AcmpcaCertificateAuthority#given_name}.
        :param initials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#initials AcmpcaCertificateAuthority#initials}.
        :param locality: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#locality AcmpcaCertificateAuthority#locality}.
        :param organization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#organization AcmpcaCertificateAuthority#organization}.
        :param organizational_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#organizational_unit AcmpcaCertificateAuthority#organizational_unit}.
        :param pseudonym: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#pseudonym AcmpcaCertificateAuthority#pseudonym}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#state AcmpcaCertificateAuthority#state}.
        :param surname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#surname AcmpcaCertificateAuthority#surname}.
        :param title: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#title AcmpcaCertificateAuthority#title}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82bca375d558c08578ce0a0f01a1652bb824e6ade9a2e63a6acd2500c464ac0)
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument distinguished_name_qualifier", value=distinguished_name_qualifier, expected_type=type_hints["distinguished_name_qualifier"])
            check_type(argname="argument generation_qualifier", value=generation_qualifier, expected_type=type_hints["generation_qualifier"])
            check_type(argname="argument given_name", value=given_name, expected_type=type_hints["given_name"])
            check_type(argname="argument initials", value=initials, expected_type=type_hints["initials"])
            check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument organizational_unit", value=organizational_unit, expected_type=type_hints["organizational_unit"])
            check_type(argname="argument pseudonym", value=pseudonym, expected_type=type_hints["pseudonym"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument surname", value=surname, expected_type=type_hints["surname"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if common_name is not None:
            self._values["common_name"] = common_name
        if country is not None:
            self._values["country"] = country
        if distinguished_name_qualifier is not None:
            self._values["distinguished_name_qualifier"] = distinguished_name_qualifier
        if generation_qualifier is not None:
            self._values["generation_qualifier"] = generation_qualifier
        if given_name is not None:
            self._values["given_name"] = given_name
        if initials is not None:
            self._values["initials"] = initials
        if locality is not None:
            self._values["locality"] = locality
        if organization is not None:
            self._values["organization"] = organization
        if organizational_unit is not None:
            self._values["organizational_unit"] = organizational_unit
        if pseudonym is not None:
            self._values["pseudonym"] = pseudonym
        if state is not None:
            self._values["state"] = state
        if surname is not None:
            self._values["surname"] = surname
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def common_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#common_name AcmpcaCertificateAuthority#common_name}.'''
        result = self._values.get("common_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#country AcmpcaCertificateAuthority#country}.'''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distinguished_name_qualifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#distinguished_name_qualifier AcmpcaCertificateAuthority#distinguished_name_qualifier}.'''
        result = self._values.get("distinguished_name_qualifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def generation_qualifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#generation_qualifier AcmpcaCertificateAuthority#generation_qualifier}.'''
        result = self._values.get("generation_qualifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def given_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#given_name AcmpcaCertificateAuthority#given_name}.'''
        result = self._values.get("given_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initials(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#initials AcmpcaCertificateAuthority#initials}.'''
        result = self._values.get("initials")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#locality AcmpcaCertificateAuthority#locality}.'''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#organization AcmpcaCertificateAuthority#organization}.'''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizational_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#organizational_unit AcmpcaCertificateAuthority#organizational_unit}.'''
        result = self._values.get("organizational_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pseudonym(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#pseudonym AcmpcaCertificateAuthority#pseudonym}.'''
        result = self._values.get("pseudonym")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#state AcmpcaCertificateAuthority#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def surname(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#surname AcmpcaCertificateAuthority#surname}.'''
        result = self._values.get("surname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#title AcmpcaCertificateAuthority#title}.'''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f10a6234a2eb1c77dbec113a1a204922e482df0bb3cf1de7a55bf09acacda1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommonName")
    def reset_common_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonName", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetDistinguishedNameQualifier")
    def reset_distinguished_name_qualifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistinguishedNameQualifier", []))

    @jsii.member(jsii_name="resetGenerationQualifier")
    def reset_generation_qualifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenerationQualifier", []))

    @jsii.member(jsii_name="resetGivenName")
    def reset_given_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGivenName", []))

    @jsii.member(jsii_name="resetInitials")
    def reset_initials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitials", []))

    @jsii.member(jsii_name="resetLocality")
    def reset_locality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocality", []))

    @jsii.member(jsii_name="resetOrganization")
    def reset_organization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganization", []))

    @jsii.member(jsii_name="resetOrganizationalUnit")
    def reset_organizational_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationalUnit", []))

    @jsii.member(jsii_name="resetPseudonym")
    def reset_pseudonym(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPseudonym", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetSurname")
    def reset_surname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSurname", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="commonNameInput")
    def common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="distinguishedNameQualifierInput")
    def distinguished_name_qualifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distinguishedNameQualifierInput"))

    @builtins.property
    @jsii.member(jsii_name="generationQualifierInput")
    def generation_qualifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationQualifierInput"))

    @builtins.property
    @jsii.member(jsii_name="givenNameInput")
    def given_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "givenNameInput"))

    @builtins.property
    @jsii.member(jsii_name="initialsInput")
    def initials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initialsInput"))

    @builtins.property
    @jsii.member(jsii_name="localityInput")
    def locality_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localityInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitInput")
    def organizational_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="pseudonymInput")
    def pseudonym_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pseudonymInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="surnameInput")
    def surname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "surnameInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @common_name.setter
    def common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5f60ee30deeda6c171e55c127cf9d51a90a87dbc21bf93b3bb1a6f2a839e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bc9f2f093b14d915d8d4eed5e3ba4fef4ab6794d199c6161e93b073b0f0711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distinguishedNameQualifier")
    def distinguished_name_qualifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distinguishedNameQualifier"))

    @distinguished_name_qualifier.setter
    def distinguished_name_qualifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee11929daf02d9ef0252b21aa9227c5c18d4dc5c250dcebec42c0f679804f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distinguishedNameQualifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generationQualifier")
    def generation_qualifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generationQualifier"))

    @generation_qualifier.setter
    def generation_qualifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ca5d6a98e60371a862af86e88f0e8ce8b5f635830be07d226ab66c1dd17e6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generationQualifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="givenName")
    def given_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "givenName"))

    @given_name.setter
    def given_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569d7759ad1c95149d6edc56fdba752b6ef501d1b84f42664844a0a27c9ae7c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "givenName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initials")
    def initials(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initials"))

    @initials.setter
    def initials(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b940150c1da96ed72d21018a4af33778c1972a7d8b8d45fad837c3923330c176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5392ee0568d277dfecf9faffbddb978d20e8b73fc1d3a628cb588d29747c3c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a9f4601a2ba285e5cce541b8f87397bdbd9fe7ef390fb9a92f8b757b604c65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationalUnit")
    def organizational_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationalUnit"))

    @organizational_unit.setter
    def organizational_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aef6bc04e0d46a1efc5bcdbc2ef22349f8c77da6c7af6bbcfecdc166e932ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pseudonym")
    def pseudonym(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pseudonym"))

    @pseudonym.setter
    def pseudonym(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d97dcc14b68071e9541026bbf123de538073476c8b2443ad80c8f88af79c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pseudonym", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068df0ae9a5e685f347b5b9b4d196560a08239c4950087e3a719d501d87ed8bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="surname")
    def surname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "surname"))

    @surname.setter
    def surname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c483fd249f2966afd18472f1b566bcffa03c62bbf086f46bf559cbde47f34011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "surname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6132ca2c2f760fdfc6cf99338f9eb51f1497b19b7720ace3271fb32bd266bcc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject]:
        return typing.cast(typing.Optional[AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1edbbea2901b6168919b5eb7b5950fd69b9bad0433364462260d16e2da3a7954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "certificate_authority_configuration": "certificateAuthorityConfiguration",
        "enabled": "enabled",
        "id": "id",
        "key_storage_security_standard": "keyStorageSecurityStandard",
        "permanent_deletion_time_in_days": "permanentDeletionTimeInDays",
        "region": "region",
        "revocation_configuration": "revocationConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "type": "type",
        "usage_mode": "usageMode",
    },
)
class AcmpcaCertificateAuthorityConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        certificate_authority_configuration: typing.Union[AcmpcaCertificateAuthorityCertificateAuthorityConfiguration, typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        key_storage_security_standard: typing.Optional[builtins.str] = None,
        permanent_deletion_time_in_days: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        revocation_configuration: typing.Optional[typing.Union["AcmpcaCertificateAuthorityRevocationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AcmpcaCertificateAuthorityTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        usage_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param certificate_authority_configuration: certificate_authority_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#certificate_authority_configuration AcmpcaCertificateAuthority#certificate_authority_configuration}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#enabled AcmpcaCertificateAuthority#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#id AcmpcaCertificateAuthority#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_storage_security_standard: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#key_storage_security_standard AcmpcaCertificateAuthority#key_storage_security_standard}.
        :param permanent_deletion_time_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#permanent_deletion_time_in_days AcmpcaCertificateAuthority#permanent_deletion_time_in_days}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#region AcmpcaCertificateAuthority#region}
        :param revocation_configuration: revocation_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#revocation_configuration AcmpcaCertificateAuthority#revocation_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#tags AcmpcaCertificateAuthority#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#tags_all AcmpcaCertificateAuthority#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#timeouts AcmpcaCertificateAuthority#timeouts}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#type AcmpcaCertificateAuthority#type}.
        :param usage_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#usage_mode AcmpcaCertificateAuthority#usage_mode}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(certificate_authority_configuration, dict):
            certificate_authority_configuration = AcmpcaCertificateAuthorityCertificateAuthorityConfiguration(**certificate_authority_configuration)
        if isinstance(revocation_configuration, dict):
            revocation_configuration = AcmpcaCertificateAuthorityRevocationConfiguration(**revocation_configuration)
        if isinstance(timeouts, dict):
            timeouts = AcmpcaCertificateAuthorityTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1062319a5b40323e81ad1fb3c9f6f20958a3e3718594f0f56b3d1e493763274c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument certificate_authority_configuration", value=certificate_authority_configuration, expected_type=type_hints["certificate_authority_configuration"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key_storage_security_standard", value=key_storage_security_standard, expected_type=type_hints["key_storage_security_standard"])
            check_type(argname="argument permanent_deletion_time_in_days", value=permanent_deletion_time_in_days, expected_type=type_hints["permanent_deletion_time_in_days"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument revocation_configuration", value=revocation_configuration, expected_type=type_hints["revocation_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument usage_mode", value=usage_mode, expected_type=type_hints["usage_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_authority_configuration": certificate_authority_configuration,
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
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if key_storage_security_standard is not None:
            self._values["key_storage_security_standard"] = key_storage_security_standard
        if permanent_deletion_time_in_days is not None:
            self._values["permanent_deletion_time_in_days"] = permanent_deletion_time_in_days
        if region is not None:
            self._values["region"] = region
        if revocation_configuration is not None:
            self._values["revocation_configuration"] = revocation_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type
        if usage_mode is not None:
            self._values["usage_mode"] = usage_mode

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
    def certificate_authority_configuration(
        self,
    ) -> AcmpcaCertificateAuthorityCertificateAuthorityConfiguration:
        '''certificate_authority_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#certificate_authority_configuration AcmpcaCertificateAuthority#certificate_authority_configuration}
        '''
        result = self._values.get("certificate_authority_configuration")
        assert result is not None, "Required property 'certificate_authority_configuration' is missing"
        return typing.cast(AcmpcaCertificateAuthorityCertificateAuthorityConfiguration, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#enabled AcmpcaCertificateAuthority#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#id AcmpcaCertificateAuthority#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_storage_security_standard(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#key_storage_security_standard AcmpcaCertificateAuthority#key_storage_security_standard}.'''
        result = self._values.get("key_storage_security_standard")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permanent_deletion_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#permanent_deletion_time_in_days AcmpcaCertificateAuthority#permanent_deletion_time_in_days}.'''
        result = self._values.get("permanent_deletion_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#region AcmpcaCertificateAuthority#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def revocation_configuration(
        self,
    ) -> typing.Optional["AcmpcaCertificateAuthorityRevocationConfiguration"]:
        '''revocation_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#revocation_configuration AcmpcaCertificateAuthority#revocation_configuration}
        '''
        result = self._values.get("revocation_configuration")
        return typing.cast(typing.Optional["AcmpcaCertificateAuthorityRevocationConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#tags AcmpcaCertificateAuthority#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#tags_all AcmpcaCertificateAuthority#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AcmpcaCertificateAuthorityTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#timeouts AcmpcaCertificateAuthority#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AcmpcaCertificateAuthorityTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#type AcmpcaCertificateAuthority#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def usage_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#usage_mode AcmpcaCertificateAuthority#usage_mode}.'''
        result = self._values.get("usage_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcmpcaCertificateAuthorityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityRevocationConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "crl_configuration": "crlConfiguration",
        "ocsp_configuration": "ocspConfiguration",
    },
)
class AcmpcaCertificateAuthorityRevocationConfiguration:
    def __init__(
        self,
        *,
        crl_configuration: typing.Optional[typing.Union["AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        ocsp_configuration: typing.Optional[typing.Union["AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param crl_configuration: crl_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#crl_configuration AcmpcaCertificateAuthority#crl_configuration}
        :param ocsp_configuration: ocsp_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#ocsp_configuration AcmpcaCertificateAuthority#ocsp_configuration}
        '''
        if isinstance(crl_configuration, dict):
            crl_configuration = AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration(**crl_configuration)
        if isinstance(ocsp_configuration, dict):
            ocsp_configuration = AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration(**ocsp_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e1958ad9b4f0ead23d86421f7829ad7995827fd5202ffd1b1ade992fddf9dd)
            check_type(argname="argument crl_configuration", value=crl_configuration, expected_type=type_hints["crl_configuration"])
            check_type(argname="argument ocsp_configuration", value=ocsp_configuration, expected_type=type_hints["ocsp_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if crl_configuration is not None:
            self._values["crl_configuration"] = crl_configuration
        if ocsp_configuration is not None:
            self._values["ocsp_configuration"] = ocsp_configuration

    @builtins.property
    def crl_configuration(
        self,
    ) -> typing.Optional["AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration"]:
        '''crl_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#crl_configuration AcmpcaCertificateAuthority#crl_configuration}
        '''
        result = self._values.get("crl_configuration")
        return typing.cast(typing.Optional["AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration"], result)

    @builtins.property
    def ocsp_configuration(
        self,
    ) -> typing.Optional["AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration"]:
        '''ocsp_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#ocsp_configuration AcmpcaCertificateAuthority#ocsp_configuration}
        '''
        result = self._values.get("ocsp_configuration")
        return typing.cast(typing.Optional["AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcmpcaCertificateAuthorityRevocationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "custom_cname": "customCname",
        "enabled": "enabled",
        "expiration_in_days": "expirationInDays",
        "s3_bucket_name": "s3BucketName",
        "s3_object_acl": "s3ObjectAcl",
    },
)
class AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration:
    def __init__(
        self,
        *,
        custom_cname: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expiration_in_days: typing.Optional[jsii.Number] = None,
        s3_bucket_name: typing.Optional[builtins.str] = None,
        s3_object_acl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_cname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#custom_cname AcmpcaCertificateAuthority#custom_cname}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#enabled AcmpcaCertificateAuthority#enabled}.
        :param expiration_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#expiration_in_days AcmpcaCertificateAuthority#expiration_in_days}.
        :param s3_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#s3_bucket_name AcmpcaCertificateAuthority#s3_bucket_name}.
        :param s3_object_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#s3_object_acl AcmpcaCertificateAuthority#s3_object_acl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294440f5ca63c782620adf6f797b60a3c408a01fcc17785afc556c45dd9ed642)
            check_type(argname="argument custom_cname", value=custom_cname, expected_type=type_hints["custom_cname"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expiration_in_days", value=expiration_in_days, expected_type=type_hints["expiration_in_days"])
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument s3_object_acl", value=s3_object_acl, expected_type=type_hints["s3_object_acl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_cname is not None:
            self._values["custom_cname"] = custom_cname
        if enabled is not None:
            self._values["enabled"] = enabled
        if expiration_in_days is not None:
            self._values["expiration_in_days"] = expiration_in_days
        if s3_bucket_name is not None:
            self._values["s3_bucket_name"] = s3_bucket_name
        if s3_object_acl is not None:
            self._values["s3_object_acl"] = s3_object_acl

    @builtins.property
    def custom_cname(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#custom_cname AcmpcaCertificateAuthority#custom_cname}.'''
        result = self._values.get("custom_cname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#enabled AcmpcaCertificateAuthority#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expiration_in_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#expiration_in_days AcmpcaCertificateAuthority#expiration_in_days}.'''
        result = self._values.get("expiration_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def s3_bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#s3_bucket_name AcmpcaCertificateAuthority#s3_bucket_name}.'''
        result = self._values.get("s3_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_object_acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#s3_object_acl AcmpcaCertificateAuthority#s3_object_acl}.'''
        result = self._values.get("s3_object_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AcmpcaCertificateAuthorityRevocationConfigurationCrlConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityRevocationConfigurationCrlConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fd3b171ffd89b96ab9a3ff26484e99885518562fb574f7bdb055bd8769cd9c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomCname")
    def reset_custom_cname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomCname", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetExpirationInDays")
    def reset_expiration_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationInDays", []))

    @jsii.member(jsii_name="resetS3BucketName")
    def reset_s3_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BucketName", []))

    @jsii.member(jsii_name="resetS3ObjectAcl")
    def reset_s3_object_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3ObjectAcl", []))

    @builtins.property
    @jsii.member(jsii_name="customCnameInput")
    def custom_cname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customCnameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationInDaysInput")
    def expiration_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expirationInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketNameInput")
    def s3_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3ObjectAclInput")
    def s3_object_acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3ObjectAclInput"))

    @builtins.property
    @jsii.member(jsii_name="customCname")
    def custom_cname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customCname"))

    @custom_cname.setter
    def custom_cname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30fcf2f4d5b468eb47158d2c6aa1da73b933ddaefeba0d36fd83f3015e6d93ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customCname", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__843bc1e13e86a63c3cd69ce4b3919407ed46a06a4ada7ddec360163f6b6b5bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationInDays")
    def expiration_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expirationInDays"))

    @expiration_in_days.setter
    def expiration_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a935ba764ebc0af97c1936c2a9e4c0d356e4845c8aa4de18c20ba60bd11ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketName"))

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f9b6276f955a191b0594956855547d244f0f4403ddd070f2968c25c976225c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3ObjectAcl")
    def s3_object_acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3ObjectAcl"))

    @s3_object_acl.setter
    def s3_object_acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f336ab9ba022d2d3b9ed9aea3a2a8fdb819cc912165008266e3f324b5986e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3ObjectAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration]:
        return typing.cast(typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4b7be9c850a73c4eeaff7c222af446d3c2429a615c18e5be8697a258b2f583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "ocsp_custom_cname": "ocspCustomCname"},
)
class AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        ocsp_custom_cname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#enabled AcmpcaCertificateAuthority#enabled}.
        :param ocsp_custom_cname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#ocsp_custom_cname AcmpcaCertificateAuthority#ocsp_custom_cname}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__196437b4827408f0dbd7fd783dc091100ad4ac7a9e04ffb039e81c7f31293b22)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument ocsp_custom_cname", value=ocsp_custom_cname, expected_type=type_hints["ocsp_custom_cname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if ocsp_custom_cname is not None:
            self._values["ocsp_custom_cname"] = ocsp_custom_cname

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#enabled AcmpcaCertificateAuthority#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def ocsp_custom_cname(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#ocsp_custom_cname AcmpcaCertificateAuthority#ocsp_custom_cname}.'''
        result = self._values.get("ocsp_custom_cname")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AcmpcaCertificateAuthorityRevocationConfigurationOcspConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityRevocationConfigurationOcspConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cc3c256403323654e57c275b502ffc318f83b9b577e13f8710061962dff8738)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOcspCustomCname")
    def reset_ocsp_custom_cname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOcspCustomCname", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ocspCustomCnameInput")
    def ocsp_custom_cname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ocspCustomCnameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f04b56a868d6123066c34a22087fd5ed6e0d37a2f41cfa5d19163136e99bd623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ocspCustomCname")
    def ocsp_custom_cname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ocspCustomCname"))

    @ocsp_custom_cname.setter
    def ocsp_custom_cname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a550772feabb3cefb3c07601a9673b4a14b666973f52da15ff958214137cc2b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ocspCustomCname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration]:
        return typing.cast(typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c549e830cf7bf01ed861d0151241a53cb26d668f5dc69618c0c234116253544f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AcmpcaCertificateAuthorityRevocationConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityRevocationConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__847a3d9a85824e17972364a9cafd58978f2f4862bfa4e438e0988d126bb5c5c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCrlConfiguration")
    def put_crl_configuration(
        self,
        *,
        custom_cname: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expiration_in_days: typing.Optional[jsii.Number] = None,
        s3_bucket_name: typing.Optional[builtins.str] = None,
        s3_object_acl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_cname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#custom_cname AcmpcaCertificateAuthority#custom_cname}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#enabled AcmpcaCertificateAuthority#enabled}.
        :param expiration_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#expiration_in_days AcmpcaCertificateAuthority#expiration_in_days}.
        :param s3_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#s3_bucket_name AcmpcaCertificateAuthority#s3_bucket_name}.
        :param s3_object_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#s3_object_acl AcmpcaCertificateAuthority#s3_object_acl}.
        '''
        value = AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration(
            custom_cname=custom_cname,
            enabled=enabled,
            expiration_in_days=expiration_in_days,
            s3_bucket_name=s3_bucket_name,
            s3_object_acl=s3_object_acl,
        )

        return typing.cast(None, jsii.invoke(self, "putCrlConfiguration", [value]))

    @jsii.member(jsii_name="putOcspConfiguration")
    def put_ocsp_configuration(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        ocsp_custom_cname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#enabled AcmpcaCertificateAuthority#enabled}.
        :param ocsp_custom_cname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#ocsp_custom_cname AcmpcaCertificateAuthority#ocsp_custom_cname}.
        '''
        value = AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration(
            enabled=enabled, ocsp_custom_cname=ocsp_custom_cname
        )

        return typing.cast(None, jsii.invoke(self, "putOcspConfiguration", [value]))

    @jsii.member(jsii_name="resetCrlConfiguration")
    def reset_crl_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrlConfiguration", []))

    @jsii.member(jsii_name="resetOcspConfiguration")
    def reset_ocsp_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOcspConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="crlConfiguration")
    def crl_configuration(
        self,
    ) -> AcmpcaCertificateAuthorityRevocationConfigurationCrlConfigurationOutputReference:
        return typing.cast(AcmpcaCertificateAuthorityRevocationConfigurationCrlConfigurationOutputReference, jsii.get(self, "crlConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="ocspConfiguration")
    def ocsp_configuration(
        self,
    ) -> AcmpcaCertificateAuthorityRevocationConfigurationOcspConfigurationOutputReference:
        return typing.cast(AcmpcaCertificateAuthorityRevocationConfigurationOcspConfigurationOutputReference, jsii.get(self, "ocspConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="crlConfigurationInput")
    def crl_configuration_input(
        self,
    ) -> typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration]:
        return typing.cast(typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration], jsii.get(self, "crlConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="ocspConfigurationInput")
    def ocsp_configuration_input(
        self,
    ) -> typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration]:
        return typing.cast(typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration], jsii.get(self, "ocspConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AcmpcaCertificateAuthorityRevocationConfiguration]:
        return typing.cast(typing.Optional[AcmpcaCertificateAuthorityRevocationConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AcmpcaCertificateAuthorityRevocationConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dceaa1743ec6319666bf4c14a80ac37704742c36d819c2a5d6f2e45c1f5ed836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class AcmpcaCertificateAuthorityTimeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#create AcmpcaCertificateAuthority#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba8f5dcb800cf88fba14dc45993a032cb962c2d75984630d671e2d78bd2821f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/acmpca_certificate_authority#create AcmpcaCertificateAuthority#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcmpcaCertificateAuthorityTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AcmpcaCertificateAuthorityTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.acmpcaCertificateAuthority.AcmpcaCertificateAuthorityTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf5b7cf59a2f3b91b1aee185d3275a9cf230314b83dd73d534b54cea887c451f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96696e6d2a885f92c36045626e8cef36f3c3e99b624b85d1960c2c427d47e63f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AcmpcaCertificateAuthorityTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AcmpcaCertificateAuthorityTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AcmpcaCertificateAuthorityTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1654e95160272a14a55fc6e219e5f32aa390cc6c002bdec96d283e2aa2577ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AcmpcaCertificateAuthority",
    "AcmpcaCertificateAuthorityCertificateAuthorityConfiguration",
    "AcmpcaCertificateAuthorityCertificateAuthorityConfigurationOutputReference",
    "AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject",
    "AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubjectOutputReference",
    "AcmpcaCertificateAuthorityConfig",
    "AcmpcaCertificateAuthorityRevocationConfiguration",
    "AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration",
    "AcmpcaCertificateAuthorityRevocationConfigurationCrlConfigurationOutputReference",
    "AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration",
    "AcmpcaCertificateAuthorityRevocationConfigurationOcspConfigurationOutputReference",
    "AcmpcaCertificateAuthorityRevocationConfigurationOutputReference",
    "AcmpcaCertificateAuthorityTimeouts",
    "AcmpcaCertificateAuthorityTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b3b5d9592aa732802f225c1a82fdb1e9380fd3e2248baa492c38afe390676cb6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    certificate_authority_configuration: typing.Union[AcmpcaCertificateAuthorityCertificateAuthorityConfiguration, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    key_storage_security_standard: typing.Optional[builtins.str] = None,
    permanent_deletion_time_in_days: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    revocation_configuration: typing.Optional[typing.Union[AcmpcaCertificateAuthorityRevocationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[AcmpcaCertificateAuthorityTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    usage_mode: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__10995fa79d98c0828e4db7e4a7ec4b560357bfeb7ebad805a7bea06727a5affb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fb8a38c615af55e12c0aca9523ceba527b64798f1db2a134b4ffb6db0dbc34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfccf4cce58a7bcc9ab0a6b23728434c31ae0677a75701163bef671dcdee3fe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963f01212c7aae6f728e8c9fb6382f6e147c356bf14f2936144f5c93a5a43dc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e4f252113aa1a088ebe348dac25cbf6adcb55b7360862267bffac658daaa6a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff956ed4175c0da1f7c928abe9744d65062378edfe13a5561b19123408b2ac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0ec898ae0d582648bf9ec9438af498cdd1c7cd7c7d96b042d635333261608c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fff978811265be6ef658e0d7ac2fce49e94c88966a30769b2d29a5c8946f59(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995cc072149cb7f7bfe8c55be8fe567a963f57e60966300f0646eedc34e14d0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5ca4a5ef88a582a061a887d6ffc9e891e5153554929a2e4f8b673a013978d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5b38a20068f231ce64482eb4b86ec57e26fc476978beee9591da5ee8cb48e6(
    *,
    key_algorithm: builtins.str,
    signing_algorithm: builtins.str,
    subject: typing.Union[AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5959cb0bd131623e643e9f8d1b51fb9653473d5b1813b1f7bd007bffd54d809c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b03c3dae126b88b5c452feffaee0210769eaefb29aad5bfb10082231d2e7cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a5ef5707fcc85230ac69e75f4bae9b58768baaefcb4045a56d071231ed0a0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3b87dfc7aa3c50993987b85dbf51b78cdb18ccc222bf2eb4119f0d8d155b82(
    value: typing.Optional[AcmpcaCertificateAuthorityCertificateAuthorityConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82bca375d558c08578ce0a0f01a1652bb824e6ade9a2e63a6acd2500c464ac0(
    *,
    common_name: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    distinguished_name_qualifier: typing.Optional[builtins.str] = None,
    generation_qualifier: typing.Optional[builtins.str] = None,
    given_name: typing.Optional[builtins.str] = None,
    initials: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    pseudonym: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    surname: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f10a6234a2eb1c77dbec113a1a204922e482df0bb3cf1de7a55bf09acacda1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5f60ee30deeda6c171e55c127cf9d51a90a87dbc21bf93b3bb1a6f2a839e7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bc9f2f093b14d915d8d4eed5e3ba4fef4ab6794d199c6161e93b073b0f0711(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee11929daf02d9ef0252b21aa9227c5c18d4dc5c250dcebec42c0f679804f7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ca5d6a98e60371a862af86e88f0e8ce8b5f635830be07d226ab66c1dd17e6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569d7759ad1c95149d6edc56fdba752b6ef501d1b84f42664844a0a27c9ae7c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b940150c1da96ed72d21018a4af33778c1972a7d8b8d45fad837c3923330c176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5392ee0568d277dfecf9faffbddb978d20e8b73fc1d3a628cb588d29747c3c64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a9f4601a2ba285e5cce541b8f87397bdbd9fe7ef390fb9a92f8b757b604c65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aef6bc04e0d46a1efc5bcdbc2ef22349f8c77da6c7af6bbcfecdc166e932ec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d97dcc14b68071e9541026bbf123de538073476c8b2443ad80c8f88af79c8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068df0ae9a5e685f347b5b9b4d196560a08239c4950087e3a719d501d87ed8bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c483fd249f2966afd18472f1b566bcffa03c62bbf086f46bf559cbde47f34011(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6132ca2c2f760fdfc6cf99338f9eb51f1497b19b7720ace3271fb32bd266bcc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edbbea2901b6168919b5eb7b5950fd69b9bad0433364462260d16e2da3a7954(
    value: typing.Optional[AcmpcaCertificateAuthorityCertificateAuthorityConfigurationSubject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1062319a5b40323e81ad1fb3c9f6f20958a3e3718594f0f56b3d1e493763274c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    certificate_authority_configuration: typing.Union[AcmpcaCertificateAuthorityCertificateAuthorityConfiguration, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    key_storage_security_standard: typing.Optional[builtins.str] = None,
    permanent_deletion_time_in_days: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    revocation_configuration: typing.Optional[typing.Union[AcmpcaCertificateAuthorityRevocationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[AcmpcaCertificateAuthorityTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    usage_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e1958ad9b4f0ead23d86421f7829ad7995827fd5202ffd1b1ade992fddf9dd(
    *,
    crl_configuration: typing.Optional[typing.Union[AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ocsp_configuration: typing.Optional[typing.Union[AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294440f5ca63c782620adf6f797b60a3c408a01fcc17785afc556c45dd9ed642(
    *,
    custom_cname: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expiration_in_days: typing.Optional[jsii.Number] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_object_acl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd3b171ffd89b96ab9a3ff26484e99885518562fb574f7bdb055bd8769cd9c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fcf2f4d5b468eb47158d2c6aa1da73b933ddaefeba0d36fd83f3015e6d93ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843bc1e13e86a63c3cd69ce4b3919407ed46a06a4ada7ddec360163f6b6b5bcf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a935ba764ebc0af97c1936c2a9e4c0d356e4845c8aa4de18c20ba60bd11ed4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f9b6276f955a191b0594956855547d244f0f4403ddd070f2968c25c976225c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f336ab9ba022d2d3b9ed9aea3a2a8fdb819cc912165008266e3f324b5986e61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4b7be9c850a73c4eeaff7c222af446d3c2429a615c18e5be8697a258b2f583(
    value: typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationCrlConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196437b4827408f0dbd7fd783dc091100ad4ac7a9e04ffb039e81c7f31293b22(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ocsp_custom_cname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc3c256403323654e57c275b502ffc318f83b9b577e13f8710061962dff8738(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04b56a868d6123066c34a22087fd5ed6e0d37a2f41cfa5d19163136e99bd623(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a550772feabb3cefb3c07601a9673b4a14b666973f52da15ff958214137cc2b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c549e830cf7bf01ed861d0151241a53cb26d668f5dc69618c0c234116253544f(
    value: typing.Optional[AcmpcaCertificateAuthorityRevocationConfigurationOcspConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847a3d9a85824e17972364a9cafd58978f2f4862bfa4e438e0988d126bb5c5c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dceaa1743ec6319666bf4c14a80ac37704742c36d819c2a5d6f2e45c1f5ed836(
    value: typing.Optional[AcmpcaCertificateAuthorityRevocationConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba8f5dcb800cf88fba14dc45993a032cb962c2d75984630d671e2d78bd2821f(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5b7cf59a2f3b91b1aee185d3275a9cf230314b83dd73d534b54cea887c451f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96696e6d2a885f92c36045626e8cef36f3c3e99b624b85d1960c2c427d47e63f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1654e95160272a14a55fc6e219e5f32aa390cc6c002bdec96d283e2aa2577ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AcmpcaCertificateAuthorityTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
