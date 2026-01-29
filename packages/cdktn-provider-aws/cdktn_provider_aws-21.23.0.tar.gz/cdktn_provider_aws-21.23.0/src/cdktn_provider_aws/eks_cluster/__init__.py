r'''
# `aws_eks_cluster`

Refer to the Terraform Registry for docs: [`aws_eks_cluster`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster).
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


class EksCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster aws_eks_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        role_arn: builtins.str,
        vpc_config: typing.Union["EksClusterVpcConfig", typing.Dict[builtins.str, typing.Any]],
        access_config: typing.Optional[typing.Union["EksClusterAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bootstrap_self_managed_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        compute_config: typing.Optional[typing.Union["EksClusterComputeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane_scaling_config: typing.Optional[typing.Union["EksClusterControlPlaneScalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled_cluster_log_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        encryption_config: typing.Optional[typing.Union["EksClusterEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        force_update_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes_network_config: typing.Optional[typing.Union["EksClusterKubernetesNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        outpost_config: typing.Optional[typing.Union["EksClusterOutpostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        remote_network_config: typing.Optional[typing.Union["EksClusterRemoteNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_config: typing.Optional[typing.Union["EksClusterStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EksClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["EksClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        zonal_shift_config: typing.Optional[typing.Union["EksClusterZonalShiftConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster aws_eks_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#name EksCluster#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#role_arn EksCluster#role_arn}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#vpc_config EksCluster#vpc_config}
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#access_config EksCluster#access_config}
        :param bootstrap_self_managed_addons: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#bootstrap_self_managed_addons EksCluster#bootstrap_self_managed_addons}.
        :param compute_config: compute_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#compute_config EksCluster#compute_config}
        :param control_plane_scaling_config: control_plane_scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#control_plane_scaling_config EksCluster#control_plane_scaling_config}
        :param deletion_protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#deletion_protection EksCluster#deletion_protection}.
        :param enabled_cluster_log_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled_cluster_log_types EksCluster#enabled_cluster_log_types}.
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#encryption_config EksCluster#encryption_config}
        :param force_update_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#force_update_version EksCluster#force_update_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#id EksCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes_network_config: kubernetes_network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#kubernetes_network_config EksCluster#kubernetes_network_config}
        :param outpost_config: outpost_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#outpost_config EksCluster#outpost_config}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#region EksCluster#region}
        :param remote_network_config: remote_network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#remote_network_config EksCluster#remote_network_config}
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#storage_config EksCluster#storage_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#tags EksCluster#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#tags_all EksCluster#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#timeouts EksCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#upgrade_policy EksCluster#upgrade_policy}
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#version EksCluster#version}.
        :param zonal_shift_config: zonal_shift_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#zonal_shift_config EksCluster#zonal_shift_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67133bc8fbfdf04570dcf8057cadd6bbfbeed17df985ce70f85c89e56ac21bf9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EksClusterConfig(
            name=name,
            role_arn=role_arn,
            vpc_config=vpc_config,
            access_config=access_config,
            bootstrap_self_managed_addons=bootstrap_self_managed_addons,
            compute_config=compute_config,
            control_plane_scaling_config=control_plane_scaling_config,
            deletion_protection=deletion_protection,
            enabled_cluster_log_types=enabled_cluster_log_types,
            encryption_config=encryption_config,
            force_update_version=force_update_version,
            id=id,
            kubernetes_network_config=kubernetes_network_config,
            outpost_config=outpost_config,
            region=region,
            remote_network_config=remote_network_config,
            storage_config=storage_config,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            upgrade_policy=upgrade_policy,
            version=version,
            zonal_shift_config=zonal_shift_config,
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
        '''Generates CDKTF code for importing a EksCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EksCluster to import.
        :param import_from_id: The id of the existing EksCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EksCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da21b767bd48ae16f9d7e86b612aec4695b2db0946043915a70d73230416414)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        *,
        authentication_mode: typing.Optional[builtins.str] = None,
        bootstrap_cluster_creator_admin_permissions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param authentication_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#authentication_mode EksCluster#authentication_mode}.
        :param bootstrap_cluster_creator_admin_permissions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#bootstrap_cluster_creator_admin_permissions EksCluster#bootstrap_cluster_creator_admin_permissions}.
        '''
        value = EksClusterAccessConfig(
            authentication_mode=authentication_mode,
            bootstrap_cluster_creator_admin_permissions=bootstrap_cluster_creator_admin_permissions,
        )

        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="putComputeConfig")
    def put_compute_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        node_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        node_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.
        :param node_pools: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#node_pools EksCluster#node_pools}.
        :param node_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#node_role_arn EksCluster#node_role_arn}.
        '''
        value = EksClusterComputeConfig(
            enabled=enabled, node_pools=node_pools, node_role_arn=node_role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putComputeConfig", [value]))

    @jsii.member(jsii_name="putControlPlaneScalingConfig")
    def put_control_plane_scaling_config(
        self,
        *,
        tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#tier EksCluster#tier}.
        '''
        value = EksClusterControlPlaneScalingConfig(tier=tier)

        return typing.cast(None, jsii.invoke(self, "putControlPlaneScalingConfig", [value]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        provider: typing.Union["EksClusterEncryptionConfigProvider", typing.Dict[builtins.str, typing.Any]],
        resources: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param provider: provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#provider EksCluster#provider}
        :param resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#resources EksCluster#resources}.
        '''
        value = EksClusterEncryptionConfig(provider=provider, resources=resources)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putKubernetesNetworkConfig")
    def put_kubernetes_network_config(
        self,
        *,
        elastic_load_balancing: typing.Optional[typing.Union["EksClusterKubernetesNetworkConfigElasticLoadBalancing", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_family: typing.Optional[builtins.str] = None,
        service_ipv4_cidr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param elastic_load_balancing: elastic_load_balancing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#elastic_load_balancing EksCluster#elastic_load_balancing}
        :param ip_family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#ip_family EksCluster#ip_family}.
        :param service_ipv4_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#service_ipv4_cidr EksCluster#service_ipv4_cidr}.
        '''
        value = EksClusterKubernetesNetworkConfig(
            elastic_load_balancing=elastic_load_balancing,
            ip_family=ip_family,
            service_ipv4_cidr=service_ipv4_cidr,
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetesNetworkConfig", [value]))

    @jsii.member(jsii_name="putOutpostConfig")
    def put_outpost_config(
        self,
        *,
        control_plane_instance_type: builtins.str,
        outpost_arns: typing.Sequence[builtins.str],
        control_plane_placement: typing.Optional[typing.Union["EksClusterOutpostConfigControlPlanePlacement", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#control_plane_instance_type EksCluster#control_plane_instance_type}.
        :param outpost_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#outpost_arns EksCluster#outpost_arns}.
        :param control_plane_placement: control_plane_placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#control_plane_placement EksCluster#control_plane_placement}
        '''
        value = EksClusterOutpostConfig(
            control_plane_instance_type=control_plane_instance_type,
            outpost_arns=outpost_arns,
            control_plane_placement=control_plane_placement,
        )

        return typing.cast(None, jsii.invoke(self, "putOutpostConfig", [value]))

    @jsii.member(jsii_name="putRemoteNetworkConfig")
    def put_remote_network_config(
        self,
        *,
        remote_node_networks: typing.Union["EksClusterRemoteNetworkConfigRemoteNodeNetworks", typing.Dict[builtins.str, typing.Any]],
        remote_pod_networks: typing.Optional[typing.Union["EksClusterRemoteNetworkConfigRemotePodNetworks", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param remote_node_networks: remote_node_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#remote_node_networks EksCluster#remote_node_networks}
        :param remote_pod_networks: remote_pod_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#remote_pod_networks EksCluster#remote_pod_networks}
        '''
        value = EksClusterRemoteNetworkConfig(
            remote_node_networks=remote_node_networks,
            remote_pod_networks=remote_pod_networks,
        )

        return typing.cast(None, jsii.invoke(self, "putRemoteNetworkConfig", [value]))

    @jsii.member(jsii_name="putStorageConfig")
    def put_storage_config(
        self,
        *,
        block_storage: typing.Optional[typing.Union["EksClusterStorageConfigBlockStorage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param block_storage: block_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#block_storage EksCluster#block_storage}
        '''
        value = EksClusterStorageConfig(block_storage=block_storage)

        return typing.cast(None, jsii.invoke(self, "putStorageConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#create EksCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#delete EksCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#update EksCluster#update}.
        '''
        value = EksClusterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpgradePolicy")
    def put_upgrade_policy(
        self,
        *,
        support_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param support_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#support_type EksCluster#support_type}.
        '''
        value = EksClusterUpgradePolicy(support_type=support_type)

        return typing.cast(None, jsii.invoke(self, "putUpgradePolicy", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        subnet_ids: typing.Sequence[builtins.str],
        endpoint_private_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_public_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_access_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#subnet_ids EksCluster#subnet_ids}.
        :param endpoint_private_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#endpoint_private_access EksCluster#endpoint_private_access}.
        :param endpoint_public_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#endpoint_public_access EksCluster#endpoint_public_access}.
        :param public_access_cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#public_access_cidrs EksCluster#public_access_cidrs}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#security_group_ids EksCluster#security_group_ids}.
        '''
        value = EksClusterVpcConfig(
            subnet_ids=subnet_ids,
            endpoint_private_access=endpoint_private_access,
            endpoint_public_access=endpoint_public_access,
            public_access_cidrs=public_access_cidrs,
            security_group_ids=security_group_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="putZonalShiftConfig")
    def put_zonal_shift_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.
        '''
        value = EksClusterZonalShiftConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putZonalShiftConfig", [value]))

    @jsii.member(jsii_name="resetAccessConfig")
    def reset_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessConfig", []))

    @jsii.member(jsii_name="resetBootstrapSelfManagedAddons")
    def reset_bootstrap_self_managed_addons(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootstrapSelfManagedAddons", []))

    @jsii.member(jsii_name="resetComputeConfig")
    def reset_compute_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeConfig", []))

    @jsii.member(jsii_name="resetControlPlaneScalingConfig")
    def reset_control_plane_scaling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneScalingConfig", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetEnabledClusterLogTypes")
    def reset_enabled_cluster_log_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabledClusterLogTypes", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetForceUpdateVersion")
    def reset_force_update_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceUpdateVersion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKubernetesNetworkConfig")
    def reset_kubernetes_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesNetworkConfig", []))

    @jsii.member(jsii_name="resetOutpostConfig")
    def reset_outpost_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutpostConfig", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRemoteNetworkConfig")
    def reset_remote_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteNetworkConfig", []))

    @jsii.member(jsii_name="resetStorageConfig")
    def reset_storage_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpgradePolicy")
    def reset_upgrade_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradePolicy", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetZonalShiftConfig")
    def reset_zonal_shift_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZonalShiftConfig", []))

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
    @jsii.member(jsii_name="accessConfig")
    def access_config(self) -> "EksClusterAccessConfigOutputReference":
        return typing.cast("EksClusterAccessConfigOutputReference", jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthority")
    def certificate_authority(self) -> "EksClusterCertificateAuthorityList":
        return typing.cast("EksClusterCertificateAuthorityList", jsii.get(self, "certificateAuthority"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @builtins.property
    @jsii.member(jsii_name="computeConfig")
    def compute_config(self) -> "EksClusterComputeConfigOutputReference":
        return typing.cast("EksClusterComputeConfigOutputReference", jsii.get(self, "computeConfig"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneScalingConfig")
    def control_plane_scaling_config(
        self,
    ) -> "EksClusterControlPlaneScalingConfigOutputReference":
        return typing.cast("EksClusterControlPlaneScalingConfigOutputReference", jsii.get(self, "controlPlaneScalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(self) -> "EksClusterEncryptionConfigOutputReference":
        return typing.cast("EksClusterEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "EksClusterIdentityList":
        return typing.cast("EksClusterIdentityList", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesNetworkConfig")
    def kubernetes_network_config(
        self,
    ) -> "EksClusterKubernetesNetworkConfigOutputReference":
        return typing.cast("EksClusterKubernetesNetworkConfigOutputReference", jsii.get(self, "kubernetesNetworkConfig"))

    @builtins.property
    @jsii.member(jsii_name="outpostConfig")
    def outpost_config(self) -> "EksClusterOutpostConfigOutputReference":
        return typing.cast("EksClusterOutpostConfigOutputReference", jsii.get(self, "outpostConfig"))

    @builtins.property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformVersion"))

    @builtins.property
    @jsii.member(jsii_name="remoteNetworkConfig")
    def remote_network_config(self) -> "EksClusterRemoteNetworkConfigOutputReference":
        return typing.cast("EksClusterRemoteNetworkConfigOutputReference", jsii.get(self, "remoteNetworkConfig"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storageConfig")
    def storage_config(self) -> "EksClusterStorageConfigOutputReference":
        return typing.cast("EksClusterStorageConfigOutputReference", jsii.get(self, "storageConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EksClusterTimeoutsOutputReference":
        return typing.cast("EksClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="upgradePolicy")
    def upgrade_policy(self) -> "EksClusterUpgradePolicyOutputReference":
        return typing.cast("EksClusterUpgradePolicyOutputReference", jsii.get(self, "upgradePolicy"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> "EksClusterVpcConfigOutputReference":
        return typing.cast("EksClusterVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="zonalShiftConfig")
    def zonal_shift_config(self) -> "EksClusterZonalShiftConfigOutputReference":
        return typing.cast("EksClusterZonalShiftConfigOutputReference", jsii.get(self, "zonalShiftConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(self) -> typing.Optional["EksClusterAccessConfig"]:
        return typing.cast(typing.Optional["EksClusterAccessConfig"], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapSelfManagedAddonsInput")
    def bootstrap_self_managed_addons_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bootstrapSelfManagedAddonsInput"))

    @builtins.property
    @jsii.member(jsii_name="computeConfigInput")
    def compute_config_input(self) -> typing.Optional["EksClusterComputeConfig"]:
        return typing.cast(typing.Optional["EksClusterComputeConfig"], jsii.get(self, "computeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneScalingConfigInput")
    def control_plane_scaling_config_input(
        self,
    ) -> typing.Optional["EksClusterControlPlaneScalingConfig"]:
        return typing.cast(typing.Optional["EksClusterControlPlaneScalingConfig"], jsii.get(self, "controlPlaneScalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledClusterLogTypesInput")
    def enabled_cluster_log_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enabledClusterLogTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(self) -> typing.Optional["EksClusterEncryptionConfig"]:
        return typing.cast(typing.Optional["EksClusterEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdateVersionInput")
    def force_update_version_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceUpdateVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesNetworkConfigInput")
    def kubernetes_network_config_input(
        self,
    ) -> typing.Optional["EksClusterKubernetesNetworkConfig"]:
        return typing.cast(typing.Optional["EksClusterKubernetesNetworkConfig"], jsii.get(self, "kubernetesNetworkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outpostConfigInput")
    def outpost_config_input(self) -> typing.Optional["EksClusterOutpostConfig"]:
        return typing.cast(typing.Optional["EksClusterOutpostConfig"], jsii.get(self, "outpostConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteNetworkConfigInput")
    def remote_network_config_input(
        self,
    ) -> typing.Optional["EksClusterRemoteNetworkConfig"]:
        return typing.cast(typing.Optional["EksClusterRemoteNetworkConfig"], jsii.get(self, "remoteNetworkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="storageConfigInput")
    def storage_config_input(self) -> typing.Optional["EksClusterStorageConfig"]:
        return typing.cast(typing.Optional["EksClusterStorageConfig"], jsii.get(self, "storageConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EksClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EksClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradePolicyInput")
    def upgrade_policy_input(self) -> typing.Optional["EksClusterUpgradePolicy"]:
        return typing.cast(typing.Optional["EksClusterUpgradePolicy"], jsii.get(self, "upgradePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(self) -> typing.Optional["EksClusterVpcConfig"]:
        return typing.cast(typing.Optional["EksClusterVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="zonalShiftConfigInput")
    def zonal_shift_config_input(self) -> typing.Optional["EksClusterZonalShiftConfig"]:
        return typing.cast(typing.Optional["EksClusterZonalShiftConfig"], jsii.get(self, "zonalShiftConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapSelfManagedAddons")
    def bootstrap_self_managed_addons(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bootstrapSelfManagedAddons"))

    @bootstrap_self_managed_addons.setter
    def bootstrap_self_managed_addons(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6603a1a9d75953b0f22bc89037b0c517bd324e8c32225754a723825bee8bba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootstrapSelfManagedAddons", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432b3f96d19de939303b88a20ede13b5e96cf671b0cc74196fe53c5645475a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabledClusterLogTypes")
    def enabled_cluster_log_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enabledClusterLogTypes"))

    @enabled_cluster_log_types.setter
    def enabled_cluster_log_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca183cc71921358c4578ec29981b1a2a59b365cbea634c43d4fb19cea3b372a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabledClusterLogTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceUpdateVersion")
    def force_update_version(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceUpdateVersion"))

    @force_update_version.setter
    def force_update_version(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517be2bbcf5fce731dcfd57c9a0b3c1111f49fabe8f9ded632ebb3182a7c452c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdateVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fec0e99bfe2f962fce410795987a191454102f5568b32919276dbcd7c895e9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0db287ae54aa7ea3d977c716ecefd5317438fe173163e577d4a8c32d59bea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91054a5a1b97afd6427f5cccb28fdf4d148a56e0db5d1792152a175d4fb4044c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e3a1284beed4b6275002e4a94c389a4cc1eb968574c9f092534fa1c7cc9166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c18def6e9b5e5985e745133024ed968d351cbee7290a1efa019b2cba751105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44004caef6c31a45646a84b80a5230de2a2e6b112c816b6a854cf67323963cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a608235eba80729f5cee0aa4fa4685b0ce4055e2b7122a659edc8fe3213ec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterAccessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_mode": "authenticationMode",
        "bootstrap_cluster_creator_admin_permissions": "bootstrapClusterCreatorAdminPermissions",
    },
)
class EksClusterAccessConfig:
    def __init__(
        self,
        *,
        authentication_mode: typing.Optional[builtins.str] = None,
        bootstrap_cluster_creator_admin_permissions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param authentication_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#authentication_mode EksCluster#authentication_mode}.
        :param bootstrap_cluster_creator_admin_permissions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#bootstrap_cluster_creator_admin_permissions EksCluster#bootstrap_cluster_creator_admin_permissions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618278714d42a51347b205fd4a247f05e912322646b1f07b8cf20b194c76b507)
            check_type(argname="argument authentication_mode", value=authentication_mode, expected_type=type_hints["authentication_mode"])
            check_type(argname="argument bootstrap_cluster_creator_admin_permissions", value=bootstrap_cluster_creator_admin_permissions, expected_type=type_hints["bootstrap_cluster_creator_admin_permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_mode is not None:
            self._values["authentication_mode"] = authentication_mode
        if bootstrap_cluster_creator_admin_permissions is not None:
            self._values["bootstrap_cluster_creator_admin_permissions"] = bootstrap_cluster_creator_admin_permissions

    @builtins.property
    def authentication_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#authentication_mode EksCluster#authentication_mode}.'''
        result = self._values.get("authentication_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bootstrap_cluster_creator_admin_permissions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#bootstrap_cluster_creator_admin_permissions EksCluster#bootstrap_cluster_creator_admin_permissions}.'''
        result = self._values.get("bootstrap_cluster_creator_admin_permissions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33503bc01bf8cfbe70ac1782a863ad555840190bd8611ab6c1f875f1edcbfc6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthenticationMode")
    def reset_authentication_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationMode", []))

    @jsii.member(jsii_name="resetBootstrapClusterCreatorAdminPermissions")
    def reset_bootstrap_cluster_creator_admin_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootstrapClusterCreatorAdminPermissions", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationModeInput")
    def authentication_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapClusterCreatorAdminPermissionsInput")
    def bootstrap_cluster_creator_admin_permissions_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bootstrapClusterCreatorAdminPermissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationMode")
    def authentication_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationMode"))

    @authentication_mode.setter
    def authentication_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40dd87f52185905a3bb05a700683ee25a29f0b37c54ece58d88e3f89e9ed447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootstrapClusterCreatorAdminPermissions")
    def bootstrap_cluster_creator_admin_permissions(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bootstrapClusterCreatorAdminPermissions"))

    @bootstrap_cluster_creator_admin_permissions.setter
    def bootstrap_cluster_creator_admin_permissions(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e838caca75bd9395882bf406f9a3e6d4155a6c0a591140f7a21268540563ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootstrapClusterCreatorAdminPermissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterAccessConfig]:
        return typing.cast(typing.Optional[EksClusterAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterAccessConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65e54648a95c238b548d69e1aa140b519176f4d61affe86fbafbd55bdd953c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterCertificateAuthority",
    jsii_struct_bases=[],
    name_mapping={},
)
class EksClusterCertificateAuthority:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterCertificateAuthority(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterCertificateAuthorityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterCertificateAuthorityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f81da356d543b5107d68f10ef5e78868e30041251099027485b732efc502878)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EksClusterCertificateAuthorityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef246e5c00ed75a1b0eccc9da40121465819710bb6501359ef4ce56897b717f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EksClusterCertificateAuthorityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761cfd31923d6b43fe979c784a4b3f0e91999ad54e8fbf88262396b562eab42b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dae6d3d5561fed06df57b316ae0bcae3a8fec901c761090106cc64ee579d0fe4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c1f2afbb5952ca7f5d527e318701485252d958e2af6177c09855cab14e7e15c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class EksClusterCertificateAuthorityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterCertificateAuthorityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3968920bd96a15eee38556b61cd758d81f263f4f8e351adcb9ef0b3cb61736a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterCertificateAuthority]:
        return typing.cast(typing.Optional[EksClusterCertificateAuthority], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterCertificateAuthority],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f077bba85b24dc1dcd63c0ce0aea07dd8c7efb901d6188bdf6d369f6ed97b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterComputeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "node_pools": "nodePools",
        "node_role_arn": "nodeRoleArn",
    },
)
class EksClusterComputeConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        node_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        node_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.
        :param node_pools: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#node_pools EksCluster#node_pools}.
        :param node_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#node_role_arn EksCluster#node_role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6f4fef01510681bcc83690f407e9afcf285e3f0b85bc26c0ba530726cc3c15)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument node_pools", value=node_pools, expected_type=type_hints["node_pools"])
            check_type(argname="argument node_role_arn", value=node_role_arn, expected_type=type_hints["node_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if node_pools is not None:
            self._values["node_pools"] = node_pools
        if node_role_arn is not None:
            self._values["node_role_arn"] = node_role_arn

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def node_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#node_pools EksCluster#node_pools}.'''
        result = self._values.get("node_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def node_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#node_role_arn EksCluster#node_role_arn}.'''
        result = self._values.get("node_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterComputeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterComputeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterComputeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83d66d5851ee3bc4893aeeac67eb8fa3575bb94c7973f732aa94ea5ee5dcb07e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetNodePools")
    def reset_node_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePools", []))

    @jsii.member(jsii_name="resetNodeRoleArn")
    def reset_node_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolsInput")
    def node_pools_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nodePoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeRoleArnInput")
    def node_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeRoleArnInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__99f4dd56cf4ef7f1dc87eebe1324ac04ab87e3c48c62b079bde4462978c76cc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodePools")
    def node_pools(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nodePools"))

    @node_pools.setter
    def node_pools(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657229f169c5bd5c1f4a160a509bd83a514aef780ff96a89f0ae64bbfff33a2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeRoleArn")
    def node_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeRoleArn"))

    @node_role_arn.setter
    def node_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035e1916afa61d594fd3ce9b8bc8cd7d4d40670af4bb9252663e952932dd5573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterComputeConfig]:
        return typing.cast(typing.Optional[EksClusterComputeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterComputeConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ada1dd346ba537d7c8a095b1c400a267b0503503a19f74c7f09a71f494e02dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterConfig",
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
        "role_arn": "roleArn",
        "vpc_config": "vpcConfig",
        "access_config": "accessConfig",
        "bootstrap_self_managed_addons": "bootstrapSelfManagedAddons",
        "compute_config": "computeConfig",
        "control_plane_scaling_config": "controlPlaneScalingConfig",
        "deletion_protection": "deletionProtection",
        "enabled_cluster_log_types": "enabledClusterLogTypes",
        "encryption_config": "encryptionConfig",
        "force_update_version": "forceUpdateVersion",
        "id": "id",
        "kubernetes_network_config": "kubernetesNetworkConfig",
        "outpost_config": "outpostConfig",
        "region": "region",
        "remote_network_config": "remoteNetworkConfig",
        "storage_config": "storageConfig",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "upgrade_policy": "upgradePolicy",
        "version": "version",
        "zonal_shift_config": "zonalShiftConfig",
    },
)
class EksClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        role_arn: builtins.str,
        vpc_config: typing.Union["EksClusterVpcConfig", typing.Dict[builtins.str, typing.Any]],
        access_config: typing.Optional[typing.Union[EksClusterAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bootstrap_self_managed_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        compute_config: typing.Optional[typing.Union[EksClusterComputeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane_scaling_config: typing.Optional[typing.Union["EksClusterControlPlaneScalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled_cluster_log_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        encryption_config: typing.Optional[typing.Union["EksClusterEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        force_update_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes_network_config: typing.Optional[typing.Union["EksClusterKubernetesNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        outpost_config: typing.Optional[typing.Union["EksClusterOutpostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        remote_network_config: typing.Optional[typing.Union["EksClusterRemoteNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_config: typing.Optional[typing.Union["EksClusterStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EksClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["EksClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        zonal_shift_config: typing.Optional[typing.Union["EksClusterZonalShiftConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#name EksCluster#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#role_arn EksCluster#role_arn}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#vpc_config EksCluster#vpc_config}
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#access_config EksCluster#access_config}
        :param bootstrap_self_managed_addons: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#bootstrap_self_managed_addons EksCluster#bootstrap_self_managed_addons}.
        :param compute_config: compute_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#compute_config EksCluster#compute_config}
        :param control_plane_scaling_config: control_plane_scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#control_plane_scaling_config EksCluster#control_plane_scaling_config}
        :param deletion_protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#deletion_protection EksCluster#deletion_protection}.
        :param enabled_cluster_log_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled_cluster_log_types EksCluster#enabled_cluster_log_types}.
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#encryption_config EksCluster#encryption_config}
        :param force_update_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#force_update_version EksCluster#force_update_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#id EksCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes_network_config: kubernetes_network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#kubernetes_network_config EksCluster#kubernetes_network_config}
        :param outpost_config: outpost_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#outpost_config EksCluster#outpost_config}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#region EksCluster#region}
        :param remote_network_config: remote_network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#remote_network_config EksCluster#remote_network_config}
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#storage_config EksCluster#storage_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#tags EksCluster#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#tags_all EksCluster#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#timeouts EksCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#upgrade_policy EksCluster#upgrade_policy}
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#version EksCluster#version}.
        :param zonal_shift_config: zonal_shift_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#zonal_shift_config EksCluster#zonal_shift_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(vpc_config, dict):
            vpc_config = EksClusterVpcConfig(**vpc_config)
        if isinstance(access_config, dict):
            access_config = EksClusterAccessConfig(**access_config)
        if isinstance(compute_config, dict):
            compute_config = EksClusterComputeConfig(**compute_config)
        if isinstance(control_plane_scaling_config, dict):
            control_plane_scaling_config = EksClusterControlPlaneScalingConfig(**control_plane_scaling_config)
        if isinstance(encryption_config, dict):
            encryption_config = EksClusterEncryptionConfig(**encryption_config)
        if isinstance(kubernetes_network_config, dict):
            kubernetes_network_config = EksClusterKubernetesNetworkConfig(**kubernetes_network_config)
        if isinstance(outpost_config, dict):
            outpost_config = EksClusterOutpostConfig(**outpost_config)
        if isinstance(remote_network_config, dict):
            remote_network_config = EksClusterRemoteNetworkConfig(**remote_network_config)
        if isinstance(storage_config, dict):
            storage_config = EksClusterStorageConfig(**storage_config)
        if isinstance(timeouts, dict):
            timeouts = EksClusterTimeouts(**timeouts)
        if isinstance(upgrade_policy, dict):
            upgrade_policy = EksClusterUpgradePolicy(**upgrade_policy)
        if isinstance(zonal_shift_config, dict):
            zonal_shift_config = EksClusterZonalShiftConfig(**zonal_shift_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc2e0c59162bf3270f7a79d96d37a30c04cf64a936617e9833e4c839d307fcd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument bootstrap_self_managed_addons", value=bootstrap_self_managed_addons, expected_type=type_hints["bootstrap_self_managed_addons"])
            check_type(argname="argument compute_config", value=compute_config, expected_type=type_hints["compute_config"])
            check_type(argname="argument control_plane_scaling_config", value=control_plane_scaling_config, expected_type=type_hints["control_plane_scaling_config"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument enabled_cluster_log_types", value=enabled_cluster_log_types, expected_type=type_hints["enabled_cluster_log_types"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument force_update_version", value=force_update_version, expected_type=type_hints["force_update_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kubernetes_network_config", value=kubernetes_network_config, expected_type=type_hints["kubernetes_network_config"])
            check_type(argname="argument outpost_config", value=outpost_config, expected_type=type_hints["outpost_config"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument remote_network_config", value=remote_network_config, expected_type=type_hints["remote_network_config"])
            check_type(argname="argument storage_config", value=storage_config, expected_type=type_hints["storage_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument upgrade_policy", value=upgrade_policy, expected_type=type_hints["upgrade_policy"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument zonal_shift_config", value=zonal_shift_config, expected_type=type_hints["zonal_shift_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "role_arn": role_arn,
            "vpc_config": vpc_config,
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
        if access_config is not None:
            self._values["access_config"] = access_config
        if bootstrap_self_managed_addons is not None:
            self._values["bootstrap_self_managed_addons"] = bootstrap_self_managed_addons
        if compute_config is not None:
            self._values["compute_config"] = compute_config
        if control_plane_scaling_config is not None:
            self._values["control_plane_scaling_config"] = control_plane_scaling_config
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if enabled_cluster_log_types is not None:
            self._values["enabled_cluster_log_types"] = enabled_cluster_log_types
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if force_update_version is not None:
            self._values["force_update_version"] = force_update_version
        if id is not None:
            self._values["id"] = id
        if kubernetes_network_config is not None:
            self._values["kubernetes_network_config"] = kubernetes_network_config
        if outpost_config is not None:
            self._values["outpost_config"] = outpost_config
        if region is not None:
            self._values["region"] = region
        if remote_network_config is not None:
            self._values["remote_network_config"] = remote_network_config
        if storage_config is not None:
            self._values["storage_config"] = storage_config
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if upgrade_policy is not None:
            self._values["upgrade_policy"] = upgrade_policy
        if version is not None:
            self._values["version"] = version
        if zonal_shift_config is not None:
            self._values["zonal_shift_config"] = zonal_shift_config

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#name EksCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#role_arn EksCluster#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_config(self) -> "EksClusterVpcConfig":
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#vpc_config EksCluster#vpc_config}
        '''
        result = self._values.get("vpc_config")
        assert result is not None, "Required property 'vpc_config' is missing"
        return typing.cast("EksClusterVpcConfig", result)

    @builtins.property
    def access_config(self) -> typing.Optional[EksClusterAccessConfig]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#access_config EksCluster#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[EksClusterAccessConfig], result)

    @builtins.property
    def bootstrap_self_managed_addons(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#bootstrap_self_managed_addons EksCluster#bootstrap_self_managed_addons}.'''
        result = self._values.get("bootstrap_self_managed_addons")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def compute_config(self) -> typing.Optional[EksClusterComputeConfig]:
        '''compute_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#compute_config EksCluster#compute_config}
        '''
        result = self._values.get("compute_config")
        return typing.cast(typing.Optional[EksClusterComputeConfig], result)

    @builtins.property
    def control_plane_scaling_config(
        self,
    ) -> typing.Optional["EksClusterControlPlaneScalingConfig"]:
        '''control_plane_scaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#control_plane_scaling_config EksCluster#control_plane_scaling_config}
        '''
        result = self._values.get("control_plane_scaling_config")
        return typing.cast(typing.Optional["EksClusterControlPlaneScalingConfig"], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#deletion_protection EksCluster#deletion_protection}.'''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled_cluster_log_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled_cluster_log_types EksCluster#enabled_cluster_log_types}.'''
        result = self._values.get("enabled_cluster_log_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def encryption_config(self) -> typing.Optional["EksClusterEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#encryption_config EksCluster#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["EksClusterEncryptionConfig"], result)

    @builtins.property
    def force_update_version(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#force_update_version EksCluster#force_update_version}.'''
        result = self._values.get("force_update_version")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#id EksCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes_network_config(
        self,
    ) -> typing.Optional["EksClusterKubernetesNetworkConfig"]:
        '''kubernetes_network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#kubernetes_network_config EksCluster#kubernetes_network_config}
        '''
        result = self._values.get("kubernetes_network_config")
        return typing.cast(typing.Optional["EksClusterKubernetesNetworkConfig"], result)

    @builtins.property
    def outpost_config(self) -> typing.Optional["EksClusterOutpostConfig"]:
        '''outpost_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#outpost_config EksCluster#outpost_config}
        '''
        result = self._values.get("outpost_config")
        return typing.cast(typing.Optional["EksClusterOutpostConfig"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#region EksCluster#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_network_config(self) -> typing.Optional["EksClusterRemoteNetworkConfig"]:
        '''remote_network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#remote_network_config EksCluster#remote_network_config}
        '''
        result = self._values.get("remote_network_config")
        return typing.cast(typing.Optional["EksClusterRemoteNetworkConfig"], result)

    @builtins.property
    def storage_config(self) -> typing.Optional["EksClusterStorageConfig"]:
        '''storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#storage_config EksCluster#storage_config}
        '''
        result = self._values.get("storage_config")
        return typing.cast(typing.Optional["EksClusterStorageConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#tags EksCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#tags_all EksCluster#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EksClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#timeouts EksCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EksClusterTimeouts"], result)

    @builtins.property
    def upgrade_policy(self) -> typing.Optional["EksClusterUpgradePolicy"]:
        '''upgrade_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#upgrade_policy EksCluster#upgrade_policy}
        '''
        result = self._values.get("upgrade_policy")
        return typing.cast(typing.Optional["EksClusterUpgradePolicy"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#version EksCluster#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zonal_shift_config(self) -> typing.Optional["EksClusterZonalShiftConfig"]:
        '''zonal_shift_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#zonal_shift_config EksCluster#zonal_shift_config}
        '''
        result = self._values.get("zonal_shift_config")
        return typing.cast(typing.Optional["EksClusterZonalShiftConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterControlPlaneScalingConfig",
    jsii_struct_bases=[],
    name_mapping={"tier": "tier"},
)
class EksClusterControlPlaneScalingConfig:
    def __init__(self, *, tier: typing.Optional[builtins.str] = None) -> None:
        '''
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#tier EksCluster#tier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ded5aae813f8f463b1eedd1007545e5ecb7ef18f03a8a8e16af110439ced3b4)
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tier is not None:
            self._values["tier"] = tier

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#tier EksCluster#tier}.'''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterControlPlaneScalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterControlPlaneScalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterControlPlaneScalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e373b56208112cba60f2d0b69e8af56db17725bca826935b07dd13cb563c6ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTier")
    def reset_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTier", []))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__251c56e1948b8c1737e81c1426a990f4c359bf404e19b16fe673934bd95ada93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterControlPlaneScalingConfig]:
        return typing.cast(typing.Optional[EksClusterControlPlaneScalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterControlPlaneScalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ce103c2a56efb1f354ba1e4c4892fd3217659919d1998063feb79d6cbe3b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"provider": "provider", "resources": "resources"},
)
class EksClusterEncryptionConfig:
    def __init__(
        self,
        *,
        provider: typing.Union["EksClusterEncryptionConfigProvider", typing.Dict[builtins.str, typing.Any]],
        resources: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param provider: provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#provider EksCluster#provider}
        :param resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#resources EksCluster#resources}.
        '''
        if isinstance(provider, dict):
            provider = EksClusterEncryptionConfigProvider(**provider)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d181429646168b3c02597fe41b41ca231f5f66a611e25648fde7c37b29e6d3)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider": provider,
            "resources": resources,
        }

    @builtins.property
    def provider(self) -> "EksClusterEncryptionConfigProvider":
        '''provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#provider EksCluster#provider}
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast("EksClusterEncryptionConfigProvider", result)

    @builtins.property
    def resources(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#resources EksCluster#resources}.'''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94f8f4a47d1ec56f7906232477b417ee5afbe9d4b59c011334eb72a0d3494872)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProvider")
    def put_provider(self, *, key_arn: builtins.str) -> None:
        '''
        :param key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#key_arn EksCluster#key_arn}.
        '''
        value = EksClusterEncryptionConfigProvider(key_arn=key_arn)

        return typing.cast(None, jsii.invoke(self, "putProvider", [value]))

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> "EksClusterEncryptionConfigProviderOutputReference":
        return typing.cast("EksClusterEncryptionConfigProviderOutputReference", jsii.get(self, "provider"))

    @builtins.property
    @jsii.member(jsii_name="providerInput")
    def provider_input(self) -> typing.Optional["EksClusterEncryptionConfigProvider"]:
        return typing.cast(typing.Optional["EksClusterEncryptionConfigProvider"], jsii.get(self, "providerInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b639ee70286e0e65932d382262da48883d1578aba7abeb445e2cc2dc97d37fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterEncryptionConfig]:
        return typing.cast(typing.Optional[EksClusterEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbb042dbb6cdc7d56d46defe3a2de84af61b5dd15017314e02ade2c500b6d74f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterEncryptionConfigProvider",
    jsii_struct_bases=[],
    name_mapping={"key_arn": "keyArn"},
)
class EksClusterEncryptionConfigProvider:
    def __init__(self, *, key_arn: builtins.str) -> None:
        '''
        :param key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#key_arn EksCluster#key_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825dfb9a4b4de6c2e85c31e673e58025c4cc275b041836c63ca6984800d6aef3)
            check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_arn": key_arn,
        }

    @builtins.property
    def key_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#key_arn EksCluster#key_arn}.'''
        result = self._values.get("key_arn")
        assert result is not None, "Required property 'key_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterEncryptionConfigProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterEncryptionConfigProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterEncryptionConfigProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e4db70b90dc34a29e1c2088d050b5c6228bc6e9e233df20655ea531d6ea315b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyArnInput")
    def key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyArn"))

    @key_arn.setter
    def key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afd7d36a5f5f358ee190eaa819b0f8df425dee0bb3256a77aa1f5f337b0af8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterEncryptionConfigProvider]:
        return typing.cast(typing.Optional[EksClusterEncryptionConfigProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterEncryptionConfigProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810ac9456c06941466386dbb914372afb598eca5408d233147be892ad7d933ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterIdentity",
    jsii_struct_bases=[],
    name_mapping={},
)
class EksClusterIdentity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterIdentityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterIdentityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9faa8daebf2603135021de798bbf3f679b95636772d7dec418587fa08866c91a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EksClusterIdentityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f4d29b567d8263c7a5dc0137f1f57c066cbb98a17bb697a23c1b2e51c99683)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EksClusterIdentityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6117b05dd5ad5734e63abfd65b19b5bf6c6a14c0be0957f70840bae43936ce5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23f8b2f573da0edf35a16902510fbbae296737d6bd447df73b63922c4b23d8aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee649703a266c31a3eeb5c4c4aefbb0dbdd695fac2bfa42da71e795d352c2d9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterIdentityOidc",
    jsii_struct_bases=[],
    name_mapping={},
)
class EksClusterIdentityOidc:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterIdentityOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterIdentityOidcList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterIdentityOidcList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__050ee6539286327355655193dc4ece2825296c71efc67b9942bccccbfab2efa0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EksClusterIdentityOidcOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dae7a160fc3d6839b075504980a97235c35f8154bdf14d5d97775c3f93ad6ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EksClusterIdentityOidcOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396cb9017fefcf8de62000a75d704ccddb047ff8c7117edd4e4451eabf305034)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa46d05411ced89a15941432edf007d22463bae0e06d6e73b603bccd04f5a0e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__516765a0beea3d7bf36522a68d1e6f773ba11333b2a393d64713850400bdba2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class EksClusterIdentityOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterIdentityOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52c1eb255149cc6b094a053f72941714ba52c82a8b5eaeefb1396b74781b6ccb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterIdentityOidc]:
        return typing.cast(typing.Optional[EksClusterIdentityOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterIdentityOidc]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28dff330362c986dbea3a3569b4a1e084bf4da9e03b08f3fe37e3ef6a33db599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EksClusterIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c34b0b400c3e080d9d2f6d61e8d897c80c5e6e23a76b37dbf5b0f541943f8a6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="oidc")
    def oidc(self) -> EksClusterIdentityOidcList:
        return typing.cast(EksClusterIdentityOidcList, jsii.get(self, "oidc"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterIdentity]:
        return typing.cast(typing.Optional[EksClusterIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edef07ebc2d0490165c6e5e8c468a9a44b24c2ad9590e2775a6c024fc5d84da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterKubernetesNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "elastic_load_balancing": "elasticLoadBalancing",
        "ip_family": "ipFamily",
        "service_ipv4_cidr": "serviceIpv4Cidr",
    },
)
class EksClusterKubernetesNetworkConfig:
    def __init__(
        self,
        *,
        elastic_load_balancing: typing.Optional[typing.Union["EksClusterKubernetesNetworkConfigElasticLoadBalancing", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_family: typing.Optional[builtins.str] = None,
        service_ipv4_cidr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param elastic_load_balancing: elastic_load_balancing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#elastic_load_balancing EksCluster#elastic_load_balancing}
        :param ip_family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#ip_family EksCluster#ip_family}.
        :param service_ipv4_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#service_ipv4_cidr EksCluster#service_ipv4_cidr}.
        '''
        if isinstance(elastic_load_balancing, dict):
            elastic_load_balancing = EksClusterKubernetesNetworkConfigElasticLoadBalancing(**elastic_load_balancing)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62e71002bbf3c75d6ee4460224d44a4b49d3c85a4b27874ecbd62db56664f3b)
            check_type(argname="argument elastic_load_balancing", value=elastic_load_balancing, expected_type=type_hints["elastic_load_balancing"])
            check_type(argname="argument ip_family", value=ip_family, expected_type=type_hints["ip_family"])
            check_type(argname="argument service_ipv4_cidr", value=service_ipv4_cidr, expected_type=type_hints["service_ipv4_cidr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if elastic_load_balancing is not None:
            self._values["elastic_load_balancing"] = elastic_load_balancing
        if ip_family is not None:
            self._values["ip_family"] = ip_family
        if service_ipv4_cidr is not None:
            self._values["service_ipv4_cidr"] = service_ipv4_cidr

    @builtins.property
    def elastic_load_balancing(
        self,
    ) -> typing.Optional["EksClusterKubernetesNetworkConfigElasticLoadBalancing"]:
        '''elastic_load_balancing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#elastic_load_balancing EksCluster#elastic_load_balancing}
        '''
        result = self._values.get("elastic_load_balancing")
        return typing.cast(typing.Optional["EksClusterKubernetesNetworkConfigElasticLoadBalancing"], result)

    @builtins.property
    def ip_family(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#ip_family EksCluster#ip_family}.'''
        result = self._values.get("ip_family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_ipv4_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#service_ipv4_cidr EksCluster#service_ipv4_cidr}.'''
        result = self._values.get("service_ipv4_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterKubernetesNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterKubernetesNetworkConfigElasticLoadBalancing",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class EksClusterKubernetesNetworkConfigElasticLoadBalancing:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f918198c26a048df2ab548bdbc33f5b33e04ae5b23cf9c197f76513239048245)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterKubernetesNetworkConfigElasticLoadBalancing(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterKubernetesNetworkConfigElasticLoadBalancingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterKubernetesNetworkConfigElasticLoadBalancingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b4fb709c4f4b4f7b7a46615fdb16decb6d72512a2918f28807f4ad9d0d0dd20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6220556ea0cd370d75f50ec82ed243c769a99060ada6eb33af4e411c285a1b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EksClusterKubernetesNetworkConfigElasticLoadBalancing]:
        return typing.cast(typing.Optional[EksClusterKubernetesNetworkConfigElasticLoadBalancing], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterKubernetesNetworkConfigElasticLoadBalancing],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa73a1d0a12a3f036c1a5312db3b2c704e88b3112c003a1904fe926513426293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EksClusterKubernetesNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterKubernetesNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f51376f3b372b03c4fd6f584f0dd2dd661c847d1b6126e4507dd2130950a3497)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putElasticLoadBalancing")
    def put_elastic_load_balancing(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.
        '''
        value = EksClusterKubernetesNetworkConfigElasticLoadBalancing(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putElasticLoadBalancing", [value]))

    @jsii.member(jsii_name="resetElasticLoadBalancing")
    def reset_elastic_load_balancing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticLoadBalancing", []))

    @jsii.member(jsii_name="resetIpFamily")
    def reset_ip_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpFamily", []))

    @jsii.member(jsii_name="resetServiceIpv4Cidr")
    def reset_service_ipv4_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceIpv4Cidr", []))

    @builtins.property
    @jsii.member(jsii_name="elasticLoadBalancing")
    def elastic_load_balancing(
        self,
    ) -> EksClusterKubernetesNetworkConfigElasticLoadBalancingOutputReference:
        return typing.cast(EksClusterKubernetesNetworkConfigElasticLoadBalancingOutputReference, jsii.get(self, "elasticLoadBalancing"))

    @builtins.property
    @jsii.member(jsii_name="serviceIpv6Cidr")
    def service_ipv6_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceIpv6Cidr"))

    @builtins.property
    @jsii.member(jsii_name="elasticLoadBalancingInput")
    def elastic_load_balancing_input(
        self,
    ) -> typing.Optional[EksClusterKubernetesNetworkConfigElasticLoadBalancing]:
        return typing.cast(typing.Optional[EksClusterKubernetesNetworkConfigElasticLoadBalancing], jsii.get(self, "elasticLoadBalancingInput"))

    @builtins.property
    @jsii.member(jsii_name="ipFamilyInput")
    def ip_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceIpv4CidrInput")
    def service_ipv4_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIpv4CidrInput"))

    @builtins.property
    @jsii.member(jsii_name="ipFamily")
    def ip_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipFamily"))

    @ip_family.setter
    def ip_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7ea08f8b61ce4a53314176038d58448daede16b0f9c56edcd006bc17392d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipFamily", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceIpv4Cidr")
    def service_ipv4_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceIpv4Cidr"))

    @service_ipv4_cidr.setter
    def service_ipv4_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15464d2befdc2ca1818f977058e6848c2e677e768d08b0af108a6fc8df7f57b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceIpv4Cidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterKubernetesNetworkConfig]:
        return typing.cast(typing.Optional[EksClusterKubernetesNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterKubernetesNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70e4292584225b96da8a29bfebacf8e0a8476cd43ec4076f118346e3576dc94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterOutpostConfig",
    jsii_struct_bases=[],
    name_mapping={
        "control_plane_instance_type": "controlPlaneInstanceType",
        "outpost_arns": "outpostArns",
        "control_plane_placement": "controlPlanePlacement",
    },
)
class EksClusterOutpostConfig:
    def __init__(
        self,
        *,
        control_plane_instance_type: builtins.str,
        outpost_arns: typing.Sequence[builtins.str],
        control_plane_placement: typing.Optional[typing.Union["EksClusterOutpostConfigControlPlanePlacement", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#control_plane_instance_type EksCluster#control_plane_instance_type}.
        :param outpost_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#outpost_arns EksCluster#outpost_arns}.
        :param control_plane_placement: control_plane_placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#control_plane_placement EksCluster#control_plane_placement}
        '''
        if isinstance(control_plane_placement, dict):
            control_plane_placement = EksClusterOutpostConfigControlPlanePlacement(**control_plane_placement)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__801d1a6ad1e716a1d20457362d540e38ca16d31819c753d6c62f13cba463ea25)
            check_type(argname="argument control_plane_instance_type", value=control_plane_instance_type, expected_type=type_hints["control_plane_instance_type"])
            check_type(argname="argument outpost_arns", value=outpost_arns, expected_type=type_hints["outpost_arns"])
            check_type(argname="argument control_plane_placement", value=control_plane_placement, expected_type=type_hints["control_plane_placement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_instance_type": control_plane_instance_type,
            "outpost_arns": outpost_arns,
        }
        if control_plane_placement is not None:
            self._values["control_plane_placement"] = control_plane_placement

    @builtins.property
    def control_plane_instance_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#control_plane_instance_type EksCluster#control_plane_instance_type}.'''
        result = self._values.get("control_plane_instance_type")
        assert result is not None, "Required property 'control_plane_instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def outpost_arns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#outpost_arns EksCluster#outpost_arns}.'''
        result = self._values.get("outpost_arns")
        assert result is not None, "Required property 'outpost_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def control_plane_placement(
        self,
    ) -> typing.Optional["EksClusterOutpostConfigControlPlanePlacement"]:
        '''control_plane_placement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#control_plane_placement EksCluster#control_plane_placement}
        '''
        result = self._values.get("control_plane_placement")
        return typing.cast(typing.Optional["EksClusterOutpostConfigControlPlanePlacement"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterOutpostConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterOutpostConfigControlPlanePlacement",
    jsii_struct_bases=[],
    name_mapping={"group_name": "groupName"},
)
class EksClusterOutpostConfigControlPlanePlacement:
    def __init__(self, *, group_name: builtins.str) -> None:
        '''
        :param group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#group_name EksCluster#group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782a98501bd35a01e54fb9ba56de27cf20640473d5a42cf80269a26152cb93bc)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_name": group_name,
        }

    @builtins.property
    def group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#group_name EksCluster#group_name}.'''
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterOutpostConfigControlPlanePlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterOutpostConfigControlPlanePlacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterOutpostConfigControlPlanePlacementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab8819ae56b1ecd5db96dc32cb80696c6ef464f36ca62db26c32628a4fe01513)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="groupNameInput")
    def group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fc0e8e817b39c83758d5e6ff40bd4a79d9e5cd8b108cdcddd978a93e512fa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EksClusterOutpostConfigControlPlanePlacement]:
        return typing.cast(typing.Optional[EksClusterOutpostConfigControlPlanePlacement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterOutpostConfigControlPlanePlacement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6159468d8ad81d679f86a571b5e3005a07947f993066e45c520b1ba96d7075db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EksClusterOutpostConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterOutpostConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c64459a26c3e1cd291cabcf6165499412a4597100b0be5c0384142607d62d5d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putControlPlanePlacement")
    def put_control_plane_placement(self, *, group_name: builtins.str) -> None:
        '''
        :param group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#group_name EksCluster#group_name}.
        '''
        value = EksClusterOutpostConfigControlPlanePlacement(group_name=group_name)

        return typing.cast(None, jsii.invoke(self, "putControlPlanePlacement", [value]))

    @jsii.member(jsii_name="resetControlPlanePlacement")
    def reset_control_plane_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlanePlacement", []))

    @builtins.property
    @jsii.member(jsii_name="controlPlanePlacement")
    def control_plane_placement(
        self,
    ) -> EksClusterOutpostConfigControlPlanePlacementOutputReference:
        return typing.cast(EksClusterOutpostConfigControlPlanePlacementOutputReference, jsii.get(self, "controlPlanePlacement"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInstanceTypeInput")
    def control_plane_instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneInstanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlanePlacementInput")
    def control_plane_placement_input(
        self,
    ) -> typing.Optional[EksClusterOutpostConfigControlPlanePlacement]:
        return typing.cast(typing.Optional[EksClusterOutpostConfigControlPlanePlacement], jsii.get(self, "controlPlanePlacementInput"))

    @builtins.property
    @jsii.member(jsii_name="outpostArnsInput")
    def outpost_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outpostArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInstanceType")
    def control_plane_instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneInstanceType"))

    @control_plane_instance_type.setter
    def control_plane_instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a6588ee8fd27025eabf59fef1cfbeb90666b677ea85a3c6267428d42db0e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneInstanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outpostArns")
    def outpost_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outpostArns"))

    @outpost_arns.setter
    def outpost_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5770b65bb2e3ac57571d3ed8e84d6ba35609a48f466bf5afa13c1a42642d3f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outpostArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterOutpostConfig]:
        return typing.cast(typing.Optional[EksClusterOutpostConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterOutpostConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbd7fc2a5b75031d831d8d12a4f81089b6702e38d72bd55f862a120b48d61548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterRemoteNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "remote_node_networks": "remoteNodeNetworks",
        "remote_pod_networks": "remotePodNetworks",
    },
)
class EksClusterRemoteNetworkConfig:
    def __init__(
        self,
        *,
        remote_node_networks: typing.Union["EksClusterRemoteNetworkConfigRemoteNodeNetworks", typing.Dict[builtins.str, typing.Any]],
        remote_pod_networks: typing.Optional[typing.Union["EksClusterRemoteNetworkConfigRemotePodNetworks", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param remote_node_networks: remote_node_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#remote_node_networks EksCluster#remote_node_networks}
        :param remote_pod_networks: remote_pod_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#remote_pod_networks EksCluster#remote_pod_networks}
        '''
        if isinstance(remote_node_networks, dict):
            remote_node_networks = EksClusterRemoteNetworkConfigRemoteNodeNetworks(**remote_node_networks)
        if isinstance(remote_pod_networks, dict):
            remote_pod_networks = EksClusterRemoteNetworkConfigRemotePodNetworks(**remote_pod_networks)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066d2842cffe80695ed832623d69d49f3ebaab055cc97e0e777dc5470f7a6663)
            check_type(argname="argument remote_node_networks", value=remote_node_networks, expected_type=type_hints["remote_node_networks"])
            check_type(argname="argument remote_pod_networks", value=remote_pod_networks, expected_type=type_hints["remote_pod_networks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote_node_networks": remote_node_networks,
        }
        if remote_pod_networks is not None:
            self._values["remote_pod_networks"] = remote_pod_networks

    @builtins.property
    def remote_node_networks(self) -> "EksClusterRemoteNetworkConfigRemoteNodeNetworks":
        '''remote_node_networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#remote_node_networks EksCluster#remote_node_networks}
        '''
        result = self._values.get("remote_node_networks")
        assert result is not None, "Required property 'remote_node_networks' is missing"
        return typing.cast("EksClusterRemoteNetworkConfigRemoteNodeNetworks", result)

    @builtins.property
    def remote_pod_networks(
        self,
    ) -> typing.Optional["EksClusterRemoteNetworkConfigRemotePodNetworks"]:
        '''remote_pod_networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#remote_pod_networks EksCluster#remote_pod_networks}
        '''
        result = self._values.get("remote_pod_networks")
        return typing.cast(typing.Optional["EksClusterRemoteNetworkConfigRemotePodNetworks"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterRemoteNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterRemoteNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterRemoteNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03dd5db0a402c833b23c432b08b58d3967a3309ace18f3a0203109831963e8c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRemoteNodeNetworks")
    def put_remote_node_networks(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#cidrs EksCluster#cidrs}.
        '''
        value = EksClusterRemoteNetworkConfigRemoteNodeNetworks(cidrs=cidrs)

        return typing.cast(None, jsii.invoke(self, "putRemoteNodeNetworks", [value]))

    @jsii.member(jsii_name="putRemotePodNetworks")
    def put_remote_pod_networks(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#cidrs EksCluster#cidrs}.
        '''
        value = EksClusterRemoteNetworkConfigRemotePodNetworks(cidrs=cidrs)

        return typing.cast(None, jsii.invoke(self, "putRemotePodNetworks", [value]))

    @jsii.member(jsii_name="resetRemotePodNetworks")
    def reset_remote_pod_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemotePodNetworks", []))

    @builtins.property
    @jsii.member(jsii_name="remoteNodeNetworks")
    def remote_node_networks(
        self,
    ) -> "EksClusterRemoteNetworkConfigRemoteNodeNetworksOutputReference":
        return typing.cast("EksClusterRemoteNetworkConfigRemoteNodeNetworksOutputReference", jsii.get(self, "remoteNodeNetworks"))

    @builtins.property
    @jsii.member(jsii_name="remotePodNetworks")
    def remote_pod_networks(
        self,
    ) -> "EksClusterRemoteNetworkConfigRemotePodNetworksOutputReference":
        return typing.cast("EksClusterRemoteNetworkConfigRemotePodNetworksOutputReference", jsii.get(self, "remotePodNetworks"))

    @builtins.property
    @jsii.member(jsii_name="remoteNodeNetworksInput")
    def remote_node_networks_input(
        self,
    ) -> typing.Optional["EksClusterRemoteNetworkConfigRemoteNodeNetworks"]:
        return typing.cast(typing.Optional["EksClusterRemoteNetworkConfigRemoteNodeNetworks"], jsii.get(self, "remoteNodeNetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="remotePodNetworksInput")
    def remote_pod_networks_input(
        self,
    ) -> typing.Optional["EksClusterRemoteNetworkConfigRemotePodNetworks"]:
        return typing.cast(typing.Optional["EksClusterRemoteNetworkConfigRemotePodNetworks"], jsii.get(self, "remotePodNetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterRemoteNetworkConfig]:
        return typing.cast(typing.Optional[EksClusterRemoteNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterRemoteNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f526197427baa7c217ad1600e3ea1fdb0e1dd6e4f6c563115f0f2a1e419f10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterRemoteNetworkConfigRemoteNodeNetworks",
    jsii_struct_bases=[],
    name_mapping={"cidrs": "cidrs"},
)
class EksClusterRemoteNetworkConfigRemoteNodeNetworks:
    def __init__(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#cidrs EksCluster#cidrs}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81f348f09bde218cd1a26033ba6ee13aeb9ed110c7c2a2b90051b5176e511c2)
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidrs is not None:
            self._values["cidrs"] = cidrs

    @builtins.property
    def cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#cidrs EksCluster#cidrs}.'''
        result = self._values.get("cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterRemoteNetworkConfigRemoteNodeNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterRemoteNetworkConfigRemoteNodeNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterRemoteNetworkConfigRemoteNodeNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e5cc55bf9dbcddfe0080e1a42f19b737514e24fb674009bc1f551bf1ad05091)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCidrs")
    def reset_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidrs", []))

    @builtins.property
    @jsii.member(jsii_name="cidrsInput")
    def cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrs")
    def cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cidrs"))

    @cidrs.setter
    def cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538694ab2c447307ef2876bf27f549d33b0109f9e17c0758557a63fd5ee028dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EksClusterRemoteNetworkConfigRemoteNodeNetworks]:
        return typing.cast(typing.Optional[EksClusterRemoteNetworkConfigRemoteNodeNetworks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterRemoteNetworkConfigRemoteNodeNetworks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abccdcda5233586c8ad568001f19697677dd2a81d0d9b486da7c717946aefa6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterRemoteNetworkConfigRemotePodNetworks",
    jsii_struct_bases=[],
    name_mapping={"cidrs": "cidrs"},
)
class EksClusterRemoteNetworkConfigRemotePodNetworks:
    def __init__(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#cidrs EksCluster#cidrs}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1626b961aea271b458dd6df61b845576824bb9c2804220310d67c47544cb08)
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidrs is not None:
            self._values["cidrs"] = cidrs

    @builtins.property
    def cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#cidrs EksCluster#cidrs}.'''
        result = self._values.get("cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterRemoteNetworkConfigRemotePodNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterRemoteNetworkConfigRemotePodNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterRemoteNetworkConfigRemotePodNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19adae212920c3e1b7cc290c4f3e7b0d1153df83ccb2705713de0407623b90fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCidrs")
    def reset_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidrs", []))

    @builtins.property
    @jsii.member(jsii_name="cidrsInput")
    def cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrs")
    def cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cidrs"))

    @cidrs.setter
    def cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4303414e9b7b7e8e08fdfdc6015ebe0717b1ac7cec49be51401561aa04928083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EksClusterRemoteNetworkConfigRemotePodNetworks]:
        return typing.cast(typing.Optional[EksClusterRemoteNetworkConfigRemotePodNetworks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterRemoteNetworkConfigRemotePodNetworks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27229e8fcbd93985108ab2e0a2e88b210413851246acaed1758bce7471fddd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterStorageConfig",
    jsii_struct_bases=[],
    name_mapping={"block_storage": "blockStorage"},
)
class EksClusterStorageConfig:
    def __init__(
        self,
        *,
        block_storage: typing.Optional[typing.Union["EksClusterStorageConfigBlockStorage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param block_storage: block_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#block_storage EksCluster#block_storage}
        '''
        if isinstance(block_storage, dict):
            block_storage = EksClusterStorageConfigBlockStorage(**block_storage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933437273a354047f9324282021abcd3d183fb853f6a53213ff527ff33686964)
            check_type(argname="argument block_storage", value=block_storage, expected_type=type_hints["block_storage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if block_storage is not None:
            self._values["block_storage"] = block_storage

    @builtins.property
    def block_storage(self) -> typing.Optional["EksClusterStorageConfigBlockStorage"]:
        '''block_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#block_storage EksCluster#block_storage}
        '''
        result = self._values.get("block_storage")
        return typing.cast(typing.Optional["EksClusterStorageConfigBlockStorage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterStorageConfigBlockStorage",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class EksClusterStorageConfigBlockStorage:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b3e399fbacf5f22b4264d7a7db092338930f3f2bc854c1231f681c57911758)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterStorageConfigBlockStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterStorageConfigBlockStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterStorageConfigBlockStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ee366a61fa97a31a6c7f0e50f28cdfab91e9c91f717b58f631703ca247ba154)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__031be166ccd285bdb8746f1efb7707f86c7a7558586a6431dd7d9d8a3006ab77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterStorageConfigBlockStorage]:
        return typing.cast(typing.Optional[EksClusterStorageConfigBlockStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterStorageConfigBlockStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8427cec5adb2e0501c50ee35d158cd0f1232659de8c99f979ec91e9f2be91dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EksClusterStorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterStorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31bd483ecd8f95d4a4b55e954260a6cefd338fdd7626457c3a3de7b6e8eff413)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBlockStorage")
    def put_block_storage(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.
        '''
        value = EksClusterStorageConfigBlockStorage(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putBlockStorage", [value]))

    @jsii.member(jsii_name="resetBlockStorage")
    def reset_block_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockStorage", []))

    @builtins.property
    @jsii.member(jsii_name="blockStorage")
    def block_storage(self) -> EksClusterStorageConfigBlockStorageOutputReference:
        return typing.cast(EksClusterStorageConfigBlockStorageOutputReference, jsii.get(self, "blockStorage"))

    @builtins.property
    @jsii.member(jsii_name="blockStorageInput")
    def block_storage_input(
        self,
    ) -> typing.Optional[EksClusterStorageConfigBlockStorage]:
        return typing.cast(typing.Optional[EksClusterStorageConfigBlockStorage], jsii.get(self, "blockStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterStorageConfig]:
        return typing.cast(typing.Optional[EksClusterStorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterStorageConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56df416462014e9cff8b7219061b40d7e68395bfd854628b1a7b62ea85118d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class EksClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#create EksCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#delete EksCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#update EksCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0562bd4a009d0de96bba4233599d79cb0cc86f582743fb40b2a5784485e9b04)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#create EksCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#delete EksCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#update EksCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1ea8996894c7a9743bdb036f80e8cca09f323a8048528e16f91c258e6e49e14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eb3040b7bd4a7b26fb24e4ffc2ddc0372de3f3b584929105f236f088822a76f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095ace7bf4b0babfb7cb7ab896e15d36f53669c1058d62a27deaf85b79eba7b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d7a77d96b17da6e9b6d9ea5622318a8bce62484a13113fc0c774ab1cc5165f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d347db10f4ee602118c211a11cb6f82b6a3b9f357ff397b3e2f470f18524982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterUpgradePolicy",
    jsii_struct_bases=[],
    name_mapping={"support_type": "supportType"},
)
class EksClusterUpgradePolicy:
    def __init__(self, *, support_type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param support_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#support_type EksCluster#support_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394695f065a0a72373b0576cb657c8281455fb465725bdabc93801abf300c245)
            check_type(argname="argument support_type", value=support_type, expected_type=type_hints["support_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if support_type is not None:
            self._values["support_type"] = support_type

    @builtins.property
    def support_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#support_type EksCluster#support_type}.'''
        result = self._values.get("support_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterUpgradePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterUpgradePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterUpgradePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b65de338376cf780ca54f0a3ded035e49e38caf308ca9636f8723908db1609a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSupportType")
    def reset_support_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportType", []))

    @builtins.property
    @jsii.member(jsii_name="supportTypeInput")
    def support_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="supportType")
    def support_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportType"))

    @support_type.setter
    def support_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aadb5765590b16a0392287baf270123d413a0ea18f9c7c8d457f5b986182804c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterUpgradePolicy]:
        return typing.cast(typing.Optional[EksClusterUpgradePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterUpgradePolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb9666e5628f07b41c0449ac2588c032e8ac686689eb2d0b4d0502723c3c29b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterVpcConfig",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_ids": "subnetIds",
        "endpoint_private_access": "endpointPrivateAccess",
        "endpoint_public_access": "endpointPublicAccess",
        "public_access_cidrs": "publicAccessCidrs",
        "security_group_ids": "securityGroupIds",
    },
)
class EksClusterVpcConfig:
    def __init__(
        self,
        *,
        subnet_ids: typing.Sequence[builtins.str],
        endpoint_private_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_public_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_access_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#subnet_ids EksCluster#subnet_ids}.
        :param endpoint_private_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#endpoint_private_access EksCluster#endpoint_private_access}.
        :param endpoint_public_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#endpoint_public_access EksCluster#endpoint_public_access}.
        :param public_access_cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#public_access_cidrs EksCluster#public_access_cidrs}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#security_group_ids EksCluster#security_group_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad36e3c5c2fdc2116f9c5f3d7f8fb773c65938a6c7d4ed6ab7a5f13ae26b24d)
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument endpoint_private_access", value=endpoint_private_access, expected_type=type_hints["endpoint_private_access"])
            check_type(argname="argument endpoint_public_access", value=endpoint_public_access, expected_type=type_hints["endpoint_public_access"])
            check_type(argname="argument public_access_cidrs", value=public_access_cidrs, expected_type=type_hints["public_access_cidrs"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_ids": subnet_ids,
        }
        if endpoint_private_access is not None:
            self._values["endpoint_private_access"] = endpoint_private_access
        if endpoint_public_access is not None:
            self._values["endpoint_public_access"] = endpoint_public_access
        if public_access_cidrs is not None:
            self._values["public_access_cidrs"] = public_access_cidrs
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#subnet_ids EksCluster#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def endpoint_private_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#endpoint_private_access EksCluster#endpoint_private_access}.'''
        result = self._values.get("endpoint_private_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpoint_public_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#endpoint_public_access EksCluster#endpoint_public_access}.'''
        result = self._values.get("endpoint_public_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_access_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#public_access_cidrs EksCluster#public_access_cidrs}.'''
        result = self._values.get("public_access_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#security_group_ids EksCluster#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterVpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52352a40775f70ecc0d25b4f4900c7197549d9bf1fbfffede61f6b7e69e08be9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndpointPrivateAccess")
    def reset_endpoint_private_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointPrivateAccess", []))

    @jsii.member(jsii_name="resetEndpointPublicAccess")
    def reset_endpoint_public_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointPublicAccess", []))

    @jsii.member(jsii_name="resetPublicAccessCidrs")
    def reset_public_access_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicAccessCidrs", []))

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterSecurityGroupId"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @builtins.property
    @jsii.member(jsii_name="endpointPrivateAccessInput")
    def endpoint_private_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "endpointPrivateAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointPublicAccessInput")
    def endpoint_public_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "endpointPublicAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="publicAccessCidrsInput")
    def public_access_cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "publicAccessCidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointPrivateAccess")
    def endpoint_private_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "endpointPrivateAccess"))

    @endpoint_private_access.setter
    def endpoint_private_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd109884bf5994f28245f94b434077ae4dcfcbeb137901ff4f0f151e5eaea09a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointPrivateAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointPublicAccess")
    def endpoint_public_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "endpointPublicAccess"))

    @endpoint_public_access.setter
    def endpoint_public_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da7ea2001b456d279b1dfdc779a01f208713d671ea1a4268f11876d2f3a87c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointPublicAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicAccessCidrs")
    def public_access_cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicAccessCidrs"))

    @public_access_cidrs.setter
    def public_access_cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1788d3762e7bef3e06e417721e399c8c4f99aecf1192fa76248b52b735a7f3ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicAccessCidrs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0094e0d69b51f5f571221f4c1e591866362005c6f7c71844014d35b09ce7658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3fe68096c764886c6db1a658a4ae241e5bc6f808db2a6a4d78b5212b2f5de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterVpcConfig]:
        return typing.cast(typing.Optional[EksClusterVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksClusterVpcConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a94a0542c89a51dfe67e53a1a34967085ad47cfce69465c44c219b07ba0b4cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterZonalShiftConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class EksClusterZonalShiftConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e24554a49fdbffca355298a48a51a1235cb4e48604b9dafcef404a25fe52c08)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_cluster#enabled EksCluster#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksClusterZonalShiftConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksClusterZonalShiftConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksCluster.EksClusterZonalShiftConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b3dd2e4420bec0e987b04641098adf54756a444dc410be89998ebc8aff6299f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1e2734e75d10fb969826fe68bfb28478608326e9aeddea9243020c313b04900b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksClusterZonalShiftConfig]:
        return typing.cast(typing.Optional[EksClusterZonalShiftConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksClusterZonalShiftConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1554860c71f39fa89412873ea61f23ed9806aa32ef239fe536aa293e399d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EksCluster",
    "EksClusterAccessConfig",
    "EksClusterAccessConfigOutputReference",
    "EksClusterCertificateAuthority",
    "EksClusterCertificateAuthorityList",
    "EksClusterCertificateAuthorityOutputReference",
    "EksClusterComputeConfig",
    "EksClusterComputeConfigOutputReference",
    "EksClusterConfig",
    "EksClusterControlPlaneScalingConfig",
    "EksClusterControlPlaneScalingConfigOutputReference",
    "EksClusterEncryptionConfig",
    "EksClusterEncryptionConfigOutputReference",
    "EksClusterEncryptionConfigProvider",
    "EksClusterEncryptionConfigProviderOutputReference",
    "EksClusterIdentity",
    "EksClusterIdentityList",
    "EksClusterIdentityOidc",
    "EksClusterIdentityOidcList",
    "EksClusterIdentityOidcOutputReference",
    "EksClusterIdentityOutputReference",
    "EksClusterKubernetesNetworkConfig",
    "EksClusterKubernetesNetworkConfigElasticLoadBalancing",
    "EksClusterKubernetesNetworkConfigElasticLoadBalancingOutputReference",
    "EksClusterKubernetesNetworkConfigOutputReference",
    "EksClusterOutpostConfig",
    "EksClusterOutpostConfigControlPlanePlacement",
    "EksClusterOutpostConfigControlPlanePlacementOutputReference",
    "EksClusterOutpostConfigOutputReference",
    "EksClusterRemoteNetworkConfig",
    "EksClusterRemoteNetworkConfigOutputReference",
    "EksClusterRemoteNetworkConfigRemoteNodeNetworks",
    "EksClusterRemoteNetworkConfigRemoteNodeNetworksOutputReference",
    "EksClusterRemoteNetworkConfigRemotePodNetworks",
    "EksClusterRemoteNetworkConfigRemotePodNetworksOutputReference",
    "EksClusterStorageConfig",
    "EksClusterStorageConfigBlockStorage",
    "EksClusterStorageConfigBlockStorageOutputReference",
    "EksClusterStorageConfigOutputReference",
    "EksClusterTimeouts",
    "EksClusterTimeoutsOutputReference",
    "EksClusterUpgradePolicy",
    "EksClusterUpgradePolicyOutputReference",
    "EksClusterVpcConfig",
    "EksClusterVpcConfigOutputReference",
    "EksClusterZonalShiftConfig",
    "EksClusterZonalShiftConfigOutputReference",
]

publication.publish()

def _typecheckingstub__67133bc8fbfdf04570dcf8057cadd6bbfbeed17df985ce70f85c89e56ac21bf9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    role_arn: builtins.str,
    vpc_config: typing.Union[EksClusterVpcConfig, typing.Dict[builtins.str, typing.Any]],
    access_config: typing.Optional[typing.Union[EksClusterAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bootstrap_self_managed_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    compute_config: typing.Optional[typing.Union[EksClusterComputeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane_scaling_config: typing.Optional[typing.Union[EksClusterControlPlaneScalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled_cluster_log_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption_config: typing.Optional[typing.Union[EksClusterEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    force_update_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes_network_config: typing.Optional[typing.Union[EksClusterKubernetesNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    outpost_config: typing.Optional[typing.Union[EksClusterOutpostConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    remote_network_config: typing.Optional[typing.Union[EksClusterRemoteNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_config: typing.Optional[typing.Union[EksClusterStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EksClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[EksClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    zonal_shift_config: typing.Optional[typing.Union[EksClusterZonalShiftConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3da21b767bd48ae16f9d7e86b612aec4695b2db0946043915a70d73230416414(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6603a1a9d75953b0f22bc89037b0c517bd324e8c32225754a723825bee8bba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432b3f96d19de939303b88a20ede13b5e96cf671b0cc74196fe53c5645475a1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca183cc71921358c4578ec29981b1a2a59b365cbea634c43d4fb19cea3b372a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517be2bbcf5fce731dcfd57c9a0b3c1111f49fabe8f9ded632ebb3182a7c452c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fec0e99bfe2f962fce410795987a191454102f5568b32919276dbcd7c895e9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0db287ae54aa7ea3d977c716ecefd5317438fe173163e577d4a8c32d59bea7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91054a5a1b97afd6427f5cccb28fdf4d148a56e0db5d1792152a175d4fb4044c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e3a1284beed4b6275002e4a94c389a4cc1eb968574c9f092534fa1c7cc9166(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c18def6e9b5e5985e745133024ed968d351cbee7290a1efa019b2cba751105(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44004caef6c31a45646a84b80a5230de2a2e6b112c816b6a854cf67323963cd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a608235eba80729f5cee0aa4fa4685b0ce4055e2b7122a659edc8fe3213ec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618278714d42a51347b205fd4a247f05e912322646b1f07b8cf20b194c76b507(
    *,
    authentication_mode: typing.Optional[builtins.str] = None,
    bootstrap_cluster_creator_admin_permissions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33503bc01bf8cfbe70ac1782a863ad555840190bd8611ab6c1f875f1edcbfc6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40dd87f52185905a3bb05a700683ee25a29f0b37c54ece58d88e3f89e9ed447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e838caca75bd9395882bf406f9a3e6d4155a6c0a591140f7a21268540563ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65e54648a95c238b548d69e1aa140b519176f4d61affe86fbafbd55bdd953c2(
    value: typing.Optional[EksClusterAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f81da356d543b5107d68f10ef5e78868e30041251099027485b732efc502878(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef246e5c00ed75a1b0eccc9da40121465819710bb6501359ef4ce56897b717f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761cfd31923d6b43fe979c784a4b3f0e91999ad54e8fbf88262396b562eab42b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae6d3d5561fed06df57b316ae0bcae3a8fec901c761090106cc64ee579d0fe4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1f2afbb5952ca7f5d527e318701485252d958e2af6177c09855cab14e7e15c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3968920bd96a15eee38556b61cd758d81f263f4f8e351adcb9ef0b3cb61736a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f077bba85b24dc1dcd63c0ce0aea07dd8c7efb901d6188bdf6d369f6ed97b72(
    value: typing.Optional[EksClusterCertificateAuthority],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6f4fef01510681bcc83690f407e9afcf285e3f0b85bc26c0ba530726cc3c15(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    node_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    node_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d66d5851ee3bc4893aeeac67eb8fa3575bb94c7973f732aa94ea5ee5dcb07e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f4dd56cf4ef7f1dc87eebe1324ac04ab87e3c48c62b079bde4462978c76cc2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657229f169c5bd5c1f4a160a509bd83a514aef780ff96a89f0ae64bbfff33a2e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035e1916afa61d594fd3ce9b8bc8cd7d4d40670af4bb9252663e952932dd5573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ada1dd346ba537d7c8a095b1c400a267b0503503a19f74c7f09a71f494e02dd(
    value: typing.Optional[EksClusterComputeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc2e0c59162bf3270f7a79d96d37a30c04cf64a936617e9833e4c839d307fcd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    role_arn: builtins.str,
    vpc_config: typing.Union[EksClusterVpcConfig, typing.Dict[builtins.str, typing.Any]],
    access_config: typing.Optional[typing.Union[EksClusterAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bootstrap_self_managed_addons: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    compute_config: typing.Optional[typing.Union[EksClusterComputeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane_scaling_config: typing.Optional[typing.Union[EksClusterControlPlaneScalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled_cluster_log_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption_config: typing.Optional[typing.Union[EksClusterEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    force_update_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes_network_config: typing.Optional[typing.Union[EksClusterKubernetesNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    outpost_config: typing.Optional[typing.Union[EksClusterOutpostConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    remote_network_config: typing.Optional[typing.Union[EksClusterRemoteNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_config: typing.Optional[typing.Union[EksClusterStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EksClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[EksClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    zonal_shift_config: typing.Optional[typing.Union[EksClusterZonalShiftConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ded5aae813f8f463b1eedd1007545e5ecb7ef18f03a8a8e16af110439ced3b4(
    *,
    tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e373b56208112cba60f2d0b69e8af56db17725bca826935b07dd13cb563c6ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251c56e1948b8c1737e81c1426a990f4c359bf404e19b16fe673934bd95ada93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ce103c2a56efb1f354ba1e4c4892fd3217659919d1998063feb79d6cbe3b12(
    value: typing.Optional[EksClusterControlPlaneScalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d181429646168b3c02597fe41b41ca231f5f66a611e25648fde7c37b29e6d3(
    *,
    provider: typing.Union[EksClusterEncryptionConfigProvider, typing.Dict[builtins.str, typing.Any]],
    resources: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f8f4a47d1ec56f7906232477b417ee5afbe9d4b59c011334eb72a0d3494872(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b639ee70286e0e65932d382262da48883d1578aba7abeb445e2cc2dc97d37fd2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb042dbb6cdc7d56d46defe3a2de84af61b5dd15017314e02ade2c500b6d74f(
    value: typing.Optional[EksClusterEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825dfb9a4b4de6c2e85c31e673e58025c4cc275b041836c63ca6984800d6aef3(
    *,
    key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4db70b90dc34a29e1c2088d050b5c6228bc6e9e233df20655ea531d6ea315b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afd7d36a5f5f358ee190eaa819b0f8df425dee0bb3256a77aa1f5f337b0af8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810ac9456c06941466386dbb914372afb598eca5408d233147be892ad7d933ff(
    value: typing.Optional[EksClusterEncryptionConfigProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9faa8daebf2603135021de798bbf3f679b95636772d7dec418587fa08866c91a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f4d29b567d8263c7a5dc0137f1f57c066cbb98a17bb697a23c1b2e51c99683(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6117b05dd5ad5734e63abfd65b19b5bf6c6a14c0be0957f70840bae43936ce5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f8b2f573da0edf35a16902510fbbae296737d6bd447df73b63922c4b23d8aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee649703a266c31a3eeb5c4c4aefbb0dbdd695fac2bfa42da71e795d352c2d9b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050ee6539286327355655193dc4ece2825296c71efc67b9942bccccbfab2efa0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dae7a160fc3d6839b075504980a97235c35f8154bdf14d5d97775c3f93ad6ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396cb9017fefcf8de62000a75d704ccddb047ff8c7117edd4e4451eabf305034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa46d05411ced89a15941432edf007d22463bae0e06d6e73b603bccd04f5a0e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516765a0beea3d7bf36522a68d1e6f773ba11333b2a393d64713850400bdba2c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c1eb255149cc6b094a053f72941714ba52c82a8b5eaeefb1396b74781b6ccb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28dff330362c986dbea3a3569b4a1e084bf4da9e03b08f3fe37e3ef6a33db599(
    value: typing.Optional[EksClusterIdentityOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34b0b400c3e080d9d2f6d61e8d897c80c5e6e23a76b37dbf5b0f541943f8a6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edef07ebc2d0490165c6e5e8c468a9a44b24c2ad9590e2775a6c024fc5d84da0(
    value: typing.Optional[EksClusterIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62e71002bbf3c75d6ee4460224d44a4b49d3c85a4b27874ecbd62db56664f3b(
    *,
    elastic_load_balancing: typing.Optional[typing.Union[EksClusterKubernetesNetworkConfigElasticLoadBalancing, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_family: typing.Optional[builtins.str] = None,
    service_ipv4_cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f918198c26a048df2ab548bdbc33f5b33e04ae5b23cf9c197f76513239048245(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4fb709c4f4b4f7b7a46615fdb16decb6d72512a2918f28807f4ad9d0d0dd20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6220556ea0cd370d75f50ec82ed243c769a99060ada6eb33af4e411c285a1b0f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa73a1d0a12a3f036c1a5312db3b2c704e88b3112c003a1904fe926513426293(
    value: typing.Optional[EksClusterKubernetesNetworkConfigElasticLoadBalancing],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51376f3b372b03c4fd6f584f0dd2dd661c847d1b6126e4507dd2130950a3497(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7ea08f8b61ce4a53314176038d58448daede16b0f9c56edcd006bc17392d70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15464d2befdc2ca1818f977058e6848c2e677e768d08b0af108a6fc8df7f57b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70e4292584225b96da8a29bfebacf8e0a8476cd43ec4076f118346e3576dc94(
    value: typing.Optional[EksClusterKubernetesNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801d1a6ad1e716a1d20457362d540e38ca16d31819c753d6c62f13cba463ea25(
    *,
    control_plane_instance_type: builtins.str,
    outpost_arns: typing.Sequence[builtins.str],
    control_plane_placement: typing.Optional[typing.Union[EksClusterOutpostConfigControlPlanePlacement, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782a98501bd35a01e54fb9ba56de27cf20640473d5a42cf80269a26152cb93bc(
    *,
    group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8819ae56b1ecd5db96dc32cb80696c6ef464f36ca62db26c32628a4fe01513(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fc0e8e817b39c83758d5e6ff40bd4a79d9e5cd8b108cdcddd978a93e512fa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6159468d8ad81d679f86a571b5e3005a07947f993066e45c520b1ba96d7075db(
    value: typing.Optional[EksClusterOutpostConfigControlPlanePlacement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64459a26c3e1cd291cabcf6165499412a4597100b0be5c0384142607d62d5d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a6588ee8fd27025eabf59fef1cfbeb90666b677ea85a3c6267428d42db0e72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5770b65bb2e3ac57571d3ed8e84d6ba35609a48f466bf5afa13c1a42642d3f26(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd7fc2a5b75031d831d8d12a4f81089b6702e38d72bd55f862a120b48d61548(
    value: typing.Optional[EksClusterOutpostConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066d2842cffe80695ed832623d69d49f3ebaab055cc97e0e777dc5470f7a6663(
    *,
    remote_node_networks: typing.Union[EksClusterRemoteNetworkConfigRemoteNodeNetworks, typing.Dict[builtins.str, typing.Any]],
    remote_pod_networks: typing.Optional[typing.Union[EksClusterRemoteNetworkConfigRemotePodNetworks, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03dd5db0a402c833b23c432b08b58d3967a3309ace18f3a0203109831963e8c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f526197427baa7c217ad1600e3ea1fdb0e1dd6e4f6c563115f0f2a1e419f10(
    value: typing.Optional[EksClusterRemoteNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81f348f09bde218cd1a26033ba6ee13aeb9ed110c7c2a2b90051b5176e511c2(
    *,
    cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5cc55bf9dbcddfe0080e1a42f19b737514e24fb674009bc1f551bf1ad05091(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538694ab2c447307ef2876bf27f549d33b0109f9e17c0758557a63fd5ee028dd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abccdcda5233586c8ad568001f19697677dd2a81d0d9b486da7c717946aefa6e(
    value: typing.Optional[EksClusterRemoteNetworkConfigRemoteNodeNetworks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1626b961aea271b458dd6df61b845576824bb9c2804220310d67c47544cb08(
    *,
    cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19adae212920c3e1b7cc290c4f3e7b0d1153df83ccb2705713de0407623b90fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4303414e9b7b7e8e08fdfdc6015ebe0717b1ac7cec49be51401561aa04928083(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27229e8fcbd93985108ab2e0a2e88b210413851246acaed1758bce7471fddd8(
    value: typing.Optional[EksClusterRemoteNetworkConfigRemotePodNetworks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933437273a354047f9324282021abcd3d183fb853f6a53213ff527ff33686964(
    *,
    block_storage: typing.Optional[typing.Union[EksClusterStorageConfigBlockStorage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b3e399fbacf5f22b4264d7a7db092338930f3f2bc854c1231f681c57911758(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee366a61fa97a31a6c7f0e50f28cdfab91e9c91f717b58f631703ca247ba154(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031be166ccd285bdb8746f1efb7707f86c7a7558586a6431dd7d9d8a3006ab77(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8427cec5adb2e0501c50ee35d158cd0f1232659de8c99f979ec91e9f2be91dc5(
    value: typing.Optional[EksClusterStorageConfigBlockStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bd483ecd8f95d4a4b55e954260a6cefd338fdd7626457c3a3de7b6e8eff413(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56df416462014e9cff8b7219061b40d7e68395bfd854628b1a7b62ea85118d52(
    value: typing.Optional[EksClusterStorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0562bd4a009d0de96bba4233599d79cb0cc86f582743fb40b2a5784485e9b04(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ea8996894c7a9743bdb036f80e8cca09f323a8048528e16f91c258e6e49e14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb3040b7bd4a7b26fb24e4ffc2ddc0372de3f3b584929105f236f088822a76f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095ace7bf4b0babfb7cb7ab896e15d36f53669c1058d62a27deaf85b79eba7b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d7a77d96b17da6e9b6d9ea5622318a8bce62484a13113fc0c774ab1cc5165f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d347db10f4ee602118c211a11cb6f82b6a3b9f357ff397b3e2f470f18524982(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394695f065a0a72373b0576cb657c8281455fb465725bdabc93801abf300c245(
    *,
    support_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b65de338376cf780ca54f0a3ded035e49e38caf308ca9636f8723908db1609a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aadb5765590b16a0392287baf270123d413a0ea18f9c7c8d457f5b986182804c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb9666e5628f07b41c0449ac2588c032e8ac686689eb2d0b4d0502723c3c29b(
    value: typing.Optional[EksClusterUpgradePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad36e3c5c2fdc2116f9c5f3d7f8fb773c65938a6c7d4ed6ab7a5f13ae26b24d(
    *,
    subnet_ids: typing.Sequence[builtins.str],
    endpoint_private_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_public_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_access_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52352a40775f70ecc0d25b4f4900c7197549d9bf1fbfffede61f6b7e69e08be9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd109884bf5994f28245f94b434077ae4dcfcbeb137901ff4f0f151e5eaea09a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da7ea2001b456d279b1dfdc779a01f208713d671ea1a4268f11876d2f3a87c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1788d3762e7bef3e06e417721e399c8c4f99aecf1192fa76248b52b735a7f3ac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0094e0d69b51f5f571221f4c1e591866362005c6f7c71844014d35b09ce7658(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3fe68096c764886c6db1a658a4ae241e5bc6f808db2a6a4d78b5212b2f5de1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a94a0542c89a51dfe67e53a1a34967085ad47cfce69465c44c219b07ba0b4cb(
    value: typing.Optional[EksClusterVpcConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e24554a49fdbffca355298a48a51a1235cb4e48604b9dafcef404a25fe52c08(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3dd2e4420bec0e987b04641098adf54756a444dc410be89998ebc8aff6299f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2734e75d10fb969826fe68bfb28478608326e9aeddea9243020c313b04900b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1554860c71f39fa89412873ea61f23ed9806aa32ef239fe536aa293e399d22(
    value: typing.Optional[EksClusterZonalShiftConfig],
) -> None:
    """Type checking stubs"""
    pass
