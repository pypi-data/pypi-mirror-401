r'''
# `aws_vpn_connection`

Refer to the Terraform Registry for docs: [`aws_vpn_connection`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection).
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


class VpnConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection aws_vpn_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        customer_gateway_id: builtins.str,
        type: builtins.str,
        enable_acceleration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        local_ipv6_network_cidr: typing.Optional[builtins.str] = None,
        outside_ip_address_type: typing.Optional[builtins.str] = None,
        preshared_key_storage: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        remote_ipv6_network_cidr: typing.Optional[builtins.str] = None,
        static_routes_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transit_gateway_id: typing.Optional[builtins.str] = None,
        transport_transit_gateway_attachment_id: typing.Optional[builtins.str] = None,
        tunnel1_dpd_timeout_action: typing.Optional[builtins.str] = None,
        tunnel1_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel1_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_inside_cidr: typing.Optional[builtins.str] = None,
        tunnel1_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
        tunnel1_log_options: typing.Optional[typing.Union["VpnConnectionTunnel1LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel1_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel1_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel1_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_preshared_key: typing.Optional[builtins.str] = None,
        tunnel1_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
        tunnel1_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_replay_window_size: typing.Optional[jsii.Number] = None,
        tunnel1_startup_action: typing.Optional[builtins.str] = None,
        tunnel2_dpd_timeout_action: typing.Optional[builtins.str] = None,
        tunnel2_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel2_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_inside_cidr: typing.Optional[builtins.str] = None,
        tunnel2_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
        tunnel2_log_options: typing.Optional[typing.Union["VpnConnectionTunnel2LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel2_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel2_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel2_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_preshared_key: typing.Optional[builtins.str] = None,
        tunnel2_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
        tunnel2_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_replay_window_size: typing.Optional[jsii.Number] = None,
        tunnel2_startup_action: typing.Optional[builtins.str] = None,
        tunnel_bandwidth: typing.Optional[builtins.str] = None,
        tunnel_inside_ip_version: typing.Optional[builtins.str] = None,
        vpn_concentrator_id: typing.Optional[builtins.str] = None,
        vpn_gateway_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection aws_vpn_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param customer_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#customer_gateway_id VpnConnection#customer_gateway_id}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#type VpnConnection#type}.
        :param enable_acceleration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#enable_acceleration VpnConnection#enable_acceleration}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#id VpnConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_ipv4_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#local_ipv4_network_cidr VpnConnection#local_ipv4_network_cidr}.
        :param local_ipv6_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#local_ipv6_network_cidr VpnConnection#local_ipv6_network_cidr}.
        :param outside_ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#outside_ip_address_type VpnConnection#outside_ip_address_type}.
        :param preshared_key_storage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#preshared_key_storage VpnConnection#preshared_key_storage}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#region VpnConnection#region}
        :param remote_ipv4_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#remote_ipv4_network_cidr VpnConnection#remote_ipv4_network_cidr}.
        :param remote_ipv6_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#remote_ipv6_network_cidr VpnConnection#remote_ipv6_network_cidr}.
        :param static_routes_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#static_routes_only VpnConnection#static_routes_only}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tags VpnConnection#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tags_all VpnConnection#tags_all}.
        :param transit_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#transit_gateway_id VpnConnection#transit_gateway_id}.
        :param transport_transit_gateway_attachment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#transport_transit_gateway_attachment_id VpnConnection#transport_transit_gateway_attachment_id}.
        :param tunnel1_dpd_timeout_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_action VpnConnection#tunnel1_dpd_timeout_action}.
        :param tunnel1_dpd_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_seconds VpnConnection#tunnel1_dpd_timeout_seconds}.
        :param tunnel1_enable_tunnel_lifecycle_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_enable_tunnel_lifecycle_control VpnConnection#tunnel1_enable_tunnel_lifecycle_control}.
        :param tunnel1_ike_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_ike_versions VpnConnection#tunnel1_ike_versions}.
        :param tunnel1_inside_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_inside_cidr VpnConnection#tunnel1_inside_cidr}.
        :param tunnel1_inside_ipv6_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_inside_ipv6_cidr VpnConnection#tunnel1_inside_ipv6_cidr}.
        :param tunnel1_log_options: tunnel1_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_log_options VpnConnection#tunnel1_log_options}
        :param tunnel1_phase1_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_dh_group_numbers VpnConnection#tunnel1_phase1_dh_group_numbers}.
        :param tunnel1_phase1_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_encryption_algorithms VpnConnection#tunnel1_phase1_encryption_algorithms}.
        :param tunnel1_phase1_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_integrity_algorithms VpnConnection#tunnel1_phase1_integrity_algorithms}.
        :param tunnel1_phase1_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_lifetime_seconds VpnConnection#tunnel1_phase1_lifetime_seconds}.
        :param tunnel1_phase2_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_dh_group_numbers VpnConnection#tunnel1_phase2_dh_group_numbers}.
        :param tunnel1_phase2_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_encryption_algorithms VpnConnection#tunnel1_phase2_encryption_algorithms}.
        :param tunnel1_phase2_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_integrity_algorithms VpnConnection#tunnel1_phase2_integrity_algorithms}.
        :param tunnel1_phase2_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_lifetime_seconds VpnConnection#tunnel1_phase2_lifetime_seconds}.
        :param tunnel1_preshared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_preshared_key VpnConnection#tunnel1_preshared_key}.
        :param tunnel1_rekey_fuzz_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_rekey_fuzz_percentage VpnConnection#tunnel1_rekey_fuzz_percentage}.
        :param tunnel1_rekey_margin_time_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_rekey_margin_time_seconds VpnConnection#tunnel1_rekey_margin_time_seconds}.
        :param tunnel1_replay_window_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_replay_window_size VpnConnection#tunnel1_replay_window_size}.
        :param tunnel1_startup_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_startup_action VpnConnection#tunnel1_startup_action}.
        :param tunnel2_dpd_timeout_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_action VpnConnection#tunnel2_dpd_timeout_action}.
        :param tunnel2_dpd_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_seconds VpnConnection#tunnel2_dpd_timeout_seconds}.
        :param tunnel2_enable_tunnel_lifecycle_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_enable_tunnel_lifecycle_control VpnConnection#tunnel2_enable_tunnel_lifecycle_control}.
        :param tunnel2_ike_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_ike_versions VpnConnection#tunnel2_ike_versions}.
        :param tunnel2_inside_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_inside_cidr VpnConnection#tunnel2_inside_cidr}.
        :param tunnel2_inside_ipv6_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_inside_ipv6_cidr VpnConnection#tunnel2_inside_ipv6_cidr}.
        :param tunnel2_log_options: tunnel2_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_log_options VpnConnection#tunnel2_log_options}
        :param tunnel2_phase1_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_dh_group_numbers VpnConnection#tunnel2_phase1_dh_group_numbers}.
        :param tunnel2_phase1_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_encryption_algorithms VpnConnection#tunnel2_phase1_encryption_algorithms}.
        :param tunnel2_phase1_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_integrity_algorithms VpnConnection#tunnel2_phase1_integrity_algorithms}.
        :param tunnel2_phase1_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_lifetime_seconds VpnConnection#tunnel2_phase1_lifetime_seconds}.
        :param tunnel2_phase2_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_dh_group_numbers VpnConnection#tunnel2_phase2_dh_group_numbers}.
        :param tunnel2_phase2_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_encryption_algorithms VpnConnection#tunnel2_phase2_encryption_algorithms}.
        :param tunnel2_phase2_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_integrity_algorithms VpnConnection#tunnel2_phase2_integrity_algorithms}.
        :param tunnel2_phase2_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_lifetime_seconds VpnConnection#tunnel2_phase2_lifetime_seconds}.
        :param tunnel2_preshared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_preshared_key VpnConnection#tunnel2_preshared_key}.
        :param tunnel2_rekey_fuzz_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_rekey_fuzz_percentage VpnConnection#tunnel2_rekey_fuzz_percentage}.
        :param tunnel2_rekey_margin_time_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_rekey_margin_time_seconds VpnConnection#tunnel2_rekey_margin_time_seconds}.
        :param tunnel2_replay_window_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_replay_window_size VpnConnection#tunnel2_replay_window_size}.
        :param tunnel2_startup_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_startup_action VpnConnection#tunnel2_startup_action}.
        :param tunnel_bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel_bandwidth VpnConnection#tunnel_bandwidth}.
        :param tunnel_inside_ip_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel_inside_ip_version VpnConnection#tunnel_inside_ip_version}.
        :param vpn_concentrator_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#vpn_concentrator_id VpnConnection#vpn_concentrator_id}.
        :param vpn_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#vpn_gateway_id VpnConnection#vpn_gateway_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf5b5bd0f94b6a817dd05cec8e3f23038379303c360bef3445814d8b31bce3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VpnConnectionConfig(
            customer_gateway_id=customer_gateway_id,
            type=type,
            enable_acceleration=enable_acceleration,
            id=id,
            local_ipv4_network_cidr=local_ipv4_network_cidr,
            local_ipv6_network_cidr=local_ipv6_network_cidr,
            outside_ip_address_type=outside_ip_address_type,
            preshared_key_storage=preshared_key_storage,
            region=region,
            remote_ipv4_network_cidr=remote_ipv4_network_cidr,
            remote_ipv6_network_cidr=remote_ipv6_network_cidr,
            static_routes_only=static_routes_only,
            tags=tags,
            tags_all=tags_all,
            transit_gateway_id=transit_gateway_id,
            transport_transit_gateway_attachment_id=transport_transit_gateway_attachment_id,
            tunnel1_dpd_timeout_action=tunnel1_dpd_timeout_action,
            tunnel1_dpd_timeout_seconds=tunnel1_dpd_timeout_seconds,
            tunnel1_enable_tunnel_lifecycle_control=tunnel1_enable_tunnel_lifecycle_control,
            tunnel1_ike_versions=tunnel1_ike_versions,
            tunnel1_inside_cidr=tunnel1_inside_cidr,
            tunnel1_inside_ipv6_cidr=tunnel1_inside_ipv6_cidr,
            tunnel1_log_options=tunnel1_log_options,
            tunnel1_phase1_dh_group_numbers=tunnel1_phase1_dh_group_numbers,
            tunnel1_phase1_encryption_algorithms=tunnel1_phase1_encryption_algorithms,
            tunnel1_phase1_integrity_algorithms=tunnel1_phase1_integrity_algorithms,
            tunnel1_phase1_lifetime_seconds=tunnel1_phase1_lifetime_seconds,
            tunnel1_phase2_dh_group_numbers=tunnel1_phase2_dh_group_numbers,
            tunnel1_phase2_encryption_algorithms=tunnel1_phase2_encryption_algorithms,
            tunnel1_phase2_integrity_algorithms=tunnel1_phase2_integrity_algorithms,
            tunnel1_phase2_lifetime_seconds=tunnel1_phase2_lifetime_seconds,
            tunnel1_preshared_key=tunnel1_preshared_key,
            tunnel1_rekey_fuzz_percentage=tunnel1_rekey_fuzz_percentage,
            tunnel1_rekey_margin_time_seconds=tunnel1_rekey_margin_time_seconds,
            tunnel1_replay_window_size=tunnel1_replay_window_size,
            tunnel1_startup_action=tunnel1_startup_action,
            tunnel2_dpd_timeout_action=tunnel2_dpd_timeout_action,
            tunnel2_dpd_timeout_seconds=tunnel2_dpd_timeout_seconds,
            tunnel2_enable_tunnel_lifecycle_control=tunnel2_enable_tunnel_lifecycle_control,
            tunnel2_ike_versions=tunnel2_ike_versions,
            tunnel2_inside_cidr=tunnel2_inside_cidr,
            tunnel2_inside_ipv6_cidr=tunnel2_inside_ipv6_cidr,
            tunnel2_log_options=tunnel2_log_options,
            tunnel2_phase1_dh_group_numbers=tunnel2_phase1_dh_group_numbers,
            tunnel2_phase1_encryption_algorithms=tunnel2_phase1_encryption_algorithms,
            tunnel2_phase1_integrity_algorithms=tunnel2_phase1_integrity_algorithms,
            tunnel2_phase1_lifetime_seconds=tunnel2_phase1_lifetime_seconds,
            tunnel2_phase2_dh_group_numbers=tunnel2_phase2_dh_group_numbers,
            tunnel2_phase2_encryption_algorithms=tunnel2_phase2_encryption_algorithms,
            tunnel2_phase2_integrity_algorithms=tunnel2_phase2_integrity_algorithms,
            tunnel2_phase2_lifetime_seconds=tunnel2_phase2_lifetime_seconds,
            tunnel2_preshared_key=tunnel2_preshared_key,
            tunnel2_rekey_fuzz_percentage=tunnel2_rekey_fuzz_percentage,
            tunnel2_rekey_margin_time_seconds=tunnel2_rekey_margin_time_seconds,
            tunnel2_replay_window_size=tunnel2_replay_window_size,
            tunnel2_startup_action=tunnel2_startup_action,
            tunnel_bandwidth=tunnel_bandwidth,
            tunnel_inside_ip_version=tunnel_inside_ip_version,
            vpn_concentrator_id=vpn_concentrator_id,
            vpn_gateway_id=vpn_gateway_id,
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
        '''Generates CDKTF code for importing a VpnConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VpnConnection to import.
        :param import_from_id: The id of the existing VpnConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VpnConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcbf9258d7691b9f16e0c348336f1c26ef869ceebed3ca795318fda9652aae0f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTunnel1LogOptions")
    def put_tunnel1_log_options(
        self,
        *,
        cloudwatch_log_options: typing.Optional[typing.Union["VpnConnectionTunnel1LogOptionsCloudwatchLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_options: cloudwatch_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        value = VpnConnectionTunnel1LogOptions(
            cloudwatch_log_options=cloudwatch_log_options
        )

        return typing.cast(None, jsii.invoke(self, "putTunnel1LogOptions", [value]))

    @jsii.member(jsii_name="putTunnel2LogOptions")
    def put_tunnel2_log_options(
        self,
        *,
        cloudwatch_log_options: typing.Optional[typing.Union["VpnConnectionTunnel2LogOptionsCloudwatchLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_options: cloudwatch_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        value = VpnConnectionTunnel2LogOptions(
            cloudwatch_log_options=cloudwatch_log_options
        )

        return typing.cast(None, jsii.invoke(self, "putTunnel2LogOptions", [value]))

    @jsii.member(jsii_name="resetEnableAcceleration")
    def reset_enable_acceleration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAcceleration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocalIpv4NetworkCidr")
    def reset_local_ipv4_network_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalIpv4NetworkCidr", []))

    @jsii.member(jsii_name="resetLocalIpv6NetworkCidr")
    def reset_local_ipv6_network_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalIpv6NetworkCidr", []))

    @jsii.member(jsii_name="resetOutsideIpAddressType")
    def reset_outside_ip_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutsideIpAddressType", []))

    @jsii.member(jsii_name="resetPresharedKeyStorage")
    def reset_preshared_key_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPresharedKeyStorage", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRemoteIpv4NetworkCidr")
    def reset_remote_ipv4_network_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteIpv4NetworkCidr", []))

    @jsii.member(jsii_name="resetRemoteIpv6NetworkCidr")
    def reset_remote_ipv6_network_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteIpv6NetworkCidr", []))

    @jsii.member(jsii_name="resetStaticRoutesOnly")
    def reset_static_routes_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticRoutesOnly", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTransitGatewayId")
    def reset_transit_gateway_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransitGatewayId", []))

    @jsii.member(jsii_name="resetTransportTransitGatewayAttachmentId")
    def reset_transport_transit_gateway_attachment_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransportTransitGatewayAttachmentId", []))

    @jsii.member(jsii_name="resetTunnel1DpdTimeoutAction")
    def reset_tunnel1_dpd_timeout_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1DpdTimeoutAction", []))

    @jsii.member(jsii_name="resetTunnel1DpdTimeoutSeconds")
    def reset_tunnel1_dpd_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1DpdTimeoutSeconds", []))

    @jsii.member(jsii_name="resetTunnel1EnableTunnelLifecycleControl")
    def reset_tunnel1_enable_tunnel_lifecycle_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1EnableTunnelLifecycleControl", []))

    @jsii.member(jsii_name="resetTunnel1IkeVersions")
    def reset_tunnel1_ike_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1IkeVersions", []))

    @jsii.member(jsii_name="resetTunnel1InsideCidr")
    def reset_tunnel1_inside_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1InsideCidr", []))

    @jsii.member(jsii_name="resetTunnel1InsideIpv6Cidr")
    def reset_tunnel1_inside_ipv6_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1InsideIpv6Cidr", []))

    @jsii.member(jsii_name="resetTunnel1LogOptions")
    def reset_tunnel1_log_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1LogOptions", []))

    @jsii.member(jsii_name="resetTunnel1Phase1DhGroupNumbers")
    def reset_tunnel1_phase1_dh_group_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase1DhGroupNumbers", []))

    @jsii.member(jsii_name="resetTunnel1Phase1EncryptionAlgorithms")
    def reset_tunnel1_phase1_encryption_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase1EncryptionAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel1Phase1IntegrityAlgorithms")
    def reset_tunnel1_phase1_integrity_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase1IntegrityAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel1Phase1LifetimeSeconds")
    def reset_tunnel1_phase1_lifetime_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase1LifetimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel1Phase2DhGroupNumbers")
    def reset_tunnel1_phase2_dh_group_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase2DhGroupNumbers", []))

    @jsii.member(jsii_name="resetTunnel1Phase2EncryptionAlgorithms")
    def reset_tunnel1_phase2_encryption_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase2EncryptionAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel1Phase2IntegrityAlgorithms")
    def reset_tunnel1_phase2_integrity_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase2IntegrityAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel1Phase2LifetimeSeconds")
    def reset_tunnel1_phase2_lifetime_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase2LifetimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel1PresharedKey")
    def reset_tunnel1_preshared_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1PresharedKey", []))

    @jsii.member(jsii_name="resetTunnel1RekeyFuzzPercentage")
    def reset_tunnel1_rekey_fuzz_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1RekeyFuzzPercentage", []))

    @jsii.member(jsii_name="resetTunnel1RekeyMarginTimeSeconds")
    def reset_tunnel1_rekey_margin_time_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1RekeyMarginTimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel1ReplayWindowSize")
    def reset_tunnel1_replay_window_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1ReplayWindowSize", []))

    @jsii.member(jsii_name="resetTunnel1StartupAction")
    def reset_tunnel1_startup_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1StartupAction", []))

    @jsii.member(jsii_name="resetTunnel2DpdTimeoutAction")
    def reset_tunnel2_dpd_timeout_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2DpdTimeoutAction", []))

    @jsii.member(jsii_name="resetTunnel2DpdTimeoutSeconds")
    def reset_tunnel2_dpd_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2DpdTimeoutSeconds", []))

    @jsii.member(jsii_name="resetTunnel2EnableTunnelLifecycleControl")
    def reset_tunnel2_enable_tunnel_lifecycle_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2EnableTunnelLifecycleControl", []))

    @jsii.member(jsii_name="resetTunnel2IkeVersions")
    def reset_tunnel2_ike_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2IkeVersions", []))

    @jsii.member(jsii_name="resetTunnel2InsideCidr")
    def reset_tunnel2_inside_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2InsideCidr", []))

    @jsii.member(jsii_name="resetTunnel2InsideIpv6Cidr")
    def reset_tunnel2_inside_ipv6_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2InsideIpv6Cidr", []))

    @jsii.member(jsii_name="resetTunnel2LogOptions")
    def reset_tunnel2_log_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2LogOptions", []))

    @jsii.member(jsii_name="resetTunnel2Phase1DhGroupNumbers")
    def reset_tunnel2_phase1_dh_group_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase1DhGroupNumbers", []))

    @jsii.member(jsii_name="resetTunnel2Phase1EncryptionAlgorithms")
    def reset_tunnel2_phase1_encryption_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase1EncryptionAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel2Phase1IntegrityAlgorithms")
    def reset_tunnel2_phase1_integrity_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase1IntegrityAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel2Phase1LifetimeSeconds")
    def reset_tunnel2_phase1_lifetime_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase1LifetimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel2Phase2DhGroupNumbers")
    def reset_tunnel2_phase2_dh_group_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase2DhGroupNumbers", []))

    @jsii.member(jsii_name="resetTunnel2Phase2EncryptionAlgorithms")
    def reset_tunnel2_phase2_encryption_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase2EncryptionAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel2Phase2IntegrityAlgorithms")
    def reset_tunnel2_phase2_integrity_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase2IntegrityAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel2Phase2LifetimeSeconds")
    def reset_tunnel2_phase2_lifetime_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase2LifetimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel2PresharedKey")
    def reset_tunnel2_preshared_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2PresharedKey", []))

    @jsii.member(jsii_name="resetTunnel2RekeyFuzzPercentage")
    def reset_tunnel2_rekey_fuzz_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2RekeyFuzzPercentage", []))

    @jsii.member(jsii_name="resetTunnel2RekeyMarginTimeSeconds")
    def reset_tunnel2_rekey_margin_time_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2RekeyMarginTimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel2ReplayWindowSize")
    def reset_tunnel2_replay_window_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2ReplayWindowSize", []))

    @jsii.member(jsii_name="resetTunnel2StartupAction")
    def reset_tunnel2_startup_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2StartupAction", []))

    @jsii.member(jsii_name="resetTunnelBandwidth")
    def reset_tunnel_bandwidth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelBandwidth", []))

    @jsii.member(jsii_name="resetTunnelInsideIpVersion")
    def reset_tunnel_inside_ip_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelInsideIpVersion", []))

    @jsii.member(jsii_name="resetVpnConcentratorId")
    def reset_vpn_concentrator_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnConcentratorId", []))

    @jsii.member(jsii_name="resetVpnGatewayId")
    def reset_vpn_gateway_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnGatewayId", []))

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
    @jsii.member(jsii_name="coreNetworkArn")
    def core_network_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coreNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="coreNetworkAttachmentArn")
    def core_network_attachment_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coreNetworkAttachmentArn"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayConfiguration")
    def customer_gateway_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="presharedKeyArn")
    def preshared_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "presharedKeyArn"))

    @builtins.property
    @jsii.member(jsii_name="routes")
    def routes(self) -> "VpnConnectionRoutesList":
        return typing.cast("VpnConnectionRoutesList", jsii.get(self, "routes"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentId"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Address")
    def tunnel1_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1Address"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1BgpAsn")
    def tunnel1_bgp_asn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1BgpAsn"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1BgpHoldtime")
    def tunnel1_bgp_holdtime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1BgpHoldtime"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1CgwInsideAddress")
    def tunnel1_cgw_inside_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1CgwInsideAddress"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1LogOptions")
    def tunnel1_log_options(self) -> "VpnConnectionTunnel1LogOptionsOutputReference":
        return typing.cast("VpnConnectionTunnel1LogOptionsOutputReference", jsii.get(self, "tunnel1LogOptions"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1VgwInsideAddress")
    def tunnel1_vgw_inside_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1VgwInsideAddress"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Address")
    def tunnel2_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2Address"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2BgpAsn")
    def tunnel2_bgp_asn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2BgpAsn"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2BgpHoldtime")
    def tunnel2_bgp_holdtime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2BgpHoldtime"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2CgwInsideAddress")
    def tunnel2_cgw_inside_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2CgwInsideAddress"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2LogOptions")
    def tunnel2_log_options(self) -> "VpnConnectionTunnel2LogOptionsOutputReference":
        return typing.cast("VpnConnectionTunnel2LogOptionsOutputReference", jsii.get(self, "tunnel2LogOptions"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2VgwInsideAddress")
    def tunnel2_vgw_inside_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2VgwInsideAddress"))

    @builtins.property
    @jsii.member(jsii_name="vgwTelemetry")
    def vgw_telemetry(self) -> "VpnConnectionVgwTelemetryList":
        return typing.cast("VpnConnectionVgwTelemetryList", jsii.get(self, "vgwTelemetry"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayIdInput")
    def customer_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAccelerationInput")
    def enable_acceleration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAccelerationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localIpv4NetworkCidrInput")
    def local_ipv4_network_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIpv4NetworkCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="localIpv6NetworkCidrInput")
    def local_ipv6_network_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIpv6NetworkCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="outsideIpAddressTypeInput")
    def outside_ip_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outsideIpAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="presharedKeyStorageInput")
    def preshared_key_storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "presharedKeyStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteIpv4NetworkCidrInput")
    def remote_ipv4_network_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteIpv4NetworkCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteIpv6NetworkCidrInput")
    def remote_ipv6_network_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteIpv6NetworkCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="staticRoutesOnlyInput")
    def static_routes_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "staticRoutesOnlyInput"))

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
    @jsii.member(jsii_name="transitGatewayIdInput")
    def transit_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="transportTransitGatewayAttachmentIdInput")
    def transport_transit_gateway_attachment_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transportTransitGatewayAttachmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1DpdTimeoutActionInput")
    def tunnel1_dpd_timeout_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel1DpdTimeoutActionInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1DpdTimeoutSecondsInput")
    def tunnel1_dpd_timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1DpdTimeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1EnableTunnelLifecycleControlInput")
    def tunnel1_enable_tunnel_lifecycle_control_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tunnel1EnableTunnelLifecycleControlInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1IkeVersionsInput")
    def tunnel1_ike_versions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel1IkeVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1InsideCidrInput")
    def tunnel1_inside_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel1InsideCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1InsideIpv6CidrInput")
    def tunnel1_inside_ipv6_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel1InsideIpv6CidrInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1LogOptionsInput")
    def tunnel1_log_options_input(
        self,
    ) -> typing.Optional["VpnConnectionTunnel1LogOptions"]:
        return typing.cast(typing.Optional["VpnConnectionTunnel1LogOptions"], jsii.get(self, "tunnel1LogOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1DhGroupNumbersInput")
    def tunnel1_phase1_dh_group_numbers_input(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "tunnel1Phase1DhGroupNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1EncryptionAlgorithmsInput")
    def tunnel1_phase1_encryption_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel1Phase1EncryptionAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1IntegrityAlgorithmsInput")
    def tunnel1_phase1_integrity_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel1Phase1IntegrityAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1LifetimeSecondsInput")
    def tunnel1_phase1_lifetime_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1Phase1LifetimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2DhGroupNumbersInput")
    def tunnel1_phase2_dh_group_numbers_input(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "tunnel1Phase2DhGroupNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2EncryptionAlgorithmsInput")
    def tunnel1_phase2_encryption_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel1Phase2EncryptionAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2IntegrityAlgorithmsInput")
    def tunnel1_phase2_integrity_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel1Phase2IntegrityAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2LifetimeSecondsInput")
    def tunnel1_phase2_lifetime_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1Phase2LifetimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1PresharedKeyInput")
    def tunnel1_preshared_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel1PresharedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1RekeyFuzzPercentageInput")
    def tunnel1_rekey_fuzz_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1RekeyFuzzPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1RekeyMarginTimeSecondsInput")
    def tunnel1_rekey_margin_time_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1RekeyMarginTimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1ReplayWindowSizeInput")
    def tunnel1_replay_window_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1ReplayWindowSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1StartupActionInput")
    def tunnel1_startup_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel1StartupActionInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2DpdTimeoutActionInput")
    def tunnel2_dpd_timeout_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel2DpdTimeoutActionInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2DpdTimeoutSecondsInput")
    def tunnel2_dpd_timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2DpdTimeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2EnableTunnelLifecycleControlInput")
    def tunnel2_enable_tunnel_lifecycle_control_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tunnel2EnableTunnelLifecycleControlInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2IkeVersionsInput")
    def tunnel2_ike_versions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel2IkeVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2InsideCidrInput")
    def tunnel2_inside_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel2InsideCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2InsideIpv6CidrInput")
    def tunnel2_inside_ipv6_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel2InsideIpv6CidrInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2LogOptionsInput")
    def tunnel2_log_options_input(
        self,
    ) -> typing.Optional["VpnConnectionTunnel2LogOptions"]:
        return typing.cast(typing.Optional["VpnConnectionTunnel2LogOptions"], jsii.get(self, "tunnel2LogOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1DhGroupNumbersInput")
    def tunnel2_phase1_dh_group_numbers_input(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "tunnel2Phase1DhGroupNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1EncryptionAlgorithmsInput")
    def tunnel2_phase1_encryption_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel2Phase1EncryptionAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1IntegrityAlgorithmsInput")
    def tunnel2_phase1_integrity_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel2Phase1IntegrityAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1LifetimeSecondsInput")
    def tunnel2_phase1_lifetime_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2Phase1LifetimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2DhGroupNumbersInput")
    def tunnel2_phase2_dh_group_numbers_input(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "tunnel2Phase2DhGroupNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2EncryptionAlgorithmsInput")
    def tunnel2_phase2_encryption_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel2Phase2EncryptionAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2IntegrityAlgorithmsInput")
    def tunnel2_phase2_integrity_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel2Phase2IntegrityAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2LifetimeSecondsInput")
    def tunnel2_phase2_lifetime_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2Phase2LifetimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2PresharedKeyInput")
    def tunnel2_preshared_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel2PresharedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2RekeyFuzzPercentageInput")
    def tunnel2_rekey_fuzz_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2RekeyFuzzPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2RekeyMarginTimeSecondsInput")
    def tunnel2_rekey_margin_time_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2RekeyMarginTimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2ReplayWindowSizeInput")
    def tunnel2_replay_window_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2ReplayWindowSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2StartupActionInput")
    def tunnel2_startup_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel2StartupActionInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelBandwidthInput")
    def tunnel_bandwidth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnelBandwidthInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelInsideIpVersionInput")
    def tunnel_inside_ip_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnelInsideIpVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnConcentratorIdInput")
    def vpn_concentrator_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnConcentratorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnGatewayIdInput")
    def vpn_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayId"))

    @customer_gateway_id.setter
    def customer_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82bf7eae2b34786903060a10e663dd69164c40f6dc5306f0a831dfb00d474279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerGatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAcceleration")
    def enable_acceleration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAcceleration"))

    @enable_acceleration.setter
    def enable_acceleration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b9a5c025e15c50d2fbdbf410010363c45dbe54c7e0a8a55703865c4617a33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAcceleration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4013f07f45f0eccca47e62140ba98447d5fea36b2a992f0087cce04aa155f95d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localIpv4NetworkCidr")
    def local_ipv4_network_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localIpv4NetworkCidr"))

    @local_ipv4_network_cidr.setter
    def local_ipv4_network_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf81778b7d69ffa56535657d890e9167d72994f22ee23a5e799e91c8d5e4eef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localIpv4NetworkCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localIpv6NetworkCidr")
    def local_ipv6_network_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localIpv6NetworkCidr"))

    @local_ipv6_network_cidr.setter
    def local_ipv6_network_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf96d4a7c3d2dfbf9e1530584a1b42bcf8489e9359879a1779a97e69c3495960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localIpv6NetworkCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outsideIpAddressType")
    def outside_ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outsideIpAddressType"))

    @outside_ip_address_type.setter
    def outside_ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68ff1a000e7b4d198548f03e3d22df32d78725022a2ffd58ab770afa3bfefae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outsideIpAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="presharedKeyStorage")
    def preshared_key_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "presharedKeyStorage"))

    @preshared_key_storage.setter
    def preshared_key_storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fd8fd10a8b6e9ef77d2203d3e330cdbbc0a953f375386201395a751f6720af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presharedKeyStorage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f1250c365fb5c42d24df7ca903e20c02a78235b329e438de2964eb6eeeb560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteIpv4NetworkCidr")
    def remote_ipv4_network_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteIpv4NetworkCidr"))

    @remote_ipv4_network_cidr.setter
    def remote_ipv4_network_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e3b4a7bf13a092b6a722bd0a4818efbaff620d4b31d72e0f1e4745ae460a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteIpv4NetworkCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteIpv6NetworkCidr")
    def remote_ipv6_network_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteIpv6NetworkCidr"))

    @remote_ipv6_network_cidr.setter
    def remote_ipv6_network_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a974f696313fd5d1e8cfb400ecc52a2736b5f0426ce1d0383bb6c21cdb5466b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteIpv6NetworkCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="staticRoutesOnly")
    def static_routes_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "staticRoutesOnly"))

    @static_routes_only.setter
    def static_routes_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b82d5e2b66992ef1337a867a4059b642ef95186e7240c96868f33d553293850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staticRoutesOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feaeccddc7160b8fb9dee941568492b511c207238e431b3f8f249200d349eea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f28afa51ab99c953afc1054aaa369bc9c53e8a8d10ccefbf9e19f83d33c4c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitGatewayId")
    def transit_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayId"))

    @transit_gateway_id.setter
    def transit_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde333cdf5709927c2ee9a7df680cbb963cf7255fbf2734cfcf9beeb49387c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitGatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transportTransitGatewayAttachmentId")
    def transport_transit_gateway_attachment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transportTransitGatewayAttachmentId"))

    @transport_transit_gateway_attachment_id.setter
    def transport_transit_gateway_attachment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4052dfda7630f80d33873163ffc10115a2b69c62e51d3a62bed046483a8952b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transportTransitGatewayAttachmentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1DpdTimeoutAction")
    def tunnel1_dpd_timeout_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1DpdTimeoutAction"))

    @tunnel1_dpd_timeout_action.setter
    def tunnel1_dpd_timeout_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2e37b8ce5ece52a4b301cbc18a81e07dcb0066911d479beea89ec641735e9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1DpdTimeoutAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1DpdTimeoutSeconds")
    def tunnel1_dpd_timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1DpdTimeoutSeconds"))

    @tunnel1_dpd_timeout_seconds.setter
    def tunnel1_dpd_timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8081f4e5868a4623118985cd0da7abb1c7bec3ec1578fc6bd766ea2997cc924a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1DpdTimeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1EnableTunnelLifecycleControl")
    def tunnel1_enable_tunnel_lifecycle_control(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tunnel1EnableTunnelLifecycleControl"))

    @tunnel1_enable_tunnel_lifecycle_control.setter
    def tunnel1_enable_tunnel_lifecycle_control(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20849a621872c2881a05f2a492230c2ac369360d212f8cfe80862640e174d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1EnableTunnelLifecycleControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1IkeVersions")
    def tunnel1_ike_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel1IkeVersions"))

    @tunnel1_ike_versions.setter
    def tunnel1_ike_versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5530b0c3aa0872741fb50b1c5640c63ac27130be7906a53244eb16647aa3f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1IkeVersions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1InsideCidr")
    def tunnel1_inside_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1InsideCidr"))

    @tunnel1_inside_cidr.setter
    def tunnel1_inside_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b2c7d7d7ea3b4f9720aaaf4d4dfecf6da96593ce63d759c9ab8ff489f17df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1InsideCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1InsideIpv6Cidr")
    def tunnel1_inside_ipv6_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1InsideIpv6Cidr"))

    @tunnel1_inside_ipv6_cidr.setter
    def tunnel1_inside_ipv6_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__582257578120336e7f4d9a1015ea1750285345bfe55a67f569b9314a7171cc6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1InsideIpv6Cidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1DhGroupNumbers")
    def tunnel1_phase1_dh_group_numbers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "tunnel1Phase1DhGroupNumbers"))

    @tunnel1_phase1_dh_group_numbers.setter
    def tunnel1_phase1_dh_group_numbers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d10ff4b1d53d8b91118d2f1893569e4c45ed613bcd361b068b1ec96d02e4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase1DhGroupNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1EncryptionAlgorithms")
    def tunnel1_phase1_encryption_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel1Phase1EncryptionAlgorithms"))

    @tunnel1_phase1_encryption_algorithms.setter
    def tunnel1_phase1_encryption_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5067f4a1faf9460809d79cb741e38f35527eca147859c43d301cbfdf38527dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase1EncryptionAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1IntegrityAlgorithms")
    def tunnel1_phase1_integrity_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel1Phase1IntegrityAlgorithms"))

    @tunnel1_phase1_integrity_algorithms.setter
    def tunnel1_phase1_integrity_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe617d131da79340fe31a5bf67888ab3325c11bead4704b179a317dc21cb1b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase1IntegrityAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1LifetimeSeconds")
    def tunnel1_phase1_lifetime_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1Phase1LifetimeSeconds"))

    @tunnel1_phase1_lifetime_seconds.setter
    def tunnel1_phase1_lifetime_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722854eb09f06751db11f0ca1ed8a933aaeea52d25c3a9b01e7f3960aafdb688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase1LifetimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2DhGroupNumbers")
    def tunnel1_phase2_dh_group_numbers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "tunnel1Phase2DhGroupNumbers"))

    @tunnel1_phase2_dh_group_numbers.setter
    def tunnel1_phase2_dh_group_numbers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5988126885aeca6b265d4563b2f3b4a5407c4db23b5084819081e7e00bc61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase2DhGroupNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2EncryptionAlgorithms")
    def tunnel1_phase2_encryption_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel1Phase2EncryptionAlgorithms"))

    @tunnel1_phase2_encryption_algorithms.setter
    def tunnel1_phase2_encryption_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79b715525af0afdaf758ef02c67f17d80eede957e23c120002094224969b382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase2EncryptionAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2IntegrityAlgorithms")
    def tunnel1_phase2_integrity_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel1Phase2IntegrityAlgorithms"))

    @tunnel1_phase2_integrity_algorithms.setter
    def tunnel1_phase2_integrity_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c36b3f6cb7775882b15f963a5c04e183ad952ecafd0999b1443591b05ff766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase2IntegrityAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2LifetimeSeconds")
    def tunnel1_phase2_lifetime_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1Phase2LifetimeSeconds"))

    @tunnel1_phase2_lifetime_seconds.setter
    def tunnel1_phase2_lifetime_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f624574ac0cf2f9168da91ef1326574aa880d38db16c44487078b9fb75149c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase2LifetimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1PresharedKey")
    def tunnel1_preshared_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1PresharedKey"))

    @tunnel1_preshared_key.setter
    def tunnel1_preshared_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804f236e3c0b5475e69ce09eb9ef0e4fc7d51339d7f6e0ee2ddcf4ed536336f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1PresharedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1RekeyFuzzPercentage")
    def tunnel1_rekey_fuzz_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1RekeyFuzzPercentage"))

    @tunnel1_rekey_fuzz_percentage.setter
    def tunnel1_rekey_fuzz_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849da896aa90a71f83802e29c3355b498bacb8d50117f061c175c5557b910a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1RekeyFuzzPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1RekeyMarginTimeSeconds")
    def tunnel1_rekey_margin_time_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1RekeyMarginTimeSeconds"))

    @tunnel1_rekey_margin_time_seconds.setter
    def tunnel1_rekey_margin_time_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0661e85d5ecf13256e0caa524f6ca2dc8454cb9778361a7c5f0d515d0754f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1RekeyMarginTimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1ReplayWindowSize")
    def tunnel1_replay_window_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1ReplayWindowSize"))

    @tunnel1_replay_window_size.setter
    def tunnel1_replay_window_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08bd1e53bde771f4f7db8e6b50e52b25585e8457efd0cba9a97ad7182dc2139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1ReplayWindowSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1StartupAction")
    def tunnel1_startup_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1StartupAction"))

    @tunnel1_startup_action.setter
    def tunnel1_startup_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbc92f1bef8eeeb97d9a90b935f811d6ff57ec47728b795b37a3f38fbc5677f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1StartupAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2DpdTimeoutAction")
    def tunnel2_dpd_timeout_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2DpdTimeoutAction"))

    @tunnel2_dpd_timeout_action.setter
    def tunnel2_dpd_timeout_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b183813e3af228f382449240b807926b47394a6d4e3233c420948e9686cfa890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2DpdTimeoutAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2DpdTimeoutSeconds")
    def tunnel2_dpd_timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2DpdTimeoutSeconds"))

    @tunnel2_dpd_timeout_seconds.setter
    def tunnel2_dpd_timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e907b5163ee422fad85fac87dd0e0d889e5ecb160c5980c8517b6d55e7878b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2DpdTimeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2EnableTunnelLifecycleControl")
    def tunnel2_enable_tunnel_lifecycle_control(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tunnel2EnableTunnelLifecycleControl"))

    @tunnel2_enable_tunnel_lifecycle_control.setter
    def tunnel2_enable_tunnel_lifecycle_control(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3242a323ba4a2f5729b650f33aa713728123d07b77a2ed4dd89d8d8b6a3d3083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2EnableTunnelLifecycleControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2IkeVersions")
    def tunnel2_ike_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel2IkeVersions"))

    @tunnel2_ike_versions.setter
    def tunnel2_ike_versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760bdc480e65383f61d0850bb0231b422d588d187c3f53d6612900c9fcfb66cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2IkeVersions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2InsideCidr")
    def tunnel2_inside_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2InsideCidr"))

    @tunnel2_inside_cidr.setter
    def tunnel2_inside_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796e86597330bd6299b67b76a4efe432f44407a16252119816ea6746842b9452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2InsideCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2InsideIpv6Cidr")
    def tunnel2_inside_ipv6_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2InsideIpv6Cidr"))

    @tunnel2_inside_ipv6_cidr.setter
    def tunnel2_inside_ipv6_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630f1c52f6ec908c1134b0d306335f6f7f1d897c14230d7f1e9f21e42b8fa807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2InsideIpv6Cidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1DhGroupNumbers")
    def tunnel2_phase1_dh_group_numbers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "tunnel2Phase1DhGroupNumbers"))

    @tunnel2_phase1_dh_group_numbers.setter
    def tunnel2_phase1_dh_group_numbers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538c2b944ffc84a9942a9ec814b6876fa2b681f8478ae43f09460be6e5f10389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase1DhGroupNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1EncryptionAlgorithms")
    def tunnel2_phase1_encryption_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel2Phase1EncryptionAlgorithms"))

    @tunnel2_phase1_encryption_algorithms.setter
    def tunnel2_phase1_encryption_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb37a696e976b5589eaabd58ccaab2823a677a4d5ca45f8ec874757686cdb18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase1EncryptionAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1IntegrityAlgorithms")
    def tunnel2_phase1_integrity_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel2Phase1IntegrityAlgorithms"))

    @tunnel2_phase1_integrity_algorithms.setter
    def tunnel2_phase1_integrity_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e26fb3e77458dc2aa629e5d7c0ba9326879393005512199545daa63f6a9b451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase1IntegrityAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1LifetimeSeconds")
    def tunnel2_phase1_lifetime_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2Phase1LifetimeSeconds"))

    @tunnel2_phase1_lifetime_seconds.setter
    def tunnel2_phase1_lifetime_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff243aa66ad9b2bc0515f01de2f5af3786fa031930e8c5d3deaf27754adc8b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase1LifetimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2DhGroupNumbers")
    def tunnel2_phase2_dh_group_numbers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "tunnel2Phase2DhGroupNumbers"))

    @tunnel2_phase2_dh_group_numbers.setter
    def tunnel2_phase2_dh_group_numbers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446e7e613120deef52a81e267d8b30d388ed9944a7825c95f7d381169531efc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase2DhGroupNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2EncryptionAlgorithms")
    def tunnel2_phase2_encryption_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel2Phase2EncryptionAlgorithms"))

    @tunnel2_phase2_encryption_algorithms.setter
    def tunnel2_phase2_encryption_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7405e08dc7d7b602df3000efff3a150b56aa65d58cccb5bf80c4afd3e3b26a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase2EncryptionAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2IntegrityAlgorithms")
    def tunnel2_phase2_integrity_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel2Phase2IntegrityAlgorithms"))

    @tunnel2_phase2_integrity_algorithms.setter
    def tunnel2_phase2_integrity_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb51c48701b822549594e4369d41a31c209424f7b36efb86b3362005852ee7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase2IntegrityAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2LifetimeSeconds")
    def tunnel2_phase2_lifetime_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2Phase2LifetimeSeconds"))

    @tunnel2_phase2_lifetime_seconds.setter
    def tunnel2_phase2_lifetime_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dedc6c3a2217796603cac7b0aa63dd59516ec10333a3bf61c329a02a1661abee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase2LifetimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2PresharedKey")
    def tunnel2_preshared_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2PresharedKey"))

    @tunnel2_preshared_key.setter
    def tunnel2_preshared_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__febd839acf4082a2c7bee87f62b1b61786f7a4beff7fdea5b588b738563f0b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2PresharedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2RekeyFuzzPercentage")
    def tunnel2_rekey_fuzz_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2RekeyFuzzPercentage"))

    @tunnel2_rekey_fuzz_percentage.setter
    def tunnel2_rekey_fuzz_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd8b0257348cde101fd00aeadf5ca2538ad88f9dad1172c9a8cfa8a250a6e44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2RekeyFuzzPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2RekeyMarginTimeSeconds")
    def tunnel2_rekey_margin_time_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2RekeyMarginTimeSeconds"))

    @tunnel2_rekey_margin_time_seconds.setter
    def tunnel2_rekey_margin_time_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92bb9af14cdcebfb1a8d2c976428258fff197de1bc18521070ef3120d938677b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2RekeyMarginTimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2ReplayWindowSize")
    def tunnel2_replay_window_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2ReplayWindowSize"))

    @tunnel2_replay_window_size.setter
    def tunnel2_replay_window_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf283db36747392986d14cdbb381c59e2f0ef3fb6e40e1cc3ad8815a5f5f045f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2ReplayWindowSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2StartupAction")
    def tunnel2_startup_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2StartupAction"))

    @tunnel2_startup_action.setter
    def tunnel2_startup_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99420354c7fa01fcfece7c5815ba9d3d39e3cddcd61a8a4e32f9d64b31bf3ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2StartupAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnelBandwidth")
    def tunnel_bandwidth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnelBandwidth"))

    @tunnel_bandwidth.setter
    def tunnel_bandwidth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be338833c795eb205951291231479f97d229ffdcee09e6d3a450e2903722b47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelBandwidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnelInsideIpVersion")
    def tunnel_inside_ip_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnelInsideIpVersion"))

    @tunnel_inside_ip_version.setter
    def tunnel_inside_ip_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb544aaf518930aeac69132b5503050ce394c44eed30280856ea7c7909bb2a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelInsideIpVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__998250c1359d2c194fbcf9cf5d80dbdc0c8ac391b4c314d33993b25dc81869b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnConcentratorId")
    def vpn_concentrator_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpnConcentratorId"))

    @vpn_concentrator_id.setter
    def vpn_concentrator_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e51939d32cc34ddb1a7744cae29eb7af2ffbba60cc202e30390289445a4d3b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnConcentratorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpnGatewayId"))

    @vpn_gateway_id.setter
    def vpn_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfe1217b45ff8aebb3357e74e1178357a0e4b5ff1b8a20dbfb597147cc4de09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnGatewayId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "customer_gateway_id": "customerGatewayId",
        "type": "type",
        "enable_acceleration": "enableAcceleration",
        "id": "id",
        "local_ipv4_network_cidr": "localIpv4NetworkCidr",
        "local_ipv6_network_cidr": "localIpv6NetworkCidr",
        "outside_ip_address_type": "outsideIpAddressType",
        "preshared_key_storage": "presharedKeyStorage",
        "region": "region",
        "remote_ipv4_network_cidr": "remoteIpv4NetworkCidr",
        "remote_ipv6_network_cidr": "remoteIpv6NetworkCidr",
        "static_routes_only": "staticRoutesOnly",
        "tags": "tags",
        "tags_all": "tagsAll",
        "transit_gateway_id": "transitGatewayId",
        "transport_transit_gateway_attachment_id": "transportTransitGatewayAttachmentId",
        "tunnel1_dpd_timeout_action": "tunnel1DpdTimeoutAction",
        "tunnel1_dpd_timeout_seconds": "tunnel1DpdTimeoutSeconds",
        "tunnel1_enable_tunnel_lifecycle_control": "tunnel1EnableTunnelLifecycleControl",
        "tunnel1_ike_versions": "tunnel1IkeVersions",
        "tunnel1_inside_cidr": "tunnel1InsideCidr",
        "tunnel1_inside_ipv6_cidr": "tunnel1InsideIpv6Cidr",
        "tunnel1_log_options": "tunnel1LogOptions",
        "tunnel1_phase1_dh_group_numbers": "tunnel1Phase1DhGroupNumbers",
        "tunnel1_phase1_encryption_algorithms": "tunnel1Phase1EncryptionAlgorithms",
        "tunnel1_phase1_integrity_algorithms": "tunnel1Phase1IntegrityAlgorithms",
        "tunnel1_phase1_lifetime_seconds": "tunnel1Phase1LifetimeSeconds",
        "tunnel1_phase2_dh_group_numbers": "tunnel1Phase2DhGroupNumbers",
        "tunnel1_phase2_encryption_algorithms": "tunnel1Phase2EncryptionAlgorithms",
        "tunnel1_phase2_integrity_algorithms": "tunnel1Phase2IntegrityAlgorithms",
        "tunnel1_phase2_lifetime_seconds": "tunnel1Phase2LifetimeSeconds",
        "tunnel1_preshared_key": "tunnel1PresharedKey",
        "tunnel1_rekey_fuzz_percentage": "tunnel1RekeyFuzzPercentage",
        "tunnel1_rekey_margin_time_seconds": "tunnel1RekeyMarginTimeSeconds",
        "tunnel1_replay_window_size": "tunnel1ReplayWindowSize",
        "tunnel1_startup_action": "tunnel1StartupAction",
        "tunnel2_dpd_timeout_action": "tunnel2DpdTimeoutAction",
        "tunnel2_dpd_timeout_seconds": "tunnel2DpdTimeoutSeconds",
        "tunnel2_enable_tunnel_lifecycle_control": "tunnel2EnableTunnelLifecycleControl",
        "tunnel2_ike_versions": "tunnel2IkeVersions",
        "tunnel2_inside_cidr": "tunnel2InsideCidr",
        "tunnel2_inside_ipv6_cidr": "tunnel2InsideIpv6Cidr",
        "tunnel2_log_options": "tunnel2LogOptions",
        "tunnel2_phase1_dh_group_numbers": "tunnel2Phase1DhGroupNumbers",
        "tunnel2_phase1_encryption_algorithms": "tunnel2Phase1EncryptionAlgorithms",
        "tunnel2_phase1_integrity_algorithms": "tunnel2Phase1IntegrityAlgorithms",
        "tunnel2_phase1_lifetime_seconds": "tunnel2Phase1LifetimeSeconds",
        "tunnel2_phase2_dh_group_numbers": "tunnel2Phase2DhGroupNumbers",
        "tunnel2_phase2_encryption_algorithms": "tunnel2Phase2EncryptionAlgorithms",
        "tunnel2_phase2_integrity_algorithms": "tunnel2Phase2IntegrityAlgorithms",
        "tunnel2_phase2_lifetime_seconds": "tunnel2Phase2LifetimeSeconds",
        "tunnel2_preshared_key": "tunnel2PresharedKey",
        "tunnel2_rekey_fuzz_percentage": "tunnel2RekeyFuzzPercentage",
        "tunnel2_rekey_margin_time_seconds": "tunnel2RekeyMarginTimeSeconds",
        "tunnel2_replay_window_size": "tunnel2ReplayWindowSize",
        "tunnel2_startup_action": "tunnel2StartupAction",
        "tunnel_bandwidth": "tunnelBandwidth",
        "tunnel_inside_ip_version": "tunnelInsideIpVersion",
        "vpn_concentrator_id": "vpnConcentratorId",
        "vpn_gateway_id": "vpnGatewayId",
    },
)
class VpnConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        customer_gateway_id: builtins.str,
        type: builtins.str,
        enable_acceleration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        local_ipv6_network_cidr: typing.Optional[builtins.str] = None,
        outside_ip_address_type: typing.Optional[builtins.str] = None,
        preshared_key_storage: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        remote_ipv6_network_cidr: typing.Optional[builtins.str] = None,
        static_routes_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transit_gateway_id: typing.Optional[builtins.str] = None,
        transport_transit_gateway_attachment_id: typing.Optional[builtins.str] = None,
        tunnel1_dpd_timeout_action: typing.Optional[builtins.str] = None,
        tunnel1_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel1_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_inside_cidr: typing.Optional[builtins.str] = None,
        tunnel1_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
        tunnel1_log_options: typing.Optional[typing.Union["VpnConnectionTunnel1LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel1_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel1_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel1_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_preshared_key: typing.Optional[builtins.str] = None,
        tunnel1_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
        tunnel1_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_replay_window_size: typing.Optional[jsii.Number] = None,
        tunnel1_startup_action: typing.Optional[builtins.str] = None,
        tunnel2_dpd_timeout_action: typing.Optional[builtins.str] = None,
        tunnel2_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel2_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_inside_cidr: typing.Optional[builtins.str] = None,
        tunnel2_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
        tunnel2_log_options: typing.Optional[typing.Union["VpnConnectionTunnel2LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel2_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel2_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel2_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_preshared_key: typing.Optional[builtins.str] = None,
        tunnel2_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
        tunnel2_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_replay_window_size: typing.Optional[jsii.Number] = None,
        tunnel2_startup_action: typing.Optional[builtins.str] = None,
        tunnel_bandwidth: typing.Optional[builtins.str] = None,
        tunnel_inside_ip_version: typing.Optional[builtins.str] = None,
        vpn_concentrator_id: typing.Optional[builtins.str] = None,
        vpn_gateway_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param customer_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#customer_gateway_id VpnConnection#customer_gateway_id}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#type VpnConnection#type}.
        :param enable_acceleration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#enable_acceleration VpnConnection#enable_acceleration}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#id VpnConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_ipv4_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#local_ipv4_network_cidr VpnConnection#local_ipv4_network_cidr}.
        :param local_ipv6_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#local_ipv6_network_cidr VpnConnection#local_ipv6_network_cidr}.
        :param outside_ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#outside_ip_address_type VpnConnection#outside_ip_address_type}.
        :param preshared_key_storage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#preshared_key_storage VpnConnection#preshared_key_storage}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#region VpnConnection#region}
        :param remote_ipv4_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#remote_ipv4_network_cidr VpnConnection#remote_ipv4_network_cidr}.
        :param remote_ipv6_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#remote_ipv6_network_cidr VpnConnection#remote_ipv6_network_cidr}.
        :param static_routes_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#static_routes_only VpnConnection#static_routes_only}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tags VpnConnection#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tags_all VpnConnection#tags_all}.
        :param transit_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#transit_gateway_id VpnConnection#transit_gateway_id}.
        :param transport_transit_gateway_attachment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#transport_transit_gateway_attachment_id VpnConnection#transport_transit_gateway_attachment_id}.
        :param tunnel1_dpd_timeout_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_action VpnConnection#tunnel1_dpd_timeout_action}.
        :param tunnel1_dpd_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_seconds VpnConnection#tunnel1_dpd_timeout_seconds}.
        :param tunnel1_enable_tunnel_lifecycle_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_enable_tunnel_lifecycle_control VpnConnection#tunnel1_enable_tunnel_lifecycle_control}.
        :param tunnel1_ike_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_ike_versions VpnConnection#tunnel1_ike_versions}.
        :param tunnel1_inside_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_inside_cidr VpnConnection#tunnel1_inside_cidr}.
        :param tunnel1_inside_ipv6_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_inside_ipv6_cidr VpnConnection#tunnel1_inside_ipv6_cidr}.
        :param tunnel1_log_options: tunnel1_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_log_options VpnConnection#tunnel1_log_options}
        :param tunnel1_phase1_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_dh_group_numbers VpnConnection#tunnel1_phase1_dh_group_numbers}.
        :param tunnel1_phase1_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_encryption_algorithms VpnConnection#tunnel1_phase1_encryption_algorithms}.
        :param tunnel1_phase1_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_integrity_algorithms VpnConnection#tunnel1_phase1_integrity_algorithms}.
        :param tunnel1_phase1_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_lifetime_seconds VpnConnection#tunnel1_phase1_lifetime_seconds}.
        :param tunnel1_phase2_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_dh_group_numbers VpnConnection#tunnel1_phase2_dh_group_numbers}.
        :param tunnel1_phase2_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_encryption_algorithms VpnConnection#tunnel1_phase2_encryption_algorithms}.
        :param tunnel1_phase2_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_integrity_algorithms VpnConnection#tunnel1_phase2_integrity_algorithms}.
        :param tunnel1_phase2_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_lifetime_seconds VpnConnection#tunnel1_phase2_lifetime_seconds}.
        :param tunnel1_preshared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_preshared_key VpnConnection#tunnel1_preshared_key}.
        :param tunnel1_rekey_fuzz_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_rekey_fuzz_percentage VpnConnection#tunnel1_rekey_fuzz_percentage}.
        :param tunnel1_rekey_margin_time_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_rekey_margin_time_seconds VpnConnection#tunnel1_rekey_margin_time_seconds}.
        :param tunnel1_replay_window_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_replay_window_size VpnConnection#tunnel1_replay_window_size}.
        :param tunnel1_startup_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_startup_action VpnConnection#tunnel1_startup_action}.
        :param tunnel2_dpd_timeout_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_action VpnConnection#tunnel2_dpd_timeout_action}.
        :param tunnel2_dpd_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_seconds VpnConnection#tunnel2_dpd_timeout_seconds}.
        :param tunnel2_enable_tunnel_lifecycle_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_enable_tunnel_lifecycle_control VpnConnection#tunnel2_enable_tunnel_lifecycle_control}.
        :param tunnel2_ike_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_ike_versions VpnConnection#tunnel2_ike_versions}.
        :param tunnel2_inside_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_inside_cidr VpnConnection#tunnel2_inside_cidr}.
        :param tunnel2_inside_ipv6_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_inside_ipv6_cidr VpnConnection#tunnel2_inside_ipv6_cidr}.
        :param tunnel2_log_options: tunnel2_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_log_options VpnConnection#tunnel2_log_options}
        :param tunnel2_phase1_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_dh_group_numbers VpnConnection#tunnel2_phase1_dh_group_numbers}.
        :param tunnel2_phase1_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_encryption_algorithms VpnConnection#tunnel2_phase1_encryption_algorithms}.
        :param tunnel2_phase1_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_integrity_algorithms VpnConnection#tunnel2_phase1_integrity_algorithms}.
        :param tunnel2_phase1_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_lifetime_seconds VpnConnection#tunnel2_phase1_lifetime_seconds}.
        :param tunnel2_phase2_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_dh_group_numbers VpnConnection#tunnel2_phase2_dh_group_numbers}.
        :param tunnel2_phase2_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_encryption_algorithms VpnConnection#tunnel2_phase2_encryption_algorithms}.
        :param tunnel2_phase2_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_integrity_algorithms VpnConnection#tunnel2_phase2_integrity_algorithms}.
        :param tunnel2_phase2_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_lifetime_seconds VpnConnection#tunnel2_phase2_lifetime_seconds}.
        :param tunnel2_preshared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_preshared_key VpnConnection#tunnel2_preshared_key}.
        :param tunnel2_rekey_fuzz_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_rekey_fuzz_percentage VpnConnection#tunnel2_rekey_fuzz_percentage}.
        :param tunnel2_rekey_margin_time_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_rekey_margin_time_seconds VpnConnection#tunnel2_rekey_margin_time_seconds}.
        :param tunnel2_replay_window_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_replay_window_size VpnConnection#tunnel2_replay_window_size}.
        :param tunnel2_startup_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_startup_action VpnConnection#tunnel2_startup_action}.
        :param tunnel_bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel_bandwidth VpnConnection#tunnel_bandwidth}.
        :param tunnel_inside_ip_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel_inside_ip_version VpnConnection#tunnel_inside_ip_version}.
        :param vpn_concentrator_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#vpn_concentrator_id VpnConnection#vpn_concentrator_id}.
        :param vpn_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#vpn_gateway_id VpnConnection#vpn_gateway_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(tunnel1_log_options, dict):
            tunnel1_log_options = VpnConnectionTunnel1LogOptions(**tunnel1_log_options)
        if isinstance(tunnel2_log_options, dict):
            tunnel2_log_options = VpnConnectionTunnel2LogOptions(**tunnel2_log_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d539dfcb5f5046b37c3d1fc83a34eaee535c0e69e96cc154206a9755063b0e6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument customer_gateway_id", value=customer_gateway_id, expected_type=type_hints["customer_gateway_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument enable_acceleration", value=enable_acceleration, expected_type=type_hints["enable_acceleration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument local_ipv4_network_cidr", value=local_ipv4_network_cidr, expected_type=type_hints["local_ipv4_network_cidr"])
            check_type(argname="argument local_ipv6_network_cidr", value=local_ipv6_network_cidr, expected_type=type_hints["local_ipv6_network_cidr"])
            check_type(argname="argument outside_ip_address_type", value=outside_ip_address_type, expected_type=type_hints["outside_ip_address_type"])
            check_type(argname="argument preshared_key_storage", value=preshared_key_storage, expected_type=type_hints["preshared_key_storage"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument remote_ipv4_network_cidr", value=remote_ipv4_network_cidr, expected_type=type_hints["remote_ipv4_network_cidr"])
            check_type(argname="argument remote_ipv6_network_cidr", value=remote_ipv6_network_cidr, expected_type=type_hints["remote_ipv6_network_cidr"])
            check_type(argname="argument static_routes_only", value=static_routes_only, expected_type=type_hints["static_routes_only"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument transit_gateway_id", value=transit_gateway_id, expected_type=type_hints["transit_gateway_id"])
            check_type(argname="argument transport_transit_gateway_attachment_id", value=transport_transit_gateway_attachment_id, expected_type=type_hints["transport_transit_gateway_attachment_id"])
            check_type(argname="argument tunnel1_dpd_timeout_action", value=tunnel1_dpd_timeout_action, expected_type=type_hints["tunnel1_dpd_timeout_action"])
            check_type(argname="argument tunnel1_dpd_timeout_seconds", value=tunnel1_dpd_timeout_seconds, expected_type=type_hints["tunnel1_dpd_timeout_seconds"])
            check_type(argname="argument tunnel1_enable_tunnel_lifecycle_control", value=tunnel1_enable_tunnel_lifecycle_control, expected_type=type_hints["tunnel1_enable_tunnel_lifecycle_control"])
            check_type(argname="argument tunnel1_ike_versions", value=tunnel1_ike_versions, expected_type=type_hints["tunnel1_ike_versions"])
            check_type(argname="argument tunnel1_inside_cidr", value=tunnel1_inside_cidr, expected_type=type_hints["tunnel1_inside_cidr"])
            check_type(argname="argument tunnel1_inside_ipv6_cidr", value=tunnel1_inside_ipv6_cidr, expected_type=type_hints["tunnel1_inside_ipv6_cidr"])
            check_type(argname="argument tunnel1_log_options", value=tunnel1_log_options, expected_type=type_hints["tunnel1_log_options"])
            check_type(argname="argument tunnel1_phase1_dh_group_numbers", value=tunnel1_phase1_dh_group_numbers, expected_type=type_hints["tunnel1_phase1_dh_group_numbers"])
            check_type(argname="argument tunnel1_phase1_encryption_algorithms", value=tunnel1_phase1_encryption_algorithms, expected_type=type_hints["tunnel1_phase1_encryption_algorithms"])
            check_type(argname="argument tunnel1_phase1_integrity_algorithms", value=tunnel1_phase1_integrity_algorithms, expected_type=type_hints["tunnel1_phase1_integrity_algorithms"])
            check_type(argname="argument tunnel1_phase1_lifetime_seconds", value=tunnel1_phase1_lifetime_seconds, expected_type=type_hints["tunnel1_phase1_lifetime_seconds"])
            check_type(argname="argument tunnel1_phase2_dh_group_numbers", value=tunnel1_phase2_dh_group_numbers, expected_type=type_hints["tunnel1_phase2_dh_group_numbers"])
            check_type(argname="argument tunnel1_phase2_encryption_algorithms", value=tunnel1_phase2_encryption_algorithms, expected_type=type_hints["tunnel1_phase2_encryption_algorithms"])
            check_type(argname="argument tunnel1_phase2_integrity_algorithms", value=tunnel1_phase2_integrity_algorithms, expected_type=type_hints["tunnel1_phase2_integrity_algorithms"])
            check_type(argname="argument tunnel1_phase2_lifetime_seconds", value=tunnel1_phase2_lifetime_seconds, expected_type=type_hints["tunnel1_phase2_lifetime_seconds"])
            check_type(argname="argument tunnel1_preshared_key", value=tunnel1_preshared_key, expected_type=type_hints["tunnel1_preshared_key"])
            check_type(argname="argument tunnel1_rekey_fuzz_percentage", value=tunnel1_rekey_fuzz_percentage, expected_type=type_hints["tunnel1_rekey_fuzz_percentage"])
            check_type(argname="argument tunnel1_rekey_margin_time_seconds", value=tunnel1_rekey_margin_time_seconds, expected_type=type_hints["tunnel1_rekey_margin_time_seconds"])
            check_type(argname="argument tunnel1_replay_window_size", value=tunnel1_replay_window_size, expected_type=type_hints["tunnel1_replay_window_size"])
            check_type(argname="argument tunnel1_startup_action", value=tunnel1_startup_action, expected_type=type_hints["tunnel1_startup_action"])
            check_type(argname="argument tunnel2_dpd_timeout_action", value=tunnel2_dpd_timeout_action, expected_type=type_hints["tunnel2_dpd_timeout_action"])
            check_type(argname="argument tunnel2_dpd_timeout_seconds", value=tunnel2_dpd_timeout_seconds, expected_type=type_hints["tunnel2_dpd_timeout_seconds"])
            check_type(argname="argument tunnel2_enable_tunnel_lifecycle_control", value=tunnel2_enable_tunnel_lifecycle_control, expected_type=type_hints["tunnel2_enable_tunnel_lifecycle_control"])
            check_type(argname="argument tunnel2_ike_versions", value=tunnel2_ike_versions, expected_type=type_hints["tunnel2_ike_versions"])
            check_type(argname="argument tunnel2_inside_cidr", value=tunnel2_inside_cidr, expected_type=type_hints["tunnel2_inside_cidr"])
            check_type(argname="argument tunnel2_inside_ipv6_cidr", value=tunnel2_inside_ipv6_cidr, expected_type=type_hints["tunnel2_inside_ipv6_cidr"])
            check_type(argname="argument tunnel2_log_options", value=tunnel2_log_options, expected_type=type_hints["tunnel2_log_options"])
            check_type(argname="argument tunnel2_phase1_dh_group_numbers", value=tunnel2_phase1_dh_group_numbers, expected_type=type_hints["tunnel2_phase1_dh_group_numbers"])
            check_type(argname="argument tunnel2_phase1_encryption_algorithms", value=tunnel2_phase1_encryption_algorithms, expected_type=type_hints["tunnel2_phase1_encryption_algorithms"])
            check_type(argname="argument tunnel2_phase1_integrity_algorithms", value=tunnel2_phase1_integrity_algorithms, expected_type=type_hints["tunnel2_phase1_integrity_algorithms"])
            check_type(argname="argument tunnel2_phase1_lifetime_seconds", value=tunnel2_phase1_lifetime_seconds, expected_type=type_hints["tunnel2_phase1_lifetime_seconds"])
            check_type(argname="argument tunnel2_phase2_dh_group_numbers", value=tunnel2_phase2_dh_group_numbers, expected_type=type_hints["tunnel2_phase2_dh_group_numbers"])
            check_type(argname="argument tunnel2_phase2_encryption_algorithms", value=tunnel2_phase2_encryption_algorithms, expected_type=type_hints["tunnel2_phase2_encryption_algorithms"])
            check_type(argname="argument tunnel2_phase2_integrity_algorithms", value=tunnel2_phase2_integrity_algorithms, expected_type=type_hints["tunnel2_phase2_integrity_algorithms"])
            check_type(argname="argument tunnel2_phase2_lifetime_seconds", value=tunnel2_phase2_lifetime_seconds, expected_type=type_hints["tunnel2_phase2_lifetime_seconds"])
            check_type(argname="argument tunnel2_preshared_key", value=tunnel2_preshared_key, expected_type=type_hints["tunnel2_preshared_key"])
            check_type(argname="argument tunnel2_rekey_fuzz_percentage", value=tunnel2_rekey_fuzz_percentage, expected_type=type_hints["tunnel2_rekey_fuzz_percentage"])
            check_type(argname="argument tunnel2_rekey_margin_time_seconds", value=tunnel2_rekey_margin_time_seconds, expected_type=type_hints["tunnel2_rekey_margin_time_seconds"])
            check_type(argname="argument tunnel2_replay_window_size", value=tunnel2_replay_window_size, expected_type=type_hints["tunnel2_replay_window_size"])
            check_type(argname="argument tunnel2_startup_action", value=tunnel2_startup_action, expected_type=type_hints["tunnel2_startup_action"])
            check_type(argname="argument tunnel_bandwidth", value=tunnel_bandwidth, expected_type=type_hints["tunnel_bandwidth"])
            check_type(argname="argument tunnel_inside_ip_version", value=tunnel_inside_ip_version, expected_type=type_hints["tunnel_inside_ip_version"])
            check_type(argname="argument vpn_concentrator_id", value=vpn_concentrator_id, expected_type=type_hints["vpn_concentrator_id"])
            check_type(argname="argument vpn_gateway_id", value=vpn_gateway_id, expected_type=type_hints["vpn_gateway_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "customer_gateway_id": customer_gateway_id,
            "type": type,
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
        if enable_acceleration is not None:
            self._values["enable_acceleration"] = enable_acceleration
        if id is not None:
            self._values["id"] = id
        if local_ipv4_network_cidr is not None:
            self._values["local_ipv4_network_cidr"] = local_ipv4_network_cidr
        if local_ipv6_network_cidr is not None:
            self._values["local_ipv6_network_cidr"] = local_ipv6_network_cidr
        if outside_ip_address_type is not None:
            self._values["outside_ip_address_type"] = outside_ip_address_type
        if preshared_key_storage is not None:
            self._values["preshared_key_storage"] = preshared_key_storage
        if region is not None:
            self._values["region"] = region
        if remote_ipv4_network_cidr is not None:
            self._values["remote_ipv4_network_cidr"] = remote_ipv4_network_cidr
        if remote_ipv6_network_cidr is not None:
            self._values["remote_ipv6_network_cidr"] = remote_ipv6_network_cidr
        if static_routes_only is not None:
            self._values["static_routes_only"] = static_routes_only
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if transit_gateway_id is not None:
            self._values["transit_gateway_id"] = transit_gateway_id
        if transport_transit_gateway_attachment_id is not None:
            self._values["transport_transit_gateway_attachment_id"] = transport_transit_gateway_attachment_id
        if tunnel1_dpd_timeout_action is not None:
            self._values["tunnel1_dpd_timeout_action"] = tunnel1_dpd_timeout_action
        if tunnel1_dpd_timeout_seconds is not None:
            self._values["tunnel1_dpd_timeout_seconds"] = tunnel1_dpd_timeout_seconds
        if tunnel1_enable_tunnel_lifecycle_control is not None:
            self._values["tunnel1_enable_tunnel_lifecycle_control"] = tunnel1_enable_tunnel_lifecycle_control
        if tunnel1_ike_versions is not None:
            self._values["tunnel1_ike_versions"] = tunnel1_ike_versions
        if tunnel1_inside_cidr is not None:
            self._values["tunnel1_inside_cidr"] = tunnel1_inside_cidr
        if tunnel1_inside_ipv6_cidr is not None:
            self._values["tunnel1_inside_ipv6_cidr"] = tunnel1_inside_ipv6_cidr
        if tunnel1_log_options is not None:
            self._values["tunnel1_log_options"] = tunnel1_log_options
        if tunnel1_phase1_dh_group_numbers is not None:
            self._values["tunnel1_phase1_dh_group_numbers"] = tunnel1_phase1_dh_group_numbers
        if tunnel1_phase1_encryption_algorithms is not None:
            self._values["tunnel1_phase1_encryption_algorithms"] = tunnel1_phase1_encryption_algorithms
        if tunnel1_phase1_integrity_algorithms is not None:
            self._values["tunnel1_phase1_integrity_algorithms"] = tunnel1_phase1_integrity_algorithms
        if tunnel1_phase1_lifetime_seconds is not None:
            self._values["tunnel1_phase1_lifetime_seconds"] = tunnel1_phase1_lifetime_seconds
        if tunnel1_phase2_dh_group_numbers is not None:
            self._values["tunnel1_phase2_dh_group_numbers"] = tunnel1_phase2_dh_group_numbers
        if tunnel1_phase2_encryption_algorithms is not None:
            self._values["tunnel1_phase2_encryption_algorithms"] = tunnel1_phase2_encryption_algorithms
        if tunnel1_phase2_integrity_algorithms is not None:
            self._values["tunnel1_phase2_integrity_algorithms"] = tunnel1_phase2_integrity_algorithms
        if tunnel1_phase2_lifetime_seconds is not None:
            self._values["tunnel1_phase2_lifetime_seconds"] = tunnel1_phase2_lifetime_seconds
        if tunnel1_preshared_key is not None:
            self._values["tunnel1_preshared_key"] = tunnel1_preshared_key
        if tunnel1_rekey_fuzz_percentage is not None:
            self._values["tunnel1_rekey_fuzz_percentage"] = tunnel1_rekey_fuzz_percentage
        if tunnel1_rekey_margin_time_seconds is not None:
            self._values["tunnel1_rekey_margin_time_seconds"] = tunnel1_rekey_margin_time_seconds
        if tunnel1_replay_window_size is not None:
            self._values["tunnel1_replay_window_size"] = tunnel1_replay_window_size
        if tunnel1_startup_action is not None:
            self._values["tunnel1_startup_action"] = tunnel1_startup_action
        if tunnel2_dpd_timeout_action is not None:
            self._values["tunnel2_dpd_timeout_action"] = tunnel2_dpd_timeout_action
        if tunnel2_dpd_timeout_seconds is not None:
            self._values["tunnel2_dpd_timeout_seconds"] = tunnel2_dpd_timeout_seconds
        if tunnel2_enable_tunnel_lifecycle_control is not None:
            self._values["tunnel2_enable_tunnel_lifecycle_control"] = tunnel2_enable_tunnel_lifecycle_control
        if tunnel2_ike_versions is not None:
            self._values["tunnel2_ike_versions"] = tunnel2_ike_versions
        if tunnel2_inside_cidr is not None:
            self._values["tunnel2_inside_cidr"] = tunnel2_inside_cidr
        if tunnel2_inside_ipv6_cidr is not None:
            self._values["tunnel2_inside_ipv6_cidr"] = tunnel2_inside_ipv6_cidr
        if tunnel2_log_options is not None:
            self._values["tunnel2_log_options"] = tunnel2_log_options
        if tunnel2_phase1_dh_group_numbers is not None:
            self._values["tunnel2_phase1_dh_group_numbers"] = tunnel2_phase1_dh_group_numbers
        if tunnel2_phase1_encryption_algorithms is not None:
            self._values["tunnel2_phase1_encryption_algorithms"] = tunnel2_phase1_encryption_algorithms
        if tunnel2_phase1_integrity_algorithms is not None:
            self._values["tunnel2_phase1_integrity_algorithms"] = tunnel2_phase1_integrity_algorithms
        if tunnel2_phase1_lifetime_seconds is not None:
            self._values["tunnel2_phase1_lifetime_seconds"] = tunnel2_phase1_lifetime_seconds
        if tunnel2_phase2_dh_group_numbers is not None:
            self._values["tunnel2_phase2_dh_group_numbers"] = tunnel2_phase2_dh_group_numbers
        if tunnel2_phase2_encryption_algorithms is not None:
            self._values["tunnel2_phase2_encryption_algorithms"] = tunnel2_phase2_encryption_algorithms
        if tunnel2_phase2_integrity_algorithms is not None:
            self._values["tunnel2_phase2_integrity_algorithms"] = tunnel2_phase2_integrity_algorithms
        if tunnel2_phase2_lifetime_seconds is not None:
            self._values["tunnel2_phase2_lifetime_seconds"] = tunnel2_phase2_lifetime_seconds
        if tunnel2_preshared_key is not None:
            self._values["tunnel2_preshared_key"] = tunnel2_preshared_key
        if tunnel2_rekey_fuzz_percentage is not None:
            self._values["tunnel2_rekey_fuzz_percentage"] = tunnel2_rekey_fuzz_percentage
        if tunnel2_rekey_margin_time_seconds is not None:
            self._values["tunnel2_rekey_margin_time_seconds"] = tunnel2_rekey_margin_time_seconds
        if tunnel2_replay_window_size is not None:
            self._values["tunnel2_replay_window_size"] = tunnel2_replay_window_size
        if tunnel2_startup_action is not None:
            self._values["tunnel2_startup_action"] = tunnel2_startup_action
        if tunnel_bandwidth is not None:
            self._values["tunnel_bandwidth"] = tunnel_bandwidth
        if tunnel_inside_ip_version is not None:
            self._values["tunnel_inside_ip_version"] = tunnel_inside_ip_version
        if vpn_concentrator_id is not None:
            self._values["vpn_concentrator_id"] = vpn_concentrator_id
        if vpn_gateway_id is not None:
            self._values["vpn_gateway_id"] = vpn_gateway_id

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
    def customer_gateway_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#customer_gateway_id VpnConnection#customer_gateway_id}.'''
        result = self._values.get("customer_gateway_id")
        assert result is not None, "Required property 'customer_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#type VpnConnection#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_acceleration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#enable_acceleration VpnConnection#enable_acceleration}.'''
        result = self._values.get("enable_acceleration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#id VpnConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ipv4_network_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#local_ipv4_network_cidr VpnConnection#local_ipv4_network_cidr}.'''
        result = self._values.get("local_ipv4_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ipv6_network_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#local_ipv6_network_cidr VpnConnection#local_ipv6_network_cidr}.'''
        result = self._values.get("local_ipv6_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outside_ip_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#outside_ip_address_type VpnConnection#outside_ip_address_type}.'''
        result = self._values.get("outside_ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preshared_key_storage(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#preshared_key_storage VpnConnection#preshared_key_storage}.'''
        result = self._values.get("preshared_key_storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#region VpnConnection#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_ipv4_network_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#remote_ipv4_network_cidr VpnConnection#remote_ipv4_network_cidr}.'''
        result = self._values.get("remote_ipv4_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_ipv6_network_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#remote_ipv6_network_cidr VpnConnection#remote_ipv6_network_cidr}.'''
        result = self._values.get("remote_ipv6_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_routes_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#static_routes_only VpnConnection#static_routes_only}.'''
        result = self._values.get("static_routes_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tags VpnConnection#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tags_all VpnConnection#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def transit_gateway_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#transit_gateway_id VpnConnection#transit_gateway_id}.'''
        result = self._values.get("transit_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transport_transit_gateway_attachment_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#transport_transit_gateway_attachment_id VpnConnection#transport_transit_gateway_attachment_id}.'''
        result = self._values.get("transport_transit_gateway_attachment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel1_dpd_timeout_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_action VpnConnection#tunnel1_dpd_timeout_action}.'''
        result = self._values.get("tunnel1_dpd_timeout_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel1_dpd_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_seconds VpnConnection#tunnel1_dpd_timeout_seconds}.'''
        result = self._values.get("tunnel1_dpd_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_enable_tunnel_lifecycle_control(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_enable_tunnel_lifecycle_control VpnConnection#tunnel1_enable_tunnel_lifecycle_control}.'''
        result = self._values.get("tunnel1_enable_tunnel_lifecycle_control")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tunnel1_ike_versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_ike_versions VpnConnection#tunnel1_ike_versions}.'''
        result = self._values.get("tunnel1_ike_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel1_inside_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_inside_cidr VpnConnection#tunnel1_inside_cidr}.'''
        result = self._values.get("tunnel1_inside_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel1_inside_ipv6_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_inside_ipv6_cidr VpnConnection#tunnel1_inside_ipv6_cidr}.'''
        result = self._values.get("tunnel1_inside_ipv6_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel1_log_options(self) -> typing.Optional["VpnConnectionTunnel1LogOptions"]:
        '''tunnel1_log_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_log_options VpnConnection#tunnel1_log_options}
        '''
        result = self._values.get("tunnel1_log_options")
        return typing.cast(typing.Optional["VpnConnectionTunnel1LogOptions"], result)

    @builtins.property
    def tunnel1_phase1_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_dh_group_numbers VpnConnection#tunnel1_phase1_dh_group_numbers}.'''
        result = self._values.get("tunnel1_phase1_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def tunnel1_phase1_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_encryption_algorithms VpnConnection#tunnel1_phase1_encryption_algorithms}.'''
        result = self._values.get("tunnel1_phase1_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel1_phase1_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_integrity_algorithms VpnConnection#tunnel1_phase1_integrity_algorithms}.'''
        result = self._values.get("tunnel1_phase1_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel1_phase1_lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase1_lifetime_seconds VpnConnection#tunnel1_phase1_lifetime_seconds}.'''
        result = self._values.get("tunnel1_phase1_lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_phase2_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_dh_group_numbers VpnConnection#tunnel1_phase2_dh_group_numbers}.'''
        result = self._values.get("tunnel1_phase2_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def tunnel1_phase2_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_encryption_algorithms VpnConnection#tunnel1_phase2_encryption_algorithms}.'''
        result = self._values.get("tunnel1_phase2_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel1_phase2_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_integrity_algorithms VpnConnection#tunnel1_phase2_integrity_algorithms}.'''
        result = self._values.get("tunnel1_phase2_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel1_phase2_lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_phase2_lifetime_seconds VpnConnection#tunnel1_phase2_lifetime_seconds}.'''
        result = self._values.get("tunnel1_phase2_lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_preshared_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_preshared_key VpnConnection#tunnel1_preshared_key}.'''
        result = self._values.get("tunnel1_preshared_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel1_rekey_fuzz_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_rekey_fuzz_percentage VpnConnection#tunnel1_rekey_fuzz_percentage}.'''
        result = self._values.get("tunnel1_rekey_fuzz_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_rekey_margin_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_rekey_margin_time_seconds VpnConnection#tunnel1_rekey_margin_time_seconds}.'''
        result = self._values.get("tunnel1_rekey_margin_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_replay_window_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_replay_window_size VpnConnection#tunnel1_replay_window_size}.'''
        result = self._values.get("tunnel1_replay_window_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_startup_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel1_startup_action VpnConnection#tunnel1_startup_action}.'''
        result = self._values.get("tunnel1_startup_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel2_dpd_timeout_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_action VpnConnection#tunnel2_dpd_timeout_action}.'''
        result = self._values.get("tunnel2_dpd_timeout_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel2_dpd_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_seconds VpnConnection#tunnel2_dpd_timeout_seconds}.'''
        result = self._values.get("tunnel2_dpd_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_enable_tunnel_lifecycle_control(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_enable_tunnel_lifecycle_control VpnConnection#tunnel2_enable_tunnel_lifecycle_control}.'''
        result = self._values.get("tunnel2_enable_tunnel_lifecycle_control")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tunnel2_ike_versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_ike_versions VpnConnection#tunnel2_ike_versions}.'''
        result = self._values.get("tunnel2_ike_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel2_inside_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_inside_cidr VpnConnection#tunnel2_inside_cidr}.'''
        result = self._values.get("tunnel2_inside_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel2_inside_ipv6_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_inside_ipv6_cidr VpnConnection#tunnel2_inside_ipv6_cidr}.'''
        result = self._values.get("tunnel2_inside_ipv6_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel2_log_options(self) -> typing.Optional["VpnConnectionTunnel2LogOptions"]:
        '''tunnel2_log_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_log_options VpnConnection#tunnel2_log_options}
        '''
        result = self._values.get("tunnel2_log_options")
        return typing.cast(typing.Optional["VpnConnectionTunnel2LogOptions"], result)

    @builtins.property
    def tunnel2_phase1_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_dh_group_numbers VpnConnection#tunnel2_phase1_dh_group_numbers}.'''
        result = self._values.get("tunnel2_phase1_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def tunnel2_phase1_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_encryption_algorithms VpnConnection#tunnel2_phase1_encryption_algorithms}.'''
        result = self._values.get("tunnel2_phase1_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel2_phase1_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_integrity_algorithms VpnConnection#tunnel2_phase1_integrity_algorithms}.'''
        result = self._values.get("tunnel2_phase1_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel2_phase1_lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase1_lifetime_seconds VpnConnection#tunnel2_phase1_lifetime_seconds}.'''
        result = self._values.get("tunnel2_phase1_lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_phase2_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_dh_group_numbers VpnConnection#tunnel2_phase2_dh_group_numbers}.'''
        result = self._values.get("tunnel2_phase2_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def tunnel2_phase2_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_encryption_algorithms VpnConnection#tunnel2_phase2_encryption_algorithms}.'''
        result = self._values.get("tunnel2_phase2_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel2_phase2_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_integrity_algorithms VpnConnection#tunnel2_phase2_integrity_algorithms}.'''
        result = self._values.get("tunnel2_phase2_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel2_phase2_lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_phase2_lifetime_seconds VpnConnection#tunnel2_phase2_lifetime_seconds}.'''
        result = self._values.get("tunnel2_phase2_lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_preshared_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_preshared_key VpnConnection#tunnel2_preshared_key}.'''
        result = self._values.get("tunnel2_preshared_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel2_rekey_fuzz_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_rekey_fuzz_percentage VpnConnection#tunnel2_rekey_fuzz_percentage}.'''
        result = self._values.get("tunnel2_rekey_fuzz_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_rekey_margin_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_rekey_margin_time_seconds VpnConnection#tunnel2_rekey_margin_time_seconds}.'''
        result = self._values.get("tunnel2_rekey_margin_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_replay_window_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_replay_window_size VpnConnection#tunnel2_replay_window_size}.'''
        result = self._values.get("tunnel2_replay_window_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_startup_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel2_startup_action VpnConnection#tunnel2_startup_action}.'''
        result = self._values.get("tunnel2_startup_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel_bandwidth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel_bandwidth VpnConnection#tunnel_bandwidth}.'''
        result = self._values.get("tunnel_bandwidth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel_inside_ip_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#tunnel_inside_ip_version VpnConnection#tunnel_inside_ip_version}.'''
        result = self._values.get("tunnel_inside_ip_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_concentrator_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#vpn_concentrator_id VpnConnection#vpn_concentrator_id}.'''
        result = self._values.get("vpn_concentrator_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_gateway_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#vpn_gateway_id VpnConnection#vpn_gateway_id}.'''
        result = self._values.get("vpn_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionRoutes",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpnConnectionRoutes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionRoutes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnConnectionRoutesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionRoutesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e5f38012187b6b2a24dbb249b06f2ed709f461ab899f7d0705f9cf304b2654e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VpnConnectionRoutesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14cb20f1c3256fdc37c43d2df2c637d7a45606bfaf19778c5718679f7f58a57)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnConnectionRoutesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c2f1ca7f271a38fc4e59fc2bbfa1dd912c7f7766c4c1307ec666e5f663eb6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe26d745dfac0c860a3629633afa4beaa7abf4578a7c58b4eda5974b51c64760)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61f148b16355d4595653a2dc0a5232d7c809b369212091b614b8395427f2123e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VpnConnectionRoutesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionRoutesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6a0a030168475c901c032d09f9029ef67ef3066c5e82f7c8c0316aa6b65c8fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="destinationCidrBlock")
    def destination_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationCidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnConnectionRoutes]:
        return typing.cast(typing.Optional[VpnConnectionRoutes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VpnConnectionRoutes]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77232ca34c1f2302b3ab79192087c7a4e14fcad119192c221b09f1004c48c0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionTunnel1LogOptions",
    jsii_struct_bases=[],
    name_mapping={"cloudwatch_log_options": "cloudwatchLogOptions"},
)
class VpnConnectionTunnel1LogOptions:
    def __init__(
        self,
        *,
        cloudwatch_log_options: typing.Optional[typing.Union["VpnConnectionTunnel1LogOptionsCloudwatchLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_options: cloudwatch_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        if isinstance(cloudwatch_log_options, dict):
            cloudwatch_log_options = VpnConnectionTunnel1LogOptionsCloudwatchLogOptions(**cloudwatch_log_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2d49162cfd9860840f889ea10d4e9d3bafe8e37a76f3e0f4cec8b7154146a0)
            check_type(argname="argument cloudwatch_log_options", value=cloudwatch_log_options, expected_type=type_hints["cloudwatch_log_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_log_options is not None:
            self._values["cloudwatch_log_options"] = cloudwatch_log_options

    @builtins.property
    def cloudwatch_log_options(
        self,
    ) -> typing.Optional["VpnConnectionTunnel1LogOptionsCloudwatchLogOptions"]:
        '''cloudwatch_log_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        result = self._values.get("cloudwatch_log_options")
        return typing.cast(typing.Optional["VpnConnectionTunnel1LogOptionsCloudwatchLogOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionTunnel1LogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionTunnel1LogOptionsCloudwatchLogOptions",
    jsii_struct_bases=[],
    name_mapping={
        "bgp_log_enabled": "bgpLogEnabled",
        "bgp_log_group_arn": "bgpLogGroupArn",
        "bgp_log_output_format": "bgpLogOutputFormat",
        "log_enabled": "logEnabled",
        "log_group_arn": "logGroupArn",
        "log_output_format": "logOutputFormat",
    },
)
class VpnConnectionTunnel1LogOptionsCloudwatchLogOptions:
    def __init__(
        self,
        *,
        bgp_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_log_group_arn: typing.Optional[builtins.str] = None,
        bgp_log_output_format: typing.Optional[builtins.str] = None,
        log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_arn: typing.Optional[builtins.str] = None,
        log_output_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bgp_log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_enabled VpnConnection#bgp_log_enabled}.
        :param bgp_log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_group_arn VpnConnection#bgp_log_group_arn}.
        :param bgp_log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_output_format VpnConnection#bgp_log_output_format}.
        :param log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.
        :param log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e3fc0c50ca4b4470e976826042e1104269c0db960402b9c2077229e23eacd2)
            check_type(argname="argument bgp_log_enabled", value=bgp_log_enabled, expected_type=type_hints["bgp_log_enabled"])
            check_type(argname="argument bgp_log_group_arn", value=bgp_log_group_arn, expected_type=type_hints["bgp_log_group_arn"])
            check_type(argname="argument bgp_log_output_format", value=bgp_log_output_format, expected_type=type_hints["bgp_log_output_format"])
            check_type(argname="argument log_enabled", value=log_enabled, expected_type=type_hints["log_enabled"])
            check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            check_type(argname="argument log_output_format", value=log_output_format, expected_type=type_hints["log_output_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bgp_log_enabled is not None:
            self._values["bgp_log_enabled"] = bgp_log_enabled
        if bgp_log_group_arn is not None:
            self._values["bgp_log_group_arn"] = bgp_log_group_arn
        if bgp_log_output_format is not None:
            self._values["bgp_log_output_format"] = bgp_log_output_format
        if log_enabled is not None:
            self._values["log_enabled"] = log_enabled
        if log_group_arn is not None:
            self._values["log_group_arn"] = log_group_arn
        if log_output_format is not None:
            self._values["log_output_format"] = log_output_format

    @builtins.property
    def bgp_log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_enabled VpnConnection#bgp_log_enabled}.'''
        result = self._values.get("bgp_log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bgp_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_group_arn VpnConnection#bgp_log_group_arn}.'''
        result = self._values.get("bgp_log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bgp_log_output_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_output_format VpnConnection#bgp_log_output_format}.'''
        result = self._values.get("bgp_log_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.'''
        result = self._values.get("log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.'''
        result = self._values.get("log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_output_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.'''
        result = self._values.get("log_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionTunnel1LogOptionsCloudwatchLogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnConnectionTunnel1LogOptionsCloudwatchLogOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionTunnel1LogOptionsCloudwatchLogOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be57345ae21dee9fd7c120090920b4a19c5d8d961cfe7b3c86a61abf6079fc2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBgpLogEnabled")
    def reset_bgp_log_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpLogEnabled", []))

    @jsii.member(jsii_name="resetBgpLogGroupArn")
    def reset_bgp_log_group_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpLogGroupArn", []))

    @jsii.member(jsii_name="resetBgpLogOutputFormat")
    def reset_bgp_log_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpLogOutputFormat", []))

    @jsii.member(jsii_name="resetLogEnabled")
    def reset_log_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogEnabled", []))

    @jsii.member(jsii_name="resetLogGroupArn")
    def reset_log_group_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupArn", []))

    @jsii.member(jsii_name="resetLogOutputFormat")
    def reset_log_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogOutputFormat", []))

    @builtins.property
    @jsii.member(jsii_name="bgpLogEnabledInput")
    def bgp_log_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bgpLogEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpLogGroupArnInput")
    def bgp_log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bgpLogGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpLogOutputFormatInput")
    def bgp_log_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bgpLogOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="logEnabledInput")
    def log_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupArnInput")
    def log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logOutputFormatInput")
    def log_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpLogEnabled")
    def bgp_log_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bgpLogEnabled"))

    @bgp_log_enabled.setter
    def bgp_log_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176c481bc682be007b1c798c21f4155fb63109b5638273d274126d78d242a2c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpLogEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpLogGroupArn")
    def bgp_log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpLogGroupArn"))

    @bgp_log_group_arn.setter
    def bgp_log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a0ad19787b4290afcedcc9b1ca62a896cfbe1112f781f2cf0f4ce435dbd599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpLogGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpLogOutputFormat")
    def bgp_log_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpLogOutputFormat"))

    @bgp_log_output_format.setter
    def bgp_log_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6323a48561fb1da6a3224a2af433b099a04293f099756a85cd02ba93132247d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpLogOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logEnabled")
    def log_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logEnabled"))

    @log_enabled.setter
    def log_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f928319676f1364abbf064ab6e168d159aa5e00a825a7121987b7fff1af60d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @log_group_arn.setter
    def log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89590e514637f5d698ade8e666a17633ce3e725c3971cbfb27217a3d4d56735b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logOutputFormat")
    def log_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logOutputFormat"))

    @log_output_format.setter
    def log_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29503dc2fea89f3479ed983704ae8f150aa91738beb02566aeb75757aff409b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda4274c319abefc88185925790f149c68fb81226b2fe1bbf6e255e6aca59404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnConnectionTunnel1LogOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionTunnel1LogOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4952d81998c9bf2c9c83068da93736d933af943b6ce01a50b89d3dd758874dbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLogOptions")
    def put_cloudwatch_log_options(
        self,
        *,
        bgp_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_log_group_arn: typing.Optional[builtins.str] = None,
        bgp_log_output_format: typing.Optional[builtins.str] = None,
        log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_arn: typing.Optional[builtins.str] = None,
        log_output_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bgp_log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_enabled VpnConnection#bgp_log_enabled}.
        :param bgp_log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_group_arn VpnConnection#bgp_log_group_arn}.
        :param bgp_log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_output_format VpnConnection#bgp_log_output_format}.
        :param log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.
        :param log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.
        '''
        value = VpnConnectionTunnel1LogOptionsCloudwatchLogOptions(
            bgp_log_enabled=bgp_log_enabled,
            bgp_log_group_arn=bgp_log_group_arn,
            bgp_log_output_format=bgp_log_output_format,
            log_enabled=log_enabled,
            log_group_arn=log_group_arn,
            log_output_format=log_output_format,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogOptions", [value]))

    @jsii.member(jsii_name="resetCloudwatchLogOptions")
    def reset_cloudwatch_log_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogOptions", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogOptions")
    def cloudwatch_log_options(
        self,
    ) -> VpnConnectionTunnel1LogOptionsCloudwatchLogOptionsOutputReference:
        return typing.cast(VpnConnectionTunnel1LogOptionsCloudwatchLogOptionsOutputReference, jsii.get(self, "cloudwatchLogOptions"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogOptionsInput")
    def cloudwatch_log_options_input(
        self,
    ) -> typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions], jsii.get(self, "cloudwatchLogOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnConnectionTunnel1LogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel1LogOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnConnectionTunnel1LogOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936840d6271cd4eef942e62120786f56b3392ae5fd0a76e9e9b638d475b6eebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionTunnel2LogOptions",
    jsii_struct_bases=[],
    name_mapping={"cloudwatch_log_options": "cloudwatchLogOptions"},
)
class VpnConnectionTunnel2LogOptions:
    def __init__(
        self,
        *,
        cloudwatch_log_options: typing.Optional[typing.Union["VpnConnectionTunnel2LogOptionsCloudwatchLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_options: cloudwatch_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        if isinstance(cloudwatch_log_options, dict):
            cloudwatch_log_options = VpnConnectionTunnel2LogOptionsCloudwatchLogOptions(**cloudwatch_log_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7c6d3d46defe5da655a05c6ceb588663e77df4471080f29bdc5a67ebb9ba56)
            check_type(argname="argument cloudwatch_log_options", value=cloudwatch_log_options, expected_type=type_hints["cloudwatch_log_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_log_options is not None:
            self._values["cloudwatch_log_options"] = cloudwatch_log_options

    @builtins.property
    def cloudwatch_log_options(
        self,
    ) -> typing.Optional["VpnConnectionTunnel2LogOptionsCloudwatchLogOptions"]:
        '''cloudwatch_log_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        result = self._values.get("cloudwatch_log_options")
        return typing.cast(typing.Optional["VpnConnectionTunnel2LogOptionsCloudwatchLogOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionTunnel2LogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionTunnel2LogOptionsCloudwatchLogOptions",
    jsii_struct_bases=[],
    name_mapping={
        "bgp_log_enabled": "bgpLogEnabled",
        "bgp_log_group_arn": "bgpLogGroupArn",
        "bgp_log_output_format": "bgpLogOutputFormat",
        "log_enabled": "logEnabled",
        "log_group_arn": "logGroupArn",
        "log_output_format": "logOutputFormat",
    },
)
class VpnConnectionTunnel2LogOptionsCloudwatchLogOptions:
    def __init__(
        self,
        *,
        bgp_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_log_group_arn: typing.Optional[builtins.str] = None,
        bgp_log_output_format: typing.Optional[builtins.str] = None,
        log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_arn: typing.Optional[builtins.str] = None,
        log_output_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bgp_log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_enabled VpnConnection#bgp_log_enabled}.
        :param bgp_log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_group_arn VpnConnection#bgp_log_group_arn}.
        :param bgp_log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_output_format VpnConnection#bgp_log_output_format}.
        :param log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.
        :param log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ff1c7b80df48e8a561b24a61965387ae4cbab6574a2fa6084eda48903446e6)
            check_type(argname="argument bgp_log_enabled", value=bgp_log_enabled, expected_type=type_hints["bgp_log_enabled"])
            check_type(argname="argument bgp_log_group_arn", value=bgp_log_group_arn, expected_type=type_hints["bgp_log_group_arn"])
            check_type(argname="argument bgp_log_output_format", value=bgp_log_output_format, expected_type=type_hints["bgp_log_output_format"])
            check_type(argname="argument log_enabled", value=log_enabled, expected_type=type_hints["log_enabled"])
            check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            check_type(argname="argument log_output_format", value=log_output_format, expected_type=type_hints["log_output_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bgp_log_enabled is not None:
            self._values["bgp_log_enabled"] = bgp_log_enabled
        if bgp_log_group_arn is not None:
            self._values["bgp_log_group_arn"] = bgp_log_group_arn
        if bgp_log_output_format is not None:
            self._values["bgp_log_output_format"] = bgp_log_output_format
        if log_enabled is not None:
            self._values["log_enabled"] = log_enabled
        if log_group_arn is not None:
            self._values["log_group_arn"] = log_group_arn
        if log_output_format is not None:
            self._values["log_output_format"] = log_output_format

    @builtins.property
    def bgp_log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_enabled VpnConnection#bgp_log_enabled}.'''
        result = self._values.get("bgp_log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bgp_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_group_arn VpnConnection#bgp_log_group_arn}.'''
        result = self._values.get("bgp_log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bgp_log_output_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_output_format VpnConnection#bgp_log_output_format}.'''
        result = self._values.get("bgp_log_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.'''
        result = self._values.get("log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.'''
        result = self._values.get("log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_output_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.'''
        result = self._values.get("log_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionTunnel2LogOptionsCloudwatchLogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnConnectionTunnel2LogOptionsCloudwatchLogOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionTunnel2LogOptionsCloudwatchLogOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c64d051283f7d93cbccd4cc4be98689a6f9f3771b0eb15324579ce717df5f15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBgpLogEnabled")
    def reset_bgp_log_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpLogEnabled", []))

    @jsii.member(jsii_name="resetBgpLogGroupArn")
    def reset_bgp_log_group_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpLogGroupArn", []))

    @jsii.member(jsii_name="resetBgpLogOutputFormat")
    def reset_bgp_log_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpLogOutputFormat", []))

    @jsii.member(jsii_name="resetLogEnabled")
    def reset_log_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogEnabled", []))

    @jsii.member(jsii_name="resetLogGroupArn")
    def reset_log_group_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupArn", []))

    @jsii.member(jsii_name="resetLogOutputFormat")
    def reset_log_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogOutputFormat", []))

    @builtins.property
    @jsii.member(jsii_name="bgpLogEnabledInput")
    def bgp_log_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bgpLogEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpLogGroupArnInput")
    def bgp_log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bgpLogGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpLogOutputFormatInput")
    def bgp_log_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bgpLogOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="logEnabledInput")
    def log_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupArnInput")
    def log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logOutputFormatInput")
    def log_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpLogEnabled")
    def bgp_log_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bgpLogEnabled"))

    @bgp_log_enabled.setter
    def bgp_log_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57399963fe8c2fd83dfbedbf0c34dfbedebcda791733189fde369fe5e44517bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpLogEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpLogGroupArn")
    def bgp_log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpLogGroupArn"))

    @bgp_log_group_arn.setter
    def bgp_log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11fc2ba8001411ad983262072f4eac7c52c47014192cafc3d4a1e4fbecaf67c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpLogGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpLogOutputFormat")
    def bgp_log_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpLogOutputFormat"))

    @bgp_log_output_format.setter
    def bgp_log_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8575c2838dc3f34d5cf337f19408e10f5170fe79d9f3a2d34e7f7e7753cec389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpLogOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logEnabled")
    def log_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logEnabled"))

    @log_enabled.setter
    def log_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a21b68d64a196a2fee3b3865c01b45d94fe18db949a6e6d57b1158315428dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @log_group_arn.setter
    def log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8267641bdd27d7c57ece0db9e9b534438fc101e9fe204bcdaf400e2da2f6a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logOutputFormat")
    def log_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logOutputFormat"))

    @log_output_format.setter
    def log_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288858d525f0d6a36dcd6051d7084f85580b5467b2c45a3de0a9a2a8fc2b040b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9662048aecb9cae5370ff9310934210b773d2aeefcae56550a7ce662984e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnConnectionTunnel2LogOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionTunnel2LogOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20d66a28be84d4479effd26f63f5d30ffa2bca2ba943889921c507b0eacc8f99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLogOptions")
    def put_cloudwatch_log_options(
        self,
        *,
        bgp_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_log_group_arn: typing.Optional[builtins.str] = None,
        bgp_log_output_format: typing.Optional[builtins.str] = None,
        log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_arn: typing.Optional[builtins.str] = None,
        log_output_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bgp_log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_enabled VpnConnection#bgp_log_enabled}.
        :param bgp_log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_group_arn VpnConnection#bgp_log_group_arn}.
        :param bgp_log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#bgp_log_output_format VpnConnection#bgp_log_output_format}.
        :param log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.
        :param log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.
        '''
        value = VpnConnectionTunnel2LogOptionsCloudwatchLogOptions(
            bgp_log_enabled=bgp_log_enabled,
            bgp_log_group_arn=bgp_log_group_arn,
            bgp_log_output_format=bgp_log_output_format,
            log_enabled=log_enabled,
            log_group_arn=log_group_arn,
            log_output_format=log_output_format,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogOptions", [value]))

    @jsii.member(jsii_name="resetCloudwatchLogOptions")
    def reset_cloudwatch_log_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogOptions", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogOptions")
    def cloudwatch_log_options(
        self,
    ) -> VpnConnectionTunnel2LogOptionsCloudwatchLogOptionsOutputReference:
        return typing.cast(VpnConnectionTunnel2LogOptionsCloudwatchLogOptionsOutputReference, jsii.get(self, "cloudwatchLogOptions"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogOptionsInput")
    def cloudwatch_log_options_input(
        self,
    ) -> typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions], jsii.get(self, "cloudwatchLogOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnConnectionTunnel2LogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel2LogOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnConnectionTunnel2LogOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3f5285de97aeee2a6f0be46bdd54bd7885739f58456ba015c1540e34cd6730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionVgwTelemetry",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpnConnectionVgwTelemetry:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionVgwTelemetry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnConnectionVgwTelemetryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionVgwTelemetryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26fe707478389990909862a82842b61d84e90e01071d8d40f514e076ae22f404)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VpnConnectionVgwTelemetryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e21e8e6a3c56f3d5823be885a5811cf48455312ae94cd93c33df29016043ba9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnConnectionVgwTelemetryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829f3cfea37ad4b01db6e3fcb27f32ee09c764b5ba4b6f055a4d444b6e310f2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e9cad457208ace91c03997424e7f8f11f341e29fb4d591f393198f1fb1803bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e00d4a5c2219a5735d20e31db5e719fd3db04b57ef30dee5c50e2df23f93faa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VpnConnectionVgwTelemetryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.vpnConnection.VpnConnectionVgwTelemetryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc0d88a50ddf49462c1fc250ef154cf7209a239b9e655bef6d308a2a10e78296)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="acceptedRouteCount")
    def accepted_route_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceptedRouteCount"))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @builtins.property
    @jsii.member(jsii_name="lastStatusChange")
    def last_status_change(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastStatusChange"))

    @builtins.property
    @jsii.member(jsii_name="outsideIpAddress")
    def outside_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outsideIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusMessage")
    def status_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnConnectionVgwTelemetry]:
        return typing.cast(typing.Optional[VpnConnectionVgwTelemetry], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VpnConnectionVgwTelemetry]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5b5b5999f20f6a0083d95c47f36ad8eb377180ddd789f830dfe46b881ce225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VpnConnection",
    "VpnConnectionConfig",
    "VpnConnectionRoutes",
    "VpnConnectionRoutesList",
    "VpnConnectionRoutesOutputReference",
    "VpnConnectionTunnel1LogOptions",
    "VpnConnectionTunnel1LogOptionsCloudwatchLogOptions",
    "VpnConnectionTunnel1LogOptionsCloudwatchLogOptionsOutputReference",
    "VpnConnectionTunnel1LogOptionsOutputReference",
    "VpnConnectionTunnel2LogOptions",
    "VpnConnectionTunnel2LogOptionsCloudwatchLogOptions",
    "VpnConnectionTunnel2LogOptionsCloudwatchLogOptionsOutputReference",
    "VpnConnectionTunnel2LogOptionsOutputReference",
    "VpnConnectionVgwTelemetry",
    "VpnConnectionVgwTelemetryList",
    "VpnConnectionVgwTelemetryOutputReference",
]

publication.publish()

def _typecheckingstub__9cf5b5bd0f94b6a817dd05cec8e3f23038379303c360bef3445814d8b31bce3a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    customer_gateway_id: builtins.str,
    type: builtins.str,
    enable_acceleration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
    local_ipv6_network_cidr: typing.Optional[builtins.str] = None,
    outside_ip_address_type: typing.Optional[builtins.str] = None,
    preshared_key_storage: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
    remote_ipv6_network_cidr: typing.Optional[builtins.str] = None,
    static_routes_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    transit_gateway_id: typing.Optional[builtins.str] = None,
    transport_transit_gateway_attachment_id: typing.Optional[builtins.str] = None,
    tunnel1_dpd_timeout_action: typing.Optional[builtins.str] = None,
    tunnel1_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel1_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_inside_cidr: typing.Optional[builtins.str] = None,
    tunnel1_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
    tunnel1_log_options: typing.Optional[typing.Union[VpnConnectionTunnel1LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel1_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel1_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel1_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_preshared_key: typing.Optional[builtins.str] = None,
    tunnel1_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
    tunnel1_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_replay_window_size: typing.Optional[jsii.Number] = None,
    tunnel1_startup_action: typing.Optional[builtins.str] = None,
    tunnel2_dpd_timeout_action: typing.Optional[builtins.str] = None,
    tunnel2_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel2_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_inside_cidr: typing.Optional[builtins.str] = None,
    tunnel2_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
    tunnel2_log_options: typing.Optional[typing.Union[VpnConnectionTunnel2LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel2_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel2_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel2_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_preshared_key: typing.Optional[builtins.str] = None,
    tunnel2_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
    tunnel2_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_replay_window_size: typing.Optional[jsii.Number] = None,
    tunnel2_startup_action: typing.Optional[builtins.str] = None,
    tunnel_bandwidth: typing.Optional[builtins.str] = None,
    tunnel_inside_ip_version: typing.Optional[builtins.str] = None,
    vpn_concentrator_id: typing.Optional[builtins.str] = None,
    vpn_gateway_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__bcbf9258d7691b9f16e0c348336f1c26ef869ceebed3ca795318fda9652aae0f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82bf7eae2b34786903060a10e663dd69164c40f6dc5306f0a831dfb00d474279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b9a5c025e15c50d2fbdbf410010363c45dbe54c7e0a8a55703865c4617a33f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4013f07f45f0eccca47e62140ba98447d5fea36b2a992f0087cce04aa155f95d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf81778b7d69ffa56535657d890e9167d72994f22ee23a5e799e91c8d5e4eef3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf96d4a7c3d2dfbf9e1530584a1b42bcf8489e9359879a1779a97e69c3495960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68ff1a000e7b4d198548f03e3d22df32d78725022a2ffd58ab770afa3bfefae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fd8fd10a8b6e9ef77d2203d3e330cdbbc0a953f375386201395a751f6720af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f1250c365fb5c42d24df7ca903e20c02a78235b329e438de2964eb6eeeb560(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e3b4a7bf13a092b6a722bd0a4818efbaff620d4b31d72e0f1e4745ae460a84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a974f696313fd5d1e8cfb400ecc52a2736b5f0426ce1d0383bb6c21cdb5466b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b82d5e2b66992ef1337a867a4059b642ef95186e7240c96868f33d553293850(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feaeccddc7160b8fb9dee941568492b511c207238e431b3f8f249200d349eea1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f28afa51ab99c953afc1054aaa369bc9c53e8a8d10ccefbf9e19f83d33c4c49(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde333cdf5709927c2ee9a7df680cbb963cf7255fbf2734cfcf9beeb49387c6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4052dfda7630f80d33873163ffc10115a2b69c62e51d3a62bed046483a8952b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e37b8ce5ece52a4b301cbc18a81e07dcb0066911d479beea89ec641735e9df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8081f4e5868a4623118985cd0da7abb1c7bec3ec1578fc6bd766ea2997cc924a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20849a621872c2881a05f2a492230c2ac369360d212f8cfe80862640e174d5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5530b0c3aa0872741fb50b1c5640c63ac27130be7906a53244eb16647aa3f7b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b2c7d7d7ea3b4f9720aaaf4d4dfecf6da96593ce63d759c9ab8ff489f17df9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582257578120336e7f4d9a1015ea1750285345bfe55a67f569b9314a7171cc6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d10ff4b1d53d8b91118d2f1893569e4c45ed613bcd361b068b1ec96d02e4e4(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5067f4a1faf9460809d79cb741e38f35527eca147859c43d301cbfdf38527dd4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe617d131da79340fe31a5bf67888ab3325c11bead4704b179a317dc21cb1b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722854eb09f06751db11f0ca1ed8a933aaeea52d25c3a9b01e7f3960aafdb688(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5988126885aeca6b265d4563b2f3b4a5407c4db23b5084819081e7e00bc61b(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79b715525af0afdaf758ef02c67f17d80eede957e23c120002094224969b382(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c36b3f6cb7775882b15f963a5c04e183ad952ecafd0999b1443591b05ff766(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f624574ac0cf2f9168da91ef1326574aa880d38db16c44487078b9fb75149c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804f236e3c0b5475e69ce09eb9ef0e4fc7d51339d7f6e0ee2ddcf4ed536336f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849da896aa90a71f83802e29c3355b498bacb8d50117f061c175c5557b910a6e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0661e85d5ecf13256e0caa524f6ca2dc8454cb9778361a7c5f0d515d0754f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08bd1e53bde771f4f7db8e6b50e52b25585e8457efd0cba9a97ad7182dc2139(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbc92f1bef8eeeb97d9a90b935f811d6ff57ec47728b795b37a3f38fbc5677f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b183813e3af228f382449240b807926b47394a6d4e3233c420948e9686cfa890(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e907b5163ee422fad85fac87dd0e0d889e5ecb160c5980c8517b6d55e7878b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3242a323ba4a2f5729b650f33aa713728123d07b77a2ed4dd89d8d8b6a3d3083(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760bdc480e65383f61d0850bb0231b422d588d187c3f53d6612900c9fcfb66cf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796e86597330bd6299b67b76a4efe432f44407a16252119816ea6746842b9452(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630f1c52f6ec908c1134b0d306335f6f7f1d897c14230d7f1e9f21e42b8fa807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538c2b944ffc84a9942a9ec814b6876fa2b681f8478ae43f09460be6e5f10389(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb37a696e976b5589eaabd58ccaab2823a677a4d5ca45f8ec874757686cdb18e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e26fb3e77458dc2aa629e5d7c0ba9326879393005512199545daa63f6a9b451(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff243aa66ad9b2bc0515f01de2f5af3786fa031930e8c5d3deaf27754adc8b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446e7e613120deef52a81e267d8b30d388ed9944a7825c95f7d381169531efc1(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7405e08dc7d7b602df3000efff3a150b56aa65d58cccb5bf80c4afd3e3b26a14(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb51c48701b822549594e4369d41a31c209424f7b36efb86b3362005852ee7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dedc6c3a2217796603cac7b0aa63dd59516ec10333a3bf61c329a02a1661abee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febd839acf4082a2c7bee87f62b1b61786f7a4beff7fdea5b588b738563f0b0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd8b0257348cde101fd00aeadf5ca2538ad88f9dad1172c9a8cfa8a250a6e44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92bb9af14cdcebfb1a8d2c976428258fff197de1bc18521070ef3120d938677b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf283db36747392986d14cdbb381c59e2f0ef3fb6e40e1cc3ad8815a5f5f045f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99420354c7fa01fcfece7c5815ba9d3d39e3cddcd61a8a4e32f9d64b31bf3ab3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be338833c795eb205951291231479f97d229ffdcee09e6d3a450e2903722b47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb544aaf518930aeac69132b5503050ce394c44eed30280856ea7c7909bb2a59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998250c1359d2c194fbcf9cf5d80dbdc0c8ac391b4c314d33993b25dc81869b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e51939d32cc34ddb1a7744cae29eb7af2ffbba60cc202e30390289445a4d3b10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfe1217b45ff8aebb3357e74e1178357a0e4b5ff1b8a20dbfb597147cc4de09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d539dfcb5f5046b37c3d1fc83a34eaee535c0e69e96cc154206a9755063b0e6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    customer_gateway_id: builtins.str,
    type: builtins.str,
    enable_acceleration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
    local_ipv6_network_cidr: typing.Optional[builtins.str] = None,
    outside_ip_address_type: typing.Optional[builtins.str] = None,
    preshared_key_storage: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
    remote_ipv6_network_cidr: typing.Optional[builtins.str] = None,
    static_routes_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    transit_gateway_id: typing.Optional[builtins.str] = None,
    transport_transit_gateway_attachment_id: typing.Optional[builtins.str] = None,
    tunnel1_dpd_timeout_action: typing.Optional[builtins.str] = None,
    tunnel1_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel1_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_inside_cidr: typing.Optional[builtins.str] = None,
    tunnel1_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
    tunnel1_log_options: typing.Optional[typing.Union[VpnConnectionTunnel1LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel1_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel1_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel1_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_preshared_key: typing.Optional[builtins.str] = None,
    tunnel1_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
    tunnel1_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_replay_window_size: typing.Optional[jsii.Number] = None,
    tunnel1_startup_action: typing.Optional[builtins.str] = None,
    tunnel2_dpd_timeout_action: typing.Optional[builtins.str] = None,
    tunnel2_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel2_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_inside_cidr: typing.Optional[builtins.str] = None,
    tunnel2_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
    tunnel2_log_options: typing.Optional[typing.Union[VpnConnectionTunnel2LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel2_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel2_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel2_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_preshared_key: typing.Optional[builtins.str] = None,
    tunnel2_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
    tunnel2_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_replay_window_size: typing.Optional[jsii.Number] = None,
    tunnel2_startup_action: typing.Optional[builtins.str] = None,
    tunnel_bandwidth: typing.Optional[builtins.str] = None,
    tunnel_inside_ip_version: typing.Optional[builtins.str] = None,
    vpn_concentrator_id: typing.Optional[builtins.str] = None,
    vpn_gateway_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5f38012187b6b2a24dbb249b06f2ed709f461ab899f7d0705f9cf304b2654e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14cb20f1c3256fdc37c43d2df2c637d7a45606bfaf19778c5718679f7f58a57(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c2f1ca7f271a38fc4e59fc2bbfa1dd912c7f7766c4c1307ec666e5f663eb6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe26d745dfac0c860a3629633afa4beaa7abf4578a7c58b4eda5974b51c64760(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f148b16355d4595653a2dc0a5232d7c809b369212091b614b8395427f2123e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a0a030168475c901c032d09f9029ef67ef3066c5e82f7c8c0316aa6b65c8fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77232ca34c1f2302b3ab79192087c7a4e14fcad119192c221b09f1004c48c0a(
    value: typing.Optional[VpnConnectionRoutes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2d49162cfd9860840f889ea10d4e9d3bafe8e37a76f3e0f4cec8b7154146a0(
    *,
    cloudwatch_log_options: typing.Optional[typing.Union[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e3fc0c50ca4b4470e976826042e1104269c0db960402b9c2077229e23eacd2(
    *,
    bgp_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bgp_log_group_arn: typing.Optional[builtins.str] = None,
    bgp_log_output_format: typing.Optional[builtins.str] = None,
    log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_arn: typing.Optional[builtins.str] = None,
    log_output_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be57345ae21dee9fd7c120090920b4a19c5d8d961cfe7b3c86a61abf6079fc2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176c481bc682be007b1c798c21f4155fb63109b5638273d274126d78d242a2c4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a0ad19787b4290afcedcc9b1ca62a896cfbe1112f781f2cf0f4ce435dbd599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6323a48561fb1da6a3224a2af433b099a04293f099756a85cd02ba93132247d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f928319676f1364abbf064ab6e168d159aa5e00a825a7121987b7fff1af60d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89590e514637f5d698ade8e666a17633ce3e725c3971cbfb27217a3d4d56735b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29503dc2fea89f3479ed983704ae8f150aa91738beb02566aeb75757aff409b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda4274c319abefc88185925790f149c68fb81226b2fe1bbf6e255e6aca59404(
    value: typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4952d81998c9bf2c9c83068da93736d933af943b6ce01a50b89d3dd758874dbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936840d6271cd4eef942e62120786f56b3392ae5fd0a76e9e9b638d475b6eebd(
    value: typing.Optional[VpnConnectionTunnel1LogOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7c6d3d46defe5da655a05c6ceb588663e77df4471080f29bdc5a67ebb9ba56(
    *,
    cloudwatch_log_options: typing.Optional[typing.Union[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ff1c7b80df48e8a561b24a61965387ae4cbab6574a2fa6084eda48903446e6(
    *,
    bgp_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bgp_log_group_arn: typing.Optional[builtins.str] = None,
    bgp_log_output_format: typing.Optional[builtins.str] = None,
    log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_arn: typing.Optional[builtins.str] = None,
    log_output_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c64d051283f7d93cbccd4cc4be98689a6f9f3771b0eb15324579ce717df5f15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57399963fe8c2fd83dfbedbf0c34dfbedebcda791733189fde369fe5e44517bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11fc2ba8001411ad983262072f4eac7c52c47014192cafc3d4a1e4fbecaf67c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8575c2838dc3f34d5cf337f19408e10f5170fe79d9f3a2d34e7f7e7753cec389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a21b68d64a196a2fee3b3865c01b45d94fe18db949a6e6d57b1158315428dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8267641bdd27d7c57ece0db9e9b534438fc101e9fe204bcdaf400e2da2f6a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288858d525f0d6a36dcd6051d7084f85580b5467b2c45a3de0a9a2a8fc2b040b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9662048aecb9cae5370ff9310934210b773d2aeefcae56550a7ce662984e2d(
    value: typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d66a28be84d4479effd26f63f5d30ffa2bca2ba943889921c507b0eacc8f99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3f5285de97aeee2a6f0be46bdd54bd7885739f58456ba015c1540e34cd6730(
    value: typing.Optional[VpnConnectionTunnel2LogOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fe707478389990909862a82842b61d84e90e01071d8d40f514e076ae22f404(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e21e8e6a3c56f3d5823be885a5811cf48455312ae94cd93c33df29016043ba9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829f3cfea37ad4b01db6e3fcb27f32ee09c764b5ba4b6f055a4d444b6e310f2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9cad457208ace91c03997424e7f8f11f341e29fb4d591f393198f1fb1803bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00d4a5c2219a5735d20e31db5e719fd3db04b57ef30dee5c50e2df23f93faa1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0d88a50ddf49462c1fc250ef154cf7209a239b9e655bef6d308a2a10e78296(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5b5b5999f20f6a0083d95c47f36ad8eb377180ddd789f830dfe46b881ce225(
    value: typing.Optional[VpnConnectionVgwTelemetry],
) -> None:
    """Type checking stubs"""
    pass
