r'''
# `aws_redshift_idc_application`

Refer to the Terraform Registry for docs: [`aws_redshift_idc_application`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application).
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


class RedshiftIdcApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application aws_redshift_idc_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        iam_role_arn: builtins.str,
        idc_display_name: builtins.str,
        idc_instance_arn: builtins.str,
        redshift_idc_application_name: builtins.str,
        application_type: typing.Optional[builtins.str] = None,
        authorized_token_issuer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationAuthorizedTokenIssuer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        identity_namespace: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        service_integration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application aws_redshift_idc_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param iam_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#iam_role_arn RedshiftIdcApplication#iam_role_arn}.
        :param idc_display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#idc_display_name RedshiftIdcApplication#idc_display_name}.
        :param idc_instance_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#idc_instance_arn RedshiftIdcApplication#idc_instance_arn}.
        :param redshift_idc_application_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#redshift_idc_application_name RedshiftIdcApplication#redshift_idc_application_name}.
        :param application_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#application_type RedshiftIdcApplication#application_type}.
        :param authorized_token_issuer: authorized_token_issuer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorized_token_issuer RedshiftIdcApplication#authorized_token_issuer}
        :param identity_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#identity_namespace RedshiftIdcApplication#identity_namespace}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#region RedshiftIdcApplication#region}
        :param service_integration: service_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#service_integration RedshiftIdcApplication#service_integration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#tags RedshiftIdcApplication#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa1f42b05ea6fdc39c774248c0a5c5e379cce1b32189baca5414874be6ae506)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = RedshiftIdcApplicationConfig(
            iam_role_arn=iam_role_arn,
            idc_display_name=idc_display_name,
            idc_instance_arn=idc_instance_arn,
            redshift_idc_application_name=redshift_idc_application_name,
            application_type=application_type,
            authorized_token_issuer=authorized_token_issuer,
            identity_namespace=identity_namespace,
            region=region,
            service_integration=service_integration,
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
        '''Generates CDKTF code for importing a RedshiftIdcApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RedshiftIdcApplication to import.
        :param import_from_id: The id of the existing RedshiftIdcApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RedshiftIdcApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a71653e93d3d4ba131d479cb3521708197f83e4022955eefca404ddc7042079)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthorizedTokenIssuer")
    def put_authorized_token_issuer(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationAuthorizedTokenIssuer", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247e1536c6cc5b715bb7db0ae0b5fb0745547a4740bbe719855345f4efa28016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthorizedTokenIssuer", [value]))

    @jsii.member(jsii_name="putServiceIntegration")
    def put_service_integration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f83d795c70de9a5a9034163d60aed42fee05ee2d9ff89a46a738fffa142c9ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServiceIntegration", [value]))

    @jsii.member(jsii_name="resetApplicationType")
    def reset_application_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationType", []))

    @jsii.member(jsii_name="resetAuthorizedTokenIssuer")
    def reset_authorized_token_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedTokenIssuer", []))

    @jsii.member(jsii_name="resetIdentityNamespace")
    def reset_identity_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityNamespace", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetServiceIntegration")
    def reset_service_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceIntegration", []))

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
    @jsii.member(jsii_name="authorizedTokenIssuer")
    def authorized_token_issuer(
        self,
    ) -> "RedshiftIdcApplicationAuthorizedTokenIssuerList":
        return typing.cast("RedshiftIdcApplicationAuthorizedTokenIssuerList", jsii.get(self, "authorizedTokenIssuer"))

    @builtins.property
    @jsii.member(jsii_name="idcManagedApplicationArn")
    def idc_managed_application_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idcManagedApplicationArn"))

    @builtins.property
    @jsii.member(jsii_name="redshiftIdcApplicationArn")
    def redshift_idc_application_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redshiftIdcApplicationArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceIntegration")
    def service_integration(self) -> "RedshiftIdcApplicationServiceIntegrationList":
        return typing.cast("RedshiftIdcApplicationServiceIntegrationList", jsii.get(self, "serviceIntegration"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="applicationTypeInput")
    def application_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedTokenIssuerInput")
    def authorized_token_issuer_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationAuthorizedTokenIssuer"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationAuthorizedTokenIssuer"]]], jsii.get(self, "authorizedTokenIssuerInput"))

    @builtins.property
    @jsii.member(jsii_name="iamRoleArnInput")
    def iam_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="idcDisplayNameInput")
    def idc_display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idcDisplayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idcInstanceArnInput")
    def idc_instance_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idcInstanceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="identityNamespaceInput")
    def identity_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftIdcApplicationNameInput")
    def redshift_idc_application_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redshiftIdcApplicationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceIntegrationInput")
    def service_integration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegration"]]], jsii.get(self, "serviceIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationType")
    def application_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationType"))

    @application_type.setter
    def application_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb4bd33b90b118fcec37e9e2828b07efd296d21cf3d79204c7d7e8d1978c5961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671a0b639e724fe6c57b3e721cef7f65ff8e627f1d25b3af7c5b13988f35c7c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idcDisplayName")
    def idc_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idcDisplayName"))

    @idc_display_name.setter
    def idc_display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52ca57115413474d6e91128870eb43b33854be53d1823286fa7382047930507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idcDisplayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idcInstanceArn")
    def idc_instance_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idcInstanceArn"))

    @idc_instance_arn.setter
    def idc_instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f5e7efd1f8b517466a40b03143f809a379819dd38391c2cb8b8c4d300ac609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idcInstanceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityNamespace")
    def identity_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityNamespace"))

    @identity_namespace.setter
    def identity_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e45b58e772606dae5f27b549eb61c224feb01290b6a3abdf64dfacf1609813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redshiftIdcApplicationName")
    def redshift_idc_application_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redshiftIdcApplicationName"))

    @redshift_idc_application_name.setter
    def redshift_idc_application_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2dfc44bbb9167385d2a66d096e11a07ae643a166dd01256a7ea91201a71402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redshiftIdcApplicationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cad34d7201fda9aac88d1e01e7885746f4c9fd2662595a6af75f6a3ccac730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b33929aa1a704bb9466b1d968dc73a68498d22e868af4971e95882e3925659a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationAuthorizedTokenIssuer",
    jsii_struct_bases=[],
    name_mapping={
        "authorized_audiences_list": "authorizedAudiencesList",
        "trusted_token_issuer_arn": "trustedTokenIssuerArn",
    },
)
class RedshiftIdcApplicationAuthorizedTokenIssuer:
    def __init__(
        self,
        *,
        authorized_audiences_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_token_issuer_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorized_audiences_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorized_audiences_list RedshiftIdcApplication#authorized_audiences_list}.
        :param trusted_token_issuer_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#trusted_token_issuer_arn RedshiftIdcApplication#trusted_token_issuer_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47cbfef11f1bf67bf3ec520b2f7515612e0bc73e1c8f2607f74c2dfdaf8c0c2)
            check_type(argname="argument authorized_audiences_list", value=authorized_audiences_list, expected_type=type_hints["authorized_audiences_list"])
            check_type(argname="argument trusted_token_issuer_arn", value=trusted_token_issuer_arn, expected_type=type_hints["trusted_token_issuer_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorized_audiences_list is not None:
            self._values["authorized_audiences_list"] = authorized_audiences_list
        if trusted_token_issuer_arn is not None:
            self._values["trusted_token_issuer_arn"] = trusted_token_issuer_arn

    @builtins.property
    def authorized_audiences_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorized_audiences_list RedshiftIdcApplication#authorized_audiences_list}.'''
        result = self._values.get("authorized_audiences_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trusted_token_issuer_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#trusted_token_issuer_arn RedshiftIdcApplication#trusted_token_issuer_arn}.'''
        result = self._values.get("trusted_token_issuer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftIdcApplicationAuthorizedTokenIssuer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedshiftIdcApplicationAuthorizedTokenIssuerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationAuthorizedTokenIssuerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23883834cae8be4e69c541bd8daffe830c2f5f4ffd7814de0f50231a4048adbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedshiftIdcApplicationAuthorizedTokenIssuerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118a44081b88077ffd6588e2232f3d05c6e911950f31262121eb181617cf1498)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedshiftIdcApplicationAuthorizedTokenIssuerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3132ed7b5e36db95721554563053c97cd03aabb2fded0790fed4a045c4988643)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acd0ef29621e2ef20757f5790a12c0e91b6e4c0fc72f416a100d651d96c10588)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b71517f803e16d1245f3d36d76dbeb56088475f43de5e1d186598a233f0ea4a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationAuthorizedTokenIssuer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationAuthorizedTokenIssuer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationAuthorizedTokenIssuer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7127dc419cc5e7e1e044d8dc1d846f754dc16cbc136654947549611a7b9c281d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationAuthorizedTokenIssuerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationAuthorizedTokenIssuerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4df7d78661996587ecd50a0afc24518bbf9e569c6219dd119912fcb4691ae02f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAuthorizedAudiencesList")
    def reset_authorized_audiences_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedAudiencesList", []))

    @jsii.member(jsii_name="resetTrustedTokenIssuerArn")
    def reset_trusted_token_issuer_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedTokenIssuerArn", []))

    @builtins.property
    @jsii.member(jsii_name="authorizedAudiencesListInput")
    def authorized_audiences_list_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "authorizedAudiencesListInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedTokenIssuerArnInput")
    def trusted_token_issuer_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustedTokenIssuerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedAudiencesList")
    def authorized_audiences_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "authorizedAudiencesList"))

    @authorized_audiences_list.setter
    def authorized_audiences_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8684c3734317e89a0d50101a2aac9af23dec728d212c86e674b92f04bccd23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedAudiencesList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedTokenIssuerArn")
    def trusted_token_issuer_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustedTokenIssuerArn"))

    @trusted_token_issuer_arn.setter
    def trusted_token_issuer_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22590dccd81e6eb2b492e31cf67a425ff628226fea137c7729751f09178db5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedTokenIssuerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationAuthorizedTokenIssuer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationAuthorizedTokenIssuer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationAuthorizedTokenIssuer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2caa97a10c9a184a7b8af50f421204a2f392673adbb695045567d342d298386c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "iam_role_arn": "iamRoleArn",
        "idc_display_name": "idcDisplayName",
        "idc_instance_arn": "idcInstanceArn",
        "redshift_idc_application_name": "redshiftIdcApplicationName",
        "application_type": "applicationType",
        "authorized_token_issuer": "authorizedTokenIssuer",
        "identity_namespace": "identityNamespace",
        "region": "region",
        "service_integration": "serviceIntegration",
        "tags": "tags",
    },
)
class RedshiftIdcApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        iam_role_arn: builtins.str,
        idc_display_name: builtins.str,
        idc_instance_arn: builtins.str,
        redshift_idc_application_name: builtins.str,
        application_type: typing.Optional[builtins.str] = None,
        authorized_token_issuer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationAuthorizedTokenIssuer, typing.Dict[builtins.str, typing.Any]]]]] = None,
        identity_namespace: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        service_integration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegration", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param iam_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#iam_role_arn RedshiftIdcApplication#iam_role_arn}.
        :param idc_display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#idc_display_name RedshiftIdcApplication#idc_display_name}.
        :param idc_instance_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#idc_instance_arn RedshiftIdcApplication#idc_instance_arn}.
        :param redshift_idc_application_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#redshift_idc_application_name RedshiftIdcApplication#redshift_idc_application_name}.
        :param application_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#application_type RedshiftIdcApplication#application_type}.
        :param authorized_token_issuer: authorized_token_issuer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorized_token_issuer RedshiftIdcApplication#authorized_token_issuer}
        :param identity_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#identity_namespace RedshiftIdcApplication#identity_namespace}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#region RedshiftIdcApplication#region}
        :param service_integration: service_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#service_integration RedshiftIdcApplication#service_integration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#tags RedshiftIdcApplication#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a0f3550ce8ea8b1c1a52dc9221720e5fbcec8ebe38038d1a55fb72c2c07f5b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument idc_display_name", value=idc_display_name, expected_type=type_hints["idc_display_name"])
            check_type(argname="argument idc_instance_arn", value=idc_instance_arn, expected_type=type_hints["idc_instance_arn"])
            check_type(argname="argument redshift_idc_application_name", value=redshift_idc_application_name, expected_type=type_hints["redshift_idc_application_name"])
            check_type(argname="argument application_type", value=application_type, expected_type=type_hints["application_type"])
            check_type(argname="argument authorized_token_issuer", value=authorized_token_issuer, expected_type=type_hints["authorized_token_issuer"])
            check_type(argname="argument identity_namespace", value=identity_namespace, expected_type=type_hints["identity_namespace"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument service_integration", value=service_integration, expected_type=type_hints["service_integration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "iam_role_arn": iam_role_arn,
            "idc_display_name": idc_display_name,
            "idc_instance_arn": idc_instance_arn,
            "redshift_idc_application_name": redshift_idc_application_name,
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
        if application_type is not None:
            self._values["application_type"] = application_type
        if authorized_token_issuer is not None:
            self._values["authorized_token_issuer"] = authorized_token_issuer
        if identity_namespace is not None:
            self._values["identity_namespace"] = identity_namespace
        if region is not None:
            self._values["region"] = region
        if service_integration is not None:
            self._values["service_integration"] = service_integration
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
    def iam_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#iam_role_arn RedshiftIdcApplication#iam_role_arn}.'''
        result = self._values.get("iam_role_arn")
        assert result is not None, "Required property 'iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def idc_display_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#idc_display_name RedshiftIdcApplication#idc_display_name}.'''
        result = self._values.get("idc_display_name")
        assert result is not None, "Required property 'idc_display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def idc_instance_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#idc_instance_arn RedshiftIdcApplication#idc_instance_arn}.'''
        result = self._values.get("idc_instance_arn")
        assert result is not None, "Required property 'idc_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def redshift_idc_application_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#redshift_idc_application_name RedshiftIdcApplication#redshift_idc_application_name}.'''
        result = self._values.get("redshift_idc_application_name")
        assert result is not None, "Required property 'redshift_idc_application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#application_type RedshiftIdcApplication#application_type}.'''
        result = self._values.get("application_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorized_token_issuer(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationAuthorizedTokenIssuer]]]:
        '''authorized_token_issuer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorized_token_issuer RedshiftIdcApplication#authorized_token_issuer}
        '''
        result = self._values.get("authorized_token_issuer")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationAuthorizedTokenIssuer]]], result)

    @builtins.property
    def identity_namespace(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#identity_namespace RedshiftIdcApplication#identity_namespace}.'''
        result = self._values.get("identity_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#region RedshiftIdcApplication#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_integration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegration"]]]:
        '''service_integration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#service_integration RedshiftIdcApplication#service_integration}
        '''
        result = self._values.get("service_integration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegration"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#tags RedshiftIdcApplication#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftIdcApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegration",
    jsii_struct_bases=[],
    name_mapping={
        "lake_formation": "lakeFormation",
        "redshift": "redshift",
        "s3_access_grants": "s3AccessGrants",
    },
)
class RedshiftIdcApplicationServiceIntegration:
    def __init__(
        self,
        *,
        lake_formation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegrationLakeFormation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redshift: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegrationRedshift", typing.Dict[builtins.str, typing.Any]]]]] = None,
        s3_access_grants: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegrationS3AccessGrants", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param lake_formation: lake_formation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#lake_formation RedshiftIdcApplication#lake_formation}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#redshift RedshiftIdcApplication#redshift}
        :param s3_access_grants: s3_access_grants block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#s3_access_grants RedshiftIdcApplication#s3_access_grants}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae0e134ea7d541ae4983bc3fd066689666bbfb3bfe43fc425c5f2239604fd2e)
            check_type(argname="argument lake_formation", value=lake_formation, expected_type=type_hints["lake_formation"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument s3_access_grants", value=s3_access_grants, expected_type=type_hints["s3_access_grants"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lake_formation is not None:
            self._values["lake_formation"] = lake_formation
        if redshift is not None:
            self._values["redshift"] = redshift
        if s3_access_grants is not None:
            self._values["s3_access_grants"] = s3_access_grants

    @builtins.property
    def lake_formation(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationLakeFormation"]]]:
        '''lake_formation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#lake_formation RedshiftIdcApplication#lake_formation}
        '''
        result = self._values.get("lake_formation")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationLakeFormation"]]], result)

    @builtins.property
    def redshift(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationRedshift"]]]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#redshift RedshiftIdcApplication#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationRedshift"]]], result)

    @builtins.property
    def s3_access_grants(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationS3AccessGrants"]]]:
        '''s3_access_grants block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#s3_access_grants RedshiftIdcApplication#s3_access_grants}
        '''
        result = self._values.get("s3_access_grants")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationS3AccessGrants"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftIdcApplicationServiceIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationLakeFormation",
    jsii_struct_bases=[],
    name_mapping={"lake_formation_query": "lakeFormationQuery"},
)
class RedshiftIdcApplicationServiceIntegrationLakeFormation:
    def __init__(
        self,
        *,
        lake_formation_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param lake_formation_query: lake_formation_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#lake_formation_query RedshiftIdcApplication#lake_formation_query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2d0ea1c69893fd3568941efe8ca2a1de81ac225d6c70bccc8844f25aca910f)
            check_type(argname="argument lake_formation_query", value=lake_formation_query, expected_type=type_hints["lake_formation_query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lake_formation_query is not None:
            self._values["lake_formation_query"] = lake_formation_query

    @builtins.property
    def lake_formation_query(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery"]]]:
        '''lake_formation_query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#lake_formation_query RedshiftIdcApplication#lake_formation_query}
        '''
        result = self._values.get("lake_formation_query")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftIdcApplicationServiceIntegrationLakeFormation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery",
    jsii_struct_bases=[],
    name_mapping={"authorization": "authorization"},
)
class RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery:
    def __init__(self, *, authorization: builtins.str) -> None:
        '''
        :param authorization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorization RedshiftIdcApplication#authorization}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a80fe4d740ecd90800e0d5c883d2cfb2f2f297b62eddf2cea19fbba882bc1f06)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization": authorization,
        }

    @builtins.property
    def authorization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorization RedshiftIdcApplication#authorization}.'''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf50d53dbd76c29a761888f455c0fa33af5aef34943d2621ff355e7ed7c6e928)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ebf3dfd8fb56eee9bec3d970d20664e4bc1fd8cafe0726adc28773ca41567d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb17b55c987edce0f281ddc25495a41ecbf126054386bf4cfe0b9a931d0d9631)
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
            type_hints = typing.get_type_hints(_typecheckingstub__901af5a18f689bab4a21ed737deb099374ecaf4dc5a9b2cf5408d97f5975d83b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdec8122849feefc5176a2258bce2d1399de9928013431f78bbbb730d3d0eada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a39e74a5cd1f8e2ad6119ba86be80d9c35d19c9b4f68cd8a878a45c3cb560f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dd7d8c05d61fc7ed15e2a88dad05a6e8e2558e1854943df0b3ee0033a7061c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorization"))

    @authorization.setter
    def authorization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794b3c422d72916234a52f95d4f6be4957e33bddef3bab146feead3daca6087e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0b3a5b159238db51eaab503578e40fd0010a1498313b93d0035348742b1c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationServiceIntegrationLakeFormationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationLakeFormationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16b39dc92dc4873e93648de51d6d77d8ccc1c0058f603ae85317de0fd3fe90b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedshiftIdcApplicationServiceIntegrationLakeFormationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb697a0121cd7d3723dacd85f7308d4c96bf95b3adad2dffd5e7fd4d16c72e8d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedshiftIdcApplicationServiceIntegrationLakeFormationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ed0d62a509ce5a1ad6cc9c9617736ded9d96de8bf0ee9aa1bd009153864936)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74cebf976098dbd87d75bf74e5691e2f7e9cd8a6304016e155e866ca5cd3ca3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fd0fcf334483dc77a84a65970ddbedf3bfa12f5415e4c78fc3ffd424af40073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fcb071f95fb93ba3bc68170c400a612106dc8a089c8eb3a4711987904bf93d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationServiceIntegrationLakeFormationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationLakeFormationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a10530a42832b57c23f2b91a1e265485c70bd357e76b84b09dd3850728af1a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLakeFormationQuery")
    def put_lake_formation_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6f4bb30fa7a850bcc1d43cf239f21df72114c454871e6f311d8ad20aab513d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLakeFormationQuery", [value]))

    @jsii.member(jsii_name="resetLakeFormationQuery")
    def reset_lake_formation_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLakeFormationQuery", []))

    @builtins.property
    @jsii.member(jsii_name="lakeFormationQuery")
    def lake_formation_query(
        self,
    ) -> RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQueryList:
        return typing.cast(RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQueryList, jsii.get(self, "lakeFormationQuery"))

    @builtins.property
    @jsii.member(jsii_name="lakeFormationQueryInput")
    def lake_formation_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery]]], jsii.get(self, "lakeFormationQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationLakeFormation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationLakeFormation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationLakeFormation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000be6dd90377298a7af5881a40c0fb8942310cb25b0ad01442b256666748ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationServiceIntegrationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8178c52ad66bc34da0323cba6f66756a88dc6f413c082aae826e7986cf52dc8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedshiftIdcApplicationServiceIntegrationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbaed67a39dddb6da375ebe61fd2f709d1694bba51053036d6ef06973bfdf445)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedshiftIdcApplicationServiceIntegrationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdd4c433c3ee9163b4f7c82decc78917ad41343e4734f4cf2514160bd33574c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d2925cd7f389eb0252abdc9f2abd9427bbfbce1ac9457309ada3165e1e60df4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e65225218544246332f61fa48c4ff224fc3a9fb2474b1af0326b2758fa521f65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff23476caa88b4527fc8f584f8dccf3db1e35ab54f50fc783badfa821e3573ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationServiceIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__507423ae8bc1c30f3db73a38333b3f825b94d6f6d2c55f738306a543db684239)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLakeFormation")
    def put_lake_formation(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationLakeFormation, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf05078d4572b34f0881ff1c5ccd08a1c2cbd4590cb91ae39a4ea4ab7fb935aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLakeFormation", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegrationRedshift", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56287cb1c1059d14e8c6eb080a46a9061bfdcf3c8b2b1674b9071e19430b59a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putS3AccessGrants")
    def put_s3_access_grants(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegrationS3AccessGrants", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9a71d092b3755ab53721837c5b846c7b60441cd027f5bddc37ef93f6e2cf46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3AccessGrants", [value]))

    @jsii.member(jsii_name="resetLakeFormation")
    def reset_lake_formation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLakeFormation", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetS3AccessGrants")
    def reset_s3_access_grants(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3AccessGrants", []))

    @builtins.property
    @jsii.member(jsii_name="lakeFormation")
    def lake_formation(
        self,
    ) -> RedshiftIdcApplicationServiceIntegrationLakeFormationList:
        return typing.cast(RedshiftIdcApplicationServiceIntegrationLakeFormationList, jsii.get(self, "lakeFormation"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(self) -> "RedshiftIdcApplicationServiceIntegrationRedshiftList":
        return typing.cast("RedshiftIdcApplicationServiceIntegrationRedshiftList", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="s3AccessGrants")
    def s3_access_grants(
        self,
    ) -> "RedshiftIdcApplicationServiceIntegrationS3AccessGrantsList":
        return typing.cast("RedshiftIdcApplicationServiceIntegrationS3AccessGrantsList", jsii.get(self, "s3AccessGrants"))

    @builtins.property
    @jsii.member(jsii_name="lakeFormationInput")
    def lake_formation_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormation]]], jsii.get(self, "lakeFormationInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationRedshift"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationRedshift"]]], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="s3AccessGrantsInput")
    def s3_access_grants_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationS3AccessGrants"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationS3AccessGrants"]]], jsii.get(self, "s3AccessGrantsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af233aa3b811c02e57f6a20d832f6a9009969673fca0bee6bcc0a3b8d1576be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationRedshift",
    jsii_struct_bases=[],
    name_mapping={"connect": "connect"},
)
class RedshiftIdcApplicationServiceIntegrationRedshift:
    def __init__(
        self,
        *,
        connect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegrationRedshiftConnect", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connect: connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#connect RedshiftIdcApplication#connect}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b012d8598e676d9b2053bff11c5ac48d45403d533ca39dc48b077a5d22a2bf4)
            check_type(argname="argument connect", value=connect, expected_type=type_hints["connect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connect is not None:
            self._values["connect"] = connect

    @builtins.property
    def connect(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationRedshiftConnect"]]]:
        '''connect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#connect RedshiftIdcApplication#connect}
        '''
        result = self._values.get("connect")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationRedshiftConnect"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftIdcApplicationServiceIntegrationRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationRedshiftConnect",
    jsii_struct_bases=[],
    name_mapping={"authorization": "authorization"},
)
class RedshiftIdcApplicationServiceIntegrationRedshiftConnect:
    def __init__(self, *, authorization: builtins.str) -> None:
        '''
        :param authorization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorization RedshiftIdcApplication#authorization}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00138a9fdadc25e5a92f25eb6e1b562090dea2dc0d06e316d07cf2e5e1f6d98)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization": authorization,
        }

    @builtins.property
    def authorization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorization RedshiftIdcApplication#authorization}.'''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftIdcApplicationServiceIntegrationRedshiftConnect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedshiftIdcApplicationServiceIntegrationRedshiftConnectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationRedshiftConnectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__074f50ac45b4908b8570dc7f01580f07e530497237a061a5dbb6728e147b6533)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedshiftIdcApplicationServiceIntegrationRedshiftConnectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd116bbc55e0098baa50d3648e9ff827fd4d763c623e7a96de34707d0f2301ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedshiftIdcApplicationServiceIntegrationRedshiftConnectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08635182d1d88dc1c346c9a93aa108229990374d80e9082bb8b3a3b13ff53bc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f957f5acb7aecc0e9838713e20a3eb713fd217dfe5cf73cf17f41b48d68bf0eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8433268d66166eb370314ce28f1619915fc43ca0203bf2fda20e40554e2aa98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationRedshiftConnect]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationRedshiftConnect]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationRedshiftConnect]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1c71a9fa3e4c40866685e212c89840d6441fd22a3eddba324b438daba8b354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationServiceIntegrationRedshiftConnectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationRedshiftConnectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53fc72a03eb5fa54e0545c59a70005801458073c8a2f8104ff3b3e631a1b5300)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorization"))

    @authorization.setter
    def authorization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea3e49bfbf2821fd70a0d34b2d769357722f8e9db8d2bcd9ad0694cbcc766d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationRedshiftConnect]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationRedshiftConnect]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationRedshiftConnect]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ed405fe2e4da800f0655144148c0e9c3a6ec2423e383800d6fc32c2cbf91a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationServiceIntegrationRedshiftList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationRedshiftList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75b6c6d416a915de51c4034f6307f5cc446a4788b852d2e9fa435f1355121b1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedshiftIdcApplicationServiceIntegrationRedshiftOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655db885043e0b132eaa7271c190d716dd36f31220d1b31cf987c220fd8a3178)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedshiftIdcApplicationServiceIntegrationRedshiftOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb4e3c8a8c79f2afd030c64b0c0dbd5b200e942bfbebdf8649cfd24c7a95ffe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb86f1eda73dddaaa6af8895c0a7c9bc902bf3439363bf07a62f9192f84f129f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f32b5564e7f9d6056594b9a40916188fb29df10d5040183e1bce8f78c16c1e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationRedshift]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationRedshift]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationRedshift]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61cdba5ef82bb48b600a09e15b35ed3e6fa1c42dc6761ed66539e7997e25be38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationServiceIntegrationRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__718fe8b98ba4122f725c60190b7d22c2d88b9bcf58256167dd4bbeee06c6de28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConnect")
    def put_connect(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationRedshiftConnect, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dba7f583987211402d0a6dcd955ec2d9dbbde4a7c7882504f6cfa36bf9a04c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnect", [value]))

    @jsii.member(jsii_name="resetConnect")
    def reset_connect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnect", []))

    @builtins.property
    @jsii.member(jsii_name="connect")
    def connect(self) -> RedshiftIdcApplicationServiceIntegrationRedshiftConnectList:
        return typing.cast(RedshiftIdcApplicationServiceIntegrationRedshiftConnectList, jsii.get(self, "connect"))

    @builtins.property
    @jsii.member(jsii_name="connectInput")
    def connect_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationRedshiftConnect]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationRedshiftConnect]]], jsii.get(self, "connectInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationRedshift]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationRedshift]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationRedshift]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea77b364b8658354be542b8fda06c8350147814350335e94a1f11f31f7c5e049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationS3AccessGrants",
    jsii_struct_bases=[],
    name_mapping={"read_write_access": "readWriteAccess"},
)
class RedshiftIdcApplicationServiceIntegrationS3AccessGrants:
    def __init__(
        self,
        *,
        read_write_access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param read_write_access: read_write_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#read_write_access RedshiftIdcApplication#read_write_access}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9528e821fb66f5dc1ada9f9567c050d7c01d4f8abd4188c53336b035083247e)
            check_type(argname="argument read_write_access", value=read_write_access, expected_type=type_hints["read_write_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read_write_access is not None:
            self._values["read_write_access"] = read_write_access

    @builtins.property
    def read_write_access(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess"]]]:
        '''read_write_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#read_write_access RedshiftIdcApplication#read_write_access}
        '''
        result = self._values.get("read_write_access")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftIdcApplicationServiceIntegrationS3AccessGrants(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedshiftIdcApplicationServiceIntegrationS3AccessGrantsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationS3AccessGrantsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbc0b5aa0961bc2fcbee743bd022ac827ab206836dfaa853a2841a65fa1c779a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedshiftIdcApplicationServiceIntegrationS3AccessGrantsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b29414adf640bed23666ba5b1dd64e89a5bde60cb9c10670234bfb46b1cc03b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedshiftIdcApplicationServiceIntegrationS3AccessGrantsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f54dfd9fdfc2c94932aef5a7bb2f16617c5a6c9de7648e686cace945bc7c5cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa45435a07aafe81930c31bc23dbebdfa52befdd465f4c90455880a3e493fe14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b53b498a1ef37f3bfcb482895e51f2f799ba7d79a7831fb2f1d95a605a0dbfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationS3AccessGrants]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationS3AccessGrants]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationS3AccessGrants]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6fc0b7c517b07fdc38aeeba30145008f545ef0d91a06070f57efe64cbc75979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationServiceIntegrationS3AccessGrantsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationS3AccessGrantsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9241874a657e6db67add8ec6da9e127329838135486146b22092238c4c2bd27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putReadWriteAccess")
    def put_read_write_access(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59de79c64b1879a5e95e274d431cea202e989bfccdcb7c4af9a953fe6e22dac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReadWriteAccess", [value]))

    @jsii.member(jsii_name="resetReadWriteAccess")
    def reset_read_write_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadWriteAccess", []))

    @builtins.property
    @jsii.member(jsii_name="readWriteAccess")
    def read_write_access(
        self,
    ) -> "RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccessList":
        return typing.cast("RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccessList", jsii.get(self, "readWriteAccess"))

    @builtins.property
    @jsii.member(jsii_name="readWriteAccessInput")
    def read_write_access_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess"]]], jsii.get(self, "readWriteAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationS3AccessGrants]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationS3AccessGrants]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationS3AccessGrants]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffaae795ef3fe19bd83d60d92316422c54de3c7daf61debf9793e9658ff8636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess",
    jsii_struct_bases=[],
    name_mapping={"authorization": "authorization"},
)
class RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess:
    def __init__(self, *, authorization: builtins.str) -> None:
        '''
        :param authorization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorization RedshiftIdcApplication#authorization}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489fd825c5947f11473001619c72325388a0b15d553f855d4a06b1dd026a0a34)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization": authorization,
        }

    @builtins.property
    def authorization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/redshift_idc_application#authorization RedshiftIdcApplication#authorization}.'''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccessList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccessList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa3e349314ba4a91bb23cb5d772ca4cf9b46afaa5968c9cc952674401dd30f74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccessOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c9a764cd1135863f54cffe7633a927f29328e27231c9ac0bbc1f43664bf1a5f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccessOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9eafc94246a52c623d070938246a373c7d422e04ac958c11a7c7005e307d015)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b894416928a2ffc7eebd34e91f690a53307c5258e6bf9e02a685e98f2c144c32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c28718d034a5e31b9799ee61f9bb494c8760385d9ca8cbf62e31ddf06dfbb4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb0054582ab0950495bd041a99c704180c2e08a9820c921db243c5ec3b31665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.redshiftIdcApplication.RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b50a0e77f84aac89fe147a08963938918dc0f9b70518e0a387df7cda2e9af223)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorization"))

    @authorization.setter
    def authorization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2566d806ad7634058b53cbcfed5bc6a105de4c62f9df542cf1f99db31c57bada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32054914fbb95553484696987cf17c3fe8d6eeac9c53d5e884b7af365909906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RedshiftIdcApplication",
    "RedshiftIdcApplicationAuthorizedTokenIssuer",
    "RedshiftIdcApplicationAuthorizedTokenIssuerList",
    "RedshiftIdcApplicationAuthorizedTokenIssuerOutputReference",
    "RedshiftIdcApplicationConfig",
    "RedshiftIdcApplicationServiceIntegration",
    "RedshiftIdcApplicationServiceIntegrationLakeFormation",
    "RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery",
    "RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQueryList",
    "RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQueryOutputReference",
    "RedshiftIdcApplicationServiceIntegrationLakeFormationList",
    "RedshiftIdcApplicationServiceIntegrationLakeFormationOutputReference",
    "RedshiftIdcApplicationServiceIntegrationList",
    "RedshiftIdcApplicationServiceIntegrationOutputReference",
    "RedshiftIdcApplicationServiceIntegrationRedshift",
    "RedshiftIdcApplicationServiceIntegrationRedshiftConnect",
    "RedshiftIdcApplicationServiceIntegrationRedshiftConnectList",
    "RedshiftIdcApplicationServiceIntegrationRedshiftConnectOutputReference",
    "RedshiftIdcApplicationServiceIntegrationRedshiftList",
    "RedshiftIdcApplicationServiceIntegrationRedshiftOutputReference",
    "RedshiftIdcApplicationServiceIntegrationS3AccessGrants",
    "RedshiftIdcApplicationServiceIntegrationS3AccessGrantsList",
    "RedshiftIdcApplicationServiceIntegrationS3AccessGrantsOutputReference",
    "RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess",
    "RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccessList",
    "RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccessOutputReference",
]

