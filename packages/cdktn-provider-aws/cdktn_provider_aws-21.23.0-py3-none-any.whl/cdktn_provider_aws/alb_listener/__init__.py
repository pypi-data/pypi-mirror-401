r'''
# `aws_alb_listener`

Refer to the Terraform Registry for docs: [`aws_alb_listener`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener).
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


class AlbListener(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListener",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener aws_alb_listener}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlbListenerDefaultAction", typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_arn: builtins.str,
        alpn_policy: typing.Optional[builtins.str] = None,
        certificate_arn: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mutual_authentication: typing.Optional[typing.Union["AlbListenerMutualAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_issuer_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_leaf_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_subject_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_validity_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_tls_cipher_suite_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_tls_version_header_name: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_allow_credentials_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_allow_headers_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_allow_methods_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_allow_origin_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_expose_headers_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_max_age_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_content_security_policy_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_server_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        routing_http_response_strict_transport_security_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_x_content_type_options_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_x_frame_options_header_value: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tcp_idle_timeout_seconds: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["AlbListenerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener aws_alb_listener} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_action: default_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#default_action AlbListener#default_action}
        :param load_balancer_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#load_balancer_arn AlbListener#load_balancer_arn}.
        :param alpn_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#alpn_policy AlbListener#alpn_policy}.
        :param certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#certificate_arn AlbListener#certificate_arn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#id AlbListener#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mutual_authentication: mutual_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#mutual_authentication AlbListener#mutual_authentication}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#port AlbListener#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#protocol AlbListener#protocol}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#region AlbListener#region}
        :param routing_http_request_x_amzn_mtls_clientcert_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_header_name}.
        :param routing_http_request_x_amzn_mtls_clientcert_issuer_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_issuer_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_issuer_header_name}.
        :param routing_http_request_x_amzn_mtls_clientcert_leaf_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_leaf_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_leaf_header_name}.
        :param routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name}.
        :param routing_http_request_x_amzn_mtls_clientcert_subject_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_subject_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_subject_header_name}.
        :param routing_http_request_x_amzn_mtls_clientcert_validity_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_validity_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_validity_header_name}.
        :param routing_http_request_x_amzn_tls_cipher_suite_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_tls_cipher_suite_header_name AlbListener#routing_http_request_x_amzn_tls_cipher_suite_header_name}.
        :param routing_http_request_x_amzn_tls_version_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_tls_version_header_name AlbListener#routing_http_request_x_amzn_tls_version_header_name}.
        :param routing_http_response_access_control_allow_credentials_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_credentials_header_value AlbListener#routing_http_response_access_control_allow_credentials_header_value}.
        :param routing_http_response_access_control_allow_headers_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_headers_header_value AlbListener#routing_http_response_access_control_allow_headers_header_value}.
        :param routing_http_response_access_control_allow_methods_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_methods_header_value AlbListener#routing_http_response_access_control_allow_methods_header_value}.
        :param routing_http_response_access_control_allow_origin_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_origin_header_value AlbListener#routing_http_response_access_control_allow_origin_header_value}.
        :param routing_http_response_access_control_expose_headers_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_expose_headers_header_value AlbListener#routing_http_response_access_control_expose_headers_header_value}.
        :param routing_http_response_access_control_max_age_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_max_age_header_value AlbListener#routing_http_response_access_control_max_age_header_value}.
        :param routing_http_response_content_security_policy_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_content_security_policy_header_value AlbListener#routing_http_response_content_security_policy_header_value}.
        :param routing_http_response_server_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_server_enabled AlbListener#routing_http_response_server_enabled}.
        :param routing_http_response_strict_transport_security_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_strict_transport_security_header_value AlbListener#routing_http_response_strict_transport_security_header_value}.
        :param routing_http_response_x_content_type_options_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_x_content_type_options_header_value AlbListener#routing_http_response_x_content_type_options_header_value}.
        :param routing_http_response_x_frame_options_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_x_frame_options_header_value AlbListener#routing_http_response_x_frame_options_header_value}.
        :param ssl_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#ssl_policy AlbListener#ssl_policy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#tags AlbListener#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#tags_all AlbListener#tags_all}.
        :param tcp_idle_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#tcp_idle_timeout_seconds AlbListener#tcp_idle_timeout_seconds}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#timeouts AlbListener#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf8746a6d47e59ae9099b04e73335e346f590c59816e096d27ea27c689ee96f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AlbListenerConfig(
            default_action=default_action,
            load_balancer_arn=load_balancer_arn,
            alpn_policy=alpn_policy,
            certificate_arn=certificate_arn,
            id=id,
            mutual_authentication=mutual_authentication,
            port=port,
            protocol=protocol,
            region=region,
            routing_http_request_x_amzn_mtls_clientcert_header_name=routing_http_request_x_amzn_mtls_clientcert_header_name,
            routing_http_request_x_amzn_mtls_clientcert_issuer_header_name=routing_http_request_x_amzn_mtls_clientcert_issuer_header_name,
            routing_http_request_x_amzn_mtls_clientcert_leaf_header_name=routing_http_request_x_amzn_mtls_clientcert_leaf_header_name,
            routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name=routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name,
            routing_http_request_x_amzn_mtls_clientcert_subject_header_name=routing_http_request_x_amzn_mtls_clientcert_subject_header_name,
            routing_http_request_x_amzn_mtls_clientcert_validity_header_name=routing_http_request_x_amzn_mtls_clientcert_validity_header_name,
            routing_http_request_x_amzn_tls_cipher_suite_header_name=routing_http_request_x_amzn_tls_cipher_suite_header_name,
            routing_http_request_x_amzn_tls_version_header_name=routing_http_request_x_amzn_tls_version_header_name,
            routing_http_response_access_control_allow_credentials_header_value=routing_http_response_access_control_allow_credentials_header_value,
            routing_http_response_access_control_allow_headers_header_value=routing_http_response_access_control_allow_headers_header_value,
            routing_http_response_access_control_allow_methods_header_value=routing_http_response_access_control_allow_methods_header_value,
            routing_http_response_access_control_allow_origin_header_value=routing_http_response_access_control_allow_origin_header_value,
            routing_http_response_access_control_expose_headers_header_value=routing_http_response_access_control_expose_headers_header_value,
            routing_http_response_access_control_max_age_header_value=routing_http_response_access_control_max_age_header_value,
            routing_http_response_content_security_policy_header_value=routing_http_response_content_security_policy_header_value,
            routing_http_response_server_enabled=routing_http_response_server_enabled,
            routing_http_response_strict_transport_security_header_value=routing_http_response_strict_transport_security_header_value,
            routing_http_response_x_content_type_options_header_value=routing_http_response_x_content_type_options_header_value,
            routing_http_response_x_frame_options_header_value=routing_http_response_x_frame_options_header_value,
            ssl_policy=ssl_policy,
            tags=tags,
            tags_all=tags_all,
            tcp_idle_timeout_seconds=tcp_idle_timeout_seconds,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a AlbListener resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AlbListener to import.
        :param import_from_id: The id of the existing AlbListener that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AlbListener to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acdc6260d85b0d8c29dc35fe879ef1f11a099046b38d241a9cef963ff7a99bf5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDefaultAction")
    def put_default_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlbListenerDefaultAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292a6d2ac5f9d7f9825be476798b0fbb8b61df0d27739f03f36c8fa122d13ff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDefaultAction", [value]))

    @jsii.member(jsii_name="putMutualAuthentication")
    def put_mutual_authentication(
        self,
        *,
        mode: builtins.str,
        advertise_trust_store_ca_names: typing.Optional[builtins.str] = None,
        ignore_client_certificate_expiry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trust_store_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#mode AlbListener#mode}.
        :param advertise_trust_store_ca_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#advertise_trust_store_ca_names AlbListener#advertise_trust_store_ca_names}.
        :param ignore_client_certificate_expiry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#ignore_client_certificate_expiry AlbListener#ignore_client_certificate_expiry}.
        :param trust_store_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#trust_store_arn AlbListener#trust_store_arn}.
        '''
        value = AlbListenerMutualAuthentication(
            mode=mode,
            advertise_trust_store_ca_names=advertise_trust_store_ca_names,
            ignore_client_certificate_expiry=ignore_client_certificate_expiry,
            trust_store_arn=trust_store_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putMutualAuthentication", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#create AlbListener#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#update AlbListener#update}.
        '''
        value = AlbListenerTimeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAlpnPolicy")
    def reset_alpn_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlpnPolicy", []))

    @jsii.member(jsii_name="resetCertificateArn")
    def reset_certificate_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateArn", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMutualAuthentication")
    def reset_mutual_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMutualAuthentication", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRoutingHttpRequestXAmznMtlsClientcertHeaderName")
    def reset_routing_http_request_x_amzn_mtls_clientcert_header_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpRequestXAmznMtlsClientcertHeaderName", []))

    @jsii.member(jsii_name="resetRoutingHttpRequestXAmznMtlsClientcertIssuerHeaderName")
    def reset_routing_http_request_x_amzn_mtls_clientcert_issuer_header_name(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpRequestXAmznMtlsClientcertIssuerHeaderName", []))

    @jsii.member(jsii_name="resetRoutingHttpRequestXAmznMtlsClientcertLeafHeaderName")
    def reset_routing_http_request_x_amzn_mtls_clientcert_leaf_header_name(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpRequestXAmznMtlsClientcertLeafHeaderName", []))

    @jsii.member(jsii_name="resetRoutingHttpRequestXAmznMtlsClientcertSerialNumberHeaderName")
    def reset_routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpRequestXAmznMtlsClientcertSerialNumberHeaderName", []))

    @jsii.member(jsii_name="resetRoutingHttpRequestXAmznMtlsClientcertSubjectHeaderName")
    def reset_routing_http_request_x_amzn_mtls_clientcert_subject_header_name(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpRequestXAmznMtlsClientcertSubjectHeaderName", []))

    @jsii.member(jsii_name="resetRoutingHttpRequestXAmznMtlsClientcertValidityHeaderName")
    def reset_routing_http_request_x_amzn_mtls_clientcert_validity_header_name(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpRequestXAmznMtlsClientcertValidityHeaderName", []))

    @jsii.member(jsii_name="resetRoutingHttpRequestXAmznTlsCipherSuiteHeaderName")
    def reset_routing_http_request_x_amzn_tls_cipher_suite_header_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpRequestXAmznTlsCipherSuiteHeaderName", []))

    @jsii.member(jsii_name="resetRoutingHttpRequestXAmznTlsVersionHeaderName")
    def reset_routing_http_request_x_amzn_tls_version_header_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpRequestXAmznTlsVersionHeaderName", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseAccessControlAllowCredentialsHeaderValue")
    def reset_routing_http_response_access_control_allow_credentials_header_value(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseAccessControlAllowCredentialsHeaderValue", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseAccessControlAllowHeadersHeaderValue")
    def reset_routing_http_response_access_control_allow_headers_header_value(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseAccessControlAllowHeadersHeaderValue", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseAccessControlAllowMethodsHeaderValue")
    def reset_routing_http_response_access_control_allow_methods_header_value(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseAccessControlAllowMethodsHeaderValue", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseAccessControlAllowOriginHeaderValue")
    def reset_routing_http_response_access_control_allow_origin_header_value(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseAccessControlAllowOriginHeaderValue", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseAccessControlExposeHeadersHeaderValue")
    def reset_routing_http_response_access_control_expose_headers_header_value(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseAccessControlExposeHeadersHeaderValue", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseAccessControlMaxAgeHeaderValue")
    def reset_routing_http_response_access_control_max_age_header_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseAccessControlMaxAgeHeaderValue", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseContentSecurityPolicyHeaderValue")
    def reset_routing_http_response_content_security_policy_header_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseContentSecurityPolicyHeaderValue", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseServerEnabled")
    def reset_routing_http_response_server_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseServerEnabled", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseStrictTransportSecurityHeaderValue")
    def reset_routing_http_response_strict_transport_security_header_value(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseStrictTransportSecurityHeaderValue", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseXContentTypeOptionsHeaderValue")
    def reset_routing_http_response_x_content_type_options_header_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseXContentTypeOptionsHeaderValue", []))

    @jsii.member(jsii_name="resetRoutingHttpResponseXFrameOptionsHeaderValue")
    def reset_routing_http_response_x_frame_options_header_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingHttpResponseXFrameOptionsHeaderValue", []))

    @jsii.member(jsii_name="resetSslPolicy")
    def reset_ssl_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslPolicy", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTcpIdleTimeoutSeconds")
    def reset_tcp_idle_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpIdleTimeoutSeconds", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="defaultAction")
    def default_action(self) -> "AlbListenerDefaultActionList":
        return typing.cast("AlbListenerDefaultActionList", jsii.get(self, "defaultAction"))

    @builtins.property
    @jsii.member(jsii_name="mutualAuthentication")
    def mutual_authentication(self) -> "AlbListenerMutualAuthenticationOutputReference":
        return typing.cast("AlbListenerMutualAuthenticationOutputReference", jsii.get(self, "mutualAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AlbListenerTimeoutsOutputReference":
        return typing.cast("AlbListenerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="alpnPolicyInput")
    def alpn_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alpnPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateArnInput")
    def certificate_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateArnInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultActionInput")
    def default_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlbListenerDefaultAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlbListenerDefaultAction"]]], jsii.get(self, "defaultActionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerArnInput")
    def load_balancer_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="mutualAuthenticationInput")
    def mutual_authentication_input(
        self,
    ) -> typing.Optional["AlbListenerMutualAuthentication"]:
        return typing.cast(typing.Optional["AlbListenerMutualAuthentication"], jsii.get(self, "mutualAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertHeaderNameInput")
    def routing_http_request_x_amzn_mtls_clientcert_header_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpRequestXAmznMtlsClientcertHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertIssuerHeaderNameInput")
    def routing_http_request_x_amzn_mtls_clientcert_issuer_header_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpRequestXAmznMtlsClientcertIssuerHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertLeafHeaderNameInput")
    def routing_http_request_x_amzn_mtls_clientcert_leaf_header_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpRequestXAmznMtlsClientcertLeafHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertSerialNumberHeaderNameInput")
    def routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpRequestXAmznMtlsClientcertSerialNumberHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertSubjectHeaderNameInput")
    def routing_http_request_x_amzn_mtls_clientcert_subject_header_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpRequestXAmznMtlsClientcertSubjectHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertValidityHeaderNameInput")
    def routing_http_request_x_amzn_mtls_clientcert_validity_header_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpRequestXAmznMtlsClientcertValidityHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznTlsCipherSuiteHeaderNameInput")
    def routing_http_request_x_amzn_tls_cipher_suite_header_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpRequestXAmznTlsCipherSuiteHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznTlsVersionHeaderNameInput")
    def routing_http_request_x_amzn_tls_version_header_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpRequestXAmznTlsVersionHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlAllowCredentialsHeaderValueInput")
    def routing_http_response_access_control_allow_credentials_header_value_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpResponseAccessControlAllowCredentialsHeaderValueInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlAllowHeadersHeaderValueInput")
    def routing_http_response_access_control_allow_headers_header_value_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpResponseAccessControlAllowHeadersHeaderValueInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlAllowMethodsHeaderValueInput")
    def routing_http_response_access_control_allow_methods_header_value_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpResponseAccessControlAllowMethodsHeaderValueInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlAllowOriginHeaderValueInput")
    def routing_http_response_access_control_allow_origin_header_value_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpResponseAccessControlAllowOriginHeaderValueInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlExposeHeadersHeaderValueInput")
    def routing_http_response_access_control_expose_headers_header_value_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpResponseAccessControlExposeHeadersHeaderValueInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlMaxAgeHeaderValueInput")
    def routing_http_response_access_control_max_age_header_value_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpResponseAccessControlMaxAgeHeaderValueInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseContentSecurityPolicyHeaderValueInput")
    def routing_http_response_content_security_policy_header_value_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpResponseContentSecurityPolicyHeaderValueInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseServerEnabledInput")
    def routing_http_response_server_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "routingHttpResponseServerEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseStrictTransportSecurityHeaderValueInput")
    def routing_http_response_strict_transport_security_header_value_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpResponseStrictTransportSecurityHeaderValueInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseXContentTypeOptionsHeaderValueInput")
    def routing_http_response_x_content_type_options_header_value_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpResponseXContentTypeOptionsHeaderValueInput"))

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseXFrameOptionsHeaderValueInput")
    def routing_http_response_x_frame_options_header_value_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingHttpResponseXFrameOptionsHeaderValueInput"))

    @builtins.property
    @jsii.member(jsii_name="sslPolicyInput")
    def ssl_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslPolicyInput"))

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
    @jsii.member(jsii_name="tcpIdleTimeoutSecondsInput")
    def tcp_idle_timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tcpIdleTimeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AlbListenerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AlbListenerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="alpnPolicy")
    def alpn_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alpnPolicy"))

    @alpn_policy.setter
    def alpn_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c1395e999cdd486c5a1b62b4c629a0129c0f374f63c129c917edd90e15cc2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alpnPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @certificate_arn.setter
    def certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145b33244ea5379032950da8648be0b24427e405ba4f3fe65911bef34fd4c6ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14112212713ae292a1d8d05c39739103c4cd21a900c43928b7a5837a1d68000a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerArn"))

    @load_balancer_arn.setter
    def load_balancer_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d714b3fa310595945b8b61e96a952c1a8b67b07163d1f0f2d0b0963464e1ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab3a5982ea9d96a33dcd7b4b7451b0d23080eb68d0cab6ea10231bbe5fd75dec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1034d9c5382401769551cd84094ce76ff885f945ce185d147cacbc0912a61049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381167ab8e2aa999c1e3b9d55bd1b02911d41e0f03becc0fee849f09007fdbd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertHeaderName")
    def routing_http_request_x_amzn_mtls_clientcert_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpRequestXAmznMtlsClientcertHeaderName"))

    @routing_http_request_x_amzn_mtls_clientcert_header_name.setter
    def routing_http_request_x_amzn_mtls_clientcert_header_name(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3b3dfd9b19d29b99c10f5fea6bd209aa9de7e694c2b45793fcd9941f927f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpRequestXAmznMtlsClientcertHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertIssuerHeaderName")
    def routing_http_request_x_amzn_mtls_clientcert_issuer_header_name(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpRequestXAmznMtlsClientcertIssuerHeaderName"))

    @routing_http_request_x_amzn_mtls_clientcert_issuer_header_name.setter
    def routing_http_request_x_amzn_mtls_clientcert_issuer_header_name(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805a6787ffc680dc67914c88bb6d5cffe61b16e2967bba6271cf9521bfe9c364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpRequestXAmznMtlsClientcertIssuerHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertLeafHeaderName")
    def routing_http_request_x_amzn_mtls_clientcert_leaf_header_name(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpRequestXAmznMtlsClientcertLeafHeaderName"))

    @routing_http_request_x_amzn_mtls_clientcert_leaf_header_name.setter
    def routing_http_request_x_amzn_mtls_clientcert_leaf_header_name(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14ac1d4c5f7fbe0b83cac1b018be1b4ca578ef80afe9f54c7dfc14746e8b899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpRequestXAmznMtlsClientcertLeafHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertSerialNumberHeaderName")
    def routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpRequestXAmznMtlsClientcertSerialNumberHeaderName"))

    @routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name.setter
    def routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4664c9255d04339585ce97cd1ca9f74750be17d48f23755cdb5022bd63a2c613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpRequestXAmznMtlsClientcertSerialNumberHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertSubjectHeaderName")
    def routing_http_request_x_amzn_mtls_clientcert_subject_header_name(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpRequestXAmznMtlsClientcertSubjectHeaderName"))

    @routing_http_request_x_amzn_mtls_clientcert_subject_header_name.setter
    def routing_http_request_x_amzn_mtls_clientcert_subject_header_name(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42b8fef6fb45883ac60f36458d1876e299bfa56e0cd8a6c275272e349f3361e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpRequestXAmznMtlsClientcertSubjectHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznMtlsClientcertValidityHeaderName")
    def routing_http_request_x_amzn_mtls_clientcert_validity_header_name(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpRequestXAmznMtlsClientcertValidityHeaderName"))

    @routing_http_request_x_amzn_mtls_clientcert_validity_header_name.setter
    def routing_http_request_x_amzn_mtls_clientcert_validity_header_name(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df664291213b8219538ba3538ca588f1faefc850937735b491c71d0a89c9fb28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpRequestXAmznMtlsClientcertValidityHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznTlsCipherSuiteHeaderName")
    def routing_http_request_x_amzn_tls_cipher_suite_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpRequestXAmznTlsCipherSuiteHeaderName"))

    @routing_http_request_x_amzn_tls_cipher_suite_header_name.setter
    def routing_http_request_x_amzn_tls_cipher_suite_header_name(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb0505a0e55d79ac06bd652951d56e380402bab631a5caef3a631535627aca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpRequestXAmznTlsCipherSuiteHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpRequestXAmznTlsVersionHeaderName")
    def routing_http_request_x_amzn_tls_version_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpRequestXAmznTlsVersionHeaderName"))

    @routing_http_request_x_amzn_tls_version_header_name.setter
    def routing_http_request_x_amzn_tls_version_header_name(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__803bbe07b2f2b906daad428af4edc86d6ca31eda30f7c6cd3c495873ce18c7ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpRequestXAmznTlsVersionHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlAllowCredentialsHeaderValue")
    def routing_http_response_access_control_allow_credentials_header_value(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpResponseAccessControlAllowCredentialsHeaderValue"))

    @routing_http_response_access_control_allow_credentials_header_value.setter
    def routing_http_response_access_control_allow_credentials_header_value(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a444807e28a0796ff0bb68a3ae3816d65f78567b3462cdaf2edfeb694f5c86c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseAccessControlAllowCredentialsHeaderValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlAllowHeadersHeaderValue")
    def routing_http_response_access_control_allow_headers_header_value(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpResponseAccessControlAllowHeadersHeaderValue"))

    @routing_http_response_access_control_allow_headers_header_value.setter
    def routing_http_response_access_control_allow_headers_header_value(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2419961ee96e9ce9d9d511bdb912d4656c4e788d8f3ca936fc663f4ed0cb4f15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseAccessControlAllowHeadersHeaderValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlAllowMethodsHeaderValue")
    def routing_http_response_access_control_allow_methods_header_value(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpResponseAccessControlAllowMethodsHeaderValue"))

    @routing_http_response_access_control_allow_methods_header_value.setter
    def routing_http_response_access_control_allow_methods_header_value(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4a28f3d0b8f3cb49eafd1f223848c2ea73f7daddfb692e0be495bdbe968f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseAccessControlAllowMethodsHeaderValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlAllowOriginHeaderValue")
    def routing_http_response_access_control_allow_origin_header_value(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpResponseAccessControlAllowOriginHeaderValue"))

    @routing_http_response_access_control_allow_origin_header_value.setter
    def routing_http_response_access_control_allow_origin_header_value(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc55b00150dce77f18db23b34bc79233362a0945baa0690e301a1a56270baa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseAccessControlAllowOriginHeaderValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlExposeHeadersHeaderValue")
    def routing_http_response_access_control_expose_headers_header_value(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpResponseAccessControlExposeHeadersHeaderValue"))

    @routing_http_response_access_control_expose_headers_header_value.setter
    def routing_http_response_access_control_expose_headers_header_value(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873028027c8ec7948329fa8c98d4fea8da07bb91cb8c42d78590fe58c2900e24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseAccessControlExposeHeadersHeaderValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseAccessControlMaxAgeHeaderValue")
    def routing_http_response_access_control_max_age_header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpResponseAccessControlMaxAgeHeaderValue"))

    @routing_http_response_access_control_max_age_header_value.setter
    def routing_http_response_access_control_max_age_header_value(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b286686f08cdc0c64c5a0b08ac3b9a57882acc4e2ced31eb7599d15fcd4edcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseAccessControlMaxAgeHeaderValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseContentSecurityPolicyHeaderValue")
    def routing_http_response_content_security_policy_header_value(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpResponseContentSecurityPolicyHeaderValue"))

    @routing_http_response_content_security_policy_header_value.setter
    def routing_http_response_content_security_policy_header_value(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609a38d60317a8eebbf1893cfe47a6d578eaf32b3f7f9ec2c1c2b9e70f77a82b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseContentSecurityPolicyHeaderValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseServerEnabled")
    def routing_http_response_server_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "routingHttpResponseServerEnabled"))

    @routing_http_response_server_enabled.setter
    def routing_http_response_server_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b033ae6e7d5ec115a42432561cc0dccb7e99f1546cce80de0ac245b6e5a8bb27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseServerEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseStrictTransportSecurityHeaderValue")
    def routing_http_response_strict_transport_security_header_value(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpResponseStrictTransportSecurityHeaderValue"))

    @routing_http_response_strict_transport_security_header_value.setter
    def routing_http_response_strict_transport_security_header_value(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2c1ed20601548a2f96c5b8fcff217fe0597652580948613a4aeb7c09be7659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseStrictTransportSecurityHeaderValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseXContentTypeOptionsHeaderValue")
    def routing_http_response_x_content_type_options_header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpResponseXContentTypeOptionsHeaderValue"))

    @routing_http_response_x_content_type_options_header_value.setter
    def routing_http_response_x_content_type_options_header_value(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3783555d0a18ee835df848ae4ceb7f5e704ecb6fda97b7c14b9a4874f4867d90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseXContentTypeOptionsHeaderValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingHttpResponseXFrameOptionsHeaderValue")
    def routing_http_response_x_frame_options_header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingHttpResponseXFrameOptionsHeaderValue"))

    @routing_http_response_x_frame_options_header_value.setter
    def routing_http_response_x_frame_options_header_value(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff1bc1bcd2a1f67e7374e11a629e418fe9944236b73fc51860f2394f72fa7d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingHttpResponseXFrameOptionsHeaderValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslPolicy"))

    @ssl_policy.setter
    def ssl_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9957a47f7c45541c05da7046bb3f7d71a166f1fc26eb8375a51284461b2fd841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4af8764f263d8f8be785a48883f404d0a7d53f614c2a91d1505f7c3e209059c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26585889f8c8d79b0fe1fdfe1f1dcd4f05ba078ec20ab052dbd34b3cc35ead15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpIdleTimeoutSeconds")
    def tcp_idle_timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpIdleTimeoutSeconds"))

    @tcp_idle_timeout_seconds.setter
    def tcp_idle_timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__058f4db2f5b02faf1c42c3d5924fdcc187eab5fcf9d9ca709f9dab555fb31142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpIdleTimeoutSeconds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_action": "defaultAction",
        "load_balancer_arn": "loadBalancerArn",
        "alpn_policy": "alpnPolicy",
        "certificate_arn": "certificateArn",
        "id": "id",
        "mutual_authentication": "mutualAuthentication",
        "port": "port",
        "protocol": "protocol",
        "region": "region",
        "routing_http_request_x_amzn_mtls_clientcert_header_name": "routingHttpRequestXAmznMtlsClientcertHeaderName",
        "routing_http_request_x_amzn_mtls_clientcert_issuer_header_name": "routingHttpRequestXAmznMtlsClientcertIssuerHeaderName",
        "routing_http_request_x_amzn_mtls_clientcert_leaf_header_name": "routingHttpRequestXAmznMtlsClientcertLeafHeaderName",
        "routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name": "routingHttpRequestXAmznMtlsClientcertSerialNumberHeaderName",
        "routing_http_request_x_amzn_mtls_clientcert_subject_header_name": "routingHttpRequestXAmznMtlsClientcertSubjectHeaderName",
        "routing_http_request_x_amzn_mtls_clientcert_validity_header_name": "routingHttpRequestXAmznMtlsClientcertValidityHeaderName",
        "routing_http_request_x_amzn_tls_cipher_suite_header_name": "routingHttpRequestXAmznTlsCipherSuiteHeaderName",
        "routing_http_request_x_amzn_tls_version_header_name": "routingHttpRequestXAmznTlsVersionHeaderName",
        "routing_http_response_access_control_allow_credentials_header_value": "routingHttpResponseAccessControlAllowCredentialsHeaderValue",
        "routing_http_response_access_control_allow_headers_header_value": "routingHttpResponseAccessControlAllowHeadersHeaderValue",
        "routing_http_response_access_control_allow_methods_header_value": "routingHttpResponseAccessControlAllowMethodsHeaderValue",
        "routing_http_response_access_control_allow_origin_header_value": "routingHttpResponseAccessControlAllowOriginHeaderValue",
        "routing_http_response_access_control_expose_headers_header_value": "routingHttpResponseAccessControlExposeHeadersHeaderValue",
        "routing_http_response_access_control_max_age_header_value": "routingHttpResponseAccessControlMaxAgeHeaderValue",
        "routing_http_response_content_security_policy_header_value": "routingHttpResponseContentSecurityPolicyHeaderValue",
        "routing_http_response_server_enabled": "routingHttpResponseServerEnabled",
        "routing_http_response_strict_transport_security_header_value": "routingHttpResponseStrictTransportSecurityHeaderValue",
        "routing_http_response_x_content_type_options_header_value": "routingHttpResponseXContentTypeOptionsHeaderValue",
        "routing_http_response_x_frame_options_header_value": "routingHttpResponseXFrameOptionsHeaderValue",
        "ssl_policy": "sslPolicy",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tcp_idle_timeout_seconds": "tcpIdleTimeoutSeconds",
        "timeouts": "timeouts",
    },
)
class AlbListenerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlbListenerDefaultAction", typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_arn: builtins.str,
        alpn_policy: typing.Optional[builtins.str] = None,
        certificate_arn: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mutual_authentication: typing.Optional[typing.Union["AlbListenerMutualAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_issuer_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_leaf_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_subject_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_mtls_clientcert_validity_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_tls_cipher_suite_header_name: typing.Optional[builtins.str] = None,
        routing_http_request_x_amzn_tls_version_header_name: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_allow_credentials_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_allow_headers_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_allow_methods_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_allow_origin_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_expose_headers_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_access_control_max_age_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_content_security_policy_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_server_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        routing_http_response_strict_transport_security_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_x_content_type_options_header_value: typing.Optional[builtins.str] = None,
        routing_http_response_x_frame_options_header_value: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tcp_idle_timeout_seconds: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["AlbListenerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_action: default_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#default_action AlbListener#default_action}
        :param load_balancer_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#load_balancer_arn AlbListener#load_balancer_arn}.
        :param alpn_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#alpn_policy AlbListener#alpn_policy}.
        :param certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#certificate_arn AlbListener#certificate_arn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#id AlbListener#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mutual_authentication: mutual_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#mutual_authentication AlbListener#mutual_authentication}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#port AlbListener#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#protocol AlbListener#protocol}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#region AlbListener#region}
        :param routing_http_request_x_amzn_mtls_clientcert_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_header_name}.
        :param routing_http_request_x_amzn_mtls_clientcert_issuer_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_issuer_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_issuer_header_name}.
        :param routing_http_request_x_amzn_mtls_clientcert_leaf_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_leaf_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_leaf_header_name}.
        :param routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name}.
        :param routing_http_request_x_amzn_mtls_clientcert_subject_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_subject_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_subject_header_name}.
        :param routing_http_request_x_amzn_mtls_clientcert_validity_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_validity_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_validity_header_name}.
        :param routing_http_request_x_amzn_tls_cipher_suite_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_tls_cipher_suite_header_name AlbListener#routing_http_request_x_amzn_tls_cipher_suite_header_name}.
        :param routing_http_request_x_amzn_tls_version_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_tls_version_header_name AlbListener#routing_http_request_x_amzn_tls_version_header_name}.
        :param routing_http_response_access_control_allow_credentials_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_credentials_header_value AlbListener#routing_http_response_access_control_allow_credentials_header_value}.
        :param routing_http_response_access_control_allow_headers_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_headers_header_value AlbListener#routing_http_response_access_control_allow_headers_header_value}.
        :param routing_http_response_access_control_allow_methods_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_methods_header_value AlbListener#routing_http_response_access_control_allow_methods_header_value}.
        :param routing_http_response_access_control_allow_origin_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_origin_header_value AlbListener#routing_http_response_access_control_allow_origin_header_value}.
        :param routing_http_response_access_control_expose_headers_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_expose_headers_header_value AlbListener#routing_http_response_access_control_expose_headers_header_value}.
        :param routing_http_response_access_control_max_age_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_max_age_header_value AlbListener#routing_http_response_access_control_max_age_header_value}.
        :param routing_http_response_content_security_policy_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_content_security_policy_header_value AlbListener#routing_http_response_content_security_policy_header_value}.
        :param routing_http_response_server_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_server_enabled AlbListener#routing_http_response_server_enabled}.
        :param routing_http_response_strict_transport_security_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_strict_transport_security_header_value AlbListener#routing_http_response_strict_transport_security_header_value}.
        :param routing_http_response_x_content_type_options_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_x_content_type_options_header_value AlbListener#routing_http_response_x_content_type_options_header_value}.
        :param routing_http_response_x_frame_options_header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_x_frame_options_header_value AlbListener#routing_http_response_x_frame_options_header_value}.
        :param ssl_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#ssl_policy AlbListener#ssl_policy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#tags AlbListener#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#tags_all AlbListener#tags_all}.
        :param tcp_idle_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#tcp_idle_timeout_seconds AlbListener#tcp_idle_timeout_seconds}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#timeouts AlbListener#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(mutual_authentication, dict):
            mutual_authentication = AlbListenerMutualAuthentication(**mutual_authentication)
        if isinstance(timeouts, dict):
            timeouts = AlbListenerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1c99867b759386eef64d60031f8b4c1c3fbe7cfdd21c3e168412ec5192774f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument load_balancer_arn", value=load_balancer_arn, expected_type=type_hints["load_balancer_arn"])
            check_type(argname="argument alpn_policy", value=alpn_policy, expected_type=type_hints["alpn_policy"])
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mutual_authentication", value=mutual_authentication, expected_type=type_hints["mutual_authentication"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument routing_http_request_x_amzn_mtls_clientcert_header_name", value=routing_http_request_x_amzn_mtls_clientcert_header_name, expected_type=type_hints["routing_http_request_x_amzn_mtls_clientcert_header_name"])
            check_type(argname="argument routing_http_request_x_amzn_mtls_clientcert_issuer_header_name", value=routing_http_request_x_amzn_mtls_clientcert_issuer_header_name, expected_type=type_hints["routing_http_request_x_amzn_mtls_clientcert_issuer_header_name"])
            check_type(argname="argument routing_http_request_x_amzn_mtls_clientcert_leaf_header_name", value=routing_http_request_x_amzn_mtls_clientcert_leaf_header_name, expected_type=type_hints["routing_http_request_x_amzn_mtls_clientcert_leaf_header_name"])
            check_type(argname="argument routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name", value=routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name, expected_type=type_hints["routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name"])
            check_type(argname="argument routing_http_request_x_amzn_mtls_clientcert_subject_header_name", value=routing_http_request_x_amzn_mtls_clientcert_subject_header_name, expected_type=type_hints["routing_http_request_x_amzn_mtls_clientcert_subject_header_name"])
            check_type(argname="argument routing_http_request_x_amzn_mtls_clientcert_validity_header_name", value=routing_http_request_x_amzn_mtls_clientcert_validity_header_name, expected_type=type_hints["routing_http_request_x_amzn_mtls_clientcert_validity_header_name"])
            check_type(argname="argument routing_http_request_x_amzn_tls_cipher_suite_header_name", value=routing_http_request_x_amzn_tls_cipher_suite_header_name, expected_type=type_hints["routing_http_request_x_amzn_tls_cipher_suite_header_name"])
            check_type(argname="argument routing_http_request_x_amzn_tls_version_header_name", value=routing_http_request_x_amzn_tls_version_header_name, expected_type=type_hints["routing_http_request_x_amzn_tls_version_header_name"])
            check_type(argname="argument routing_http_response_access_control_allow_credentials_header_value", value=routing_http_response_access_control_allow_credentials_header_value, expected_type=type_hints["routing_http_response_access_control_allow_credentials_header_value"])
            check_type(argname="argument routing_http_response_access_control_allow_headers_header_value", value=routing_http_response_access_control_allow_headers_header_value, expected_type=type_hints["routing_http_response_access_control_allow_headers_header_value"])
            check_type(argname="argument routing_http_response_access_control_allow_methods_header_value", value=routing_http_response_access_control_allow_methods_header_value, expected_type=type_hints["routing_http_response_access_control_allow_methods_header_value"])
            check_type(argname="argument routing_http_response_access_control_allow_origin_header_value", value=routing_http_response_access_control_allow_origin_header_value, expected_type=type_hints["routing_http_response_access_control_allow_origin_header_value"])
            check_type(argname="argument routing_http_response_access_control_expose_headers_header_value", value=routing_http_response_access_control_expose_headers_header_value, expected_type=type_hints["routing_http_response_access_control_expose_headers_header_value"])
            check_type(argname="argument routing_http_response_access_control_max_age_header_value", value=routing_http_response_access_control_max_age_header_value, expected_type=type_hints["routing_http_response_access_control_max_age_header_value"])
            check_type(argname="argument routing_http_response_content_security_policy_header_value", value=routing_http_response_content_security_policy_header_value, expected_type=type_hints["routing_http_response_content_security_policy_header_value"])
            check_type(argname="argument routing_http_response_server_enabled", value=routing_http_response_server_enabled, expected_type=type_hints["routing_http_response_server_enabled"])
            check_type(argname="argument routing_http_response_strict_transport_security_header_value", value=routing_http_response_strict_transport_security_header_value, expected_type=type_hints["routing_http_response_strict_transport_security_header_value"])
            check_type(argname="argument routing_http_response_x_content_type_options_header_value", value=routing_http_response_x_content_type_options_header_value, expected_type=type_hints["routing_http_response_x_content_type_options_header_value"])
            check_type(argname="argument routing_http_response_x_frame_options_header_value", value=routing_http_response_x_frame_options_header_value, expected_type=type_hints["routing_http_response_x_frame_options_header_value"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tcp_idle_timeout_seconds", value=tcp_idle_timeout_seconds, expected_type=type_hints["tcp_idle_timeout_seconds"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_action": default_action,
            "load_balancer_arn": load_balancer_arn,
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
        if alpn_policy is not None:
            self._values["alpn_policy"] = alpn_policy
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if id is not None:
            self._values["id"] = id
        if mutual_authentication is not None:
            self._values["mutual_authentication"] = mutual_authentication
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if region is not None:
            self._values["region"] = region
        if routing_http_request_x_amzn_mtls_clientcert_header_name is not None:
            self._values["routing_http_request_x_amzn_mtls_clientcert_header_name"] = routing_http_request_x_amzn_mtls_clientcert_header_name
        if routing_http_request_x_amzn_mtls_clientcert_issuer_header_name is not None:
            self._values["routing_http_request_x_amzn_mtls_clientcert_issuer_header_name"] = routing_http_request_x_amzn_mtls_clientcert_issuer_header_name
        if routing_http_request_x_amzn_mtls_clientcert_leaf_header_name is not None:
            self._values["routing_http_request_x_amzn_mtls_clientcert_leaf_header_name"] = routing_http_request_x_amzn_mtls_clientcert_leaf_header_name
        if routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name is not None:
            self._values["routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name"] = routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name
        if routing_http_request_x_amzn_mtls_clientcert_subject_header_name is not None:
            self._values["routing_http_request_x_amzn_mtls_clientcert_subject_header_name"] = routing_http_request_x_amzn_mtls_clientcert_subject_header_name
        if routing_http_request_x_amzn_mtls_clientcert_validity_header_name is not None:
            self._values["routing_http_request_x_amzn_mtls_clientcert_validity_header_name"] = routing_http_request_x_amzn_mtls_clientcert_validity_header_name
        if routing_http_request_x_amzn_tls_cipher_suite_header_name is not None:
            self._values["routing_http_request_x_amzn_tls_cipher_suite_header_name"] = routing_http_request_x_amzn_tls_cipher_suite_header_name
        if routing_http_request_x_amzn_tls_version_header_name is not None:
            self._values["routing_http_request_x_amzn_tls_version_header_name"] = routing_http_request_x_amzn_tls_version_header_name
        if routing_http_response_access_control_allow_credentials_header_value is not None:
            self._values["routing_http_response_access_control_allow_credentials_header_value"] = routing_http_response_access_control_allow_credentials_header_value
        if routing_http_response_access_control_allow_headers_header_value is not None:
            self._values["routing_http_response_access_control_allow_headers_header_value"] = routing_http_response_access_control_allow_headers_header_value
        if routing_http_response_access_control_allow_methods_header_value is not None:
            self._values["routing_http_response_access_control_allow_methods_header_value"] = routing_http_response_access_control_allow_methods_header_value
        if routing_http_response_access_control_allow_origin_header_value is not None:
            self._values["routing_http_response_access_control_allow_origin_header_value"] = routing_http_response_access_control_allow_origin_header_value
        if routing_http_response_access_control_expose_headers_header_value is not None:
            self._values["routing_http_response_access_control_expose_headers_header_value"] = routing_http_response_access_control_expose_headers_header_value
        if routing_http_response_access_control_max_age_header_value is not None:
            self._values["routing_http_response_access_control_max_age_header_value"] = routing_http_response_access_control_max_age_header_value
        if routing_http_response_content_security_policy_header_value is not None:
            self._values["routing_http_response_content_security_policy_header_value"] = routing_http_response_content_security_policy_header_value
        if routing_http_response_server_enabled is not None:
            self._values["routing_http_response_server_enabled"] = routing_http_response_server_enabled
        if routing_http_response_strict_transport_security_header_value is not None:
            self._values["routing_http_response_strict_transport_security_header_value"] = routing_http_response_strict_transport_security_header_value
        if routing_http_response_x_content_type_options_header_value is not None:
            self._values["routing_http_response_x_content_type_options_header_value"] = routing_http_response_x_content_type_options_header_value
        if routing_http_response_x_frame_options_header_value is not None:
            self._values["routing_http_response_x_frame_options_header_value"] = routing_http_response_x_frame_options_header_value
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tcp_idle_timeout_seconds is not None:
            self._values["tcp_idle_timeout_seconds"] = tcp_idle_timeout_seconds
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def default_action(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlbListenerDefaultAction"]]:
        '''default_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#default_action AlbListener#default_action}
        '''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlbListenerDefaultAction"]], result)

    @builtins.property
    def load_balancer_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#load_balancer_arn AlbListener#load_balancer_arn}.'''
        result = self._values.get("load_balancer_arn")
        assert result is not None, "Required property 'load_balancer_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alpn_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#alpn_policy AlbListener#alpn_policy}.'''
        result = self._values.get("alpn_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#certificate_arn AlbListener#certificate_arn}.'''
        result = self._values.get("certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#id AlbListener#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mutual_authentication(
        self,
    ) -> typing.Optional["AlbListenerMutualAuthentication"]:
        '''mutual_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#mutual_authentication AlbListener#mutual_authentication}
        '''
        result = self._values.get("mutual_authentication")
        return typing.cast(typing.Optional["AlbListenerMutualAuthentication"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#port AlbListener#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#protocol AlbListener#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#region AlbListener#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_request_x_amzn_mtls_clientcert_header_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_header_name}.'''
        result = self._values.get("routing_http_request_x_amzn_mtls_clientcert_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_request_x_amzn_mtls_clientcert_issuer_header_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_issuer_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_issuer_header_name}.'''
        result = self._values.get("routing_http_request_x_amzn_mtls_clientcert_issuer_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_request_x_amzn_mtls_clientcert_leaf_header_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_leaf_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_leaf_header_name}.'''
        result = self._values.get("routing_http_request_x_amzn_mtls_clientcert_leaf_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name}.'''
        result = self._values.get("routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_request_x_amzn_mtls_clientcert_subject_header_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_subject_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_subject_header_name}.'''
        result = self._values.get("routing_http_request_x_amzn_mtls_clientcert_subject_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_request_x_amzn_mtls_clientcert_validity_header_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_mtls_clientcert_validity_header_name AlbListener#routing_http_request_x_amzn_mtls_clientcert_validity_header_name}.'''
        result = self._values.get("routing_http_request_x_amzn_mtls_clientcert_validity_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_request_x_amzn_tls_cipher_suite_header_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_tls_cipher_suite_header_name AlbListener#routing_http_request_x_amzn_tls_cipher_suite_header_name}.'''
        result = self._values.get("routing_http_request_x_amzn_tls_cipher_suite_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_request_x_amzn_tls_version_header_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_request_x_amzn_tls_version_header_name AlbListener#routing_http_request_x_amzn_tls_version_header_name}.'''
        result = self._values.get("routing_http_request_x_amzn_tls_version_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_response_access_control_allow_credentials_header_value(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_credentials_header_value AlbListener#routing_http_response_access_control_allow_credentials_header_value}.'''
        result = self._values.get("routing_http_response_access_control_allow_credentials_header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_response_access_control_allow_headers_header_value(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_headers_header_value AlbListener#routing_http_response_access_control_allow_headers_header_value}.'''
        result = self._values.get("routing_http_response_access_control_allow_headers_header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_response_access_control_allow_methods_header_value(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_methods_header_value AlbListener#routing_http_response_access_control_allow_methods_header_value}.'''
        result = self._values.get("routing_http_response_access_control_allow_methods_header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_response_access_control_allow_origin_header_value(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_allow_origin_header_value AlbListener#routing_http_response_access_control_allow_origin_header_value}.'''
        result = self._values.get("routing_http_response_access_control_allow_origin_header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_response_access_control_expose_headers_header_value(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_expose_headers_header_value AlbListener#routing_http_response_access_control_expose_headers_header_value}.'''
        result = self._values.get("routing_http_response_access_control_expose_headers_header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_response_access_control_max_age_header_value(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_access_control_max_age_header_value AlbListener#routing_http_response_access_control_max_age_header_value}.'''
        result = self._values.get("routing_http_response_access_control_max_age_header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_response_content_security_policy_header_value(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_content_security_policy_header_value AlbListener#routing_http_response_content_security_policy_header_value}.'''
        result = self._values.get("routing_http_response_content_security_policy_header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_response_server_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_server_enabled AlbListener#routing_http_response_server_enabled}.'''
        result = self._values.get("routing_http_response_server_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def routing_http_response_strict_transport_security_header_value(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_strict_transport_security_header_value AlbListener#routing_http_response_strict_transport_security_header_value}.'''
        result = self._values.get("routing_http_response_strict_transport_security_header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_response_x_content_type_options_header_value(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_x_content_type_options_header_value AlbListener#routing_http_response_x_content_type_options_header_value}.'''
        result = self._values.get("routing_http_response_x_content_type_options_header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_http_response_x_frame_options_header_value(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#routing_http_response_x_frame_options_header_value AlbListener#routing_http_response_x_frame_options_header_value}.'''
        result = self._values.get("routing_http_response_x_frame_options_header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#ssl_policy AlbListener#ssl_policy}.'''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#tags AlbListener#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#tags_all AlbListener#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tcp_idle_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#tcp_idle_timeout_seconds AlbListener#tcp_idle_timeout_seconds}.'''
        result = self._values.get("tcp_idle_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AlbListenerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#timeouts AlbListener#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AlbListenerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultAction",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "authenticate_cognito": "authenticateCognito",
        "authenticate_oidc": "authenticateOidc",
        "fixed_response": "fixedResponse",
        "forward": "forward",
        "jwt_validation": "jwtValidation",
        "order": "order",
        "redirect": "redirect",
        "target_group_arn": "targetGroupArn",
    },
)
class AlbListenerDefaultAction:
    def __init__(
        self,
        *,
        type: builtins.str,
        authenticate_cognito: typing.Optional[typing.Union["AlbListenerDefaultActionAuthenticateCognito", typing.Dict[builtins.str, typing.Any]]] = None,
        authenticate_oidc: typing.Optional[typing.Union["AlbListenerDefaultActionAuthenticateOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        fixed_response: typing.Optional[typing.Union["AlbListenerDefaultActionFixedResponse", typing.Dict[builtins.str, typing.Any]]] = None,
        forward: typing.Optional[typing.Union["AlbListenerDefaultActionForward", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt_validation: typing.Optional[typing.Union["AlbListenerDefaultActionJwtValidation", typing.Dict[builtins.str, typing.Any]]] = None,
        order: typing.Optional[jsii.Number] = None,
        redirect: typing.Optional[typing.Union["AlbListenerDefaultActionRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        target_group_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#type AlbListener#type}.
        :param authenticate_cognito: authenticate_cognito block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authenticate_cognito AlbListener#authenticate_cognito}
        :param authenticate_oidc: authenticate_oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authenticate_oidc AlbListener#authenticate_oidc}
        :param fixed_response: fixed_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#fixed_response AlbListener#fixed_response}
        :param forward: forward block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#forward AlbListener#forward}
        :param jwt_validation: jwt_validation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#jwt_validation AlbListener#jwt_validation}
        :param order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#order AlbListener#order}.
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#redirect AlbListener#redirect}
        :param target_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#target_group_arn AlbListener#target_group_arn}.
        '''
        if isinstance(authenticate_cognito, dict):
            authenticate_cognito = AlbListenerDefaultActionAuthenticateCognito(**authenticate_cognito)
        if isinstance(authenticate_oidc, dict):
            authenticate_oidc = AlbListenerDefaultActionAuthenticateOidc(**authenticate_oidc)
        if isinstance(fixed_response, dict):
            fixed_response = AlbListenerDefaultActionFixedResponse(**fixed_response)
        if isinstance(forward, dict):
            forward = AlbListenerDefaultActionForward(**forward)
        if isinstance(jwt_validation, dict):
            jwt_validation = AlbListenerDefaultActionJwtValidation(**jwt_validation)
        if isinstance(redirect, dict):
            redirect = AlbListenerDefaultActionRedirect(**redirect)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3be68f3b02da0681220da0469bd55a53cae1f106330a9eaecd15f0ae00da47)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument authenticate_cognito", value=authenticate_cognito, expected_type=type_hints["authenticate_cognito"])
            check_type(argname="argument authenticate_oidc", value=authenticate_oidc, expected_type=type_hints["authenticate_oidc"])
            check_type(argname="argument fixed_response", value=fixed_response, expected_type=type_hints["fixed_response"])
            check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
            check_type(argname="argument jwt_validation", value=jwt_validation, expected_type=type_hints["jwt_validation"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument redirect", value=redirect, expected_type=type_hints["redirect"])
            check_type(argname="argument target_group_arn", value=target_group_arn, expected_type=type_hints["target_group_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if authenticate_cognito is not None:
            self._values["authenticate_cognito"] = authenticate_cognito
        if authenticate_oidc is not None:
            self._values["authenticate_oidc"] = authenticate_oidc
        if fixed_response is not None:
            self._values["fixed_response"] = fixed_response
        if forward is not None:
            self._values["forward"] = forward
        if jwt_validation is not None:
            self._values["jwt_validation"] = jwt_validation
        if order is not None:
            self._values["order"] = order
        if redirect is not None:
            self._values["redirect"] = redirect
        if target_group_arn is not None:
            self._values["target_group_arn"] = target_group_arn

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#type AlbListener#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authenticate_cognito(
        self,
    ) -> typing.Optional["AlbListenerDefaultActionAuthenticateCognito"]:
        '''authenticate_cognito block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authenticate_cognito AlbListener#authenticate_cognito}
        '''
        result = self._values.get("authenticate_cognito")
        return typing.cast(typing.Optional["AlbListenerDefaultActionAuthenticateCognito"], result)

    @builtins.property
    def authenticate_oidc(
        self,
    ) -> typing.Optional["AlbListenerDefaultActionAuthenticateOidc"]:
        '''authenticate_oidc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authenticate_oidc AlbListener#authenticate_oidc}
        '''
        result = self._values.get("authenticate_oidc")
        return typing.cast(typing.Optional["AlbListenerDefaultActionAuthenticateOidc"], result)

    @builtins.property
    def fixed_response(
        self,
    ) -> typing.Optional["AlbListenerDefaultActionFixedResponse"]:
        '''fixed_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#fixed_response AlbListener#fixed_response}
        '''
        result = self._values.get("fixed_response")
        return typing.cast(typing.Optional["AlbListenerDefaultActionFixedResponse"], result)

    @builtins.property
    def forward(self) -> typing.Optional["AlbListenerDefaultActionForward"]:
        '''forward block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#forward AlbListener#forward}
        '''
        result = self._values.get("forward")
        return typing.cast(typing.Optional["AlbListenerDefaultActionForward"], result)

    @builtins.property
    def jwt_validation(
        self,
    ) -> typing.Optional["AlbListenerDefaultActionJwtValidation"]:
        '''jwt_validation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#jwt_validation AlbListener#jwt_validation}
        '''
        result = self._values.get("jwt_validation")
        return typing.cast(typing.Optional["AlbListenerDefaultActionJwtValidation"], result)

    @builtins.property
    def order(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#order AlbListener#order}.'''
        result = self._values.get("order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redirect(self) -> typing.Optional["AlbListenerDefaultActionRedirect"]:
        '''redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#redirect AlbListener#redirect}
        '''
        result = self._values.get("redirect")
        return typing.cast(typing.Optional["AlbListenerDefaultActionRedirect"], result)

    @builtins.property
    def target_group_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#target_group_arn AlbListener#target_group_arn}.'''
        result = self._values.get("target_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerDefaultAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionAuthenticateCognito",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool_arn": "userPoolArn",
        "user_pool_client_id": "userPoolClientId",
        "user_pool_domain": "userPoolDomain",
        "authentication_request_extra_params": "authenticationRequestExtraParams",
        "on_unauthenticated_request": "onUnauthenticatedRequest",
        "scope": "scope",
        "session_cookie_name": "sessionCookieName",
        "session_timeout": "sessionTimeout",
    },
)
class AlbListenerDefaultActionAuthenticateCognito:
    def __init__(
        self,
        *,
        user_pool_arn: builtins.str,
        user_pool_client_id: builtins.str,
        user_pool_domain: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param user_pool_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_pool_arn AlbListener#user_pool_arn}.
        :param user_pool_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_pool_client_id AlbListener#user_pool_client_id}.
        :param user_pool_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_pool_domain AlbListener#user_pool_domain}.
        :param authentication_request_extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authentication_request_extra_params AlbListener#authentication_request_extra_params}.
        :param on_unauthenticated_request: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#on_unauthenticated_request AlbListener#on_unauthenticated_request}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#scope AlbListener#scope}.
        :param session_cookie_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_cookie_name AlbListener#session_cookie_name}.
        :param session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_timeout AlbListener#session_timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01de940330e4e96da05d3e94456e2d3214f4c63dc96c6d02abc0ec6a09b23c48)
            check_type(argname="argument user_pool_arn", value=user_pool_arn, expected_type=type_hints["user_pool_arn"])
            check_type(argname="argument user_pool_client_id", value=user_pool_client_id, expected_type=type_hints["user_pool_client_id"])
            check_type(argname="argument user_pool_domain", value=user_pool_domain, expected_type=type_hints["user_pool_domain"])
            check_type(argname="argument authentication_request_extra_params", value=authentication_request_extra_params, expected_type=type_hints["authentication_request_extra_params"])
            check_type(argname="argument on_unauthenticated_request", value=on_unauthenticated_request, expected_type=type_hints["on_unauthenticated_request"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument session_cookie_name", value=session_cookie_name, expected_type=type_hints["session_cookie_name"])
            check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_pool_arn": user_pool_arn,
            "user_pool_client_id": user_pool_client_id,
            "user_pool_domain": user_pool_domain,
        }
        if authentication_request_extra_params is not None:
            self._values["authentication_request_extra_params"] = authentication_request_extra_params
        if on_unauthenticated_request is not None:
            self._values["on_unauthenticated_request"] = on_unauthenticated_request
        if scope is not None:
            self._values["scope"] = scope
        if session_cookie_name is not None:
            self._values["session_cookie_name"] = session_cookie_name
        if session_timeout is not None:
            self._values["session_timeout"] = session_timeout

    @builtins.property
    def user_pool_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_pool_arn AlbListener#user_pool_arn}.'''
        result = self._values.get("user_pool_arn")
        assert result is not None, "Required property 'user_pool_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pool_client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_pool_client_id AlbListener#user_pool_client_id}.'''
        result = self._values.get("user_pool_client_id")
        assert result is not None, "Required property 'user_pool_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pool_domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_pool_domain AlbListener#user_pool_domain}.'''
        result = self._values.get("user_pool_domain")
        assert result is not None, "Required property 'user_pool_domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_request_extra_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authentication_request_extra_params AlbListener#authentication_request_extra_params}.'''
        result = self._values.get("authentication_request_extra_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#on_unauthenticated_request AlbListener#on_unauthenticated_request}.'''
        result = self._values.get("on_unauthenticated_request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#scope AlbListener#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_cookie_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_cookie_name AlbListener#session_cookie_name}.'''
        result = self._values.get("session_cookie_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_timeout AlbListener#session_timeout}.'''
        result = self._values.get("session_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerDefaultActionAuthenticateCognito(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbListenerDefaultActionAuthenticateCognitoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionAuthenticateCognitoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__144cc7bf750af4e32e717e3693d995c96755fd297cba3500e2a80ece91d04cca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthenticationRequestExtraParams")
    def reset_authentication_request_extra_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationRequestExtraParams", []))

    @jsii.member(jsii_name="resetOnUnauthenticatedRequest")
    def reset_on_unauthenticated_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnUnauthenticatedRequest", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetSessionCookieName")
    def reset_session_cookie_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionCookieName", []))

    @jsii.member(jsii_name="resetSessionTimeout")
    def reset_session_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationRequestExtraParamsInput")
    def authentication_request_extra_params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "authenticationRequestExtraParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="onUnauthenticatedRequestInput")
    def on_unauthenticated_request_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onUnauthenticatedRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionCookieNameInput")
    def session_cookie_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionCookieNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTimeoutInput")
    def session_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolArnInput")
    def user_pool_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolArnInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolClientIdInput")
    def user_pool_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolDomainInput")
    def user_pool_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationRequestExtraParams")
    def authentication_request_extra_params(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "authenticationRequestExtraParams"))

    @authentication_request_extra_params.setter
    def authentication_request_extra_params(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca45797cc39b8f1fd7f99eb8971ba6b846f478487b168d8d4fc9cfdc210f118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationRequestExtraParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onUnauthenticatedRequest")
    def on_unauthenticated_request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onUnauthenticatedRequest"))

    @on_unauthenticated_request.setter
    def on_unauthenticated_request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf9121298f02702344cf0c98d8dbc9c4b30eecdfe52690e825857152595a1a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onUnauthenticatedRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2316fb282afb339731909e82935ff528c809553cebecca77caf8e765cb07d4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionCookieName")
    def session_cookie_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionCookieName"))

    @session_cookie_name.setter
    def session_cookie_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692a618d4f1c451f70afae27d498333483defe8afbd7da2e58a4eadd05597bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionCookieName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTimeout")
    def session_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionTimeout"))

    @session_timeout.setter
    def session_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8c2a9261331f469d7c8ce6c5399988a232c6f0e535723712bb81690fd9acf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolArn"))

    @user_pool_arn.setter
    def user_pool_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317e15027431efea77caf2ca66d69e34b28a2461359cc2bbc346554a5c4f0dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPoolClientId")
    def user_pool_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolClientId"))

    @user_pool_client_id.setter
    def user_pool_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b7af17dfaa6f883a303ac921dfff58da2e8f75d6d6e6a51c36867849a7b360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPoolDomain")
    def user_pool_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolDomain"))

    @user_pool_domain.setter
    def user_pool_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b482b9b82e6fedc12f73deba9354440d5dcbc5d30b0bb01b114163f32bc923c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlbListenerDefaultActionAuthenticateCognito]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionAuthenticateCognito], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlbListenerDefaultActionAuthenticateCognito],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90b49979d2e18940d4d4ecd8edcf1de705530d99bd6acbe949b9ad294a30f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionAuthenticateOidc",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_endpoint": "authorizationEndpoint",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "issuer": "issuer",
        "token_endpoint": "tokenEndpoint",
        "user_info_endpoint": "userInfoEndpoint",
        "authentication_request_extra_params": "authenticationRequestExtraParams",
        "on_unauthenticated_request": "onUnauthenticatedRequest",
        "scope": "scope",
        "session_cookie_name": "sessionCookieName",
        "session_timeout": "sessionTimeout",
    },
)
class AlbListenerDefaultActionAuthenticateOidc:
    def __init__(
        self,
        *,
        authorization_endpoint: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        issuer: builtins.str,
        token_endpoint: builtins.str,
        user_info_endpoint: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param authorization_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authorization_endpoint AlbListener#authorization_endpoint}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#client_id AlbListener#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#client_secret AlbListener#client_secret}.
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#issuer AlbListener#issuer}.
        :param token_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#token_endpoint AlbListener#token_endpoint}.
        :param user_info_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_info_endpoint AlbListener#user_info_endpoint}.
        :param authentication_request_extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authentication_request_extra_params AlbListener#authentication_request_extra_params}.
        :param on_unauthenticated_request: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#on_unauthenticated_request AlbListener#on_unauthenticated_request}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#scope AlbListener#scope}.
        :param session_cookie_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_cookie_name AlbListener#session_cookie_name}.
        :param session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_timeout AlbListener#session_timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ac5db8dc570ec887b92e997b21dda4c168c7125d0f94c15c69715d15aac880)
            check_type(argname="argument authorization_endpoint", value=authorization_endpoint, expected_type=type_hints["authorization_endpoint"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument token_endpoint", value=token_endpoint, expected_type=type_hints["token_endpoint"])
            check_type(argname="argument user_info_endpoint", value=user_info_endpoint, expected_type=type_hints["user_info_endpoint"])
            check_type(argname="argument authentication_request_extra_params", value=authentication_request_extra_params, expected_type=type_hints["authentication_request_extra_params"])
            check_type(argname="argument on_unauthenticated_request", value=on_unauthenticated_request, expected_type=type_hints["on_unauthenticated_request"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument session_cookie_name", value=session_cookie_name, expected_type=type_hints["session_cookie_name"])
            check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization_endpoint": authorization_endpoint,
            "client_id": client_id,
            "client_secret": client_secret,
            "issuer": issuer,
            "token_endpoint": token_endpoint,
            "user_info_endpoint": user_info_endpoint,
        }
        if authentication_request_extra_params is not None:
            self._values["authentication_request_extra_params"] = authentication_request_extra_params
        if on_unauthenticated_request is not None:
            self._values["on_unauthenticated_request"] = on_unauthenticated_request
        if scope is not None:
            self._values["scope"] = scope
        if session_cookie_name is not None:
            self._values["session_cookie_name"] = session_cookie_name
        if session_timeout is not None:
            self._values["session_timeout"] = session_timeout

    @builtins.property
    def authorization_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authorization_endpoint AlbListener#authorization_endpoint}.'''
        result = self._values.get("authorization_endpoint")
        assert result is not None, "Required property 'authorization_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#client_id AlbListener#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#client_secret AlbListener#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#issuer AlbListener#issuer}.'''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#token_endpoint AlbListener#token_endpoint}.'''
        result = self._values.get("token_endpoint")
        assert result is not None, "Required property 'token_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_info_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_info_endpoint AlbListener#user_info_endpoint}.'''
        result = self._values.get("user_info_endpoint")
        assert result is not None, "Required property 'user_info_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_request_extra_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authentication_request_extra_params AlbListener#authentication_request_extra_params}.'''
        result = self._values.get("authentication_request_extra_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#on_unauthenticated_request AlbListener#on_unauthenticated_request}.'''
        result = self._values.get("on_unauthenticated_request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#scope AlbListener#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_cookie_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_cookie_name AlbListener#session_cookie_name}.'''
        result = self._values.get("session_cookie_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_timeout AlbListener#session_timeout}.'''
        result = self._values.get("session_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerDefaultActionAuthenticateOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbListenerDefaultActionAuthenticateOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionAuthenticateOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e3c4441c31a54e2be0b4bc13dca97f561439bdb369c37f2f7b160de09b2f3e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthenticationRequestExtraParams")
    def reset_authentication_request_extra_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationRequestExtraParams", []))

    @jsii.member(jsii_name="resetOnUnauthenticatedRequest")
    def reset_on_unauthenticated_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnUnauthenticatedRequest", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetSessionCookieName")
    def reset_session_cookie_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionCookieName", []))

    @jsii.member(jsii_name="resetSessionTimeout")
    def reset_session_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationRequestExtraParamsInput")
    def authentication_request_extra_params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "authenticationRequestExtraParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationEndpointInput")
    def authorization_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="onUnauthenticatedRequestInput")
    def on_unauthenticated_request_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onUnauthenticatedRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionCookieNameInput")
    def session_cookie_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionCookieNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTimeoutInput")
    def session_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenEndpointInput")
    def token_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="userInfoEndpointInput")
    def user_info_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInfoEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationRequestExtraParams")
    def authentication_request_extra_params(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "authenticationRequestExtraParams"))

    @authentication_request_extra_params.setter
    def authentication_request_extra_params(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631bc65123708276b37806c3ffb0dbc6ab615a56143f3058e80881f5a34ff865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationRequestExtraParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizationEndpoint")
    def authorization_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationEndpoint"))

    @authorization_endpoint.setter
    def authorization_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c6e40c725139f31a04104f1499df55f26160ac10a696b9c832812187b6da81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c954537d5a259f3aa7510f3ea866f4716a8aac92d5ebaed786bfc01254d196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5da43e05fa854a82a8fa86454b7c01cc27b21f79d0045a38ff49a9fa58d7fbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2d25d0d05ae9a260e165c8d17bb1d5c5b57540bab778afe8ba26b0e534ec85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onUnauthenticatedRequest")
    def on_unauthenticated_request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onUnauthenticatedRequest"))

    @on_unauthenticated_request.setter
    def on_unauthenticated_request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20cdbf73189aa8581bdfd843e350ac8d44c82d6d1cf4fe8121b9b65c98405ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onUnauthenticatedRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c188be181a107fba6beba2d25c54121c13d772aa99fa1223d7eb76f034019e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionCookieName")
    def session_cookie_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionCookieName"))

    @session_cookie_name.setter
    def session_cookie_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80694dd020dc0d32d8b7c0bd486b5b54cc6df55fe89ee27cd657ae75197ddef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionCookieName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTimeout")
    def session_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionTimeout"))

    @session_timeout.setter
    def session_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d482b33fda5ce515b33f429d5d765ce25854f58903ee6023db0aa511801f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89e46e22806438f53e0f9159d8a0bc82ad549f13fa758b89743a8f2f55b0332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userInfoEndpoint")
    def user_info_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userInfoEndpoint"))

    @user_info_endpoint.setter
    def user_info_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c52b461fb67e02c23ee7a59b5eb3045d68d45b6498e308faf8d24773eebdf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userInfoEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlbListenerDefaultActionAuthenticateOidc]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionAuthenticateOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlbListenerDefaultActionAuthenticateOidc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64082fe619b9e2e66ccca5c66380e0c5b415f2c324cd47592d9d7224fce6486c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionFixedResponse",
    jsii_struct_bases=[],
    name_mapping={
        "content_type": "contentType",
        "message_body": "messageBody",
        "status_code": "statusCode",
    },
)
class AlbListenerDefaultActionFixedResponse:
    def __init__(
        self,
        *,
        content_type: builtins.str,
        message_body: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#content_type AlbListener#content_type}.
        :param message_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#message_body AlbListener#message_body}.
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#status_code AlbListener#status_code}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693feceda86ff4d2380953941d2260393766802d0e99063060b173e34a4aa110)
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument message_body", value=message_body, expected_type=type_hints["message_body"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_type": content_type,
        }
        if message_body is not None:
            self._values["message_body"] = message_body
        if status_code is not None:
            self._values["status_code"] = status_code

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#content_type AlbListener#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_body(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#message_body AlbListener#message_body}.'''
        result = self._values.get("message_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#status_code AlbListener#status_code}.'''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerDefaultActionFixedResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbListenerDefaultActionFixedResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionFixedResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cae3373a777886359ba6cfd8677134073820c2918510bd4a432cdd589a9ec717)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessageBody")
    def reset_message_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageBody", []))

    @jsii.member(jsii_name="resetStatusCode")
    def reset_status_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusCode", []))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="messageBodyInput")
    def message_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e0cce6977c656ba1d8ae9c4776b2da391829570c4605ac55401ea311edc2a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageBody")
    def message_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageBody"))

    @message_body.setter
    def message_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc06dc57c3d9beefe36560e2482c425ae24d1da2f4687972bfb408d7546e575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102e2376ac44dd77906e680d9af5f8f4aa1184e952d26a007f7cd6d8bc855d30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlbListenerDefaultActionFixedResponse]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionFixedResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlbListenerDefaultActionFixedResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887924f9f51f0438f35ef58527305f7a509dd882ee834faed04ecdef71805cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionForward",
    jsii_struct_bases=[],
    name_mapping={"target_group": "targetGroup", "stickiness": "stickiness"},
)
class AlbListenerDefaultActionForward:
    def __init__(
        self,
        *,
        target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlbListenerDefaultActionForwardTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
        stickiness: typing.Optional[typing.Union["AlbListenerDefaultActionForwardStickiness", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target_group: target_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#target_group AlbListener#target_group}
        :param stickiness: stickiness block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#stickiness AlbListener#stickiness}
        '''
        if isinstance(stickiness, dict):
            stickiness = AlbListenerDefaultActionForwardStickiness(**stickiness)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad1b6d6aed9eb43d8adabb491af7046d9877aec29caf58cbb37be25d013c744)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
            check_type(argname="argument stickiness", value=stickiness, expected_type=type_hints["stickiness"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_group": target_group,
        }
        if stickiness is not None:
            self._values["stickiness"] = stickiness

    @builtins.property
    def target_group(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlbListenerDefaultActionForwardTargetGroup"]]:
        '''target_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#target_group AlbListener#target_group}
        '''
        result = self._values.get("target_group")
        assert result is not None, "Required property 'target_group' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlbListenerDefaultActionForwardTargetGroup"]], result)

    @builtins.property
    def stickiness(
        self,
    ) -> typing.Optional["AlbListenerDefaultActionForwardStickiness"]:
        '''stickiness block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#stickiness AlbListener#stickiness}
        '''
        result = self._values.get("stickiness")
        return typing.cast(typing.Optional["AlbListenerDefaultActionForwardStickiness"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerDefaultActionForward(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbListenerDefaultActionForwardOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionForwardOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d274a175c35b1db523d0f6b2e359ea06b5cfe5278e5e3e43a13e415c80624863)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStickiness")
    def put_stickiness(
        self,
        *,
        duration: jsii.Number,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#duration AlbListener#duration}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#enabled AlbListener#enabled}.
        '''
        value = AlbListenerDefaultActionForwardStickiness(
            duration=duration, enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putStickiness", [value]))

    @jsii.member(jsii_name="putTargetGroup")
    def put_target_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlbListenerDefaultActionForwardTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b5aa6022e49a27a0d0aece716d90314a4bbb436ff1eb796463c9b2fb5b70fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetGroup", [value]))

    @jsii.member(jsii_name="resetStickiness")
    def reset_stickiness(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStickiness", []))

    @builtins.property
    @jsii.member(jsii_name="stickiness")
    def stickiness(self) -> "AlbListenerDefaultActionForwardStickinessOutputReference":
        return typing.cast("AlbListenerDefaultActionForwardStickinessOutputReference", jsii.get(self, "stickiness"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> "AlbListenerDefaultActionForwardTargetGroupList":
        return typing.cast("AlbListenerDefaultActionForwardTargetGroupList", jsii.get(self, "targetGroup"))

    @builtins.property
    @jsii.member(jsii_name="stickinessInput")
    def stickiness_input(
        self,
    ) -> typing.Optional["AlbListenerDefaultActionForwardStickiness"]:
        return typing.cast(typing.Optional["AlbListenerDefaultActionForwardStickiness"], jsii.get(self, "stickinessInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupInput")
    def target_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlbListenerDefaultActionForwardTargetGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlbListenerDefaultActionForwardTargetGroup"]]], jsii.get(self, "targetGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlbListenerDefaultActionForward]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionForward], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlbListenerDefaultActionForward],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f110aa509ee3d5d4f97a06d492c07d6df7d44bfd2d241f1bd1cc424bcc53e5e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionForwardStickiness",
    jsii_struct_bases=[],
    name_mapping={"duration": "duration", "enabled": "enabled"},
)
class AlbListenerDefaultActionForwardStickiness:
    def __init__(
        self,
        *,
        duration: jsii.Number,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#duration AlbListener#duration}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#enabled AlbListener#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94d0310fc419ffe52e3ac55d176f208da22467c52bf4334ec3fda4d33045245)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration": duration,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def duration(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#duration AlbListener#duration}.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#enabled AlbListener#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerDefaultActionForwardStickiness(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbListenerDefaultActionForwardStickinessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionForwardStickinessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__024927e96368630f64fdd7905faf02adfc0f1dda5c4aba2b0cb0effe864c39b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4816414f331d18bc33c1aeb955e0c77ac39a4844e28d2b3c709fade9c4e4a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__4b8a8882627893977baa4ec2e78440e08ec3e587402999148a3469130768e949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlbListenerDefaultActionForwardStickiness]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionForwardStickiness], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlbListenerDefaultActionForwardStickiness],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f08d417a66366a1509e2b51893c80808f09851ae4505ed9f9553d6b334fa72e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionForwardTargetGroup",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "weight": "weight"},
)
class AlbListenerDefaultActionForwardTargetGroup:
    def __init__(
        self,
        *,
        arn: builtins.str,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#arn AlbListener#arn}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#weight AlbListener#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e33a5cc4f0d163ccb9e981468df6bde0a4bf1e79eccf9de34759c3b66c86e7)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
        }
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#arn AlbListener#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#weight AlbListener#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerDefaultActionForwardTargetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbListenerDefaultActionForwardTargetGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionForwardTargetGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__682e553a4fb21f4850f36ac4ef89f0c1f80ab4672a13730021c983bbb61986c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AlbListenerDefaultActionForwardTargetGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d7e93beb4d274b1c14011008d804062a269d8f302c31cba16322337848b63f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlbListenerDefaultActionForwardTargetGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a27aa408144d446be3efb16400e8a64da0ceda65fe45f00c680257c1d42b28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73c1e6353e9768bd2b68bc602b11f7b36d80d5864e3e75e007ba5f8c9d4ff531)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78e153199ab3712a8c995a4b37942ed376db0be4ef6973dc70b5713845bddd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultActionForwardTargetGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultActionForwardTargetGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultActionForwardTargetGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6604b1f35c7baf44106fba01a5da8760cbafda56393e189f7f6d27572446abff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlbListenerDefaultActionForwardTargetGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionForwardTargetGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c98eb1729e6203187b0d86b69ed0111d6bb1e3f7ba2dfec05ec841290f957a46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f757aa0aaf9f6c03afb35f822ebb02de6c18b77acb13d4ea292ef89fbe46c0e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05249e5e71e05a49849ee8a4f2fde504b6d2a50b9c8549c064545be9ed9ed6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultActionForwardTargetGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultActionForwardTargetGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultActionForwardTargetGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aad3e962af0a49a8d714cacea087bc0b5e163b7ecf17e245c865beaae45c0c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionJwtValidation",
    jsii_struct_bases=[],
    name_mapping={
        "issuer": "issuer",
        "jwks_endpoint": "jwksEndpoint",
        "additional_claim": "additionalClaim",
    },
)
class AlbListenerDefaultActionJwtValidation:
    def __init__(
        self,
        *,
        issuer: builtins.str,
        jwks_endpoint: builtins.str,
        additional_claim: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlbListenerDefaultActionJwtValidationAdditionalClaim", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#issuer AlbListener#issuer}.
        :param jwks_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#jwks_endpoint AlbListener#jwks_endpoint}.
        :param additional_claim: additional_claim block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#additional_claim AlbListener#additional_claim}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e286ccb44839c3192cc59688e7e06509c3f72c99b4b7d4c734c8431ac0dcd69)
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument jwks_endpoint", value=jwks_endpoint, expected_type=type_hints["jwks_endpoint"])
            check_type(argname="argument additional_claim", value=additional_claim, expected_type=type_hints["additional_claim"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer": issuer,
            "jwks_endpoint": jwks_endpoint,
        }
        if additional_claim is not None:
            self._values["additional_claim"] = additional_claim

    @builtins.property
    def issuer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#issuer AlbListener#issuer}.'''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jwks_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#jwks_endpoint AlbListener#jwks_endpoint}.'''
        result = self._values.get("jwks_endpoint")
        assert result is not None, "Required property 'jwks_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_claim(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlbListenerDefaultActionJwtValidationAdditionalClaim"]]]:
        '''additional_claim block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#additional_claim AlbListener#additional_claim}
        '''
        result = self._values.get("additional_claim")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlbListenerDefaultActionJwtValidationAdditionalClaim"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerDefaultActionJwtValidation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionJwtValidationAdditionalClaim",
    jsii_struct_bases=[],
    name_mapping={"format": "format", "name": "name", "values": "values"},
)
class AlbListenerDefaultActionJwtValidationAdditionalClaim:
    def __init__(
        self,
        *,
        format: builtins.str,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#format AlbListener#format}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#name AlbListener#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#values AlbListener#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98f34570c8946cd6787813116e000500c7b6004e551c738dc69d4a14f90627a)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "format": format,
            "name": name,
            "values": values,
        }

    @builtins.property
    def format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#format AlbListener#format}.'''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#name AlbListener#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#values AlbListener#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerDefaultActionJwtValidationAdditionalClaim(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbListenerDefaultActionJwtValidationAdditionalClaimList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionJwtValidationAdditionalClaimList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a9de8ce9645a17ae69f2049bd23eb8df9eb514db5e7f18acfd930e5685435b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AlbListenerDefaultActionJwtValidationAdditionalClaimOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d7b63ce6eaffb50aea57937c228c912262a0302ebb753f0d93658ef30420a0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlbListenerDefaultActionJwtValidationAdditionalClaimOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7eb8ae1eacb7f6c111f30773203f4c3e6c247692e68dd6974f077768ed79b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__218d3940cb54758f2e2ce9938499f16b14f2378c10e5ed2ad4cbac44ae7b2fec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6e3377466331b71f9db0414932ae49f5661b066502bc9af268e9cd5e3b08c6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultActionJwtValidationAdditionalClaim]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultActionJwtValidationAdditionalClaim]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultActionJwtValidationAdditionalClaim]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52ca5f7c066a6d4c6926fa2f28b4cd88e9b55418a1da8e0ddc23d68272a6e3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlbListenerDefaultActionJwtValidationAdditionalClaimOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionJwtValidationAdditionalClaimOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c897fe6cc48153bb163e69a40ee6495142db292cd82a5dcb749afb8e5ecb0d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf01eee97d8b260e213f8438582d3a1fe92da36370cc99561b345477e43f3b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd68ad0529afbe1facf08b58d98ca393c5583ab5c3122cde683b54a905272d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9020697d19cec4b838a8dc7f4795266f37b503502cae489f28b47144a5f9b23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultActionJwtValidationAdditionalClaim]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultActionJwtValidationAdditionalClaim]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultActionJwtValidationAdditionalClaim]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1f5bcc1ee3b18510dadfda516a38d762d6a83aa15bd42a5a43adc7d18c34d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlbListenerDefaultActionJwtValidationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionJwtValidationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c05e06c233adcf12a9fc9a76d5d265cfeee06a616d2d3c8a44564d3feb7450e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalClaim")
    def put_additional_claim(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlbListenerDefaultActionJwtValidationAdditionalClaim, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7066e03922582df9e63558062cbbe70e502170c5a87a049fa8a439bc36ce26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalClaim", [value]))

    @jsii.member(jsii_name="resetAdditionalClaim")
    def reset_additional_claim(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalClaim", []))

    @builtins.property
    @jsii.member(jsii_name="additionalClaim")
    def additional_claim(
        self,
    ) -> AlbListenerDefaultActionJwtValidationAdditionalClaimList:
        return typing.cast(AlbListenerDefaultActionJwtValidationAdditionalClaimList, jsii.get(self, "additionalClaim"))

    @builtins.property
    @jsii.member(jsii_name="additionalClaimInput")
    def additional_claim_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultActionJwtValidationAdditionalClaim]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultActionJwtValidationAdditionalClaim]]], jsii.get(self, "additionalClaimInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="jwksEndpointInput")
    def jwks_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jwksEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63cb7ac677f2d3152f71fdf224a58d018ff18f253de9533efece7a1eb0783170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwksEndpoint")
    def jwks_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwksEndpoint"))

    @jwks_endpoint.setter
    def jwks_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38369fc043415a33f9eda2e4f33a5c711fcd9a3991403e9b39ad6d284228c579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwksEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlbListenerDefaultActionJwtValidation]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionJwtValidation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlbListenerDefaultActionJwtValidation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e52b36a68adc7508595261c74a81a79d04775d483d35680094783ceefe195e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlbListenerDefaultActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dbf14af7933a2272514e837730463882215f020a107423229ab84e350d284b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AlbListenerDefaultActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7822fb7f6a17480ade5a4f612e0e7541fb898ebe3ba73c2d340d46b4876f1f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlbListenerDefaultActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4f10af5c4db776e96ae7c8130b7cfb0a83a043b9280030d9e74c330a5075fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__505cafc0002e55906c557b16847f355c15bcb2f9174a83645ffe4ed9142de07f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cec7c33dc082096571b3b6c73d7e851857939b71b83a32fa08449fb1cc358e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53b9545ac8328930e7b5ed46e61f38f985fba869d85948bedf51e61aea99a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlbListenerDefaultActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c07182ec5ace9be52648a5f8115c254d8ab815c2223edefa4a51a53bc3f3d52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthenticateCognito")
    def put_authenticate_cognito(
        self,
        *,
        user_pool_arn: builtins.str,
        user_pool_client_id: builtins.str,
        user_pool_domain: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param user_pool_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_pool_arn AlbListener#user_pool_arn}.
        :param user_pool_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_pool_client_id AlbListener#user_pool_client_id}.
        :param user_pool_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_pool_domain AlbListener#user_pool_domain}.
        :param authentication_request_extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authentication_request_extra_params AlbListener#authentication_request_extra_params}.
        :param on_unauthenticated_request: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#on_unauthenticated_request AlbListener#on_unauthenticated_request}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#scope AlbListener#scope}.
        :param session_cookie_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_cookie_name AlbListener#session_cookie_name}.
        :param session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_timeout AlbListener#session_timeout}.
        '''
        value = AlbListenerDefaultActionAuthenticateCognito(
            user_pool_arn=user_pool_arn,
            user_pool_client_id=user_pool_client_id,
            user_pool_domain=user_pool_domain,
            authentication_request_extra_params=authentication_request_extra_params,
            on_unauthenticated_request=on_unauthenticated_request,
            scope=scope,
            session_cookie_name=session_cookie_name,
            session_timeout=session_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthenticateCognito", [value]))

    @jsii.member(jsii_name="putAuthenticateOidc")
    def put_authenticate_oidc(
        self,
        *,
        authorization_endpoint: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        issuer: builtins.str,
        token_endpoint: builtins.str,
        user_info_endpoint: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param authorization_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authorization_endpoint AlbListener#authorization_endpoint}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#client_id AlbListener#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#client_secret AlbListener#client_secret}.
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#issuer AlbListener#issuer}.
        :param token_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#token_endpoint AlbListener#token_endpoint}.
        :param user_info_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#user_info_endpoint AlbListener#user_info_endpoint}.
        :param authentication_request_extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#authentication_request_extra_params AlbListener#authentication_request_extra_params}.
        :param on_unauthenticated_request: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#on_unauthenticated_request AlbListener#on_unauthenticated_request}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#scope AlbListener#scope}.
        :param session_cookie_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_cookie_name AlbListener#session_cookie_name}.
        :param session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#session_timeout AlbListener#session_timeout}.
        '''
        value = AlbListenerDefaultActionAuthenticateOidc(
            authorization_endpoint=authorization_endpoint,
            client_id=client_id,
            client_secret=client_secret,
            issuer=issuer,
            token_endpoint=token_endpoint,
            user_info_endpoint=user_info_endpoint,
            authentication_request_extra_params=authentication_request_extra_params,
            on_unauthenticated_request=on_unauthenticated_request,
            scope=scope,
            session_cookie_name=session_cookie_name,
            session_timeout=session_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthenticateOidc", [value]))

    @jsii.member(jsii_name="putFixedResponse")
    def put_fixed_response(
        self,
        *,
        content_type: builtins.str,
        message_body: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#content_type AlbListener#content_type}.
        :param message_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#message_body AlbListener#message_body}.
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#status_code AlbListener#status_code}.
        '''
        value = AlbListenerDefaultActionFixedResponse(
            content_type=content_type,
            message_body=message_body,
            status_code=status_code,
        )

        return typing.cast(None, jsii.invoke(self, "putFixedResponse", [value]))

    @jsii.member(jsii_name="putForward")
    def put_forward(
        self,
        *,
        target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlbListenerDefaultActionForwardTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
        stickiness: typing.Optional[typing.Union[AlbListenerDefaultActionForwardStickiness, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target_group: target_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#target_group AlbListener#target_group}
        :param stickiness: stickiness block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#stickiness AlbListener#stickiness}
        '''
        value = AlbListenerDefaultActionForward(
            target_group=target_group, stickiness=stickiness
        )

        return typing.cast(None, jsii.invoke(self, "putForward", [value]))

    @jsii.member(jsii_name="putJwtValidation")
    def put_jwt_validation(
        self,
        *,
        issuer: builtins.str,
        jwks_endpoint: builtins.str,
        additional_claim: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlbListenerDefaultActionJwtValidationAdditionalClaim, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#issuer AlbListener#issuer}.
        :param jwks_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#jwks_endpoint AlbListener#jwks_endpoint}.
        :param additional_claim: additional_claim block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#additional_claim AlbListener#additional_claim}
        '''
        value = AlbListenerDefaultActionJwtValidation(
            issuer=issuer,
            jwks_endpoint=jwks_endpoint,
            additional_claim=additional_claim,
        )

        return typing.cast(None, jsii.invoke(self, "putJwtValidation", [value]))

    @jsii.member(jsii_name="putRedirect")
    def put_redirect(
        self,
        *,
        status_code: builtins.str,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#status_code AlbListener#status_code}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#host AlbListener#host}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#path AlbListener#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#port AlbListener#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#protocol AlbListener#protocol}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#query AlbListener#query}.
        '''
        value = AlbListenerDefaultActionRedirect(
            status_code=status_code,
            host=host,
            path=path,
            port=port,
            protocol=protocol,
            query=query,
        )

        return typing.cast(None, jsii.invoke(self, "putRedirect", [value]))

    @jsii.member(jsii_name="resetAuthenticateCognito")
    def reset_authenticate_cognito(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticateCognito", []))

    @jsii.member(jsii_name="resetAuthenticateOidc")
    def reset_authenticate_oidc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticateOidc", []))

    @jsii.member(jsii_name="resetFixedResponse")
    def reset_fixed_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedResponse", []))

    @jsii.member(jsii_name="resetForward")
    def reset_forward(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForward", []))

    @jsii.member(jsii_name="resetJwtValidation")
    def reset_jwt_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtValidation", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @jsii.member(jsii_name="resetRedirect")
    def reset_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirect", []))

    @jsii.member(jsii_name="resetTargetGroupArn")
    def reset_target_group_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetGroupArn", []))

    @builtins.property
    @jsii.member(jsii_name="authenticateCognito")
    def authenticate_cognito(
        self,
    ) -> AlbListenerDefaultActionAuthenticateCognitoOutputReference:
        return typing.cast(AlbListenerDefaultActionAuthenticateCognitoOutputReference, jsii.get(self, "authenticateCognito"))

    @builtins.property
    @jsii.member(jsii_name="authenticateOidc")
    def authenticate_oidc(
        self,
    ) -> AlbListenerDefaultActionAuthenticateOidcOutputReference:
        return typing.cast(AlbListenerDefaultActionAuthenticateOidcOutputReference, jsii.get(self, "authenticateOidc"))

    @builtins.property
    @jsii.member(jsii_name="fixedResponse")
    def fixed_response(self) -> AlbListenerDefaultActionFixedResponseOutputReference:
        return typing.cast(AlbListenerDefaultActionFixedResponseOutputReference, jsii.get(self, "fixedResponse"))

    @builtins.property
    @jsii.member(jsii_name="forward")
    def forward(self) -> AlbListenerDefaultActionForwardOutputReference:
        return typing.cast(AlbListenerDefaultActionForwardOutputReference, jsii.get(self, "forward"))

    @builtins.property
    @jsii.member(jsii_name="jwtValidation")
    def jwt_validation(self) -> AlbListenerDefaultActionJwtValidationOutputReference:
        return typing.cast(AlbListenerDefaultActionJwtValidationOutputReference, jsii.get(self, "jwtValidation"))

    @builtins.property
    @jsii.member(jsii_name="redirect")
    def redirect(self) -> "AlbListenerDefaultActionRedirectOutputReference":
        return typing.cast("AlbListenerDefaultActionRedirectOutputReference", jsii.get(self, "redirect"))

    @builtins.property
    @jsii.member(jsii_name="authenticateCognitoInput")
    def authenticate_cognito_input(
        self,
    ) -> typing.Optional[AlbListenerDefaultActionAuthenticateCognito]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionAuthenticateCognito], jsii.get(self, "authenticateCognitoInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticateOidcInput")
    def authenticate_oidc_input(
        self,
    ) -> typing.Optional[AlbListenerDefaultActionAuthenticateOidc]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionAuthenticateOidc], jsii.get(self, "authenticateOidcInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedResponseInput")
    def fixed_response_input(
        self,
    ) -> typing.Optional[AlbListenerDefaultActionFixedResponse]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionFixedResponse], jsii.get(self, "fixedResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardInput")
    def forward_input(self) -> typing.Optional[AlbListenerDefaultActionForward]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionForward], jsii.get(self, "forwardInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtValidationInput")
    def jwt_validation_input(
        self,
    ) -> typing.Optional[AlbListenerDefaultActionJwtValidation]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionJwtValidation], jsii.get(self, "jwtValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectInput")
    def redirect_input(self) -> typing.Optional["AlbListenerDefaultActionRedirect"]:
        return typing.cast(typing.Optional["AlbListenerDefaultActionRedirect"], jsii.get(self, "redirectInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupArnInput")
    def target_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "order"))

    @order.setter
    def order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0acc6a2892ffc00f6c549547f7cf9420c40c7bc3568ef4e891fe9e9a6e1e63af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetGroupArn"))

    @target_group_arn.setter
    def target_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d654e15719bae04b6aa1e5f54a11e3f27330a85d493f473a7b46bee998479666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5b2343172298865a8808746a649e3f565d9ba8aa867806368927e3c3081a27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a64a78bf0c5831dd53dbccec808ec8fef08887919af0123a0bdae56e8336413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionRedirect",
    jsii_struct_bases=[],
    name_mapping={
        "status_code": "statusCode",
        "host": "host",
        "path": "path",
        "port": "port",
        "protocol": "protocol",
        "query": "query",
    },
)
class AlbListenerDefaultActionRedirect:
    def __init__(
        self,
        *,
        status_code: builtins.str,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#status_code AlbListener#status_code}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#host AlbListener#host}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#path AlbListener#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#port AlbListener#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#protocol AlbListener#protocol}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#query AlbListener#query}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb2ef59b9560a649d488ed10e8b995e06f6ba8dc9e41355c4de9edf98baccc6)
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status_code": status_code,
        }
        if host is not None:
            self._values["host"] = host
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def status_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#status_code AlbListener#status_code}.'''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#host AlbListener#host}.'''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#path AlbListener#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#port AlbListener#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#protocol AlbListener#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#query AlbListener#query}.'''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerDefaultActionRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbListenerDefaultActionRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerDefaultActionRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__123c896c413462fa8b552a0ece7e49e523b31aa8fb2a2584ffdad56f5309ba5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0d8f83636eb890ad48fd77797cd21d7e9f8b7c3657c61f1887a36233ed07aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3adaf1bf3818bd26132c17f6380ffebf45d04b3215e6e0d1300041573ec4eba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8cf81deb073de69c614a0611b538618c134fdbb76949975e8db84c892a4d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d38f28516c143b11723d9d69f5c51e7c9913b9e562477a40d5ec26eeb169f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3373e14a65dcef1a55619753754578c10493c1b86e8545272b55fc3ae40c0c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a21aaad69b6a0ede6e8573dbda548693813ae046792d9e9b588817f5b64795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlbListenerDefaultActionRedirect]:
        return typing.cast(typing.Optional[AlbListenerDefaultActionRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlbListenerDefaultActionRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0fc7a410b8a08b443a310f73591c424d4fc330a3ebeb37b25cf4205be7b7282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerMutualAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "advertise_trust_store_ca_names": "advertiseTrustStoreCaNames",
        "ignore_client_certificate_expiry": "ignoreClientCertificateExpiry",
        "trust_store_arn": "trustStoreArn",
    },
)
class AlbListenerMutualAuthentication:
    def __init__(
        self,
        *,
        mode: builtins.str,
        advertise_trust_store_ca_names: typing.Optional[builtins.str] = None,
        ignore_client_certificate_expiry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trust_store_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#mode AlbListener#mode}.
        :param advertise_trust_store_ca_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#advertise_trust_store_ca_names AlbListener#advertise_trust_store_ca_names}.
        :param ignore_client_certificate_expiry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#ignore_client_certificate_expiry AlbListener#ignore_client_certificate_expiry}.
        :param trust_store_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#trust_store_arn AlbListener#trust_store_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce5d7358a37bb99575a091ee9b350ad0fdbd9e4c05a752effcfbb7d317cf1e1)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument advertise_trust_store_ca_names", value=advertise_trust_store_ca_names, expected_type=type_hints["advertise_trust_store_ca_names"])
            check_type(argname="argument ignore_client_certificate_expiry", value=ignore_client_certificate_expiry, expected_type=type_hints["ignore_client_certificate_expiry"])
            check_type(argname="argument trust_store_arn", value=trust_store_arn, expected_type=type_hints["trust_store_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if advertise_trust_store_ca_names is not None:
            self._values["advertise_trust_store_ca_names"] = advertise_trust_store_ca_names
        if ignore_client_certificate_expiry is not None:
            self._values["ignore_client_certificate_expiry"] = ignore_client_certificate_expiry
        if trust_store_arn is not None:
            self._values["trust_store_arn"] = trust_store_arn

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#mode AlbListener#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advertise_trust_store_ca_names(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#advertise_trust_store_ca_names AlbListener#advertise_trust_store_ca_names}.'''
        result = self._values.get("advertise_trust_store_ca_names")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_client_certificate_expiry(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#ignore_client_certificate_expiry AlbListener#ignore_client_certificate_expiry}.'''
        result = self._values.get("ignore_client_certificate_expiry")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trust_store_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#trust_store_arn AlbListener#trust_store_arn}.'''
        result = self._values.get("trust_store_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerMutualAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbListenerMutualAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerMutualAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adc91ed602a363252d8b11931b81a77b174d7d3e07934a8aaf482f99c3ea374f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdvertiseTrustStoreCaNames")
    def reset_advertise_trust_store_ca_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertiseTrustStoreCaNames", []))

    @jsii.member(jsii_name="resetIgnoreClientCertificateExpiry")
    def reset_ignore_client_certificate_expiry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreClientCertificateExpiry", []))

    @jsii.member(jsii_name="resetTrustStoreArn")
    def reset_trust_store_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustStoreArn", []))

    @builtins.property
    @jsii.member(jsii_name="advertiseTrustStoreCaNamesInput")
    def advertise_trust_store_ca_names_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "advertiseTrustStoreCaNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreClientCertificateExpiryInput")
    def ignore_client_certificate_expiry_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreClientCertificateExpiryInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="trustStoreArnInput")
    def trust_store_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustStoreArnInput"))

    @builtins.property
    @jsii.member(jsii_name="advertiseTrustStoreCaNames")
    def advertise_trust_store_ca_names(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "advertiseTrustStoreCaNames"))

    @advertise_trust_store_ca_names.setter
    def advertise_trust_store_ca_names(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9bd8034b9dcd4a5b17af28a76530a6e2f48c9d021b888ef252f2c59706a9af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertiseTrustStoreCaNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreClientCertificateExpiry")
    def ignore_client_certificate_expiry(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreClientCertificateExpiry"))

    @ignore_client_certificate_expiry.setter
    def ignore_client_certificate_expiry(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ead992c602ca23dfaf69b8415cdc86341ebe8c21cd06501267e12526e279509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreClientCertificateExpiry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466c1d652b8d1349b13051405d5a2b4fbdfa06489769f48036576f777deaf468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustStoreArn")
    def trust_store_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustStoreArn"))

    @trust_store_arn.setter
    def trust_store_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2ce66ee6ee3f11c9198bb0727b7ad35c5b42c31a1aa26d8b5927198f9ebab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustStoreArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlbListenerMutualAuthentication]:
        return typing.cast(typing.Optional[AlbListenerMutualAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlbListenerMutualAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bc11088df72a5c1fd706c3dc3a4b7c0ad8be8d1340358d22f51f3d424271ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class AlbListenerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#create AlbListener#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#update AlbListener#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ebd037d072c077785d9598c4bb967d94b62b9952019608fa388ce60b2e848d0)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#create AlbListener#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/alb_listener#update AlbListener#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbListenerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbListenerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.albListener.AlbListenerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64267890b63d5ec98bda830cfcbfc18b4d602ef03747f9ca1d8357462220e79f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d3dc1740d2da79f8f3e85b769e695da205f13ce0fc5b3c5415e082179a77fa37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05663e0f8500da87221a1e1af552c0c34c2cb6da69a45f42291acbfc63e34ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c746cc7b614a32a1b4bf4188ebfcf240c63b52c256c13a73274a1623149abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AlbListener",
    "AlbListenerConfig",
    "AlbListenerDefaultAction",
    "AlbListenerDefaultActionAuthenticateCognito",
    "AlbListenerDefaultActionAuthenticateCognitoOutputReference",
    "AlbListenerDefaultActionAuthenticateOidc",
    "AlbListenerDefaultActionAuthenticateOidcOutputReference",
    "AlbListenerDefaultActionFixedResponse",
    "AlbListenerDefaultActionFixedResponseOutputReference",
    "AlbListenerDefaultActionForward",
    "AlbListenerDefaultActionForwardOutputReference",
    "AlbListenerDefaultActionForwardStickiness",
    "AlbListenerDefaultActionForwardStickinessOutputReference",
    "AlbListenerDefaultActionForwardTargetGroup",
    "AlbListenerDefaultActionForwardTargetGroupList",
    "AlbListenerDefaultActionForwardTargetGroupOutputReference",
    "AlbListenerDefaultActionJwtValidation",
    "AlbListenerDefaultActionJwtValidationAdditionalClaim",
    "AlbListenerDefaultActionJwtValidationAdditionalClaimList",
    "AlbListenerDefaultActionJwtValidationAdditionalClaimOutputReference",
    "AlbListenerDefaultActionJwtValidationOutputReference",
    "AlbListenerDefaultActionList",
    "AlbListenerDefaultActionOutputReference",
    "AlbListenerDefaultActionRedirect",
    "AlbListenerDefaultActionRedirectOutputReference",
    "AlbListenerMutualAuthentication",
    "AlbListenerMutualAuthenticationOutputReference",
    "AlbListenerTimeouts",
    "AlbListenerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6bf8746a6d47e59ae9099b04e73335e346f590c59816e096d27ea27c689ee96f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlbListenerDefaultAction, typing.Dict[builtins.str, typing.Any]]]],
    load_balancer_arn: builtins.str,
    alpn_policy: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mutual_authentication: typing.Optional[typing.Union[AlbListenerMutualAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_issuer_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_leaf_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_subject_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_validity_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_tls_cipher_suite_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_tls_version_header_name: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_allow_credentials_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_allow_headers_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_allow_methods_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_allow_origin_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_expose_headers_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_max_age_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_content_security_policy_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_server_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    routing_http_response_strict_transport_security_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_x_content_type_options_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_x_frame_options_header_value: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tcp_idle_timeout_seconds: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[AlbListenerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__acdc6260d85b0d8c29dc35fe879ef1f11a099046b38d241a9cef963ff7a99bf5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292a6d2ac5f9d7f9825be476798b0fbb8b61df0d27739f03f36c8fa122d13ff4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlbListenerDefaultAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c1395e999cdd486c5a1b62b4c629a0129c0f374f63c129c917edd90e15cc2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145b33244ea5379032950da8648be0b24427e405ba4f3fe65911bef34fd4c6ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14112212713ae292a1d8d05c39739103c4cd21a900c43928b7a5837a1d68000a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d714b3fa310595945b8b61e96a952c1a8b67b07163d1f0f2d0b0963464e1ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3a5982ea9d96a33dcd7b4b7451b0d23080eb68d0cab6ea10231bbe5fd75dec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1034d9c5382401769551cd84094ce76ff885f945ce185d147cacbc0912a61049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381167ab8e2aa999c1e3b9d55bd1b02911d41e0f03becc0fee849f09007fdbd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3b3dfd9b19d29b99c10f5fea6bd209aa9de7e694c2b45793fcd9941f927f36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805a6787ffc680dc67914c88bb6d5cffe61b16e2967bba6271cf9521bfe9c364(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14ac1d4c5f7fbe0b83cac1b018be1b4ca578ef80afe9f54c7dfc14746e8b899(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4664c9255d04339585ce97cd1ca9f74750be17d48f23755cdb5022bd63a2c613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42b8fef6fb45883ac60f36458d1876e299bfa56e0cd8a6c275272e349f3361e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df664291213b8219538ba3538ca588f1faefc850937735b491c71d0a89c9fb28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb0505a0e55d79ac06bd652951d56e380402bab631a5caef3a631535627aca9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803bbe07b2f2b906daad428af4edc86d6ca31eda30f7c6cd3c495873ce18c7ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a444807e28a0796ff0bb68a3ae3816d65f78567b3462cdaf2edfeb694f5c86c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2419961ee96e9ce9d9d511bdb912d4656c4e788d8f3ca936fc663f4ed0cb4f15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4a28f3d0b8f3cb49eafd1f223848c2ea73f7daddfb692e0be495bdbe968f29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc55b00150dce77f18db23b34bc79233362a0945baa0690e301a1a56270baa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873028027c8ec7948329fa8c98d4fea8da07bb91cb8c42d78590fe58c2900e24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b286686f08cdc0c64c5a0b08ac3b9a57882acc4e2ced31eb7599d15fcd4edcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609a38d60317a8eebbf1893cfe47a6d578eaf32b3f7f9ec2c1c2b9e70f77a82b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b033ae6e7d5ec115a42432561cc0dccb7e99f1546cce80de0ac245b6e5a8bb27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2c1ed20601548a2f96c5b8fcff217fe0597652580948613a4aeb7c09be7659(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3783555d0a18ee835df848ae4ceb7f5e704ecb6fda97b7c14b9a4874f4867d90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff1bc1bcd2a1f67e7374e11a629e418fe9944236b73fc51860f2394f72fa7d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9957a47f7c45541c05da7046bb3f7d71a166f1fc26eb8375a51284461b2fd841(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4af8764f263d8f8be785a48883f404d0a7d53f614c2a91d1505f7c3e209059c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26585889f8c8d79b0fe1fdfe1f1dcd4f05ba078ec20ab052dbd34b3cc35ead15(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058f4db2f5b02faf1c42c3d5924fdcc187eab5fcf9d9ca709f9dab555fb31142(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1c99867b759386eef64d60031f8b4c1c3fbe7cfdd21c3e168412ec5192774f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlbListenerDefaultAction, typing.Dict[builtins.str, typing.Any]]]],
    load_balancer_arn: builtins.str,
    alpn_policy: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mutual_authentication: typing.Optional[typing.Union[AlbListenerMutualAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_issuer_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_leaf_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_serial_number_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_subject_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_mtls_clientcert_validity_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_tls_cipher_suite_header_name: typing.Optional[builtins.str] = None,
    routing_http_request_x_amzn_tls_version_header_name: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_allow_credentials_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_allow_headers_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_allow_methods_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_allow_origin_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_expose_headers_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_access_control_max_age_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_content_security_policy_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_server_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    routing_http_response_strict_transport_security_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_x_content_type_options_header_value: typing.Optional[builtins.str] = None,
    routing_http_response_x_frame_options_header_value: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tcp_idle_timeout_seconds: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[AlbListenerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3be68f3b02da0681220da0469bd55a53cae1f106330a9eaecd15f0ae00da47(
    *,
    type: builtins.str,
    authenticate_cognito: typing.Optional[typing.Union[AlbListenerDefaultActionAuthenticateCognito, typing.Dict[builtins.str, typing.Any]]] = None,
    authenticate_oidc: typing.Optional[typing.Union[AlbListenerDefaultActionAuthenticateOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    fixed_response: typing.Optional[typing.Union[AlbListenerDefaultActionFixedResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    forward: typing.Optional[typing.Union[AlbListenerDefaultActionForward, typing.Dict[builtins.str, typing.Any]]] = None,
    jwt_validation: typing.Optional[typing.Union[AlbListenerDefaultActionJwtValidation, typing.Dict[builtins.str, typing.Any]]] = None,
    order: typing.Optional[jsii.Number] = None,
    redirect: typing.Optional[typing.Union[AlbListenerDefaultActionRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
    target_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01de940330e4e96da05d3e94456e2d3214f4c63dc96c6d02abc0ec6a09b23c48(
    *,
    user_pool_arn: builtins.str,
    user_pool_client_id: builtins.str,
    user_pool_domain: builtins.str,
    authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    on_unauthenticated_request: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    session_cookie_name: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144cc7bf750af4e32e717e3693d995c96755fd297cba3500e2a80ece91d04cca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca45797cc39b8f1fd7f99eb8971ba6b846f478487b168d8d4fc9cfdc210f118(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf9121298f02702344cf0c98d8dbc9c4b30eecdfe52690e825857152595a1a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2316fb282afb339731909e82935ff528c809553cebecca77caf8e765cb07d4be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692a618d4f1c451f70afae27d498333483defe8afbd7da2e58a4eadd05597bec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8c2a9261331f469d7c8ce6c5399988a232c6f0e535723712bb81690fd9acf3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317e15027431efea77caf2ca66d69e34b28a2461359cc2bbc346554a5c4f0dfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b7af17dfaa6f883a303ac921dfff58da2e8f75d6d6e6a51c36867849a7b360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b482b9b82e6fedc12f73deba9354440d5dcbc5d30b0bb01b114163f32bc923c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90b49979d2e18940d4d4ecd8edcf1de705530d99bd6acbe949b9ad294a30f96(
    value: typing.Optional[AlbListenerDefaultActionAuthenticateCognito],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ac5db8dc570ec887b92e997b21dda4c168c7125d0f94c15c69715d15aac880(
    *,
    authorization_endpoint: builtins.str,
    client_id: builtins.str,
    client_secret: builtins.str,
    issuer: builtins.str,
    token_endpoint: builtins.str,
    user_info_endpoint: builtins.str,
    authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    on_unauthenticated_request: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    session_cookie_name: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3c4441c31a54e2be0b4bc13dca97f561439bdb369c37f2f7b160de09b2f3e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631bc65123708276b37806c3ffb0dbc6ab615a56143f3058e80881f5a34ff865(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c6e40c725139f31a04104f1499df55f26160ac10a696b9c832812187b6da81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c954537d5a259f3aa7510f3ea866f4716a8aac92d5ebaed786bfc01254d196(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5da43e05fa854a82a8fa86454b7c01cc27b21f79d0045a38ff49a9fa58d7fbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2d25d0d05ae9a260e165c8d17bb1d5c5b57540bab778afe8ba26b0e534ec85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20cdbf73189aa8581bdfd843e350ac8d44c82d6d1cf4fe8121b9b65c98405ce6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c188be181a107fba6beba2d25c54121c13d772aa99fa1223d7eb76f034019e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80694dd020dc0d32d8b7c0bd486b5b54cc6df55fe89ee27cd657ae75197ddef8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d482b33fda5ce515b33f429d5d765ce25854f58903ee6023db0aa511801f12(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89e46e22806438f53e0f9159d8a0bc82ad549f13fa758b89743a8f2f55b0332(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c52b461fb67e02c23ee7a59b5eb3045d68d45b6498e308faf8d24773eebdf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64082fe619b9e2e66ccca5c66380e0c5b415f2c324cd47592d9d7224fce6486c(
    value: typing.Optional[AlbListenerDefaultActionAuthenticateOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693feceda86ff4d2380953941d2260393766802d0e99063060b173e34a4aa110(
    *,
    content_type: builtins.str,
    message_body: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae3373a777886359ba6cfd8677134073820c2918510bd4a432cdd589a9ec717(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e0cce6977c656ba1d8ae9c4776b2da391829570c4605ac55401ea311edc2a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc06dc57c3d9beefe36560e2482c425ae24d1da2f4687972bfb408d7546e575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102e2376ac44dd77906e680d9af5f8f4aa1184e952d26a007f7cd6d8bc855d30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887924f9f51f0438f35ef58527305f7a509dd882ee834faed04ecdef71805cfd(
    value: typing.Optional[AlbListenerDefaultActionFixedResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad1b6d6aed9eb43d8adabb491af7046d9877aec29caf58cbb37be25d013c744(
    *,
    target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlbListenerDefaultActionForwardTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
    stickiness: typing.Optional[typing.Union[AlbListenerDefaultActionForwardStickiness, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d274a175c35b1db523d0f6b2e359ea06b5cfe5278e5e3e43a13e415c80624863(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b5aa6022e49a27a0d0aece716d90314a4bbb436ff1eb796463c9b2fb5b70fd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlbListenerDefaultActionForwardTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f110aa509ee3d5d4f97a06d492c07d6df7d44bfd2d241f1bd1cc424bcc53e5e3(
    value: typing.Optional[AlbListenerDefaultActionForward],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94d0310fc419ffe52e3ac55d176f208da22467c52bf4334ec3fda4d33045245(
    *,
    duration: jsii.Number,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024927e96368630f64fdd7905faf02adfc0f1dda5c4aba2b0cb0effe864c39b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4816414f331d18bc33c1aeb955e0c77ac39a4844e28d2b3c709fade9c4e4a31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8a8882627893977baa4ec2e78440e08ec3e587402999148a3469130768e949(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f08d417a66366a1509e2b51893c80808f09851ae4505ed9f9553d6b334fa72e(
    value: typing.Optional[AlbListenerDefaultActionForwardStickiness],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e33a5cc4f0d163ccb9e981468df6bde0a4bf1e79eccf9de34759c3b66c86e7(
    *,
    arn: builtins.str,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682e553a4fb21f4850f36ac4ef89f0c1f80ab4672a13730021c983bbb61986c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d7e93beb4d274b1c14011008d804062a269d8f302c31cba16322337848b63f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a27aa408144d446be3efb16400e8a64da0ceda65fe45f00c680257c1d42b28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c1e6353e9768bd2b68bc602b11f7b36d80d5864e3e75e007ba5f8c9d4ff531(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e153199ab3712a8c995a4b37942ed376db0be4ef6973dc70b5713845bddd31(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6604b1f35c7baf44106fba01a5da8760cbafda56393e189f7f6d27572446abff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultActionForwardTargetGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98eb1729e6203187b0d86b69ed0111d6bb1e3f7ba2dfec05ec841290f957a46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f757aa0aaf9f6c03afb35f822ebb02de6c18b77acb13d4ea292ef89fbe46c0e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05249e5e71e05a49849ee8a4f2fde504b6d2a50b9c8549c064545be9ed9ed6f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aad3e962af0a49a8d714cacea087bc0b5e163b7ecf17e245c865beaae45c0c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultActionForwardTargetGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e286ccb44839c3192cc59688e7e06509c3f72c99b4b7d4c734c8431ac0dcd69(
    *,
    issuer: builtins.str,
    jwks_endpoint: builtins.str,
    additional_claim: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlbListenerDefaultActionJwtValidationAdditionalClaim, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98f34570c8946cd6787813116e000500c7b6004e551c738dc69d4a14f90627a(
    *,
    format: builtins.str,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9de8ce9645a17ae69f2049bd23eb8df9eb514db5e7f18acfd930e5685435b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d7b63ce6eaffb50aea57937c228c912262a0302ebb753f0d93658ef30420a0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7eb8ae1eacb7f6c111f30773203f4c3e6c247692e68dd6974f077768ed79b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218d3940cb54758f2e2ce9938499f16b14f2378c10e5ed2ad4cbac44ae7b2fec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e3377466331b71f9db0414932ae49f5661b066502bc9af268e9cd5e3b08c6e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52ca5f7c066a6d4c6926fa2f28b4cd88e9b55418a1da8e0ddc23d68272a6e3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultActionJwtValidationAdditionalClaim]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c897fe6cc48153bb163e69a40ee6495142db292cd82a5dcb749afb8e5ecb0d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf01eee97d8b260e213f8438582d3a1fe92da36370cc99561b345477e43f3b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd68ad0529afbe1facf08b58d98ca393c5583ab5c3122cde683b54a905272d6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9020697d19cec4b838a8dc7f4795266f37b503502cae489f28b47144a5f9b23(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1f5bcc1ee3b18510dadfda516a38d762d6a83aa15bd42a5a43adc7d18c34d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultActionJwtValidationAdditionalClaim]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c05e06c233adcf12a9fc9a76d5d265cfeee06a616d2d3c8a44564d3feb7450e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7066e03922582df9e63558062cbbe70e502170c5a87a049fa8a439bc36ce26(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlbListenerDefaultActionJwtValidationAdditionalClaim, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cb7ac677f2d3152f71fdf224a58d018ff18f253de9533efece7a1eb0783170(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38369fc043415a33f9eda2e4f33a5c711fcd9a3991403e9b39ad6d284228c579(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e52b36a68adc7508595261c74a81a79d04775d483d35680094783ceefe195e(
    value: typing.Optional[AlbListenerDefaultActionJwtValidation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dbf14af7933a2272514e837730463882215f020a107423229ab84e350d284b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7822fb7f6a17480ade5a4f612e0e7541fb898ebe3ba73c2d340d46b4876f1f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4f10af5c4db776e96ae7c8130b7cfb0a83a043b9280030d9e74c330a5075fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505cafc0002e55906c557b16847f355c15bcb2f9174a83645ffe4ed9142de07f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cec7c33dc082096571b3b6c73d7e851857939b71b83a32fa08449fb1cc358e0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53b9545ac8328930e7b5ed46e61f38f985fba869d85948bedf51e61aea99a3e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlbListenerDefaultAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c07182ec5ace9be52648a5f8115c254d8ab815c2223edefa4a51a53bc3f3d52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acc6a2892ffc00f6c549547f7cf9420c40c7bc3568ef4e891fe9e9a6e1e63af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d654e15719bae04b6aa1e5f54a11e3f27330a85d493f473a7b46bee998479666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5b2343172298865a8808746a649e3f565d9ba8aa867806368927e3c3081a27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a64a78bf0c5831dd53dbccec808ec8fef08887919af0123a0bdae56e8336413(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerDefaultAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb2ef59b9560a649d488ed10e8b995e06f6ba8dc9e41355c4de9edf98baccc6(
    *,
    status_code: builtins.str,
    host: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123c896c413462fa8b552a0ece7e49e523b31aa8fb2a2584ffdad56f5309ba5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0d8f83636eb890ad48fd77797cd21d7e9f8b7c3657c61f1887a36233ed07aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3adaf1bf3818bd26132c17f6380ffebf45d04b3215e6e0d1300041573ec4eba2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8cf81deb073de69c614a0611b538618c134fdbb76949975e8db84c892a4d63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d38f28516c143b11723d9d69f5c51e7c9913b9e562477a40d5ec26eeb169f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3373e14a65dcef1a55619753754578c10493c1b86e8545272b55fc3ae40c0c7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a21aaad69b6a0ede6e8573dbda548693813ae046792d9e9b588817f5b64795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fc7a410b8a08b443a310f73591c424d4fc330a3ebeb37b25cf4205be7b7282(
    value: typing.Optional[AlbListenerDefaultActionRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce5d7358a37bb99575a091ee9b350ad0fdbd9e4c05a752effcfbb7d317cf1e1(
    *,
    mode: builtins.str,
    advertise_trust_store_ca_names: typing.Optional[builtins.str] = None,
    ignore_client_certificate_expiry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trust_store_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc91ed602a363252d8b11931b81a77b174d7d3e07934a8aaf482f99c3ea374f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9bd8034b9dcd4a5b17af28a76530a6e2f48c9d021b888ef252f2c59706a9af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ead992c602ca23dfaf69b8415cdc86341ebe8c21cd06501267e12526e279509(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466c1d652b8d1349b13051405d5a2b4fbdfa06489769f48036576f777deaf468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2ce66ee6ee3f11c9198bb0727b7ad35c5b42c31a1aa26d8b5927198f9ebab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bc11088df72a5c1fd706c3dc3a4b7c0ad8be8d1340358d22f51f3d424271ca(
    value: typing.Optional[AlbListenerMutualAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebd037d072c077785d9598c4bb967d94b62b9952019608fa388ce60b2e848d0(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64267890b63d5ec98bda830cfcbfc18b4d602ef03747f9ca1d8357462220e79f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3dc1740d2da79f8f3e85b769e695da205f13ce0fc5b3c5415e082179a77fa37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05663e0f8500da87221a1e1af552c0c34c2cb6da69a45f42291acbfc63e34ea1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c746cc7b614a32a1b4bf4188ebfcf240c63b52c256c13a73274a1623149abb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlbListenerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
