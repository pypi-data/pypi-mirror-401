r'''
# `aws_cloudfront_response_headers_policy`

Refer to the Terraform Registry for docs: [`aws_cloudfront_response_headers_policy`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy).
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


class CloudfrontResponseHeadersPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy aws_cloudfront_response_headers_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        cors_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCorsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCustomHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        remove_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyRemoveHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        server_timing_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy aws_cloudfront_response_headers_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#name CloudfrontResponseHeadersPolicy#name}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#comment CloudfrontResponseHeadersPolicy#comment}.
        :param cors_config: cors_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#cors_config CloudfrontResponseHeadersPolicy#cors_config}
        :param custom_headers_config: custom_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#custom_headers_config CloudfrontResponseHeadersPolicy#custom_headers_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#id CloudfrontResponseHeadersPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param remove_headers_config: remove_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#remove_headers_config CloudfrontResponseHeadersPolicy#remove_headers_config}
        :param security_headers_config: security_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#security_headers_config CloudfrontResponseHeadersPolicy#security_headers_config}
        :param server_timing_headers_config: server_timing_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#server_timing_headers_config CloudfrontResponseHeadersPolicy#server_timing_headers_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3469e0d2c3a77d5fcbee424b7c5484b3a933e595b3a268960fdf5ec852fe2544)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudfrontResponseHeadersPolicyConfig(
            name=name,
            comment=comment,
            cors_config=cors_config,
            custom_headers_config=custom_headers_config,
            id=id,
            remove_headers_config=remove_headers_config,
            security_headers_config=security_headers_config,
            server_timing_headers_config=server_timing_headers_config,
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
        '''Generates CDKTF code for importing a CloudfrontResponseHeadersPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudfrontResponseHeadersPolicy to import.
        :param import_from_id: The id of the existing CloudfrontResponseHeadersPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudfrontResponseHeadersPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64755218843f4eaba2353c6052b3fa8cf9e8ea421b1f925152be382bdc168385)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCorsConfig")
    def put_cors_config(
        self,
        *,
        access_control_allow_credentials: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        access_control_allow_headers: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders", typing.Dict[builtins.str, typing.Any]],
        access_control_allow_methods: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods", typing.Dict[builtins.str, typing.Any]],
        access_control_allow_origins: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins", typing.Dict[builtins.str, typing.Any]],
        origin_override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        access_control_expose_headers: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders", typing.Dict[builtins.str, typing.Any]]] = None,
        access_control_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param access_control_allow_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_credentials CloudfrontResponseHeadersPolicy#access_control_allow_credentials}.
        :param access_control_allow_headers: access_control_allow_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_headers CloudfrontResponseHeadersPolicy#access_control_allow_headers}
        :param access_control_allow_methods: access_control_allow_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_methods CloudfrontResponseHeadersPolicy#access_control_allow_methods}
        :param access_control_allow_origins: access_control_allow_origins block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_origins CloudfrontResponseHeadersPolicy#access_control_allow_origins}
        :param origin_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#origin_override CloudfrontResponseHeadersPolicy#origin_override}.
        :param access_control_expose_headers: access_control_expose_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_expose_headers CloudfrontResponseHeadersPolicy#access_control_expose_headers}
        :param access_control_max_age_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.
        '''
        value = CloudfrontResponseHeadersPolicyCorsConfig(
            access_control_allow_credentials=access_control_allow_credentials,
            access_control_allow_headers=access_control_allow_headers,
            access_control_allow_methods=access_control_allow_methods,
            access_control_allow_origins=access_control_allow_origins,
            origin_override=origin_override,
            access_control_expose_headers=access_control_expose_headers,
            access_control_max_age_sec=access_control_max_age_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putCorsConfig", [value]))

    @jsii.member(jsii_name="putCustomHeadersConfig")
    def put_custom_headers_config(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontResponseHeadersPolicyCustomHeadersConfigItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        value = CloudfrontResponseHeadersPolicyCustomHeadersConfig(items=items)

        return typing.cast(None, jsii.invoke(self, "putCustomHeadersConfig", [value]))

    @jsii.member(jsii_name="putRemoveHeadersConfig")
    def put_remove_headers_config(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        value = CloudfrontResponseHeadersPolicyRemoveHeadersConfig(items=items)

        return typing.cast(None, jsii.invoke(self, "putRemoveHeadersConfig", [value]))

    @jsii.member(jsii_name="putSecurityHeadersConfig")
    def put_security_headers_config(
        self,
        *,
        content_security_policy: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        content_type_options: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        frame_options: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        referrer_policy: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        strict_transport_security: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
        xss_protection: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param content_security_policy: content_security_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}
        :param content_type_options: content_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#content_type_options CloudfrontResponseHeadersPolicy#content_type_options}
        :param frame_options: frame_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#frame_options CloudfrontResponseHeadersPolicy#frame_options}
        :param referrer_policy: referrer_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}
        :param strict_transport_security: strict_transport_security block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#strict_transport_security CloudfrontResponseHeadersPolicy#strict_transport_security}
        :param xss_protection: xss_protection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#xss_protection CloudfrontResponseHeadersPolicy#xss_protection}
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfig(
            content_security_policy=content_security_policy,
            content_type_options=content_type_options,
            frame_options=frame_options,
            referrer_policy=referrer_policy,
            strict_transport_security=strict_transport_security,
            xss_protection=xss_protection,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityHeadersConfig", [value]))

    @jsii.member(jsii_name="putServerTimingHeadersConfig")
    def put_server_timing_headers_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        sampling_rate: jsii.Number,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#enabled CloudfrontResponseHeadersPolicy#enabled}.
        :param sampling_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#sampling_rate CloudfrontResponseHeadersPolicy#sampling_rate}.
        '''
        value = CloudfrontResponseHeadersPolicyServerTimingHeadersConfig(
            enabled=enabled, sampling_rate=sampling_rate
        )

        return typing.cast(None, jsii.invoke(self, "putServerTimingHeadersConfig", [value]))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetCorsConfig")
    def reset_cors_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsConfig", []))

    @jsii.member(jsii_name="resetCustomHeadersConfig")
    def reset_custom_headers_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomHeadersConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRemoveHeadersConfig")
    def reset_remove_headers_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoveHeadersConfig", []))

    @jsii.member(jsii_name="resetSecurityHeadersConfig")
    def reset_security_headers_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityHeadersConfig", []))

    @jsii.member(jsii_name="resetServerTimingHeadersConfig")
    def reset_server_timing_headers_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerTimingHeadersConfig", []))

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
    @jsii.member(jsii_name="corsConfig")
    def cors_config(self) -> "CloudfrontResponseHeadersPolicyCorsConfigOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicyCorsConfigOutputReference", jsii.get(self, "corsConfig"))

    @builtins.property
    @jsii.member(jsii_name="customHeadersConfig")
    def custom_headers_config(
        self,
    ) -> "CloudfrontResponseHeadersPolicyCustomHeadersConfigOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicyCustomHeadersConfigOutputReference", jsii.get(self, "customHeadersConfig"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="removeHeadersConfig")
    def remove_headers_config(
        self,
    ) -> "CloudfrontResponseHeadersPolicyRemoveHeadersConfigOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicyRemoveHeadersConfigOutputReference", jsii.get(self, "removeHeadersConfig"))

    @builtins.property
    @jsii.member(jsii_name="securityHeadersConfig")
    def security_headers_config(
        self,
    ) -> "CloudfrontResponseHeadersPolicySecurityHeadersConfigOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicySecurityHeadersConfigOutputReference", jsii.get(self, "securityHeadersConfig"))

    @builtins.property
    @jsii.member(jsii_name="serverTimingHeadersConfig")
    def server_timing_headers_config(
        self,
    ) -> "CloudfrontResponseHeadersPolicyServerTimingHeadersConfigOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicyServerTimingHeadersConfigOutputReference", jsii.get(self, "serverTimingHeadersConfig"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="corsConfigInput")
    def cors_config_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyCorsConfig"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyCorsConfig"], jsii.get(self, "corsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="customHeadersConfigInput")
    def custom_headers_config_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyCustomHeadersConfig"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyCustomHeadersConfig"], jsii.get(self, "customHeadersConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="removeHeadersConfigInput")
    def remove_headers_config_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyRemoveHeadersConfig"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyRemoveHeadersConfig"], jsii.get(self, "removeHeadersConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="securityHeadersConfigInput")
    def security_headers_config_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfig"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfig"], jsii.get(self, "securityHeadersConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serverTimingHeadersConfigInput")
    def server_timing_headers_config_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig"], jsii.get(self, "serverTimingHeadersConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275d408dc528f6dc86a5c31c9bd2510e55151e90898b1eed4a259c0740eca769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d87b2083b9b3e1902ce1b67728162a35611a696e5890f4162a02f6e4ada767e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804ce5545b56ffd4922616f5972e2d6fe716f3bda635554dbfe850488f17a6f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "comment": "comment",
        "cors_config": "corsConfig",
        "custom_headers_config": "customHeadersConfig",
        "id": "id",
        "remove_headers_config": "removeHeadersConfig",
        "security_headers_config": "securityHeadersConfig",
        "server_timing_headers_config": "serverTimingHeadersConfig",
    },
)
class CloudfrontResponseHeadersPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        cors_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCorsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCustomHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        remove_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyRemoveHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        server_timing_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#name CloudfrontResponseHeadersPolicy#name}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#comment CloudfrontResponseHeadersPolicy#comment}.
        :param cors_config: cors_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#cors_config CloudfrontResponseHeadersPolicy#cors_config}
        :param custom_headers_config: custom_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#custom_headers_config CloudfrontResponseHeadersPolicy#custom_headers_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#id CloudfrontResponseHeadersPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param remove_headers_config: remove_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#remove_headers_config CloudfrontResponseHeadersPolicy#remove_headers_config}
        :param security_headers_config: security_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#security_headers_config CloudfrontResponseHeadersPolicy#security_headers_config}
        :param server_timing_headers_config: server_timing_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#server_timing_headers_config CloudfrontResponseHeadersPolicy#server_timing_headers_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cors_config, dict):
            cors_config = CloudfrontResponseHeadersPolicyCorsConfig(**cors_config)
        if isinstance(custom_headers_config, dict):
            custom_headers_config = CloudfrontResponseHeadersPolicyCustomHeadersConfig(**custom_headers_config)
        if isinstance(remove_headers_config, dict):
            remove_headers_config = CloudfrontResponseHeadersPolicyRemoveHeadersConfig(**remove_headers_config)
        if isinstance(security_headers_config, dict):
            security_headers_config = CloudfrontResponseHeadersPolicySecurityHeadersConfig(**security_headers_config)
        if isinstance(server_timing_headers_config, dict):
            server_timing_headers_config = CloudfrontResponseHeadersPolicyServerTimingHeadersConfig(**server_timing_headers_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fd2c2fd196f9bebf54e452b0da6f3cbe1e20eb4016c40a80e60d5df89092a1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument cors_config", value=cors_config, expected_type=type_hints["cors_config"])
            check_type(argname="argument custom_headers_config", value=custom_headers_config, expected_type=type_hints["custom_headers_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument remove_headers_config", value=remove_headers_config, expected_type=type_hints["remove_headers_config"])
            check_type(argname="argument security_headers_config", value=security_headers_config, expected_type=type_hints["security_headers_config"])
            check_type(argname="argument server_timing_headers_config", value=server_timing_headers_config, expected_type=type_hints["server_timing_headers_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if comment is not None:
            self._values["comment"] = comment
        if cors_config is not None:
            self._values["cors_config"] = cors_config
        if custom_headers_config is not None:
            self._values["custom_headers_config"] = custom_headers_config
        if id is not None:
            self._values["id"] = id
        if remove_headers_config is not None:
            self._values["remove_headers_config"] = remove_headers_config
        if security_headers_config is not None:
            self._values["security_headers_config"] = security_headers_config
        if server_timing_headers_config is not None:
            self._values["server_timing_headers_config"] = server_timing_headers_config

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#name CloudfrontResponseHeadersPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#comment CloudfrontResponseHeadersPolicy#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_config(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyCorsConfig"]:
        '''cors_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#cors_config CloudfrontResponseHeadersPolicy#cors_config}
        '''
        result = self._values.get("cors_config")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyCorsConfig"], result)

    @builtins.property
    def custom_headers_config(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyCustomHeadersConfig"]:
        '''custom_headers_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#custom_headers_config CloudfrontResponseHeadersPolicy#custom_headers_config}
        '''
        result = self._values.get("custom_headers_config")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyCustomHeadersConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#id CloudfrontResponseHeadersPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove_headers_config(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyRemoveHeadersConfig"]:
        '''remove_headers_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#remove_headers_config CloudfrontResponseHeadersPolicy#remove_headers_config}
        '''
        result = self._values.get("remove_headers_config")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyRemoveHeadersConfig"], result)

    @builtins.property
    def security_headers_config(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfig"]:
        '''security_headers_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#security_headers_config CloudfrontResponseHeadersPolicy#security_headers_config}
        '''
        result = self._values.get("security_headers_config")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfig"], result)

    @builtins.property
    def server_timing_headers_config(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig"]:
        '''server_timing_headers_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#server_timing_headers_config CloudfrontResponseHeadersPolicy#server_timing_headers_config}
        '''
        result = self._values.get("server_timing_headers_config")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_control_allow_credentials": "accessControlAllowCredentials",
        "access_control_allow_headers": "accessControlAllowHeaders",
        "access_control_allow_methods": "accessControlAllowMethods",
        "access_control_allow_origins": "accessControlAllowOrigins",
        "origin_override": "originOverride",
        "access_control_expose_headers": "accessControlExposeHeaders",
        "access_control_max_age_sec": "accessControlMaxAgeSec",
    },
)
class CloudfrontResponseHeadersPolicyCorsConfig:
    def __init__(
        self,
        *,
        access_control_allow_credentials: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        access_control_allow_headers: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders", typing.Dict[builtins.str, typing.Any]],
        access_control_allow_methods: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods", typing.Dict[builtins.str, typing.Any]],
        access_control_allow_origins: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins", typing.Dict[builtins.str, typing.Any]],
        origin_override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        access_control_expose_headers: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders", typing.Dict[builtins.str, typing.Any]]] = None,
        access_control_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param access_control_allow_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_credentials CloudfrontResponseHeadersPolicy#access_control_allow_credentials}.
        :param access_control_allow_headers: access_control_allow_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_headers CloudfrontResponseHeadersPolicy#access_control_allow_headers}
        :param access_control_allow_methods: access_control_allow_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_methods CloudfrontResponseHeadersPolicy#access_control_allow_methods}
        :param access_control_allow_origins: access_control_allow_origins block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_origins CloudfrontResponseHeadersPolicy#access_control_allow_origins}
        :param origin_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#origin_override CloudfrontResponseHeadersPolicy#origin_override}.
        :param access_control_expose_headers: access_control_expose_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_expose_headers CloudfrontResponseHeadersPolicy#access_control_expose_headers}
        :param access_control_max_age_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.
        '''
        if isinstance(access_control_allow_headers, dict):
            access_control_allow_headers = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders(**access_control_allow_headers)
        if isinstance(access_control_allow_methods, dict):
            access_control_allow_methods = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods(**access_control_allow_methods)
        if isinstance(access_control_allow_origins, dict):
            access_control_allow_origins = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins(**access_control_allow_origins)
        if isinstance(access_control_expose_headers, dict):
            access_control_expose_headers = CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders(**access_control_expose_headers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca6a9fc06fdd0d26a29df3a2c8d37ba4aaa1e10eb74fe60ed8cf100e4317f94)
            check_type(argname="argument access_control_allow_credentials", value=access_control_allow_credentials, expected_type=type_hints["access_control_allow_credentials"])
            check_type(argname="argument access_control_allow_headers", value=access_control_allow_headers, expected_type=type_hints["access_control_allow_headers"])
            check_type(argname="argument access_control_allow_methods", value=access_control_allow_methods, expected_type=type_hints["access_control_allow_methods"])
            check_type(argname="argument access_control_allow_origins", value=access_control_allow_origins, expected_type=type_hints["access_control_allow_origins"])
            check_type(argname="argument origin_override", value=origin_override, expected_type=type_hints["origin_override"])
            check_type(argname="argument access_control_expose_headers", value=access_control_expose_headers, expected_type=type_hints["access_control_expose_headers"])
            check_type(argname="argument access_control_max_age_sec", value=access_control_max_age_sec, expected_type=type_hints["access_control_max_age_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_control_allow_credentials": access_control_allow_credentials,
            "access_control_allow_headers": access_control_allow_headers,
            "access_control_allow_methods": access_control_allow_methods,
            "access_control_allow_origins": access_control_allow_origins,
            "origin_override": origin_override,
        }
        if access_control_expose_headers is not None:
            self._values["access_control_expose_headers"] = access_control_expose_headers
        if access_control_max_age_sec is not None:
            self._values["access_control_max_age_sec"] = access_control_max_age_sec

    @builtins.property
    def access_control_allow_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_credentials CloudfrontResponseHeadersPolicy#access_control_allow_credentials}.'''
        result = self._values.get("access_control_allow_credentials")
        assert result is not None, "Required property 'access_control_allow_credentials' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def access_control_allow_headers(
        self,
    ) -> "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders":
        '''access_control_allow_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_headers CloudfrontResponseHeadersPolicy#access_control_allow_headers}
        '''
        result = self._values.get("access_control_allow_headers")
        assert result is not None, "Required property 'access_control_allow_headers' is missing"
        return typing.cast("CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders", result)

    @builtins.property
    def access_control_allow_methods(
        self,
    ) -> "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods":
        '''access_control_allow_methods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_methods CloudfrontResponseHeadersPolicy#access_control_allow_methods}
        '''
        result = self._values.get("access_control_allow_methods")
        assert result is not None, "Required property 'access_control_allow_methods' is missing"
        return typing.cast("CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods", result)

    @builtins.property
    def access_control_allow_origins(
        self,
    ) -> "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins":
        '''access_control_allow_origins block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_origins CloudfrontResponseHeadersPolicy#access_control_allow_origins}
        '''
        result = self._values.get("access_control_allow_origins")
        assert result is not None, "Required property 'access_control_allow_origins' is missing"
        return typing.cast("CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins", result)

    @builtins.property
    def origin_override(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#origin_override CloudfrontResponseHeadersPolicy#origin_override}.'''
        result = self._values.get("origin_override")
        assert result is not None, "Required property 'origin_override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def access_control_expose_headers(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders"]:
        '''access_control_expose_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_expose_headers CloudfrontResponseHeadersPolicy#access_control_expose_headers}
        '''
        result = self._values.get("access_control_expose_headers")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders"], result)

    @builtins.property
    def access_control_max_age_sec(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.'''
        result = self._values.get("access_control_max_age_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCorsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6a4d9c3bbf632e49b8663b00a91da4c4bbcc577753f04c453d0619e56295ed)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35a613a21b54f40e21d9e6faee0bf8be2b5721589eb17c1a3fe8fdd1db4b93e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab22de074d43c58a46e8a08a1c2d05ebf3dec1bf96fee331ea497d8df047b9c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945e8f05986238a4895b2a8a872207e8755ae607a820994cebbfbf1bb15fb3f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2b008eb944619b7f42b499c31a1ef877d93693ee0aea62b749dd0b3e7245a0)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e58b65aa0644e05f328b6d483c87c7e526694d848703aa497a3cc31188460196)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc9e4f0f040c28c247a40d918a000269d6d9f9db5bbd825c29c5e1342731a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91fd43badc2f8e83f398c0806c6d4f92aea841118d2582f0bbd847537753a60a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3baead73467b07aef9842b71f049104117ca4cfc35c48dfd8ce32889b6bedd)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOriginsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOriginsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6372c19ed8c27c205c609e33f86720f88bb798a3eb1c6746b18a31c150c5d861)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812b7b4a9ddf94718a7eaa5df901f5469a3ae81536221aff5834fc7aefd62d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aab51b4dac62a5d5627ad00c91dcc253e6314dbcdf1d4dc6415f2ab3c8f0152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c167a55dbd5142c8679da45bcb380e132a16c4c514266e0ee2d458ac73f62a)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f36dc01859b4194064c0c3e71d1d6822e9b2c0f25598ab897b2e9c0869d6f69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40efece05d26568091733e88b1fa7f5a5f2ad1378a2627a014d261dc551a244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81d7bc9722fd05fbf23d60a06481ff86d90f175367ec4f353aa9744c68aaca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicyCorsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33a11d970fd8ee0a9d9f5d1797d5e9d46f09f8eced56b94b6df10147b562578f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessControlAllowHeaders")
    def put_access_control_allow_headers(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        value = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders(
            items=items
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControlAllowHeaders", [value]))

    @jsii.member(jsii_name="putAccessControlAllowMethods")
    def put_access_control_allow_methods(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        value = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods(
            items=items
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControlAllowMethods", [value]))

    @jsii.member(jsii_name="putAccessControlAllowOrigins")
    def put_access_control_allow_origins(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        value = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins(
            items=items
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControlAllowOrigins", [value]))

    @jsii.member(jsii_name="putAccessControlExposeHeaders")
    def put_access_control_expose_headers(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        value = CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders(
            items=items
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControlExposeHeaders", [value]))

    @jsii.member(jsii_name="resetAccessControlExposeHeaders")
    def reset_access_control_expose_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessControlExposeHeaders", []))

    @jsii.member(jsii_name="resetAccessControlMaxAgeSec")
    def reset_access_control_max_age_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessControlMaxAgeSec", []))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowHeaders")
    def access_control_allow_headers(
        self,
    ) -> CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeadersOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeadersOutputReference, jsii.get(self, "accessControlAllowHeaders"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowMethods")
    def access_control_allow_methods(
        self,
    ) -> CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethodsOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethodsOutputReference, jsii.get(self, "accessControlAllowMethods"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowOrigins")
    def access_control_allow_origins(
        self,
    ) -> CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOriginsOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOriginsOutputReference, jsii.get(self, "accessControlAllowOrigins"))

    @builtins.property
    @jsii.member(jsii_name="accessControlExposeHeaders")
    def access_control_expose_headers(
        self,
    ) -> CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeadersOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeadersOutputReference, jsii.get(self, "accessControlExposeHeaders"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowCredentialsInput")
    def access_control_allow_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessControlAllowCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowHeadersInput")
    def access_control_allow_headers_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders], jsii.get(self, "accessControlAllowHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowMethodsInput")
    def access_control_allow_methods_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods], jsii.get(self, "accessControlAllowMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowOriginsInput")
    def access_control_allow_origins_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins], jsii.get(self, "accessControlAllowOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlExposeHeadersInput")
    def access_control_expose_headers_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders], jsii.get(self, "accessControlExposeHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlMaxAgeSecInput")
    def access_control_max_age_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accessControlMaxAgeSecInput"))

    @builtins.property
    @jsii.member(jsii_name="originOverrideInput")
    def origin_override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "originOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowCredentials")
    def access_control_allow_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessControlAllowCredentials"))

    @access_control_allow_credentials.setter
    def access_control_allow_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fcfee7e3a295567880b8e87504afe7e86267964d491574e68acca46edee516c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessControlAllowCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessControlMaxAgeSec")
    def access_control_max_age_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accessControlMaxAgeSec"))

    @access_control_max_age_sec.setter
    def access_control_max_age_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0933b57f20553e3890337dd3dbe2384ef069bcba0622eff6209c3d1c48a375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessControlMaxAgeSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originOverride")
    def origin_override(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "originOverride"))

    @origin_override.setter
    def origin_override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f263905b141c4890601943d51bcdf34bb5f05066d5ecb39b324ac7e0682fa91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfig]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa12a860a6017991befb24e8174574a26a62b98fee698fbaa4d4bf8bfafddee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCustomHeadersConfig",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyCustomHeadersConfig:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontResponseHeadersPolicyCustomHeadersConfigItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4aba3d3a16c805e4e92243e8835df45fb19df25064408a4160c26e8af50b6d1)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontResponseHeadersPolicyCustomHeadersConfigItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontResponseHeadersPolicyCustomHeadersConfigItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCustomHeadersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCustomHeadersConfigItems",
    jsii_struct_bases=[],
    name_mapping={"header": "header", "override": "override", "value": "value"},
)
class CloudfrontResponseHeadersPolicyCustomHeadersConfigItems:
    def __init__(
        self,
        *,
        header: builtins.str,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        value: builtins.str,
    ) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#header CloudfrontResponseHeadersPolicy#header}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#value CloudfrontResponseHeadersPolicy#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598bd6abbff23f48ac2b9f8383191becf69dcd6904fcfde751d366b620c6f623)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header": header,
            "override": override,
            "value": value,
        }

    @builtins.property
    def header(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#header CloudfrontResponseHeadersPolicy#header}.'''
        result = self._values.get("header")
        assert result is not None, "Required property 'header' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#value CloudfrontResponseHeadersPolicy#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCustomHeadersConfigItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__562216f1d5d811ad568508c4d25180614b8d679728908badaa01e84d4c979ee2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a27b40ce6d2da628338823e61d5f90241cc53b7d7ba0efefe204699e493a6b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4b9e1c4ffbfe2ceff639e90ab9b96450130e88e166bfacaf8db2178d2d89ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17aebf54e4b2874b1e42682357aa5776e0950c079370d0292e69255d800dfa96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__255da06ff5ed37dc3cd3eacc7cd04fd55b5adf9a5b2593596315356ed1c48ffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e8ef15bfdffa0bf2ff947378ce41329717faefae35a765a0bb2d55d7c1a205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c73e775276cf1a5b0a412dd115670c83dbab5ed7ea1d9b19d170cfdf5c47b66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "header"))

    @header.setter
    def header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a6ad836926b4b3790a988ad8a5815bccbe92f8d6698834f4fc50cb284fcc0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab907f42cfe640e5e05fba696a9d72c39cbd9ea025f206f731c4d7e6f8d81e76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205363190339a172e5b4f4b6cbc6a9a4fd1073302c37ac4aaa852b22f4afb8d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1051dca093aaad269464dffcf3c62bc4bb56bc5afa586c07698d10b086ae96e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicyCustomHeadersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCustomHeadersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__009916e3ea8679fdbe602ae54de05bcd9636fa6e735d4ddc314b38653de0cc19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d79875d5412a4b51d0600bb1d2faeb7d5919507475dadd64ff42cd161bb4f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItems", [value]))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsList:
        return typing.cast(CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCustomHeadersConfig]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCustomHeadersConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCustomHeadersConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18cd4548fcd984608bd1e4493409cc96392bbc84a9578b6d025ab275cf904a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyRemoveHeadersConfig",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyRemoveHeadersConfig:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e15a028a6f8e592cc67c268594d0856ac8ce17f398835d57d5e1d5d94e0b08)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyRemoveHeadersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems",
    jsii_struct_bases=[],
    name_mapping={"header": "header"},
)
class CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems:
    def __init__(self, *, header: builtins.str) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#header CloudfrontResponseHeadersPolicy#header}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895973d151cbe23ca00dc8a4b3deebf4d10340297f57ad467492c01ba07c670f)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header": header,
        }

    @builtins.property
    def header(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#header CloudfrontResponseHeadersPolicy#header}.'''
        result = self._values.get("header")
        assert result is not None, "Required property 'header' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f136b6a8e63069f498031497800d824481f4ddc2f472d9563e40e8f2e4785258)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a652ebbcca4a1672af51ebd20b7dba5f2444d1e2cc027884461847b7198ccd35)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdf570f626e81cea1fccd85d8246b77c2d5007578c214df93ec2037d02e8248)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ff43cd8ea2a34856db37885969df5ec23b6a857784ade92975addc3303919bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43143fcfb5995c45099a6916a3e40396207a5b12817798c7be226ffe24b73449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3412d54932676c3956369934c6135725df6fefaa3a3cb2d04e560d12947f75e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__972fa73fdf920953659d491cb9f867c16dbe1c84c480d980f057a137930adfda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "header"))

    @header.setter
    def header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f022e38a52a4c93dd9af2224e4d9fede2fb79ce6bfa6933aee461238bbd80da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e154023026c1ec528cf05c101f338a30680559fc25d4944bb9692bc95ed9e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicyRemoveHeadersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyRemoveHeadersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01555ee6d0c23e1783b0278fdff831ddf0d90bfa653c9b6721bbb935014244a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4007f6e5760d49cea668f98d4dcb48774a22f897465943b391789bb3edb6557b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItems", [value]))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsList:
        return typing.cast(CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyRemoveHeadersConfig]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyRemoveHeadersConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyRemoveHeadersConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08498880e8810d94db2c752952ebb77ed639e85cb15fd9378338ea5cf2fc8d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfig",
    jsii_struct_bases=[],
    name_mapping={
        "content_security_policy": "contentSecurityPolicy",
        "content_type_options": "contentTypeOptions",
        "frame_options": "frameOptions",
        "referrer_policy": "referrerPolicy",
        "strict_transport_security": "strictTransportSecurity",
        "xss_protection": "xssProtection",
    },
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfig:
    def __init__(
        self,
        *,
        content_security_policy: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        content_type_options: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        frame_options: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        referrer_policy: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        strict_transport_security: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
        xss_protection: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param content_security_policy: content_security_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}
        :param content_type_options: content_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#content_type_options CloudfrontResponseHeadersPolicy#content_type_options}
        :param frame_options: frame_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#frame_options CloudfrontResponseHeadersPolicy#frame_options}
        :param referrer_policy: referrer_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}
        :param strict_transport_security: strict_transport_security block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#strict_transport_security CloudfrontResponseHeadersPolicy#strict_transport_security}
        :param xss_protection: xss_protection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#xss_protection CloudfrontResponseHeadersPolicy#xss_protection}
        '''
        if isinstance(content_security_policy, dict):
            content_security_policy = CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy(**content_security_policy)
        if isinstance(content_type_options, dict):
            content_type_options = CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions(**content_type_options)
        if isinstance(frame_options, dict):
            frame_options = CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions(**frame_options)
        if isinstance(referrer_policy, dict):
            referrer_policy = CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy(**referrer_policy)
        if isinstance(strict_transport_security, dict):
            strict_transport_security = CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity(**strict_transport_security)
        if isinstance(xss_protection, dict):
            xss_protection = CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection(**xss_protection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe4a8fb6dc9b6732b448fe9597f27453e55b08162c78209101740240ec20b9d)
            check_type(argname="argument content_security_policy", value=content_security_policy, expected_type=type_hints["content_security_policy"])
            check_type(argname="argument content_type_options", value=content_type_options, expected_type=type_hints["content_type_options"])
            check_type(argname="argument frame_options", value=frame_options, expected_type=type_hints["frame_options"])
            check_type(argname="argument referrer_policy", value=referrer_policy, expected_type=type_hints["referrer_policy"])
            check_type(argname="argument strict_transport_security", value=strict_transport_security, expected_type=type_hints["strict_transport_security"])
            check_type(argname="argument xss_protection", value=xss_protection, expected_type=type_hints["xss_protection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_security_policy is not None:
            self._values["content_security_policy"] = content_security_policy
        if content_type_options is not None:
            self._values["content_type_options"] = content_type_options
        if frame_options is not None:
            self._values["frame_options"] = frame_options
        if referrer_policy is not None:
            self._values["referrer_policy"] = referrer_policy
        if strict_transport_security is not None:
            self._values["strict_transport_security"] = strict_transport_security
        if xss_protection is not None:
            self._values["xss_protection"] = xss_protection

    @builtins.property
    def content_security_policy(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy"]:
        '''content_security_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}
        '''
        result = self._values.get("content_security_policy")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy"], result)

    @builtins.property
    def content_type_options(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions"]:
        '''content_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#content_type_options CloudfrontResponseHeadersPolicy#content_type_options}
        '''
        result = self._values.get("content_type_options")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions"], result)

    @builtins.property
    def frame_options(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions"]:
        '''frame_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#frame_options CloudfrontResponseHeadersPolicy#frame_options}
        '''
        result = self._values.get("frame_options")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions"], result)

    @builtins.property
    def referrer_policy(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy"]:
        '''referrer_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}
        '''
        result = self._values.get("referrer_policy")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy"], result)

    @builtins.property
    def strict_transport_security(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity"]:
        '''strict_transport_security block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#strict_transport_security CloudfrontResponseHeadersPolicy#strict_transport_security}
        '''
        result = self._values.get("strict_transport_security")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity"], result)

    @builtins.property
    def xss_protection(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection"]:
        '''xss_protection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#xss_protection CloudfrontResponseHeadersPolicy#xss_protection}
        '''
        result = self._values.get("xss_protection")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "content_security_policy": "contentSecurityPolicy",
        "override": "override",
    },
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy:
    def __init__(
        self,
        *,
        content_security_policy: builtins.str,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param content_security_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a997127bb75a27e18fd697b9f1caebf3d8b60d6907f4bb4e65aeb94ed857dd48)
            check_type(argname="argument content_security_policy", value=content_security_policy, expected_type=type_hints["content_security_policy"])
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_security_policy": content_security_policy,
            "override": override,
        }

    @builtins.property
    def content_security_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}.'''
        result = self._values.get("content_security_policy")
        assert result is not None, "Required property 'content_security_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__201a078470943ca894fc90094bd96b9535651183d77428bfcc07ac310bb2c2f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="contentSecurityPolicyInput")
    def content_security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentSecurityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="contentSecurityPolicy")
    def content_security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentSecurityPolicy"))

    @content_security_policy.setter
    def content_security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5d1dd05fde63ecdebefefc84642cc9144bced897efe1f4161cb38d6fb4dd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentSecurityPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b20e80b3cad3424708167d3fb07fc048d49375247e6a7a638d6a04c936ec5c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760bafb8925cfcba282093fbe4b5845814a9fb723089a9830054afc47067a14b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions",
    jsii_struct_bases=[],
    name_mapping={"override": "override"},
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions:
    def __init__(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591bf45431cb85b3af5b5f334fb172b8e9157bb5cd8abeaa961249106fa34dda)
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "override": override,
        }

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66833fd9a40904b5c50d7c8e4693e87d726f478c9ceb8ebf8d0a577dfef68461)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435b940edf54cb445e947a6b3b499a9c8006c2ec29888148b23f0ab5c9e5a50c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb9e463cbe45e87b42f54262dba485df87b7a90f15a2c3e1838fce012c7a047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions",
    jsii_struct_bases=[],
    name_mapping={"frame_option": "frameOption", "override": "override"},
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions:
    def __init__(
        self,
        *,
        frame_option: builtins.str,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param frame_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#frame_option CloudfrontResponseHeadersPolicy#frame_option}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7bfad5f54f48fe02590edfcd5a50d96775670946be96c132712a11c6160b4c6)
            check_type(argname="argument frame_option", value=frame_option, expected_type=type_hints["frame_option"])
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frame_option": frame_option,
            "override": override,
        }

    @builtins.property
    def frame_option(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#frame_option CloudfrontResponseHeadersPolicy#frame_option}.'''
        result = self._values.get("frame_option")
        assert result is not None, "Required property 'frame_option' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92a0a55f6ae5d213b75a1d62cb5168f30a51fac5cbf703ed0f0b6a66e9dc9fe4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="frameOptionInput")
    def frame_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frameOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="frameOption")
    def frame_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frameOption"))

    @frame_option.setter
    def frame_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a37bee800c8243000c0c4fdf6be110cc2a0bf4ed79271bae948508633b8932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frameOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8da329922cb77666049f81beb007131039807ee5c26e0d77c7c7f29eebc6653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0431657d3e7d06c7245f2dc2c7cca7caaef5b507e2dae7c48e9293c37d60d8d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicySecurityHeadersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88f0722d0dea13b168d03d952d2cffec850c92a7ce464ee1195d7b52ee3a326e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContentSecurityPolicy")
    def put_content_security_policy(
        self,
        *,
        content_security_policy: builtins.str,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param content_security_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy(
            content_security_policy=content_security_policy, override=override
        )

        return typing.cast(None, jsii.invoke(self, "putContentSecurityPolicy", [value]))

    @jsii.member(jsii_name="putContentTypeOptions")
    def put_content_type_options(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions(
            override=override
        )

        return typing.cast(None, jsii.invoke(self, "putContentTypeOptions", [value]))

    @jsii.member(jsii_name="putFrameOptions")
    def put_frame_options(
        self,
        *,
        frame_option: builtins.str,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param frame_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#frame_option CloudfrontResponseHeadersPolicy#frame_option}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions(
            frame_option=frame_option, override=override
        )

        return typing.cast(None, jsii.invoke(self, "putFrameOptions", [value]))

    @jsii.member(jsii_name="putReferrerPolicy")
    def put_referrer_policy(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        referrer_policy: builtins.str,
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param referrer_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy(
            override=override, referrer_policy=referrer_policy
        )

        return typing.cast(None, jsii.invoke(self, "putReferrerPolicy", [value]))

    @jsii.member(jsii_name="putStrictTransportSecurity")
    def put_strict_transport_security(
        self,
        *,
        access_control_max_age_sec: jsii.Number,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_control_max_age_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param include_subdomains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#include_subdomains CloudfrontResponseHeadersPolicy#include_subdomains}.
        :param preload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#preload CloudfrontResponseHeadersPolicy#preload}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity(
            access_control_max_age_sec=access_control_max_age_sec,
            override=override,
            include_subdomains=include_subdomains,
            preload=preload,
        )

        return typing.cast(None, jsii.invoke(self, "putStrictTransportSecurity", [value]))

    @jsii.member(jsii_name="putXssProtection")
    def put_xss_protection(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        protection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        mode_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        report_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#protection CloudfrontResponseHeadersPolicy#protection}.
        :param mode_block: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#mode_block CloudfrontResponseHeadersPolicy#mode_block}.
        :param report_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#report_uri CloudfrontResponseHeadersPolicy#report_uri}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection(
            override=override,
            protection=protection,
            mode_block=mode_block,
            report_uri=report_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putXssProtection", [value]))

    @jsii.member(jsii_name="resetContentSecurityPolicy")
    def reset_content_security_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentSecurityPolicy", []))

    @jsii.member(jsii_name="resetContentTypeOptions")
    def reset_content_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentTypeOptions", []))

    @jsii.member(jsii_name="resetFrameOptions")
    def reset_frame_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrameOptions", []))

    @jsii.member(jsii_name="resetReferrerPolicy")
    def reset_referrer_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferrerPolicy", []))

    @jsii.member(jsii_name="resetStrictTransportSecurity")
    def reset_strict_transport_security(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictTransportSecurity", []))

    @jsii.member(jsii_name="resetXssProtection")
    def reset_xss_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXssProtection", []))

    @builtins.property
    @jsii.member(jsii_name="contentSecurityPolicy")
    def content_security_policy(
        self,
    ) -> CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicyOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicyOutputReference, jsii.get(self, "contentSecurityPolicy"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeOptions")
    def content_type_options(
        self,
    ) -> CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptionsOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptionsOutputReference, jsii.get(self, "contentTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="frameOptions")
    def frame_options(
        self,
    ) -> CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptionsOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptionsOutputReference, jsii.get(self, "frameOptions"))

    @builtins.property
    @jsii.member(jsii_name="referrerPolicy")
    def referrer_policy(
        self,
    ) -> "CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicyOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicyOutputReference", jsii.get(self, "referrerPolicy"))

    @builtins.property
    @jsii.member(jsii_name="strictTransportSecurity")
    def strict_transport_security(
        self,
    ) -> "CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurityOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurityOutputReference", jsii.get(self, "strictTransportSecurity"))

    @builtins.property
    @jsii.member(jsii_name="xssProtection")
    def xss_protection(
        self,
    ) -> "CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtectionOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtectionOutputReference", jsii.get(self, "xssProtection"))

    @builtins.property
    @jsii.member(jsii_name="contentSecurityPolicyInput")
    def content_security_policy_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy], jsii.get(self, "contentSecurityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeOptionsInput")
    def content_type_options_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions], jsii.get(self, "contentTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="frameOptionsInput")
    def frame_options_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions], jsii.get(self, "frameOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="referrerPolicyInput")
    def referrer_policy_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy"], jsii.get(self, "referrerPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="strictTransportSecurityInput")
    def strict_transport_security_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity"], jsii.get(self, "strictTransportSecurityInput"))

    @builtins.property
    @jsii.member(jsii_name="xssProtectionInput")
    def xss_protection_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection"], jsii.get(self, "xssProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfig]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743d3d1ae27071b17a4c8d00391ca276d0b4192e638abd20c7bcc7794c500b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy",
    jsii_struct_bases=[],
    name_mapping={"override": "override", "referrer_policy": "referrerPolicy"},
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy:
    def __init__(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        referrer_policy: builtins.str,
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param referrer_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96cef8fe755eaf5935f2ccab6d688678483e208a2b34cb9f1e5ac7498318da3)
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
            check_type(argname="argument referrer_policy", value=referrer_policy, expected_type=type_hints["referrer_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "override": override,
            "referrer_policy": referrer_policy,
        }

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def referrer_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}.'''
        result = self._values.get("referrer_policy")
        assert result is not None, "Required property 'referrer_policy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da2bf7b0ca90d15f2153c9e91ba4d7c6819961c4cdd81b59b1b540fa1da183a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="referrerPolicyInput")
    def referrer_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referrerPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608616ba24beb1b1b34bcc4302484a375309c486f68155bb0e33f0f645bba0b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referrerPolicy")
    def referrer_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referrerPolicy"))

    @referrer_policy.setter
    def referrer_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ae440648602fe30b7da1e3037da995533eac382b7ef951b8a7b2c246c38e44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referrerPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896028b2af3652453b658238d528cde6ecab6ad1afb92a3cb571c10c3accf1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity",
    jsii_struct_bases=[],
    name_mapping={
        "access_control_max_age_sec": "accessControlMaxAgeSec",
        "override": "override",
        "include_subdomains": "includeSubdomains",
        "preload": "preload",
    },
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity:
    def __init__(
        self,
        *,
        access_control_max_age_sec: jsii.Number,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_control_max_age_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param include_subdomains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#include_subdomains CloudfrontResponseHeadersPolicy#include_subdomains}.
        :param preload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#preload CloudfrontResponseHeadersPolicy#preload}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b4a5e9a2aa5f93b2eb8be98e305c5477d779a408f9d5ad494ac4e6b6406867)
            check_type(argname="argument access_control_max_age_sec", value=access_control_max_age_sec, expected_type=type_hints["access_control_max_age_sec"])
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
            check_type(argname="argument include_subdomains", value=include_subdomains, expected_type=type_hints["include_subdomains"])
            check_type(argname="argument preload", value=preload, expected_type=type_hints["preload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_control_max_age_sec": access_control_max_age_sec,
            "override": override,
        }
        if include_subdomains is not None:
            self._values["include_subdomains"] = include_subdomains
        if preload is not None:
            self._values["preload"] = preload

    @builtins.property
    def access_control_max_age_sec(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.'''
        result = self._values.get("access_control_max_age_sec")
        assert result is not None, "Required property 'access_control_max_age_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def include_subdomains(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#include_subdomains CloudfrontResponseHeadersPolicy#include_subdomains}.'''
        result = self._values.get("include_subdomains")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def preload(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#preload CloudfrontResponseHeadersPolicy#preload}.'''
        result = self._values.get("preload")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed7f6f8d760042dfcb40cd4329a07f2a82abcbdf923ea45d15eb926d3c9b77d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeSubdomains")
    def reset_include_subdomains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSubdomains", []))

    @jsii.member(jsii_name="resetPreload")
    def reset_preload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreload", []))

    @builtins.property
    @jsii.member(jsii_name="accessControlMaxAgeSecInput")
    def access_control_max_age_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accessControlMaxAgeSecInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSubdomainsInput")
    def include_subdomains_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeSubdomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="preloadInput")
    def preload_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preloadInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlMaxAgeSec")
    def access_control_max_age_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accessControlMaxAgeSec"))

    @access_control_max_age_sec.setter
    def access_control_max_age_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d79d28658f66f605d2820b46c2608d3b620a7e55ada05b3e20b3a49eab447b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessControlMaxAgeSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeSubdomains")
    def include_subdomains(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeSubdomains"))

    @include_subdomains.setter
    def include_subdomains(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a426770f01c56263240f6bd5dad56539bcf60dcbb64d10f49fc32287f9dc05e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeSubdomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2378cf1fc38cb8d5d6c56a8d6f127b1282b9af11210adb117938829643ddaaaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preload")
    def preload(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preload"))

    @preload.setter
    def preload(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2eb899d341c3b4a05cb6b4d0582b2c939ea84a46ec8ef7e353b6d631c972745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a025f9ef2635691a62cf6b21d42147e057f3d54d4ec9d0666cca5f34018320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection",
    jsii_struct_bases=[],
    name_mapping={
        "override": "override",
        "protection": "protection",
        "mode_block": "modeBlock",
        "report_uri": "reportUri",
    },
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection:
    def __init__(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        protection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        mode_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        report_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#protection CloudfrontResponseHeadersPolicy#protection}.
        :param mode_block: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#mode_block CloudfrontResponseHeadersPolicy#mode_block}.
        :param report_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#report_uri CloudfrontResponseHeadersPolicy#report_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f320e180d6421f0982d5437b4b54b2f20bdf3616fcc10a59b03340ff2814240)
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
            check_type(argname="argument protection", value=protection, expected_type=type_hints["protection"])
            check_type(argname="argument mode_block", value=mode_block, expected_type=type_hints["mode_block"])
            check_type(argname="argument report_uri", value=report_uri, expected_type=type_hints["report_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "override": override,
            "protection": protection,
        }
        if mode_block is not None:
            self._values["mode_block"] = mode_block
        if report_uri is not None:
            self._values["report_uri"] = report_uri

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def protection(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#protection CloudfrontResponseHeadersPolicy#protection}.'''
        result = self._values.get("protection")
        assert result is not None, "Required property 'protection' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def mode_block(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#mode_block CloudfrontResponseHeadersPolicy#mode_block}.'''
        result = self._values.get("mode_block")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def report_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#report_uri CloudfrontResponseHeadersPolicy#report_uri}.'''
        result = self._values.get("report_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b01d78db1ec37ad40813e976ce7b42ca8578f7fe99d1aa5aad3265af8377cfe4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetModeBlock")
    def reset_mode_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModeBlock", []))

    @jsii.member(jsii_name="resetReportUri")
    def reset_report_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReportUri", []))

    @builtins.property
    @jsii.member(jsii_name="modeBlockInput")
    def mode_block_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "modeBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="protectionInput")
    def protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "protectionInput"))

    @builtins.property
    @jsii.member(jsii_name="reportUriInput")
    def report_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reportUriInput"))

    @builtins.property
    @jsii.member(jsii_name="modeBlock")
    def mode_block(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "modeBlock"))

    @mode_block.setter
    def mode_block(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e6a8a6fced9922d1773f48a6199077a5d452afa02f5242f7b3091769648877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modeBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba235cb13c156ab8eb99892ac549014172d0e3c0d5fce0759d264793da70038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protection")
    def protection(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "protection"))

    @protection.setter
    def protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b5f7fb701eeb9a55f30b349d5a0a157742c6a5bd0e6096ce91cd50d1dc7f21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reportUri")
    def report_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reportUri"))

    @report_uri.setter
    def report_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a68916b15f38c9c68b4678bbea7bd3e5ea69cea6969424cb2924389f91d2dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68cd0782513bc02e887d3d472910f4f51ca766cd5882360bff4e245b92669ef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyServerTimingHeadersConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "sampling_rate": "samplingRate"},
)
class CloudfrontResponseHeadersPolicyServerTimingHeadersConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        sampling_rate: jsii.Number,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#enabled CloudfrontResponseHeadersPolicy#enabled}.
        :param sampling_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#sampling_rate CloudfrontResponseHeadersPolicy#sampling_rate}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7edce38b836c369ca67bc23c5598ded5b20a5cc3c85b726abadda69542b3cb1)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument sampling_rate", value=sampling_rate, expected_type=type_hints["sampling_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "sampling_rate": sampling_rate,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#enabled CloudfrontResponseHeadersPolicy#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def sampling_rate(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_response_headers_policy#sampling_rate CloudfrontResponseHeadersPolicy#sampling_rate}.'''
        result = self._values.get("sampling_rate")
        assert result is not None, "Required property 'sampling_rate' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyServerTimingHeadersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyServerTimingHeadersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyServerTimingHeadersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98ff967fb48a25d0c772a07774e3125504d773e4100e249b817f5503dcaa4855)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingRateInput")
    def sampling_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingRateInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7cb8075f629b0a9bd8e2089523dff8cd2bff382158b38efc7245bbf03eea67d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samplingRate")
    def sampling_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingRate"))

    @sampling_rate.setter
    def sampling_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8815b9757b7bc81ac7585ba929a97b05363dd48f7785fd5f68e35b7be77beaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd18920e8ca0c29a35da3158829f41373ad9ebb8a56e165b727138b38395612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudfrontResponseHeadersPolicy",
    "CloudfrontResponseHeadersPolicyConfig",
    "CloudfrontResponseHeadersPolicyCorsConfig",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeadersOutputReference",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethodsOutputReference",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOriginsOutputReference",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeadersOutputReference",
    "CloudfrontResponseHeadersPolicyCorsConfigOutputReference",
    "CloudfrontResponseHeadersPolicyCustomHeadersConfig",
    "CloudfrontResponseHeadersPolicyCustomHeadersConfigItems",
    "CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsList",
    "CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsOutputReference",
    "CloudfrontResponseHeadersPolicyCustomHeadersConfigOutputReference",
    "CloudfrontResponseHeadersPolicyRemoveHeadersConfig",
    "CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems",
    "CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsList",
    "CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsOutputReference",
    "CloudfrontResponseHeadersPolicyRemoveHeadersConfigOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfig",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicyOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptionsOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptionsOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicyOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurityOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtectionOutputReference",
    "CloudfrontResponseHeadersPolicyServerTimingHeadersConfig",
    "CloudfrontResponseHeadersPolicyServerTimingHeadersConfigOutputReference",
]