publication.publish()

def _typecheckingstub__efa1f42b05ea6fdc39c774248c0a5c5e379cce1b32189baca5414874be6ae506(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    iam_role_arn: builtins.str,
    idc_display_name: builtins.str,
    idc_instance_arn: builtins.str,
    redshift_idc_application_name: builtins.str,
    application_type: typing.Optional[builtins.str] = None,
    authorized_token_issuer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationAuthorizedTokenIssuer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    identity_namespace: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    service_integration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegration, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__3a71653e93d3d4ba131d479cb3521708197f83e4022955eefca404ddc7042079(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247e1536c6cc5b715bb7db0ae0b5fb0745547a4740bbe719855345f4efa28016(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationAuthorizedTokenIssuer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f83d795c70de9a5a9034163d60aed42fee05ee2d9ff89a46a738fffa142c9ab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4bd33b90b118fcec37e9e2828b07efd296d21cf3d79204c7d7e8d1978c5961(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671a0b639e724fe6c57b3e721cef7f65ff8e627f1d25b3af7c5b13988f35c7c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52ca57115413474d6e91128870eb43b33854be53d1823286fa7382047930507(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f5e7efd1f8b517466a40b03143f809a379819dd38391c2cb8b8c4d300ac609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e45b58e772606dae5f27b549eb61c224feb01290b6a3abdf64dfacf1609813(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2dfc44bbb9167385d2a66d096e11a07ae643a166dd01256a7ea91201a71402(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cad34d7201fda9aac88d1e01e7885746f4c9fd2662595a6af75f6a3ccac730(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b33929aa1a704bb9466b1d968dc73a68498d22e868af4971e95882e3925659a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47cbfef11f1bf67bf3ec520b2f7515612e0bc73e1c8f2607f74c2dfdaf8c0c2(
    *,
    authorized_audiences_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    trusted_token_issuer_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23883834cae8be4e69c541bd8daffe830c2f5f4ffd7814de0f50231a4048adbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118a44081b88077ffd6588e2232f3d05c6e911950f31262121eb181617cf1498(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3132ed7b5e36db95721554563053c97cd03aabb2fded0790fed4a045c4988643(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd0ef29621e2ef20757f5790a12c0e91b6e4c0fc72f416a100d651d96c10588(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71517f803e16d1245f3d36d76dbeb56088475f43de5e1d186598a233f0ea4a9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7127dc419cc5e7e1e044d8dc1d846f754dc16cbc136654947549611a7b9c281d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationAuthorizedTokenIssuer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df7d78661996587ecd50a0afc24518bbf9e569c6219dd119912fcb4691ae02f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8684c3734317e89a0d50101a2aac9af23dec728d212c86e674b92f04bccd23(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22590dccd81e6eb2b492e31cf67a425ff628226fea137c7729751f09178db5a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2caa97a10c9a184a7b8af50f421204a2f392673adbb695045567d342d298386c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationAuthorizedTokenIssuer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a0f3550ce8ea8b1c1a52dc9221720e5fbcec8ebe38038d1a55fb72c2c07f5b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    iam_role_arn: builtins.str,
    idc_display_name: builtins.str,
    idc_instance_arn: builtins.str,
    redshift_idc_application_name: builtins.str,
    application_type: typing.Optional[builtins.str] = None,
    authorized_token_issuer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationAuthorizedTokenIssuer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    identity_namespace: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    service_integration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae0e134ea7d541ae4983bc3fd066689666bbfb3bfe43fc425c5f2239604fd2e(
    *,
    lake_formation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationLakeFormation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redshift: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationRedshift, typing.Dict[builtins.str, typing.Any]]]]] = None,
    s3_access_grants: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationS3AccessGrants, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2d0ea1c69893fd3568941efe8ca2a1de81ac225d6c70bccc8844f25aca910f(
    *,
    lake_formation_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a80fe4d740ecd90800e0d5c883d2cfb2f2f297b62eddf2cea19fbba882bc1f06(
    *,
    authorization: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf50d53dbd76c29a761888f455c0fa33af5aef34943d2621ff355e7ed7c6e928(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ebf3dfd8fb56eee9bec3d970d20664e4bc1fd8cafe0726adc28773ca41567d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb17b55c987edce0f281ddc25495a41ecbf126054386bf4cfe0b9a931d0d9631(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901af5a18f689bab4a21ed737deb099374ecaf4dc5a9b2cf5408d97f5975d83b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdec8122849feefc5176a2258bce2d1399de9928013431f78bbbb730d3d0eada(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a39e74a5cd1f8e2ad6119ba86be80d9c35d19c9b4f68cd8a878a45c3cb560f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd7d8c05d61fc7ed15e2a88dad05a6e8e2558e1854943df0b3ee0033a7061c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794b3c422d72916234a52f95d4f6be4957e33bddef3bab146feead3daca6087e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0b3a5b159238db51eaab503578e40fd0010a1498313b93d0035348742b1c34(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b39dc92dc4873e93648de51d6d77d8ccc1c0058f603ae85317de0fd3fe90b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb697a0121cd7d3723dacd85f7308d4c96bf95b3adad2dffd5e7fd4d16c72e8d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ed0d62a509ce5a1ad6cc9c9617736ded9d96de8bf0ee9aa1bd009153864936(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74cebf976098dbd87d75bf74e5691e2f7e9cd8a6304016e155e866ca5cd3ca3a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd0fcf334483dc77a84a65970ddbedf3bfa12f5415e4c78fc3ffd424af40073(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fcb071f95fb93ba3bc68170c400a612106dc8a089c8eb3a4711987904bf93d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationLakeFormation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a10530a42832b57c23f2b91a1e265485c70bd357e76b84b09dd3850728af1a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6f4bb30fa7a850bcc1d43cf239f21df72114c454871e6f311d8ad20aab513d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationLakeFormationLakeFormationQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000be6dd90377298a7af5881a40c0fb8942310cb25b0ad01442b256666748ec1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationLakeFormation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8178c52ad66bc34da0323cba6f66756a88dc6f413c082aae826e7986cf52dc8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbaed67a39dddb6da375ebe61fd2f709d1694bba51053036d6ef06973bfdf445(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdd4c433c3ee9163b4f7c82decc78917ad41343e4734f4cf2514160bd33574c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2925cd7f389eb0252abdc9f2abd9427bbfbce1ac9457309ada3165e1e60df4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65225218544246332f61fa48c4ff224fc3a9fb2474b1af0326b2758fa521f65(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff23476caa88b4527fc8f584f8dccf3db1e35ab54f50fc783badfa821e3573ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507423ae8bc1c30f3db73a38333b3f825b94d6f6d2c55f738306a543db684239(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf05078d4572b34f0881ff1c5ccd08a1c2cbd4590cb91ae39a4ea4ab7fb935aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationLakeFormation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56287cb1c1059d14e8c6eb080a46a9061bfdcf3c8b2b1674b9071e19430b59a0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationRedshift, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9a71d092b3755ab53721837c5b846c7b60441cd027f5bddc37ef93f6e2cf46(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationS3AccessGrants, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af233aa3b811c02e57f6a20d832f6a9009969673fca0bee6bcc0a3b8d1576be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b012d8598e676d9b2053bff11c5ac48d45403d533ca39dc48b077a5d22a2bf4(
    *,
    connect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationRedshiftConnect, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00138a9fdadc25e5a92f25eb6e1b562090dea2dc0d06e316d07cf2e5e1f6d98(
    *,
    authorization: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074f50ac45b4908b8570dc7f01580f07e530497237a061a5dbb6728e147b6533(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd116bbc55e0098baa50d3648e9ff827fd4d763c623e7a96de34707d0f2301ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08635182d1d88dc1c346c9a93aa108229990374d80e9082bb8b3a3b13ff53bc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f957f5acb7aecc0e9838713e20a3eb713fd217dfe5cf73cf17f41b48d68bf0eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8433268d66166eb370314ce28f1619915fc43ca0203bf2fda20e40554e2aa98(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1c71a9fa3e4c40866685e212c89840d6441fd22a3eddba324b438daba8b354(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationRedshiftConnect]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fc72a03eb5fa54e0545c59a70005801458073c8a2f8104ff3b3e631a1b5300(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea3e49bfbf2821fd70a0d34b2d769357722f8e9db8d2bcd9ad0694cbcc766d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ed405fe2e4da800f0655144148c0e9c3a6ec2423e383800d6fc32c2cbf91a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationRedshiftConnect]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b6c6d416a915de51c4034f6307f5cc446a4788b852d2e9fa435f1355121b1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655db885043e0b132eaa7271c190d716dd36f31220d1b31cf987c220fd8a3178(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb4e3c8a8c79f2afd030c64b0c0dbd5b200e942bfbebdf8649cfd24c7a95ffe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb86f1eda73dddaaa6af8895c0a7c9bc902bf3439363bf07a62f9192f84f129f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f32b5564e7f9d6056594b9a40916188fb29df10d5040183e1bce8f78c16c1e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61cdba5ef82bb48b600a09e15b35ed3e6fa1c42dc6761ed66539e7997e25be38(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationRedshift]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718fe8b98ba4122f725c60190b7d22c2d88b9bcf58256167dd4bbeee06c6de28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dba7f583987211402d0a6dcd955ec2d9dbbde4a7c7882504f6cfa36bf9a04c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationRedshiftConnect, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea77b364b8658354be542b8fda06c8350147814350335e94a1f11f31f7c5e049(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationRedshift]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9528e821fb66f5dc1ada9f9567c050d7c01d4f8abd4188c53336b035083247e(
    *,
    read_write_access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc0b5aa0961bc2fcbee743bd022ac827ab206836dfaa853a2841a65fa1c779a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b29414adf640bed23666ba5b1dd64e89a5bde60cb9c10670234bfb46b1cc03b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f54dfd9fdfc2c94932aef5a7bb2f16617c5a6c9de7648e686cace945bc7c5cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa45435a07aafe81930c31bc23dbebdfa52befdd465f4c90455880a3e493fe14(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b53b498a1ef37f3bfcb482895e51f2f799ba7d79a7831fb2f1d95a605a0dbfa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fc0b7c517b07fdc38aeeba30145008f545ef0d91a06070f57efe64cbc75979(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationS3AccessGrants]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9241874a657e6db67add8ec6da9e127329838135486146b22092238c4c2bd27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59de79c64b1879a5e95e274d431cea202e989bfccdcb7c4af9a953fe6e22dac1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffaae795ef3fe19bd83d60d92316422c54de3c7daf61debf9793e9658ff8636(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationS3AccessGrants]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489fd825c5947f11473001619c72325388a0b15d553f855d4a06b1dd026a0a34(
    *,
    authorization: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3e349314ba4a91bb23cb5d772ca4cf9b46afaa5968c9cc952674401dd30f74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9a764cd1135863f54cffe7633a927f29328e27231c9ac0bbc1f43664bf1a5f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9eafc94246a52c623d070938246a373c7d422e04ac958c11a7c7005e307d015(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b894416928a2ffc7eebd34e91f690a53307c5258e6bf9e02a685e98f2c144c32(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c28718d034a5e31b9799ee61f9bb494c8760385d9ca8cbf62e31ddf06dfbb4c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb0054582ab0950495bd041a99c704180c2e08a9820c921db243c5ec3b31665(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50a0e77f84aac89fe147a08963938918dc0f9b70518e0a387df7cda2e9af223(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2566d806ad7634058b53cbcfed5bc6a105de4c62f9df542cf1f99db31c57bada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32054914fbb95553484696987cf17c3fe8d6eeac9c53d5e884b7af365909906(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedshiftIdcApplicationServiceIntegrationS3AccessGrantsReadWriteAccess]],
) -> None:
    """Type checking stubs"""
    pass
