r'''
# `aws_ec2_client_vpn_endpoint`

Refer to the Terraform Registry for docs: [`aws_ec2_client_vpn_endpoint`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint).
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


class Ec2ClientVpnEndpoint(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpoint",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint aws_ec2_client_vpn_endpoint}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authentication_options: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Ec2ClientVpnEndpointAuthenticationOptions", typing.Dict[builtins.str, typing.Any]]]],
        connection_log_options: typing.Union["Ec2ClientVpnEndpointConnectionLogOptions", typing.Dict[builtins.str, typing.Any]],
        server_certificate_arn: builtins.str,
        client_cidr_block: typing.Optional[builtins.str] = None,
        client_connect_options: typing.Optional[typing.Union["Ec2ClientVpnEndpointClientConnectOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        client_login_banner_options: typing.Optional[typing.Union["Ec2ClientVpnEndpointClientLoginBannerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        client_route_enforcement_options: typing.Optional[typing.Union["Ec2ClientVpnEndpointClientRouteEnforcementOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disconnect_on_session_timeout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        endpoint_ip_address_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        self_service_portal: typing.Optional[builtins.str] = None,
        session_timeout_hours: typing.Optional[jsii.Number] = None,
        split_tunnel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        traffic_ip_address_type: typing.Optional[builtins.str] = None,
        transport_protocol: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        vpn_port: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint aws_ec2_client_vpn_endpoint} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authentication_options: authentication_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#authentication_options Ec2ClientVpnEndpoint#authentication_options}
        :param connection_log_options: connection_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#connection_log_options Ec2ClientVpnEndpoint#connection_log_options}
        :param server_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#server_certificate_arn Ec2ClientVpnEndpoint#server_certificate_arn}.
        :param client_cidr_block: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_cidr_block Ec2ClientVpnEndpoint#client_cidr_block}.
        :param client_connect_options: client_connect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_connect_options Ec2ClientVpnEndpoint#client_connect_options}
        :param client_login_banner_options: client_login_banner_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_login_banner_options Ec2ClientVpnEndpoint#client_login_banner_options}
        :param client_route_enforcement_options: client_route_enforcement_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_route_enforcement_options Ec2ClientVpnEndpoint#client_route_enforcement_options}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#description Ec2ClientVpnEndpoint#description}.
        :param disconnect_on_session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#disconnect_on_session_timeout Ec2ClientVpnEndpoint#disconnect_on_session_timeout}.
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#dns_servers Ec2ClientVpnEndpoint#dns_servers}.
        :param endpoint_ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#endpoint_ip_address_type Ec2ClientVpnEndpoint#endpoint_ip_address_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#id Ec2ClientVpnEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#region Ec2ClientVpnEndpoint#region}
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#security_group_ids Ec2ClientVpnEndpoint#security_group_ids}.
        :param self_service_portal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#self_service_portal Ec2ClientVpnEndpoint#self_service_portal}.
        :param session_timeout_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#session_timeout_hours Ec2ClientVpnEndpoint#session_timeout_hours}.
        :param split_tunnel: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#split_tunnel Ec2ClientVpnEndpoint#split_tunnel}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#tags Ec2ClientVpnEndpoint#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#tags_all Ec2ClientVpnEndpoint#tags_all}.
        :param traffic_ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#traffic_ip_address_type Ec2ClientVpnEndpoint#traffic_ip_address_type}.
        :param transport_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#transport_protocol Ec2ClientVpnEndpoint#transport_protocol}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#vpc_id Ec2ClientVpnEndpoint#vpc_id}.
        :param vpn_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#vpn_port Ec2ClientVpnEndpoint#vpn_port}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d873d14a32100666c8ccfdce77e7c229380f4808ded7d01e5de907978fc46f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Ec2ClientVpnEndpointConfig(
            authentication_options=authentication_options,
            connection_log_options=connection_log_options,
            server_certificate_arn=server_certificate_arn,
            client_cidr_block=client_cidr_block,
            client_connect_options=client_connect_options,
            client_login_banner_options=client_login_banner_options,
            client_route_enforcement_options=client_route_enforcement_options,
            description=description,
            disconnect_on_session_timeout=disconnect_on_session_timeout,
            dns_servers=dns_servers,
            endpoint_ip_address_type=endpoint_ip_address_type,
            id=id,
            region=region,
            security_group_ids=security_group_ids,
            self_service_portal=self_service_portal,
            session_timeout_hours=session_timeout_hours,
            split_tunnel=split_tunnel,
            tags=tags,
            tags_all=tags_all,
            traffic_ip_address_type=traffic_ip_address_type,
            transport_protocol=transport_protocol,
            vpc_id=vpc_id,
            vpn_port=vpn_port,
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
        '''Generates CDKTF code for importing a Ec2ClientVpnEndpoint resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Ec2ClientVpnEndpoint to import.
        :param import_from_id: The id of the existing Ec2ClientVpnEndpoint that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Ec2ClientVpnEndpoint to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56ee7ea21e564f07b05096834e406a8fdfda127f97d9d74229e4ea043f56cd0a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthenticationOptions")
    def put_authentication_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Ec2ClientVpnEndpointAuthenticationOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b845f549298dbbe2d91afa09bac89d0d0edacb43618d600a34f8741ede831080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthenticationOptions", [value]))

    @jsii.member(jsii_name="putClientConnectOptions")
    def put_client_connect_options(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lambda_function_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enabled Ec2ClientVpnEndpoint#enabled}.
        :param lambda_function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#lambda_function_arn Ec2ClientVpnEndpoint#lambda_function_arn}.
        '''
        value = Ec2ClientVpnEndpointClientConnectOptions(
            enabled=enabled, lambda_function_arn=lambda_function_arn
        )

        return typing.cast(None, jsii.invoke(self, "putClientConnectOptions", [value]))

    @jsii.member(jsii_name="putClientLoginBannerOptions")
    def put_client_login_banner_options(
        self,
        *,
        banner_text: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param banner_text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#banner_text Ec2ClientVpnEndpoint#banner_text}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enabled Ec2ClientVpnEndpoint#enabled}.
        '''
        value = Ec2ClientVpnEndpointClientLoginBannerOptions(
            banner_text=banner_text, enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putClientLoginBannerOptions", [value]))

    @jsii.member(jsii_name="putClientRouteEnforcementOptions")
    def put_client_route_enforcement_options(
        self,
        *,
        enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enforced: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enforced Ec2ClientVpnEndpoint#enforced}.
        '''
        value = Ec2ClientVpnEndpointClientRouteEnforcementOptions(enforced=enforced)

        return typing.cast(None, jsii.invoke(self, "putClientRouteEnforcementOptions", [value]))

    @jsii.member(jsii_name="putConnectionLogOptions")
    def put_connection_log_options(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cloudwatch_log_group: typing.Optional[builtins.str] = None,
        cloudwatch_log_stream: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enabled Ec2ClientVpnEndpoint#enabled}.
        :param cloudwatch_log_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#cloudwatch_log_group Ec2ClientVpnEndpoint#cloudwatch_log_group}.
        :param cloudwatch_log_stream: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#cloudwatch_log_stream Ec2ClientVpnEndpoint#cloudwatch_log_stream}.
        '''
        value = Ec2ClientVpnEndpointConnectionLogOptions(
            enabled=enabled,
            cloudwatch_log_group=cloudwatch_log_group,
            cloudwatch_log_stream=cloudwatch_log_stream,
        )

        return typing.cast(None, jsii.invoke(self, "putConnectionLogOptions", [value]))

    @jsii.member(jsii_name="resetClientCidrBlock")
    def reset_client_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCidrBlock", []))

    @jsii.member(jsii_name="resetClientConnectOptions")
    def reset_client_connect_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientConnectOptions", []))

    @jsii.member(jsii_name="resetClientLoginBannerOptions")
    def reset_client_login_banner_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientLoginBannerOptions", []))

    @jsii.member(jsii_name="resetClientRouteEnforcementOptions")
    def reset_client_route_enforcement_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientRouteEnforcementOptions", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisconnectOnSessionTimeout")
    def reset_disconnect_on_session_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisconnectOnSessionTimeout", []))

    @jsii.member(jsii_name="resetDnsServers")
    def reset_dns_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServers", []))

    @jsii.member(jsii_name="resetEndpointIpAddressType")
    def reset_endpoint_ip_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointIpAddressType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSelfServicePortal")
    def reset_self_service_portal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfServicePortal", []))

    @jsii.member(jsii_name="resetSessionTimeoutHours")
    def reset_session_timeout_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTimeoutHours", []))

    @jsii.member(jsii_name="resetSplitTunnel")
    def reset_split_tunnel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplitTunnel", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTrafficIpAddressType")
    def reset_traffic_ip_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrafficIpAddressType", []))

    @jsii.member(jsii_name="resetTransportProtocol")
    def reset_transport_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransportProtocol", []))

    @jsii.member(jsii_name="resetVpcId")
    def reset_vpc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcId", []))

    @jsii.member(jsii_name="resetVpnPort")
    def reset_vpn_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnPort", []))

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
    @jsii.member(jsii_name="authenticationOptions")
    def authentication_options(self) -> "Ec2ClientVpnEndpointAuthenticationOptionsList":
        return typing.cast("Ec2ClientVpnEndpointAuthenticationOptionsList", jsii.get(self, "authenticationOptions"))

    @builtins.property
    @jsii.member(jsii_name="clientConnectOptions")
    def client_connect_options(
        self,
    ) -> "Ec2ClientVpnEndpointClientConnectOptionsOutputReference":
        return typing.cast("Ec2ClientVpnEndpointClientConnectOptionsOutputReference", jsii.get(self, "clientConnectOptions"))

    @builtins.property
    @jsii.member(jsii_name="clientLoginBannerOptions")
    def client_login_banner_options(
        self,
    ) -> "Ec2ClientVpnEndpointClientLoginBannerOptionsOutputReference":
        return typing.cast("Ec2ClientVpnEndpointClientLoginBannerOptionsOutputReference", jsii.get(self, "clientLoginBannerOptions"))

    @builtins.property
    @jsii.member(jsii_name="clientRouteEnforcementOptions")
    def client_route_enforcement_options(
        self,
    ) -> "Ec2ClientVpnEndpointClientRouteEnforcementOptionsOutputReference":
        return typing.cast("Ec2ClientVpnEndpointClientRouteEnforcementOptionsOutputReference", jsii.get(self, "clientRouteEnforcementOptions"))

    @builtins.property
    @jsii.member(jsii_name="connectionLogOptions")
    def connection_log_options(
        self,
    ) -> "Ec2ClientVpnEndpointConnectionLogOptionsOutputReference":
        return typing.cast("Ec2ClientVpnEndpointConnectionLogOptionsOutputReference", jsii.get(self, "connectionLogOptions"))

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @builtins.property
    @jsii.member(jsii_name="selfServicePortalUrl")
    def self_service_portal_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfServicePortalUrl"))

    @builtins.property
    @jsii.member(jsii_name="authenticationOptionsInput")
    def authentication_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Ec2ClientVpnEndpointAuthenticationOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Ec2ClientVpnEndpointAuthenticationOptions"]]], jsii.get(self, "authenticationOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCidrBlockInput")
    def client_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="clientConnectOptionsInput")
    def client_connect_options_input(
        self,
    ) -> typing.Optional["Ec2ClientVpnEndpointClientConnectOptions"]:
        return typing.cast(typing.Optional["Ec2ClientVpnEndpointClientConnectOptions"], jsii.get(self, "clientConnectOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientLoginBannerOptionsInput")
    def client_login_banner_options_input(
        self,
    ) -> typing.Optional["Ec2ClientVpnEndpointClientLoginBannerOptions"]:
        return typing.cast(typing.Optional["Ec2ClientVpnEndpointClientLoginBannerOptions"], jsii.get(self, "clientLoginBannerOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientRouteEnforcementOptionsInput")
    def client_route_enforcement_options_input(
        self,
    ) -> typing.Optional["Ec2ClientVpnEndpointClientRouteEnforcementOptions"]:
        return typing.cast(typing.Optional["Ec2ClientVpnEndpointClientRouteEnforcementOptions"], jsii.get(self, "clientRouteEnforcementOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionLogOptionsInput")
    def connection_log_options_input(
        self,
    ) -> typing.Optional["Ec2ClientVpnEndpointConnectionLogOptions"]:
        return typing.cast(typing.Optional["Ec2ClientVpnEndpointConnectionLogOptions"], jsii.get(self, "connectionLogOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disconnectOnSessionTimeoutInput")
    def disconnect_on_session_timeout_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disconnectOnSessionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServersInput")
    def dns_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsServersInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointIpAddressTypeInput")
    def endpoint_ip_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointIpAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="selfServicePortalInput")
    def self_service_portal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selfServicePortalInput"))

    @builtins.property
    @jsii.member(jsii_name="serverCertificateArnInput")
    def server_certificate_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverCertificateArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTimeoutHoursInput")
    def session_timeout_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionTimeoutHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="splitTunnelInput")
    def split_tunnel_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "splitTunnelInput"))

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
    @jsii.member(jsii_name="trafficIpAddressTypeInput")
    def traffic_ip_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trafficIpAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="transportProtocolInput")
    def transport_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transportProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnPortInput")
    def vpn_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vpnPortInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCidrBlock")
    def client_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCidrBlock"))

    @client_cidr_block.setter
    def client_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d086ecd3c43cc0000f00dde2976875a0308d191ccb217703bd9c6a4f3f3d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebbc2e22dcb29f33ba06f0f16c045fbc6bb37f6591e90e03c23fadfa8268f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disconnectOnSessionTimeout")
    def disconnect_on_session_timeout(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disconnectOnSessionTimeout"))

    @disconnect_on_session_timeout.setter
    def disconnect_on_session_timeout(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8428d57f3a05ebaca6a7f837c114e58bb2a72a530d1d837b603e6e4553f79ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disconnectOnSessionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsServers")
    def dns_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsServers"))

    @dns_servers.setter
    def dns_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6592e709edae5fdd4024815c9df0a8fb25874ab45fccc31bc4cd57fadb178d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointIpAddressType")
    def endpoint_ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointIpAddressType"))

    @endpoint_ip_address_type.setter
    def endpoint_ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f09ec2449e01b4078d35267902b2e1ecb137c95d1169b45694f13115dfe5ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointIpAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133a29dd53881373079021a3758417b309d985a5d91c27758b8c804be8083f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac65b72acd3fdef4a34c273d36aef0157dd787fdae9e29be5292ec400ef4fe3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fbe6adcb0073e519756670d67f1acf9a805417fe99c4db8f14e84fcaaa920fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selfServicePortal")
    def self_service_portal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfServicePortal"))

    @self_service_portal.setter
    def self_service_portal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d16caabe9537819c60c0dd62368a12ea64eb1d4698fc5620021745ff729b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selfServicePortal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverCertificateArn")
    def server_certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverCertificateArn"))

    @server_certificate_arn.setter
    def server_certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb27e5b84559e79282dd6887d513649673bc734b7f07a28d8add750177ba9b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCertificateArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTimeoutHours")
    def session_timeout_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionTimeoutHours"))

    @session_timeout_hours.setter
    def session_timeout_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__801ac60419c81726e53a4c87e74a27249efe18e73b05492c77ac5045526fbf0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTimeoutHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="splitTunnel")
    def split_tunnel(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "splitTunnel"))

    @split_tunnel.setter
    def split_tunnel(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d7eea71e980e83d0a9209798b46423c97683aab9afea0ccc522a5bb2c974ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "splitTunnel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70434b7873618973b28c2ac6324ff2e5585971e62c99403be83434b9b7d1fc24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c780af4d5de516c0549c94a18bb8ffbec9510506228eb9b13cf7d5f838d61ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trafficIpAddressType")
    def traffic_ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trafficIpAddressType"))

    @traffic_ip_address_type.setter
    def traffic_ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b3e551a721c4a72551bfc9f1107d23a35012f7309fdf1e5c745ade8091425e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trafficIpAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transportProtocol")
    def transport_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transportProtocol"))

    @transport_protocol.setter
    def transport_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24e794dee54309572177bce94233e6448100d98842e8a38f54c1236b2626882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transportProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507ac394839afc89e7bd35a49914fe38a7d2694b14aeed19946466031cf2eef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnPort")
    def vpn_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vpnPort"))

    @vpn_port.setter
    def vpn_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b599c507713641f68a937de9078098866ef06eb468d02b6130c9f2f4e5779f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnPort", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointAuthenticationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "active_directory_id": "activeDirectoryId",
        "root_certificate_chain_arn": "rootCertificateChainArn",
        "saml_provider_arn": "samlProviderArn",
        "self_service_saml_provider_arn": "selfServiceSamlProviderArn",
    },
)
class Ec2ClientVpnEndpointAuthenticationOptions:
    def __init__(
        self,
        *,
        type: builtins.str,
        active_directory_id: typing.Optional[builtins.str] = None,
        root_certificate_chain_arn: typing.Optional[builtins.str] = None,
        saml_provider_arn: typing.Optional[builtins.str] = None,
        self_service_saml_provider_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#type Ec2ClientVpnEndpoint#type}.
        :param active_directory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#active_directory_id Ec2ClientVpnEndpoint#active_directory_id}.
        :param root_certificate_chain_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#root_certificate_chain_arn Ec2ClientVpnEndpoint#root_certificate_chain_arn}.
        :param saml_provider_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#saml_provider_arn Ec2ClientVpnEndpoint#saml_provider_arn}.
        :param self_service_saml_provider_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#self_service_saml_provider_arn Ec2ClientVpnEndpoint#self_service_saml_provider_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d92b4c33fc0bd976252341657b2f2d430937257821128cacae63e42095a622d)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument active_directory_id", value=active_directory_id, expected_type=type_hints["active_directory_id"])
            check_type(argname="argument root_certificate_chain_arn", value=root_certificate_chain_arn, expected_type=type_hints["root_certificate_chain_arn"])
            check_type(argname="argument saml_provider_arn", value=saml_provider_arn, expected_type=type_hints["saml_provider_arn"])
            check_type(argname="argument self_service_saml_provider_arn", value=self_service_saml_provider_arn, expected_type=type_hints["self_service_saml_provider_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if active_directory_id is not None:
            self._values["active_directory_id"] = active_directory_id
        if root_certificate_chain_arn is not None:
            self._values["root_certificate_chain_arn"] = root_certificate_chain_arn
        if saml_provider_arn is not None:
            self._values["saml_provider_arn"] = saml_provider_arn
        if self_service_saml_provider_arn is not None:
            self._values["self_service_saml_provider_arn"] = self_service_saml_provider_arn

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#type Ec2ClientVpnEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_directory_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#active_directory_id Ec2ClientVpnEndpoint#active_directory_id}.'''
        result = self._values.get("active_directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_certificate_chain_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#root_certificate_chain_arn Ec2ClientVpnEndpoint#root_certificate_chain_arn}.'''
        result = self._values.get("root_certificate_chain_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_provider_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#saml_provider_arn Ec2ClientVpnEndpoint#saml_provider_arn}.'''
        result = self._values.get("saml_provider_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def self_service_saml_provider_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#self_service_saml_provider_arn Ec2ClientVpnEndpoint#self_service_saml_provider_arn}.'''
        result = self._values.get("self_service_saml_provider_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2ClientVpnEndpointAuthenticationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ec2ClientVpnEndpointAuthenticationOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointAuthenticationOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93a5b6f77a9d5bedc1861c648ff77f49a36b9fd6c9acaa984fe34f83963fc169)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Ec2ClientVpnEndpointAuthenticationOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebff868510b33179f917d421520a237a8ea370db241db865fe9a86570320b5db)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Ec2ClientVpnEndpointAuthenticationOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2247e99fbe06134ac74c7b4ae0704fb07db918e1ae002d8cf6bdded7ea70f5fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8564965acdf2170878e366d81ebc141c14892f4dc630a9f84cde7ed267e4bf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba13d75424f1f0661a97fcf42ed9c395ce63a90a745522cd36c2a41bdf6082a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2ClientVpnEndpointAuthenticationOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2ClientVpnEndpointAuthenticationOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2ClientVpnEndpointAuthenticationOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f4066d6fa05d404c4d02752e4422a66bdeaf88837b31944c4ef4645285370c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Ec2ClientVpnEndpointAuthenticationOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointAuthenticationOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b67ec33598488f206ffd88c73229e2a3058b639b86f62a41ef77bd9dde83f807)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetActiveDirectoryId")
    def reset_active_directory_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectoryId", []))

    @jsii.member(jsii_name="resetRootCertificateChainArn")
    def reset_root_certificate_chain_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootCertificateChainArn", []))

    @jsii.member(jsii_name="resetSamlProviderArn")
    def reset_saml_provider_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamlProviderArn", []))

    @jsii.member(jsii_name="resetSelfServiceSamlProviderArn")
    def reset_self_service_saml_provider_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfServiceSamlProviderArn", []))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryIdInput")
    def active_directory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeDirectoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="rootCertificateChainArnInput")
    def root_certificate_chain_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootCertificateChainArnInput"))

    @builtins.property
    @jsii.member(jsii_name="samlProviderArnInput")
    def saml_provider_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "samlProviderArnInput"))

    @builtins.property
    @jsii.member(jsii_name="selfServiceSamlProviderArnInput")
    def self_service_saml_provider_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selfServiceSamlProviderArnInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryId")
    def active_directory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeDirectoryId"))

    @active_directory_id.setter
    def active_directory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cad43102a07b432701822927e1bacf45553abe3d51dd01f2d5fcb6513a20650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootCertificateChainArn")
    def root_certificate_chain_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootCertificateChainArn"))

    @root_certificate_chain_arn.setter
    def root_certificate_chain_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c754b903e2463bc33542fc744d48533408664e25f7b6ad4c152cb36bb8b49a2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootCertificateChainArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samlProviderArn")
    def saml_provider_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "samlProviderArn"))

    @saml_provider_arn.setter
    def saml_provider_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d26fc6bb790a408933b2516f626a8e7986c2c1213649a046ef0cc5f1163f0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlProviderArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selfServiceSamlProviderArn")
    def self_service_saml_provider_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfServiceSamlProviderArn"))

    @self_service_saml_provider_arn.setter
    def self_service_saml_provider_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed27eaa3c7ea1db2e7883ca7b19fcba60d727b555773cd49866d0edb9229bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selfServiceSamlProviderArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c2e65a46d621b09dcc37e541ac9c8248c2df945ef5c16a198d53ad14314e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2ClientVpnEndpointAuthenticationOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2ClientVpnEndpointAuthenticationOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2ClientVpnEndpointAuthenticationOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f880b4620ba21069406d49520c28f9aa19ed7ddfdb63cb6c10e543b3bca4e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointClientConnectOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "lambda_function_arn": "lambdaFunctionArn"},
)
class Ec2ClientVpnEndpointClientConnectOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lambda_function_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enabled Ec2ClientVpnEndpoint#enabled}.
        :param lambda_function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#lambda_function_arn Ec2ClientVpnEndpoint#lambda_function_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f80d66cf2feb972e400e1aacac54ac1b45c83b9667c6000a08a34c369e7e2c8)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument lambda_function_arn", value=lambda_function_arn, expected_type=type_hints["lambda_function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if lambda_function_arn is not None:
            self._values["lambda_function_arn"] = lambda_function_arn

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enabled Ec2ClientVpnEndpoint#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lambda_function_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#lambda_function_arn Ec2ClientVpnEndpoint#lambda_function_arn}.'''
        result = self._values.get("lambda_function_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2ClientVpnEndpointClientConnectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ec2ClientVpnEndpointClientConnectOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointClientConnectOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2aa8ccd7eb2eed3b028a730c00b4442f2289f5bdf5709189bf740ad71c477893)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLambdaFunctionArn")
    def reset_lambda_function_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaFunctionArn", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionArnInput")
    def lambda_function_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaFunctionArnInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a312eced09f98fb2ffb5cba2e6963ff3b105cb7d866a364cf6dac4129c4fa0d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionArn")
    def lambda_function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaFunctionArn"))

    @lambda_function_arn.setter
    def lambda_function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5951c6fc800e9d9a90fd1f042370c682ca09d4e3a03f3fb77fbfca31ae5b5e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaFunctionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Ec2ClientVpnEndpointClientConnectOptions]:
        return typing.cast(typing.Optional[Ec2ClientVpnEndpointClientConnectOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Ec2ClientVpnEndpointClientConnectOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6007ea0ed02c4bf3d48091c48f3660f470d007e60888eb4bc5c3e83a90a7cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointClientLoginBannerOptions",
    jsii_struct_bases=[],
    name_mapping={"banner_text": "bannerText", "enabled": "enabled"},
)
class Ec2ClientVpnEndpointClientLoginBannerOptions:
    def __init__(
        self,
        *,
        banner_text: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param banner_text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#banner_text Ec2ClientVpnEndpoint#banner_text}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enabled Ec2ClientVpnEndpoint#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec44007e4dbd4db5ff9ecafc04b269d6defe4a62c56f7ca050f8102dcc0acea0)
            check_type(argname="argument banner_text", value=banner_text, expected_type=type_hints["banner_text"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if banner_text is not None:
            self._values["banner_text"] = banner_text
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def banner_text(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#banner_text Ec2ClientVpnEndpoint#banner_text}.'''
        result = self._values.get("banner_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enabled Ec2ClientVpnEndpoint#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2ClientVpnEndpointClientLoginBannerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ec2ClientVpnEndpointClientLoginBannerOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointClientLoginBannerOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0b93def3ee3f6077a16b938b949b3189eab794569b17a2114fdc0b643035886)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBannerText")
    def reset_banner_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBannerText", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="bannerTextInput")
    def banner_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bannerTextInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="bannerText")
    def banner_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bannerText"))

    @banner_text.setter
    def banner_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6749999ccc93d9c5da9ca4d9703c04395bf3ec626e76b389f15c08aa2ab83e0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bannerText", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__64cbc5ade6a0163e00a4debd00505ced92aad37f63bf1ceb9114aa512a579556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Ec2ClientVpnEndpointClientLoginBannerOptions]:
        return typing.cast(typing.Optional[Ec2ClientVpnEndpointClientLoginBannerOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Ec2ClientVpnEndpointClientLoginBannerOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__decba8541070dd947077fb020e9db226d99acac6359c55f3e4c615fea7b2a585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointClientRouteEnforcementOptions",
    jsii_struct_bases=[],
    name_mapping={"enforced": "enforced"},
)
class Ec2ClientVpnEndpointClientRouteEnforcementOptions:
    def __init__(
        self,
        *,
        enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enforced: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enforced Ec2ClientVpnEndpoint#enforced}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b9b064e3bd3d537ffd4d4754d4e5a7333393ab63db4da37172e5757b60f217d)
            check_type(argname="argument enforced", value=enforced, expected_type=type_hints["enforced"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enforced is not None:
            self._values["enforced"] = enforced

    @builtins.property
    def enforced(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enforced Ec2ClientVpnEndpoint#enforced}.'''
        result = self._values.get("enforced")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2ClientVpnEndpointClientRouteEnforcementOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ec2ClientVpnEndpointClientRouteEnforcementOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointClientRouteEnforcementOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93787094daa291b5f75eadba111c4edaa38fa2f57b194f43bc659d478dc4a95a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnforced")
    def reset_enforced(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforced", []))

    @builtins.property
    @jsii.member(jsii_name="enforcedInput")
    def enforced_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforcedInput"))

    @builtins.property
    @jsii.member(jsii_name="enforced")
    def enforced(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforced"))

    @enforced.setter
    def enforced(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e2d76bc20b88ca440c5400d82c0ab4857a6a7760f127bbfb3035ed9e3dff65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforced", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Ec2ClientVpnEndpointClientRouteEnforcementOptions]:
        return typing.cast(typing.Optional[Ec2ClientVpnEndpointClientRouteEnforcementOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Ec2ClientVpnEndpointClientRouteEnforcementOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97014ddc8112a481be732c141d726ab18e2897f51c852d3c7be2556349e9a6b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "authentication_options": "authenticationOptions",
        "connection_log_options": "connectionLogOptions",
        "server_certificate_arn": "serverCertificateArn",
        "client_cidr_block": "clientCidrBlock",
        "client_connect_options": "clientConnectOptions",
        "client_login_banner_options": "clientLoginBannerOptions",
        "client_route_enforcement_options": "clientRouteEnforcementOptions",
        "description": "description",
        "disconnect_on_session_timeout": "disconnectOnSessionTimeout",
        "dns_servers": "dnsServers",
        "endpoint_ip_address_type": "endpointIpAddressType",
        "id": "id",
        "region": "region",
        "security_group_ids": "securityGroupIds",
        "self_service_portal": "selfServicePortal",
        "session_timeout_hours": "sessionTimeoutHours",
        "split_tunnel": "splitTunnel",
        "tags": "tags",
        "tags_all": "tagsAll",
        "traffic_ip_address_type": "trafficIpAddressType",
        "transport_protocol": "transportProtocol",
        "vpc_id": "vpcId",
        "vpn_port": "vpnPort",
    },
)
class Ec2ClientVpnEndpointConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authentication_options: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2ClientVpnEndpointAuthenticationOptions, typing.Dict[builtins.str, typing.Any]]]],
        connection_log_options: typing.Union["Ec2ClientVpnEndpointConnectionLogOptions", typing.Dict[builtins.str, typing.Any]],
        server_certificate_arn: builtins.str,
        client_cidr_block: typing.Optional[builtins.str] = None,
        client_connect_options: typing.Optional[typing.Union[Ec2ClientVpnEndpointClientConnectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        client_login_banner_options: typing.Optional[typing.Union[Ec2ClientVpnEndpointClientLoginBannerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        client_route_enforcement_options: typing.Optional[typing.Union[Ec2ClientVpnEndpointClientRouteEnforcementOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disconnect_on_session_timeout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        endpoint_ip_address_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        self_service_portal: typing.Optional[builtins.str] = None,
        session_timeout_hours: typing.Optional[jsii.Number] = None,
        split_tunnel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        traffic_ip_address_type: typing.Optional[builtins.str] = None,
        transport_protocol: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        vpn_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authentication_options: authentication_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#authentication_options Ec2ClientVpnEndpoint#authentication_options}
        :param connection_log_options: connection_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#connection_log_options Ec2ClientVpnEndpoint#connection_log_options}
        :param server_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#server_certificate_arn Ec2ClientVpnEndpoint#server_certificate_arn}.
        :param client_cidr_block: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_cidr_block Ec2ClientVpnEndpoint#client_cidr_block}.
        :param client_connect_options: client_connect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_connect_options Ec2ClientVpnEndpoint#client_connect_options}
        :param client_login_banner_options: client_login_banner_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_login_banner_options Ec2ClientVpnEndpoint#client_login_banner_options}
        :param client_route_enforcement_options: client_route_enforcement_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_route_enforcement_options Ec2ClientVpnEndpoint#client_route_enforcement_options}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#description Ec2ClientVpnEndpoint#description}.
        :param disconnect_on_session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#disconnect_on_session_timeout Ec2ClientVpnEndpoint#disconnect_on_session_timeout}.
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#dns_servers Ec2ClientVpnEndpoint#dns_servers}.
        :param endpoint_ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#endpoint_ip_address_type Ec2ClientVpnEndpoint#endpoint_ip_address_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#id Ec2ClientVpnEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#region Ec2ClientVpnEndpoint#region}
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#security_group_ids Ec2ClientVpnEndpoint#security_group_ids}.
        :param self_service_portal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#self_service_portal Ec2ClientVpnEndpoint#self_service_portal}.
        :param session_timeout_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#session_timeout_hours Ec2ClientVpnEndpoint#session_timeout_hours}.
        :param split_tunnel: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#split_tunnel Ec2ClientVpnEndpoint#split_tunnel}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#tags Ec2ClientVpnEndpoint#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#tags_all Ec2ClientVpnEndpoint#tags_all}.
        :param traffic_ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#traffic_ip_address_type Ec2ClientVpnEndpoint#traffic_ip_address_type}.
        :param transport_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#transport_protocol Ec2ClientVpnEndpoint#transport_protocol}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#vpc_id Ec2ClientVpnEndpoint#vpc_id}.
        :param vpn_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#vpn_port Ec2ClientVpnEndpoint#vpn_port}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(connection_log_options, dict):
            connection_log_options = Ec2ClientVpnEndpointConnectionLogOptions(**connection_log_options)
        if isinstance(client_connect_options, dict):
            client_connect_options = Ec2ClientVpnEndpointClientConnectOptions(**client_connect_options)
        if isinstance(client_login_banner_options, dict):
            client_login_banner_options = Ec2ClientVpnEndpointClientLoginBannerOptions(**client_login_banner_options)
        if isinstance(client_route_enforcement_options, dict):
            client_route_enforcement_options = Ec2ClientVpnEndpointClientRouteEnforcementOptions(**client_route_enforcement_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca63e1fe0e5357e7affe71291b9da1c332290ac84dcbb0c7acc0296e73523727)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authentication_options", value=authentication_options, expected_type=type_hints["authentication_options"])
            check_type(argname="argument connection_log_options", value=connection_log_options, expected_type=type_hints["connection_log_options"])
            check_type(argname="argument server_certificate_arn", value=server_certificate_arn, expected_type=type_hints["server_certificate_arn"])
            check_type(argname="argument client_cidr_block", value=client_cidr_block, expected_type=type_hints["client_cidr_block"])
            check_type(argname="argument client_connect_options", value=client_connect_options, expected_type=type_hints["client_connect_options"])
            check_type(argname="argument client_login_banner_options", value=client_login_banner_options, expected_type=type_hints["client_login_banner_options"])
            check_type(argname="argument client_route_enforcement_options", value=client_route_enforcement_options, expected_type=type_hints["client_route_enforcement_options"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disconnect_on_session_timeout", value=disconnect_on_session_timeout, expected_type=type_hints["disconnect_on_session_timeout"])
            check_type(argname="argument dns_servers", value=dns_servers, expected_type=type_hints["dns_servers"])
            check_type(argname="argument endpoint_ip_address_type", value=endpoint_ip_address_type, expected_type=type_hints["endpoint_ip_address_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument self_service_portal", value=self_service_portal, expected_type=type_hints["self_service_portal"])
            check_type(argname="argument session_timeout_hours", value=session_timeout_hours, expected_type=type_hints["session_timeout_hours"])
            check_type(argname="argument split_tunnel", value=split_tunnel, expected_type=type_hints["split_tunnel"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument traffic_ip_address_type", value=traffic_ip_address_type, expected_type=type_hints["traffic_ip_address_type"])
            check_type(argname="argument transport_protocol", value=transport_protocol, expected_type=type_hints["transport_protocol"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument vpn_port", value=vpn_port, expected_type=type_hints["vpn_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_options": authentication_options,
            "connection_log_options": connection_log_options,
            "server_certificate_arn": server_certificate_arn,
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
        if client_cidr_block is not None:
            self._values["client_cidr_block"] = client_cidr_block
        if client_connect_options is not None:
            self._values["client_connect_options"] = client_connect_options
        if client_login_banner_options is not None:
            self._values["client_login_banner_options"] = client_login_banner_options
        if client_route_enforcement_options is not None:
            self._values["client_route_enforcement_options"] = client_route_enforcement_options
        if description is not None:
            self._values["description"] = description
        if disconnect_on_session_timeout is not None:
            self._values["disconnect_on_session_timeout"] = disconnect_on_session_timeout
        if dns_servers is not None:
            self._values["dns_servers"] = dns_servers
        if endpoint_ip_address_type is not None:
            self._values["endpoint_ip_address_type"] = endpoint_ip_address_type
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if self_service_portal is not None:
            self._values["self_service_portal"] = self_service_portal
        if session_timeout_hours is not None:
            self._values["session_timeout_hours"] = session_timeout_hours
        if split_tunnel is not None:
            self._values["split_tunnel"] = split_tunnel
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if traffic_ip_address_type is not None:
            self._values["traffic_ip_address_type"] = traffic_ip_address_type
        if transport_protocol is not None:
            self._values["transport_protocol"] = transport_protocol
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id
        if vpn_port is not None:
            self._values["vpn_port"] = vpn_port

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
    def authentication_options(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2ClientVpnEndpointAuthenticationOptions]]:
        '''authentication_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#authentication_options Ec2ClientVpnEndpoint#authentication_options}
        '''
        result = self._values.get("authentication_options")
        assert result is not None, "Required property 'authentication_options' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2ClientVpnEndpointAuthenticationOptions]], result)

    @builtins.property
    def connection_log_options(self) -> "Ec2ClientVpnEndpointConnectionLogOptions":
        '''connection_log_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#connection_log_options Ec2ClientVpnEndpoint#connection_log_options}
        '''
        result = self._values.get("connection_log_options")
        assert result is not None, "Required property 'connection_log_options' is missing"
        return typing.cast("Ec2ClientVpnEndpointConnectionLogOptions", result)

    @builtins.property
    def server_certificate_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#server_certificate_arn Ec2ClientVpnEndpoint#server_certificate_arn}.'''
        result = self._values.get("server_certificate_arn")
        assert result is not None, "Required property 'server_certificate_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_cidr_block(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_cidr_block Ec2ClientVpnEndpoint#client_cidr_block}.'''
        result = self._values.get("client_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_connect_options(
        self,
    ) -> typing.Optional[Ec2ClientVpnEndpointClientConnectOptions]:
        '''client_connect_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_connect_options Ec2ClientVpnEndpoint#client_connect_options}
        '''
        result = self._values.get("client_connect_options")
        return typing.cast(typing.Optional[Ec2ClientVpnEndpointClientConnectOptions], result)

    @builtins.property
    def client_login_banner_options(
        self,
    ) -> typing.Optional[Ec2ClientVpnEndpointClientLoginBannerOptions]:
        '''client_login_banner_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_login_banner_options Ec2ClientVpnEndpoint#client_login_banner_options}
        '''
        result = self._values.get("client_login_banner_options")
        return typing.cast(typing.Optional[Ec2ClientVpnEndpointClientLoginBannerOptions], result)

    @builtins.property
    def client_route_enforcement_options(
        self,
    ) -> typing.Optional[Ec2ClientVpnEndpointClientRouteEnforcementOptions]:
        '''client_route_enforcement_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#client_route_enforcement_options Ec2ClientVpnEndpoint#client_route_enforcement_options}
        '''
        result = self._values.get("client_route_enforcement_options")
        return typing.cast(typing.Optional[Ec2ClientVpnEndpointClientRouteEnforcementOptions], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#description Ec2ClientVpnEndpoint#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disconnect_on_session_timeout(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#disconnect_on_session_timeout Ec2ClientVpnEndpoint#disconnect_on_session_timeout}.'''
        result = self._values.get("disconnect_on_session_timeout")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#dns_servers Ec2ClientVpnEndpoint#dns_servers}.'''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def endpoint_ip_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#endpoint_ip_address_type Ec2ClientVpnEndpoint#endpoint_ip_address_type}.'''
        result = self._values.get("endpoint_ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#id Ec2ClientVpnEndpoint#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#region Ec2ClientVpnEndpoint#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#security_group_ids Ec2ClientVpnEndpoint#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def self_service_portal(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#self_service_portal Ec2ClientVpnEndpoint#self_service_portal}.'''
        result = self._values.get("self_service_portal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_timeout_hours(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#session_timeout_hours Ec2ClientVpnEndpoint#session_timeout_hours}.'''
        result = self._values.get("session_timeout_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def split_tunnel(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#split_tunnel Ec2ClientVpnEndpoint#split_tunnel}.'''
        result = self._values.get("split_tunnel")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#tags Ec2ClientVpnEndpoint#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#tags_all Ec2ClientVpnEndpoint#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def traffic_ip_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#traffic_ip_address_type Ec2ClientVpnEndpoint#traffic_ip_address_type}.'''
        result = self._values.get("traffic_ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transport_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#transport_protocol Ec2ClientVpnEndpoint#transport_protocol}.'''
        result = self._values.get("transport_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#vpc_id Ec2ClientVpnEndpoint#vpc_id}.'''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#vpn_port Ec2ClientVpnEndpoint#vpn_port}.'''
        result = self._values.get("vpn_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2ClientVpnEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointConnectionLogOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "cloudwatch_log_group": "cloudwatchLogGroup",
        "cloudwatch_log_stream": "cloudwatchLogStream",
    },
)
class Ec2ClientVpnEndpointConnectionLogOptions:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cloudwatch_log_group: typing.Optional[builtins.str] = None,
        cloudwatch_log_stream: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enabled Ec2ClientVpnEndpoint#enabled}.
        :param cloudwatch_log_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#cloudwatch_log_group Ec2ClientVpnEndpoint#cloudwatch_log_group}.
        :param cloudwatch_log_stream: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#cloudwatch_log_stream Ec2ClientVpnEndpoint#cloudwatch_log_stream}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e8a9a9452530e4024f939f25a655de0699a59863838c913bf801bef3033313)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument cloudwatch_log_group", value=cloudwatch_log_group, expected_type=type_hints["cloudwatch_log_group"])
            check_type(argname="argument cloudwatch_log_stream", value=cloudwatch_log_stream, expected_type=type_hints["cloudwatch_log_stream"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if cloudwatch_log_group is not None:
            self._values["cloudwatch_log_group"] = cloudwatch_log_group
        if cloudwatch_log_stream is not None:
            self._values["cloudwatch_log_stream"] = cloudwatch_log_stream

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#enabled Ec2ClientVpnEndpoint#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def cloudwatch_log_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#cloudwatch_log_group Ec2ClientVpnEndpoint#cloudwatch_log_group}.'''
        result = self._values.get("cloudwatch_log_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatch_log_stream(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ec2_client_vpn_endpoint#cloudwatch_log_stream Ec2ClientVpnEndpoint#cloudwatch_log_stream}.'''
        result = self._values.get("cloudwatch_log_stream")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2ClientVpnEndpointConnectionLogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ec2ClientVpnEndpointConnectionLogOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ec2ClientVpnEndpoint.Ec2ClientVpnEndpointConnectionLogOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccd44489ddbc9ea567cf4b0910c0fe4b574d869fa6f11dc2a996aa0d30868782)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCloudwatchLogGroup")
    def reset_cloudwatch_log_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogGroup", []))

    @jsii.member(jsii_name="resetCloudwatchLogStream")
    def reset_cloudwatch_log_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogStream", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogGroupInput")
    def cloudwatch_log_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchLogGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogStreamInput")
    def cloudwatch_log_stream_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchLogStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogGroup")
    def cloudwatch_log_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchLogGroup"))

    @cloudwatch_log_group.setter
    def cloudwatch_log_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98c52b2b1c13448e51bec526d291af38c463a286e46a1d03b5948feaa43d0cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchLogGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogStream")
    def cloudwatch_log_stream(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchLogStream"))

    @cloudwatch_log_stream.setter
    def cloudwatch_log_stream(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bdb25757e6a7eaca60ae02730d2c6da7baf4d886dfc78240bad366d730c9e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchLogStream", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__2b7c94e98b38e6c430228d054221d935c8ac527f1d53e1e681db8f9443c9db55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Ec2ClientVpnEndpointConnectionLogOptions]:
        return typing.cast(typing.Optional[Ec2ClientVpnEndpointConnectionLogOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Ec2ClientVpnEndpointConnectionLogOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5692f2a0ca39b86720db3f239cf97214ffb9a419dd145ecb68f1d361b2bb368d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Ec2ClientVpnEndpoint",
    "Ec2ClientVpnEndpointAuthenticationOptions",
    "Ec2ClientVpnEndpointAuthenticationOptionsList",
    "Ec2ClientVpnEndpointAuthenticationOptionsOutputReference",
    "Ec2ClientVpnEndpointClientConnectOptions",
    "Ec2ClientVpnEndpointClientConnectOptionsOutputReference",
    "Ec2ClientVpnEndpointClientLoginBannerOptions",
    "Ec2ClientVpnEndpointClientLoginBannerOptionsOutputReference",
    "Ec2ClientVpnEndpointClientRouteEnforcementOptions",
    "Ec2ClientVpnEndpointClientRouteEnforcementOptionsOutputReference",
    "Ec2ClientVpnEndpointConfig",
    "Ec2ClientVpnEndpointConnectionLogOptions",
    "Ec2ClientVpnEndpointConnectionLogOptionsOutputReference",
]

publication.publish()

def _typecheckingstub__83d873d14a32100666c8ccfdce77e7c229380f4808ded7d01e5de907978fc46f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authentication_options: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2ClientVpnEndpointAuthenticationOptions, typing.Dict[builtins.str, typing.Any]]]],
    connection_log_options: typing.Union[Ec2ClientVpnEndpointConnectionLogOptions, typing.Dict[builtins.str, typing.Any]],
    server_certificate_arn: builtins.str,
    client_cidr_block: typing.Optional[builtins.str] = None,
    client_connect_options: typing.Optional[typing.Union[Ec2ClientVpnEndpointClientConnectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    client_login_banner_options: typing.Optional[typing.Union[Ec2ClientVpnEndpointClientLoginBannerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    client_route_enforcement_options: typing.Optional[typing.Union[Ec2ClientVpnEndpointClientRouteEnforcementOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disconnect_on_session_timeout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    endpoint_ip_address_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    self_service_portal: typing.Optional[builtins.str] = None,
    session_timeout_hours: typing.Optional[jsii.Number] = None,
    split_tunnel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    traffic_ip_address_type: typing.Optional[builtins.str] = None,
    transport_protocol: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
    vpn_port: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__56ee7ea21e564f07b05096834e406a8fdfda127f97d9d74229e4ea043f56cd0a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b845f549298dbbe2d91afa09bac89d0d0edacb43618d600a34f8741ede831080(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2ClientVpnEndpointAuthenticationOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d086ecd3c43cc0000f00dde2976875a0308d191ccb217703bd9c6a4f3f3d02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebbc2e22dcb29f33ba06f0f16c045fbc6bb37f6591e90e03c23fadfa8268f8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8428d57f3a05ebaca6a7f837c114e58bb2a72a530d1d837b603e6e4553f79ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6592e709edae5fdd4024815c9df0a8fb25874ab45fccc31bc4cd57fadb178d2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f09ec2449e01b4078d35267902b2e1ecb137c95d1169b45694f13115dfe5ff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133a29dd53881373079021a3758417b309d985a5d91c27758b8c804be8083f48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac65b72acd3fdef4a34c273d36aef0157dd787fdae9e29be5292ec400ef4fe3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbe6adcb0073e519756670d67f1acf9a805417fe99c4db8f14e84fcaaa920fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d16caabe9537819c60c0dd62368a12ea64eb1d4698fc5620021745ff729b18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb27e5b84559e79282dd6887d513649673bc734b7f07a28d8add750177ba9b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801ac60419c81726e53a4c87e74a27249efe18e73b05492c77ac5045526fbf0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d7eea71e980e83d0a9209798b46423c97683aab9afea0ccc522a5bb2c974ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70434b7873618973b28c2ac6324ff2e5585971e62c99403be83434b9b7d1fc24(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c780af4d5de516c0549c94a18bb8ffbec9510506228eb9b13cf7d5f838d61ce0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b3e551a721c4a72551bfc9f1107d23a35012f7309fdf1e5c745ade8091425e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24e794dee54309572177bce94233e6448100d98842e8a38f54c1236b2626882(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507ac394839afc89e7bd35a49914fe38a7d2694b14aeed19946466031cf2eef7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b599c507713641f68a937de9078098866ef06eb468d02b6130c9f2f4e5779f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d92b4c33fc0bd976252341657b2f2d430937257821128cacae63e42095a622d(
    *,
    type: builtins.str,
    active_directory_id: typing.Optional[builtins.str] = None,
    root_certificate_chain_arn: typing.Optional[builtins.str] = None,
    saml_provider_arn: typing.Optional[builtins.str] = None,
    self_service_saml_provider_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a5b6f77a9d5bedc1861c648ff77f49a36b9fd6c9acaa984fe34f83963fc169(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebff868510b33179f917d421520a237a8ea370db241db865fe9a86570320b5db(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2247e99fbe06134ac74c7b4ae0704fb07db918e1ae002d8cf6bdded7ea70f5fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8564965acdf2170878e366d81ebc141c14892f4dc630a9f84cde7ed267e4bf2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba13d75424f1f0661a97fcf42ed9c395ce63a90a745522cd36c2a41bdf6082a4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f4066d6fa05d404c4d02752e4422a66bdeaf88837b31944c4ef4645285370c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2ClientVpnEndpointAuthenticationOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67ec33598488f206ffd88c73229e2a3058b639b86f62a41ef77bd9dde83f807(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cad43102a07b432701822927e1bacf45553abe3d51dd01f2d5fcb6513a20650(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c754b903e2463bc33542fc744d48533408664e25f7b6ad4c152cb36bb8b49a2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d26fc6bb790a408933b2516f626a8e7986c2c1213649a046ef0cc5f1163f0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed27eaa3c7ea1db2e7883ca7b19fcba60d727b555773cd49866d0edb9229bab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c2e65a46d621b09dcc37e541ac9c8248c2df945ef5c16a198d53ad14314e90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f880b4620ba21069406d49520c28f9aa19ed7ddfdb63cb6c10e543b3bca4e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2ClientVpnEndpointAuthenticationOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f80d66cf2feb972e400e1aacac54ac1b45c83b9667c6000a08a34c369e7e2c8(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lambda_function_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa8ccd7eb2eed3b028a730c00b4442f2289f5bdf5709189bf740ad71c477893(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a312eced09f98fb2ffb5cba2e6963ff3b105cb7d866a364cf6dac4129c4fa0d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5951c6fc800e9d9a90fd1f042370c682ca09d4e3a03f3fb77fbfca31ae5b5e5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6007ea0ed02c4bf3d48091c48f3660f470d007e60888eb4bc5c3e83a90a7cf8(
    value: typing.Optional[Ec2ClientVpnEndpointClientConnectOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec44007e4dbd4db5ff9ecafc04b269d6defe4a62c56f7ca050f8102dcc0acea0(
    *,
    banner_text: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b93def3ee3f6077a16b938b949b3189eab794569b17a2114fdc0b643035886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6749999ccc93d9c5da9ca4d9703c04395bf3ec626e76b389f15c08aa2ab83e0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cbc5ade6a0163e00a4debd00505ced92aad37f63bf1ceb9114aa512a579556(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__decba8541070dd947077fb020e9db226d99acac6359c55f3e4c615fea7b2a585(
    value: typing.Optional[Ec2ClientVpnEndpointClientLoginBannerOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9b064e3bd3d537ffd4d4754d4e5a7333393ab63db4da37172e5757b60f217d(
    *,
    enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93787094daa291b5f75eadba111c4edaa38fa2f57b194f43bc659d478dc4a95a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e2d76bc20b88ca440c5400d82c0ab4857a6a7760f127bbfb3035ed9e3dff65(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97014ddc8112a481be732c141d726ab18e2897f51c852d3c7be2556349e9a6b7(
    value: typing.Optional[Ec2ClientVpnEndpointClientRouteEnforcementOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca63e1fe0e5357e7affe71291b9da1c332290ac84dcbb0c7acc0296e73523727(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authentication_options: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2ClientVpnEndpointAuthenticationOptions, typing.Dict[builtins.str, typing.Any]]]],
    connection_log_options: typing.Union[Ec2ClientVpnEndpointConnectionLogOptions, typing.Dict[builtins.str, typing.Any]],
    server_certificate_arn: builtins.str,
    client_cidr_block: typing.Optional[builtins.str] = None,
    client_connect_options: typing.Optional[typing.Union[Ec2ClientVpnEndpointClientConnectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    client_login_banner_options: typing.Optional[typing.Union[Ec2ClientVpnEndpointClientLoginBannerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    client_route_enforcement_options: typing.Optional[typing.Union[Ec2ClientVpnEndpointClientRouteEnforcementOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disconnect_on_session_timeout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    endpoint_ip_address_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    self_service_portal: typing.Optional[builtins.str] = None,
    session_timeout_hours: typing.Optional[jsii.Number] = None,
    split_tunnel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    traffic_ip_address_type: typing.Optional[builtins.str] = None,
    transport_protocol: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
    vpn_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e8a9a9452530e4024f939f25a655de0699a59863838c913bf801bef3033313(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    cloudwatch_log_group: typing.Optional[builtins.str] = None,
    cloudwatch_log_stream: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd44489ddbc9ea567cf4b0910c0fe4b574d869fa6f11dc2a996aa0d30868782(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98c52b2b1c13448e51bec526d291af38c463a286e46a1d03b5948feaa43d0cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bdb25757e6a7eaca60ae02730d2c6da7baf4d886dfc78240bad366d730c9e95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7c94e98b38e6c430228d054221d935c8ac527f1d53e1e681db8f9443c9db55(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5692f2a0ca39b86720db3f239cf97214ffb9a419dd145ecb68f1d361b2bb368d(
    value: typing.Optional[Ec2ClientVpnEndpointConnectionLogOptions],
) -> None:
    """Type checking stubs"""
    pass