publication.publish()

def _typecheckingstub__3469e0d2c3a77d5fcbee424b7c5484b3a933e595b3a268960fdf5ec852fe2544(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    cors_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyCorsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyCustomHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    remove_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyRemoveHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    server_timing_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__64755218843f4eaba2353c6052b3fa8cf9e8ea421b1f925152be382bdc168385(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275d408dc528f6dc86a5c31c9bd2510e55151e90898b1eed4a259c0740eca769(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d87b2083b9b3e1902ce1b67728162a35611a696e5890f4162a02f6e4ada767e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804ce5545b56ffd4922616f5972e2d6fe716f3bda635554dbfe850488f17a6f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fd2c2fd196f9bebf54e452b0da6f3cbe1e20eb4016c40a80e60d5df89092a1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    cors_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyCorsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyCustomHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    remove_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyRemoveHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    server_timing_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca6a9fc06fdd0d26a29df3a2c8d37ba4aaa1e10eb74fe60ed8cf100e4317f94(
    *,
    access_control_allow_credentials: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    access_control_allow_headers: typing.Union[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders, typing.Dict[builtins.str, typing.Any]],
    access_control_allow_methods: typing.Union[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods, typing.Dict[builtins.str, typing.Any]],
    access_control_allow_origins: typing.Union[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins, typing.Dict[builtins.str, typing.Any]],
    origin_override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    access_control_expose_headers: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders, typing.Dict[builtins.str, typing.Any]]] = None,
    access_control_max_age_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6a4d9c3bbf632e49b8663b00a91da4c4bbcc577753f04c453d0619e56295ed(
    *,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a613a21b54f40e21d9e6faee0bf8be2b5721589eb17c1a3fe8fdd1db4b93e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab22de074d43c58a46e8a08a1c2d05ebf3dec1bf96fee331ea497d8df047b9c1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945e8f05986238a4895b2a8a872207e8755ae607a820994cebbfbf1bb15fb3f8(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2b008eb944619b7f42b499c31a1ef877d93693ee0aea62b749dd0b3e7245a0(
    *,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58b65aa0644e05f328b6d483c87c7e526694d848703aa497a3cc31188460196(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc9e4f0f040c28c247a40d918a000269d6d9f9db5bbd825c29c5e1342731a87(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fd43badc2f8e83f398c0806c6d4f92aea841118d2582f0bbd847537753a60a(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3baead73467b07aef9842b71f049104117ca4cfc35c48dfd8ce32889b6bedd(
    *,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6372c19ed8c27c205c609e33f86720f88bb798a3eb1c6746b18a31c150c5d861(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812b7b4a9ddf94718a7eaa5df901f5469a3ae81536221aff5834fc7aefd62d59(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aab51b4dac62a5d5627ad00c91dcc253e6314dbcdf1d4dc6415f2ab3c8f0152(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c167a55dbd5142c8679da45bcb380e132a16c4c514266e0ee2d458ac73f62a(
    *,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f36dc01859b4194064c0c3e71d1d6822e9b2c0f25598ab897b2e9c0869d6f69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40efece05d26568091733e88b1fa7f5a5f2ad1378a2627a014d261dc551a244(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81d7bc9722fd05fbf23d60a06481ff86d90f175367ec4f353aa9744c68aaca8(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a11d970fd8ee0a9d9f5d1797d5e9d46f09f8eced56b94b6df10147b562578f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fcfee7e3a295567880b8e87504afe7e86267964d491574e68acca46edee516c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0933b57f20553e3890337dd3dbe2384ef069bcba0622eff6209c3d1c48a375(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f263905b141c4890601943d51bcdf34bb5f05066d5ecb39b324ac7e0682fa91(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa12a860a6017991befb24e8174574a26a62b98fee698fbaa4d4bf8bfafddee(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4aba3d3a16c805e4e92243e8835df45fb19df25064408a4160c26e8af50b6d1(
    *,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598bd6abbff23f48ac2b9f8383191becf69dcd6904fcfde751d366b620c6f623(
    *,
    header: builtins.str,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562216f1d5d811ad568508c4d25180614b8d679728908badaa01e84d4c979ee2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a27b40ce6d2da628338823e61d5f90241cc53b7d7ba0efefe204699e493a6b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4b9e1c4ffbfe2ceff639e90ab9b96450130e88e166bfacaf8db2178d2d89ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17aebf54e4b2874b1e42682357aa5776e0950c079370d0292e69255d800dfa96(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255da06ff5ed37dc3cd3eacc7cd04fd55b5adf9a5b2593596315356ed1c48ffd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e8ef15bfdffa0bf2ff947378ce41329717faefae35a765a0bb2d55d7c1a205(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c73e775276cf1a5b0a412dd115670c83dbab5ed7ea1d9b19d170cfdf5c47b66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a6ad836926b4b3790a988ad8a5815bccbe92f8d6698834f4fc50cb284fcc0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab907f42cfe640e5e05fba696a9d72c39cbd9ea025f206f731c4d7e6f8d81e76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205363190339a172e5b4f4b6cbc6a9a4fd1073302c37ac4aaa852b22f4afb8d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1051dca093aaad269464dffcf3c62bc4bb56bc5afa586c07698d10b086ae96e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009916e3ea8679fdbe602ae54de05bcd9636fa6e735d4ddc314b38653de0cc19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d79875d5412a4b51d0600bb1d2faeb7d5919507475dadd64ff42cd161bb4f88(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18cd4548fcd984608bd1e4493409cc96392bbc84a9578b6d025ab275cf904a5(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCustomHeadersConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e15a028a6f8e592cc67c268594d0856ac8ce17f398835d57d5e1d5d94e0b08(
    *,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895973d151cbe23ca00dc8a4b3deebf4d10340297f57ad467492c01ba07c670f(
    *,
    header: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f136b6a8e63069f498031497800d824481f4ddc2f472d9563e40e8f2e4785258(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a652ebbcca4a1672af51ebd20b7dba5f2444d1e2cc027884461847b7198ccd35(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdf570f626e81cea1fccd85d8246b77c2d5007578c214df93ec2037d02e8248(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff43cd8ea2a34856db37885969df5ec23b6a857784ade92975addc3303919bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43143fcfb5995c45099a6916a3e40396207a5b12817798c7be226ffe24b73449(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3412d54932676c3956369934c6135725df6fefaa3a3cb2d04e560d12947f75e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972fa73fdf920953659d491cb9f867c16dbe1c84c480d980f057a137930adfda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f022e38a52a4c93dd9af2224e4d9fede2fb79ce6bfa6933aee461238bbd80da0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e154023026c1ec528cf05c101f338a30680559fc25d4944bb9692bc95ed9e63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01555ee6d0c23e1783b0278fdff831ddf0d90bfa653c9b6721bbb935014244a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4007f6e5760d49cea668f98d4dcb48774a22f897465943b391789bb3edb6557b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08498880e8810d94db2c752952ebb77ed639e85cb15fd9378338ea5cf2fc8d55(
    value: typing.Optional[CloudfrontResponseHeadersPolicyRemoveHeadersConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe4a8fb6dc9b6732b448fe9597f27453e55b08162c78209101740240ec20b9d(
    *,
    content_security_policy: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    content_type_options: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    frame_options: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    referrer_policy: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    strict_transport_security: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity, typing.Dict[builtins.str, typing.Any]]] = None,
    xss_protection: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a997127bb75a27e18fd697b9f1caebf3d8b60d6907f4bb4e65aeb94ed857dd48(
    *,
    content_security_policy: builtins.str,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201a078470943ca894fc90094bd96b9535651183d77428bfcc07ac310bb2c2f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5d1dd05fde63ecdebefefc84642cc9144bced897efe1f4161cb38d6fb4dd31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b20e80b3cad3424708167d3fb07fc048d49375247e6a7a638d6a04c936ec5c3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760bafb8925cfcba282093fbe4b5845814a9fb723089a9830054afc47067a14b(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591bf45431cb85b3af5b5f334fb172b8e9157bb5cd8abeaa961249106fa34dda(
    *,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66833fd9a40904b5c50d7c8e4693e87d726f478c9ceb8ebf8d0a577dfef68461(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435b940edf54cb445e947a6b3b499a9c8006c2ec29888148b23f0ab5c9e5a50c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb9e463cbe45e87b42f54262dba485df87b7a90f15a2c3e1838fce012c7a047(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bfad5f54f48fe02590edfcd5a50d96775670946be96c132712a11c6160b4c6(
    *,
    frame_option: builtins.str,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a0a55f6ae5d213b75a1d62cb5168f30a51fac5cbf703ed0f0b6a66e9dc9fe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a37bee800c8243000c0c4fdf6be110cc2a0bf4ed79271bae948508633b8932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8da329922cb77666049f81beb007131039807ee5c26e0d77c7c7f29eebc6653(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0431657d3e7d06c7245f2dc2c7cca7caaef5b507e2dae7c48e9293c37d60d8d8(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f0722d0dea13b168d03d952d2cffec850c92a7ce464ee1195d7b52ee3a326e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743d3d1ae27071b17a4c8d00391ca276d0b4192e638abd20c7bcc7794c500b3a(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96cef8fe755eaf5935f2ccab6d688678483e208a2b34cb9f1e5ac7498318da3(
    *,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    referrer_policy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2bf7b0ca90d15f2153c9e91ba4d7c6819961c4cdd81b59b1b540fa1da183a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608616ba24beb1b1b34bcc4302484a375309c486f68155bb0e33f0f645bba0b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ae440648602fe30b7da1e3037da995533eac382b7ef951b8a7b2c246c38e44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896028b2af3652453b658238d528cde6ecab6ad1afb92a3cb571c10c3accf1ba(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b4a5e9a2aa5f93b2eb8be98e305c5477d779a408f9d5ad494ac4e6b6406867(
    *,
    access_control_max_age_sec: jsii.Number,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7f6f8d760042dfcb40cd4329a07f2a82abcbdf923ea45d15eb926d3c9b77d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d79d28658f66f605d2820b46c2608d3b620a7e55ada05b3e20b3a49eab447b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a426770f01c56263240f6bd5dad56539bcf60dcbb64d10f49fc32287f9dc05e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2378cf1fc38cb8d5d6c56a8d6f127b1282b9af11210adb117938829643ddaaaa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2eb899d341c3b4a05cb6b4d0582b2c939ea84a46ec8ef7e353b6d631c972745(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a025f9ef2635691a62cf6b21d42147e057f3d54d4ec9d0666cca5f34018320(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f320e180d6421f0982d5437b4b54b2f20bdf3616fcc10a59b03340ff2814240(
    *,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    protection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    mode_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    report_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01d78db1ec37ad40813e976ce7b42ca8578f7fe99d1aa5aad3265af8377cfe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e6a8a6fced9922d1773f48a6199077a5d452afa02f5242f7b3091769648877(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba235cb13c156ab8eb99892ac549014172d0e3c0d5fce0759d264793da70038(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b5f7fb701eeb9a55f30b349d5a0a157742c6a5bd0e6096ce91cd50d1dc7f21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a68916b15f38c9c68b4678bbea7bd3e5ea69cea6969424cb2924389f91d2dbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68cd0782513bc02e887d3d472910f4f51ca766cd5882360bff4e245b92669ef2(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7edce38b836c369ca67bc23c5598ded5b20a5cc3c85b726abadda69542b3cb1(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    sampling_rate: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ff967fb48a25d0c772a07774e3125504d773e4100e249b817f5503dcaa4855(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb8075f629b0a9bd8e2089523dff8cd2bff382158b38efc7245bbf03eea67d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8815b9757b7bc81ac7585ba929a97b05363dd48f7785fd5f68e35b7be77beaf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd18920e8ca0c29a35da3158829f41373ad9ebb8a56e165b727138b38395612(
    value: typing.Optional[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig],
) -> None:
    """Type checking stubs"""
    pass
