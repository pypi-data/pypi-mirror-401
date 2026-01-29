r'''
# `aws_eks_node_group`

Refer to the Terraform Registry for docs: [`aws_eks_node_group`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group).
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


class EksNodeGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group aws_eks_node_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_name: builtins.str,
        node_role_arn: builtins.str,
        scaling_config: typing.Union["EksNodeGroupScalingConfig", typing.Dict[builtins.str, typing.Any]],
        subnet_ids: typing.Sequence[builtins.str],
        ami_type: typing.Optional[builtins.str] = None,
        capacity_type: typing.Optional[builtins.str] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_template: typing.Optional[typing.Union["EksNodeGroupLaunchTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        node_group_name: typing.Optional[builtins.str] = None,
        node_group_name_prefix: typing.Optional[builtins.str] = None,
        node_repair_config: typing.Optional[typing.Union["EksNodeGroupNodeRepairConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        release_version: typing.Optional[builtins.str] = None,
        remote_access: typing.Optional[typing.Union["EksNodeGroupRemoteAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EksNodeGroupTaint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["EksNodeGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_config: typing.Optional[typing.Union["EksNodeGroupUpdateConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group aws_eks_node_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#cluster_name EksNodeGroup#cluster_name}.
        :param node_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_role_arn EksNodeGroup#node_role_arn}.
        :param scaling_config: scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#scaling_config EksNodeGroup#scaling_config}
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#subnet_ids EksNodeGroup#subnet_ids}.
        :param ami_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#ami_type EksNodeGroup#ami_type}.
        :param capacity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#capacity_type EksNodeGroup#capacity_type}.
        :param disk_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#disk_size EksNodeGroup#disk_size}.
        :param force_update_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#force_update_version EksNodeGroup#force_update_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#id EksNodeGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#instance_types EksNodeGroup#instance_types}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#labels EksNodeGroup#labels}.
        :param launch_template: launch_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#launch_template EksNodeGroup#launch_template}
        :param node_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_group_name EksNodeGroup#node_group_name}.
        :param node_group_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_group_name_prefix EksNodeGroup#node_group_name_prefix}.
        :param node_repair_config: node_repair_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_repair_config EksNodeGroup#node_repair_config}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#region EksNodeGroup#region}
        :param release_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#release_version EksNodeGroup#release_version}.
        :param remote_access: remote_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#remote_access EksNodeGroup#remote_access}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#tags EksNodeGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#tags_all EksNodeGroup#tags_all}.
        :param taint: taint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#taint EksNodeGroup#taint}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#timeouts EksNodeGroup#timeouts}
        :param update_config: update_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#update_config EksNodeGroup#update_config}
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#version EksNodeGroup#version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48461204c8b5196e0df0deec2b4c3c912ac530a335447e23c2d45026693900c9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EksNodeGroupConfig(
            cluster_name=cluster_name,
            node_role_arn=node_role_arn,
            scaling_config=scaling_config,
            subnet_ids=subnet_ids,
            ami_type=ami_type,
            capacity_type=capacity_type,
            disk_size=disk_size,
            force_update_version=force_update_version,
            id=id,
            instance_types=instance_types,
            labels=labels,
            launch_template=launch_template,
            node_group_name=node_group_name,
            node_group_name_prefix=node_group_name_prefix,
            node_repair_config=node_repair_config,
            region=region,
            release_version=release_version,
            remote_access=remote_access,
            tags=tags,
            tags_all=tags_all,
            taint=taint,
            timeouts=timeouts,
            update_config=update_config,
            version=version,
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
        '''Generates CDKTF code for importing a EksNodeGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EksNodeGroup to import.
        :param import_from_id: The id of the existing EksNodeGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EksNodeGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1122379c8ca39e3707d595fe83e441320f61b72f39cfeed759c64ccda636b04)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLaunchTemplate")
    def put_launch_template(
        self,
        *,
        version: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#version EksNodeGroup#version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#id EksNodeGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#name EksNodeGroup#name}.
        '''
        value = EksNodeGroupLaunchTemplate(version=version, id=id, name=name)

        return typing.cast(None, jsii.invoke(self, "putLaunchTemplate", [value]))

    @jsii.member(jsii_name="putNodeRepairConfig")
    def put_node_repair_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_parallel_nodes_repaired_count: typing.Optional[jsii.Number] = None,
        max_parallel_nodes_repaired_percentage: typing.Optional[jsii.Number] = None,
        max_unhealthy_node_threshold_count: typing.Optional[jsii.Number] = None,
        max_unhealthy_node_threshold_percentage: typing.Optional[jsii.Number] = None,
        node_repair_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#enabled EksNodeGroup#enabled}.
        :param max_parallel_nodes_repaired_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_parallel_nodes_repaired_count EksNodeGroup#max_parallel_nodes_repaired_count}.
        :param max_parallel_nodes_repaired_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_parallel_nodes_repaired_percentage EksNodeGroup#max_parallel_nodes_repaired_percentage}.
        :param max_unhealthy_node_threshold_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unhealthy_node_threshold_count EksNodeGroup#max_unhealthy_node_threshold_count}.
        :param max_unhealthy_node_threshold_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unhealthy_node_threshold_percentage EksNodeGroup#max_unhealthy_node_threshold_percentage}.
        :param node_repair_config_overrides: node_repair_config_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_repair_config_overrides EksNodeGroup#node_repair_config_overrides}
        '''
        value = EksNodeGroupNodeRepairConfig(
            enabled=enabled,
            max_parallel_nodes_repaired_count=max_parallel_nodes_repaired_count,
            max_parallel_nodes_repaired_percentage=max_parallel_nodes_repaired_percentage,
            max_unhealthy_node_threshold_count=max_unhealthy_node_threshold_count,
            max_unhealthy_node_threshold_percentage=max_unhealthy_node_threshold_percentage,
            node_repair_config_overrides=node_repair_config_overrides,
        )

        return typing.cast(None, jsii.invoke(self, "putNodeRepairConfig", [value]))

    @jsii.member(jsii_name="putRemoteAccess")
    def put_remote_access(
        self,
        *,
        ec2_ssh_key: typing.Optional[builtins.str] = None,
        source_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ec2_ssh_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#ec2_ssh_key EksNodeGroup#ec2_ssh_key}.
        :param source_security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#source_security_group_ids EksNodeGroup#source_security_group_ids}.
        '''
        value = EksNodeGroupRemoteAccess(
            ec2_ssh_key=ec2_ssh_key,
            source_security_group_ids=source_security_group_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putRemoteAccess", [value]))

    @jsii.member(jsii_name="putScalingConfig")
    def put_scaling_config(
        self,
        *,
        desired_size: jsii.Number,
        max_size: jsii.Number,
        min_size: jsii.Number,
    ) -> None:
        '''
        :param desired_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#desired_size EksNodeGroup#desired_size}.
        :param max_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_size EksNodeGroup#max_size}.
        :param min_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#min_size EksNodeGroup#min_size}.
        '''
        value = EksNodeGroupScalingConfig(
            desired_size=desired_size, max_size=max_size, min_size=min_size
        )

        return typing.cast(None, jsii.invoke(self, "putScalingConfig", [value]))

    @jsii.member(jsii_name="putTaint")
    def put_taint(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EksNodeGroupTaint", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0dd258fc63014d1a3032f0b88e893ae52adec552690729bb460617b560acd8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaint", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#create EksNodeGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#delete EksNodeGroup#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#update EksNodeGroup#update}.
        '''
        value = EksNodeGroupTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpdateConfig")
    def put_update_config(
        self,
        *,
        max_unavailable: typing.Optional[jsii.Number] = None,
        max_unavailable_percentage: typing.Optional[jsii.Number] = None,
        update_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_unavailable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unavailable EksNodeGroup#max_unavailable}.
        :param max_unavailable_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unavailable_percentage EksNodeGroup#max_unavailable_percentage}.
        :param update_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#update_strategy EksNodeGroup#update_strategy}.
        '''
        value = EksNodeGroupUpdateConfig(
            max_unavailable=max_unavailable,
            max_unavailable_percentage=max_unavailable_percentage,
            update_strategy=update_strategy,
        )

        return typing.cast(None, jsii.invoke(self, "putUpdateConfig", [value]))

    @jsii.member(jsii_name="resetAmiType")
    def reset_ami_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmiType", []))

    @jsii.member(jsii_name="resetCapacityType")
    def reset_capacity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityType", []))

    @jsii.member(jsii_name="resetDiskSize")
    def reset_disk_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSize", []))

    @jsii.member(jsii_name="resetForceUpdateVersion")
    def reset_force_update_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceUpdateVersion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceTypes")
    def reset_instance_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceTypes", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLaunchTemplate")
    def reset_launch_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchTemplate", []))

    @jsii.member(jsii_name="resetNodeGroupName")
    def reset_node_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeGroupName", []))

    @jsii.member(jsii_name="resetNodeGroupNamePrefix")
    def reset_node_group_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeGroupNamePrefix", []))

    @jsii.member(jsii_name="resetNodeRepairConfig")
    def reset_node_repair_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeRepairConfig", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReleaseVersion")
    def reset_release_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReleaseVersion", []))

    @jsii.member(jsii_name="resetRemoteAccess")
    def reset_remote_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteAccess", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTaint")
    def reset_taint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaint", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpdateConfig")
    def reset_update_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateConfig", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(self) -> "EksNodeGroupLaunchTemplateOutputReference":
        return typing.cast("EksNodeGroupLaunchTemplateOutputReference", jsii.get(self, "launchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="nodeRepairConfig")
    def node_repair_config(self) -> "EksNodeGroupNodeRepairConfigOutputReference":
        return typing.cast("EksNodeGroupNodeRepairConfigOutputReference", jsii.get(self, "nodeRepairConfig"))

    @builtins.property
    @jsii.member(jsii_name="remoteAccess")
    def remote_access(self) -> "EksNodeGroupRemoteAccessOutputReference":
        return typing.cast("EksNodeGroupRemoteAccessOutputReference", jsii.get(self, "remoteAccess"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> "EksNodeGroupResourcesList":
        return typing.cast("EksNodeGroupResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfig")
    def scaling_config(self) -> "EksNodeGroupScalingConfigOutputReference":
        return typing.cast("EksNodeGroupScalingConfigOutputReference", jsii.get(self, "scalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="taint")
    def taint(self) -> "EksNodeGroupTaintList":
        return typing.cast("EksNodeGroupTaintList", jsii.get(self, "taint"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EksNodeGroupTimeoutsOutputReference":
        return typing.cast("EksNodeGroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateConfig")
    def update_config(self) -> "EksNodeGroupUpdateConfigOutputReference":
        return typing.cast("EksNodeGroupUpdateConfigOutputReference", jsii.get(self, "updateConfig"))

    @builtins.property
    @jsii.member(jsii_name="amiTypeInput")
    def ami_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "amiTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityTypeInput")
    def capacity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeInput")
    def disk_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeInput"))

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
    @jsii.member(jsii_name="instanceTypesInput")
    def instance_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instanceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateInput")
    def launch_template_input(self) -> typing.Optional["EksNodeGroupLaunchTemplate"]:
        return typing.cast(typing.Optional["EksNodeGroupLaunchTemplate"], jsii.get(self, "launchTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupNameInput")
    def node_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupNamePrefixInput")
    def node_group_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeGroupNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeRepairConfigInput")
    def node_repair_config_input(
        self,
    ) -> typing.Optional["EksNodeGroupNodeRepairConfig"]:
        return typing.cast(typing.Optional["EksNodeGroupNodeRepairConfig"], jsii.get(self, "nodeRepairConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeRoleArnInput")
    def node_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="releaseVersionInput")
    def release_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releaseVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteAccessInput")
    def remote_access_input(self) -> typing.Optional["EksNodeGroupRemoteAccess"]:
        return typing.cast(typing.Optional["EksNodeGroupRemoteAccess"], jsii.get(self, "remoteAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigInput")
    def scaling_config_input(self) -> typing.Optional["EksNodeGroupScalingConfig"]:
        return typing.cast(typing.Optional["EksNodeGroupScalingConfig"], jsii.get(self, "scalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

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
    @jsii.member(jsii_name="taintInput")
    def taint_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EksNodeGroupTaint"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EksNodeGroupTaint"]]], jsii.get(self, "taintInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EksNodeGroupTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EksNodeGroupTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="updateConfigInput")
    def update_config_input(self) -> typing.Optional["EksNodeGroupUpdateConfig"]:
        return typing.cast(typing.Optional["EksNodeGroupUpdateConfig"], jsii.get(self, "updateConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="amiType")
    def ami_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "amiType"))

    @ami_type.setter
    def ami_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d6e33e2dcfd9b6b985234b49ef9fe01d09566f27b39656d0c8bf279fe281ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amiType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacityType")
    def capacity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityType"))

    @capacity_type.setter
    def capacity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db16e5b2970693f7717c87846e7cdf51d5a9bfe8ae300ca270ad98fbdca49713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c23f62741dc66eaa49229a10e16d79b540aa3895979b50c4381382b50ec111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSize")
    def disk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSize"))

    @disk_size.setter
    def disk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8632f76cc6768e21362d4c64fff9d3ddaa0e6cad3be3bf54d61cbe5edc50f36b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSize", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__741d17096ff53769e615cc7818b234d4f4adf8d878fd921be0c21454255eb9bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdateVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0310d3450254965d2b58cdb674fe09fb88d693402a824f86c1c9e5ec9ff15f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceTypes"))

    @instance_types.setter
    def instance_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c930d28d2b6fe8d6b3d11fd2c524b3d8a3e06656f5391b7936f74e77d600dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b763f59bd8f2f83da4a8356759fb00e8aacd7075026d531fe898eb1cd6b5a7af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeGroupName")
    def node_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeGroupName"))

    @node_group_name.setter
    def node_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa2ef5d85a87c5ca590ed3637ad14eed7f82ba0957676fe9677d7ba9cebf4c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeGroupNamePrefix")
    def node_group_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeGroupNamePrefix"))

    @node_group_name_prefix.setter
    def node_group_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad78dcf78fd17ac15063b12dff1be54631ba253a17fb6d0da4e8687619cdb8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeGroupNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeRoleArn")
    def node_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeRoleArn"))

    @node_role_arn.setter
    def node_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__440afaa81b4c707f65cf06aa5f261ca175427db756f4e946cf31b86ce0df63c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beade79a2af90a8ffe0a9a9a8cd6973c5d8464ee237a4c0446f6065f044590c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseVersion"))

    @release_version.setter
    def release_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c06c8914dbaef1de20b1de87cf572212373effe04ea67c888a8f116e9d15db8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b81ea4493ea6e5dbdfc83eb229d96b9b17b856e1160b8a17c5bba5805205bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d291b6761262fc37c52f9589cb495aefce4556f0c244372932ee23f46942dff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db3b2987a5600a1b356f0aa46a18fcd19d75db3fbf30cb9ea18a82979129adac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb787398634c2f327d93f3d2dfe77cda5fc106ae62ccde0dcca8e4b23dac633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_name": "clusterName",
        "node_role_arn": "nodeRoleArn",
        "scaling_config": "scalingConfig",
        "subnet_ids": "subnetIds",
        "ami_type": "amiType",
        "capacity_type": "capacityType",
        "disk_size": "diskSize",
        "force_update_version": "forceUpdateVersion",
        "id": "id",
        "instance_types": "instanceTypes",
        "labels": "labels",
        "launch_template": "launchTemplate",
        "node_group_name": "nodeGroupName",
        "node_group_name_prefix": "nodeGroupNamePrefix",
        "node_repair_config": "nodeRepairConfig",
        "region": "region",
        "release_version": "releaseVersion",
        "remote_access": "remoteAccess",
        "tags": "tags",
        "tags_all": "tagsAll",
        "taint": "taint",
        "timeouts": "timeouts",
        "update_config": "updateConfig",
        "version": "version",
    },
)
class EksNodeGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_name: builtins.str,
        node_role_arn: builtins.str,
        scaling_config: typing.Union["EksNodeGroupScalingConfig", typing.Dict[builtins.str, typing.Any]],
        subnet_ids: typing.Sequence[builtins.str],
        ami_type: typing.Optional[builtins.str] = None,
        capacity_type: typing.Optional[builtins.str] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_template: typing.Optional[typing.Union["EksNodeGroupLaunchTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        node_group_name: typing.Optional[builtins.str] = None,
        node_group_name_prefix: typing.Optional[builtins.str] = None,
        node_repair_config: typing.Optional[typing.Union["EksNodeGroupNodeRepairConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        release_version: typing.Optional[builtins.str] = None,
        remote_access: typing.Optional[typing.Union["EksNodeGroupRemoteAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EksNodeGroupTaint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["EksNodeGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_config: typing.Optional[typing.Union["EksNodeGroupUpdateConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#cluster_name EksNodeGroup#cluster_name}.
        :param node_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_role_arn EksNodeGroup#node_role_arn}.
        :param scaling_config: scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#scaling_config EksNodeGroup#scaling_config}
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#subnet_ids EksNodeGroup#subnet_ids}.
        :param ami_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#ami_type EksNodeGroup#ami_type}.
        :param capacity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#capacity_type EksNodeGroup#capacity_type}.
        :param disk_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#disk_size EksNodeGroup#disk_size}.
        :param force_update_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#force_update_version EksNodeGroup#force_update_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#id EksNodeGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#instance_types EksNodeGroup#instance_types}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#labels EksNodeGroup#labels}.
        :param launch_template: launch_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#launch_template EksNodeGroup#launch_template}
        :param node_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_group_name EksNodeGroup#node_group_name}.
        :param node_group_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_group_name_prefix EksNodeGroup#node_group_name_prefix}.
        :param node_repair_config: node_repair_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_repair_config EksNodeGroup#node_repair_config}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#region EksNodeGroup#region}
        :param release_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#release_version EksNodeGroup#release_version}.
        :param remote_access: remote_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#remote_access EksNodeGroup#remote_access}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#tags EksNodeGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#tags_all EksNodeGroup#tags_all}.
        :param taint: taint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#taint EksNodeGroup#taint}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#timeouts EksNodeGroup#timeouts}
        :param update_config: update_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#update_config EksNodeGroup#update_config}
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#version EksNodeGroup#version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(scaling_config, dict):
            scaling_config = EksNodeGroupScalingConfig(**scaling_config)
        if isinstance(launch_template, dict):
            launch_template = EksNodeGroupLaunchTemplate(**launch_template)
        if isinstance(node_repair_config, dict):
            node_repair_config = EksNodeGroupNodeRepairConfig(**node_repair_config)
        if isinstance(remote_access, dict):
            remote_access = EksNodeGroupRemoteAccess(**remote_access)
        if isinstance(timeouts, dict):
            timeouts = EksNodeGroupTimeouts(**timeouts)
        if isinstance(update_config, dict):
            update_config = EksNodeGroupUpdateConfig(**update_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1801ec0f597f111dac90e5874085cd59c4278b861c272ba57d56a5b6950211)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument node_role_arn", value=node_role_arn, expected_type=type_hints["node_role_arn"])
            check_type(argname="argument scaling_config", value=scaling_config, expected_type=type_hints["scaling_config"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument ami_type", value=ami_type, expected_type=type_hints["ami_type"])
            check_type(argname="argument capacity_type", value=capacity_type, expected_type=type_hints["capacity_type"])
            check_type(argname="argument disk_size", value=disk_size, expected_type=type_hints["disk_size"])
            check_type(argname="argument force_update_version", value=force_update_version, expected_type=type_hints["force_update_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument node_group_name", value=node_group_name, expected_type=type_hints["node_group_name"])
            check_type(argname="argument node_group_name_prefix", value=node_group_name_prefix, expected_type=type_hints["node_group_name_prefix"])
            check_type(argname="argument node_repair_config", value=node_repair_config, expected_type=type_hints["node_repair_config"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument release_version", value=release_version, expected_type=type_hints["release_version"])
            check_type(argname="argument remote_access", value=remote_access, expected_type=type_hints["remote_access"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument taint", value=taint, expected_type=type_hints["taint"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument update_config", value=update_config, expected_type=type_hints["update_config"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "node_role_arn": node_role_arn,
            "scaling_config": scaling_config,
            "subnet_ids": subnet_ids,
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
        if ami_type is not None:
            self._values["ami_type"] = ami_type
        if capacity_type is not None:
            self._values["capacity_type"] = capacity_type
        if disk_size is not None:
            self._values["disk_size"] = disk_size
        if force_update_version is not None:
            self._values["force_update_version"] = force_update_version
        if id is not None:
            self._values["id"] = id
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if labels is not None:
            self._values["labels"] = labels
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if node_group_name is not None:
            self._values["node_group_name"] = node_group_name
        if node_group_name_prefix is not None:
            self._values["node_group_name_prefix"] = node_group_name_prefix
        if node_repair_config is not None:
            self._values["node_repair_config"] = node_repair_config
        if region is not None:
            self._values["region"] = region
        if release_version is not None:
            self._values["release_version"] = release_version
        if remote_access is not None:
            self._values["remote_access"] = remote_access
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if taint is not None:
            self._values["taint"] = taint
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if update_config is not None:
            self._values["update_config"] = update_config
        if version is not None:
            self._values["version"] = version

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
    def cluster_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#cluster_name EksNodeGroup#cluster_name}.'''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_role_arn EksNodeGroup#node_role_arn}.'''
        result = self._values.get("node_role_arn")
        assert result is not None, "Required property 'node_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_config(self) -> "EksNodeGroupScalingConfig":
        '''scaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#scaling_config EksNodeGroup#scaling_config}
        '''
        result = self._values.get("scaling_config")
        assert result is not None, "Required property 'scaling_config' is missing"
        return typing.cast("EksNodeGroupScalingConfig", result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#subnet_ids EksNodeGroup#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ami_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#ami_type EksNodeGroup#ami_type}.'''
        result = self._values.get("ami_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capacity_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#capacity_type EksNodeGroup#capacity_type}.'''
        result = self._values.get("capacity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#disk_size EksNodeGroup#disk_size}.'''
        result = self._values.get("disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def force_update_version(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#force_update_version EksNodeGroup#force_update_version}.'''
        result = self._values.get("force_update_version")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#id EksNodeGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#instance_types EksNodeGroup#instance_types}.'''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#labels EksNodeGroup#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def launch_template(self) -> typing.Optional["EksNodeGroupLaunchTemplate"]:
        '''launch_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#launch_template EksNodeGroup#launch_template}
        '''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional["EksNodeGroupLaunchTemplate"], result)

    @builtins.property
    def node_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_group_name EksNodeGroup#node_group_name}.'''
        result = self._values.get("node_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_group_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_group_name_prefix EksNodeGroup#node_group_name_prefix}.'''
        result = self._values.get("node_group_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_repair_config(self) -> typing.Optional["EksNodeGroupNodeRepairConfig"]:
        '''node_repair_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_repair_config EksNodeGroup#node_repair_config}
        '''
        result = self._values.get("node_repair_config")
        return typing.cast(typing.Optional["EksNodeGroupNodeRepairConfig"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#region EksNodeGroup#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#release_version EksNodeGroup#release_version}.'''
        result = self._values.get("release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_access(self) -> typing.Optional["EksNodeGroupRemoteAccess"]:
        '''remote_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#remote_access EksNodeGroup#remote_access}
        '''
        result = self._values.get("remote_access")
        return typing.cast(typing.Optional["EksNodeGroupRemoteAccess"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#tags EksNodeGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#tags_all EksNodeGroup#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def taint(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EksNodeGroupTaint"]]]:
        '''taint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#taint EksNodeGroup#taint}
        '''
        result = self._values.get("taint")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EksNodeGroupTaint"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EksNodeGroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#timeouts EksNodeGroup#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EksNodeGroupTimeouts"], result)

    @builtins.property
    def update_config(self) -> typing.Optional["EksNodeGroupUpdateConfig"]:
        '''update_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#update_config EksNodeGroup#update_config}
        '''
        result = self._values.get("update_config")
        return typing.cast(typing.Optional["EksNodeGroupUpdateConfig"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#version EksNodeGroup#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupLaunchTemplate",
    jsii_struct_bases=[],
    name_mapping={"version": "version", "id": "id", "name": "name"},
)
class EksNodeGroupLaunchTemplate:
    def __init__(
        self,
        *,
        version: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#version EksNodeGroup#version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#id EksNodeGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#name EksNodeGroup#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145dbe37290467a0aa6f74c4023de8df40b94d5f2101e512426a13c8bbf2884d)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#version EksNodeGroup#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#id EksNodeGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#name EksNodeGroup#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupLaunchTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksNodeGroupLaunchTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupLaunchTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__195da0acbdf561cb3a4c82add90af8f3cd638768122a78d1c7ada4e0a7a289bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4354f752d733041145917c9b77cddcf45bb184e26e05170e453910f4ff01ff6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e309900de318ed4df1e595dcb582d03102174ee870de3c0655c44af4b10342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b829022aa8f7ab4a2ceb99ffc65b9e89ef31e81cca86c7eb8e400a451305b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksNodeGroupLaunchTemplate]:
        return typing.cast(typing.Optional[EksNodeGroupLaunchTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksNodeGroupLaunchTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc396e299c74ef20b76ae6e3cd313b36513a85b28d10786bdb57765b85c9a72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupNodeRepairConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "max_parallel_nodes_repaired_count": "maxParallelNodesRepairedCount",
        "max_parallel_nodes_repaired_percentage": "maxParallelNodesRepairedPercentage",
        "max_unhealthy_node_threshold_count": "maxUnhealthyNodeThresholdCount",
        "max_unhealthy_node_threshold_percentage": "maxUnhealthyNodeThresholdPercentage",
        "node_repair_config_overrides": "nodeRepairConfigOverrides",
    },
)
class EksNodeGroupNodeRepairConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_parallel_nodes_repaired_count: typing.Optional[jsii.Number] = None,
        max_parallel_nodes_repaired_percentage: typing.Optional[jsii.Number] = None,
        max_unhealthy_node_threshold_count: typing.Optional[jsii.Number] = None,
        max_unhealthy_node_threshold_percentage: typing.Optional[jsii.Number] = None,
        node_repair_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#enabled EksNodeGroup#enabled}.
        :param max_parallel_nodes_repaired_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_parallel_nodes_repaired_count EksNodeGroup#max_parallel_nodes_repaired_count}.
        :param max_parallel_nodes_repaired_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_parallel_nodes_repaired_percentage EksNodeGroup#max_parallel_nodes_repaired_percentage}.
        :param max_unhealthy_node_threshold_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unhealthy_node_threshold_count EksNodeGroup#max_unhealthy_node_threshold_count}.
        :param max_unhealthy_node_threshold_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unhealthy_node_threshold_percentage EksNodeGroup#max_unhealthy_node_threshold_percentage}.
        :param node_repair_config_overrides: node_repair_config_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_repair_config_overrides EksNodeGroup#node_repair_config_overrides}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e2599466a967ddebd58cf5d9c0e327745a93f2b1f61014d796209ff425083b)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_parallel_nodes_repaired_count", value=max_parallel_nodes_repaired_count, expected_type=type_hints["max_parallel_nodes_repaired_count"])
            check_type(argname="argument max_parallel_nodes_repaired_percentage", value=max_parallel_nodes_repaired_percentage, expected_type=type_hints["max_parallel_nodes_repaired_percentage"])
            check_type(argname="argument max_unhealthy_node_threshold_count", value=max_unhealthy_node_threshold_count, expected_type=type_hints["max_unhealthy_node_threshold_count"])
            check_type(argname="argument max_unhealthy_node_threshold_percentage", value=max_unhealthy_node_threshold_percentage, expected_type=type_hints["max_unhealthy_node_threshold_percentage"])
            check_type(argname="argument node_repair_config_overrides", value=node_repair_config_overrides, expected_type=type_hints["node_repair_config_overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_parallel_nodes_repaired_count is not None:
            self._values["max_parallel_nodes_repaired_count"] = max_parallel_nodes_repaired_count
        if max_parallel_nodes_repaired_percentage is not None:
            self._values["max_parallel_nodes_repaired_percentage"] = max_parallel_nodes_repaired_percentage
        if max_unhealthy_node_threshold_count is not None:
            self._values["max_unhealthy_node_threshold_count"] = max_unhealthy_node_threshold_count
        if max_unhealthy_node_threshold_percentage is not None:
            self._values["max_unhealthy_node_threshold_percentage"] = max_unhealthy_node_threshold_percentage
        if node_repair_config_overrides is not None:
            self._values["node_repair_config_overrides"] = node_repair_config_overrides

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#enabled EksNodeGroup#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_parallel_nodes_repaired_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_parallel_nodes_repaired_count EksNodeGroup#max_parallel_nodes_repaired_count}.'''
        result = self._values.get("max_parallel_nodes_repaired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_parallel_nodes_repaired_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_parallel_nodes_repaired_percentage EksNodeGroup#max_parallel_nodes_repaired_percentage}.'''
        result = self._values.get("max_parallel_nodes_repaired_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unhealthy_node_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unhealthy_node_threshold_count EksNodeGroup#max_unhealthy_node_threshold_count}.'''
        result = self._values.get("max_unhealthy_node_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unhealthy_node_threshold_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unhealthy_node_threshold_percentage EksNodeGroup#max_unhealthy_node_threshold_percentage}.'''
        result = self._values.get("max_unhealthy_node_threshold_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_repair_config_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides"]]]:
        '''node_repair_config_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_repair_config_overrides EksNodeGroup#node_repair_config_overrides}
        '''
        result = self._values.get("node_repair_config_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupNodeRepairConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "min_repair_wait_time_mins": "minRepairWaitTimeMins",
        "node_monitoring_condition": "nodeMonitoringCondition",
        "node_unhealthy_reason": "nodeUnhealthyReason",
        "repair_action": "repairAction",
    },
)
class EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides:
    def __init__(
        self,
        *,
        min_repair_wait_time_mins: jsii.Number,
        node_monitoring_condition: builtins.str,
        node_unhealthy_reason: builtins.str,
        repair_action: builtins.str,
    ) -> None:
        '''
        :param min_repair_wait_time_mins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#min_repair_wait_time_mins EksNodeGroup#min_repair_wait_time_mins}.
        :param node_monitoring_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_monitoring_condition EksNodeGroup#node_monitoring_condition}.
        :param node_unhealthy_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_unhealthy_reason EksNodeGroup#node_unhealthy_reason}.
        :param repair_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#repair_action EksNodeGroup#repair_action}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5387dc65098e3cd79d2cc918b491c1b7938b6919855d057793be3a3fc736b710)
            check_type(argname="argument min_repair_wait_time_mins", value=min_repair_wait_time_mins, expected_type=type_hints["min_repair_wait_time_mins"])
            check_type(argname="argument node_monitoring_condition", value=node_monitoring_condition, expected_type=type_hints["node_monitoring_condition"])
            check_type(argname="argument node_unhealthy_reason", value=node_unhealthy_reason, expected_type=type_hints["node_unhealthy_reason"])
            check_type(argname="argument repair_action", value=repair_action, expected_type=type_hints["repair_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "min_repair_wait_time_mins": min_repair_wait_time_mins,
            "node_monitoring_condition": node_monitoring_condition,
            "node_unhealthy_reason": node_unhealthy_reason,
            "repair_action": repair_action,
        }

    @builtins.property
    def min_repair_wait_time_mins(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#min_repair_wait_time_mins EksNodeGroup#min_repair_wait_time_mins}.'''
        result = self._values.get("min_repair_wait_time_mins")
        assert result is not None, "Required property 'min_repair_wait_time_mins' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def node_monitoring_condition(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_monitoring_condition EksNodeGroup#node_monitoring_condition}.'''
        result = self._values.get("node_monitoring_condition")
        assert result is not None, "Required property 'node_monitoring_condition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_unhealthy_reason(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#node_unhealthy_reason EksNodeGroup#node_unhealthy_reason}.'''
        result = self._values.get("node_unhealthy_reason")
        assert result is not None, "Required property 'node_unhealthy_reason' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repair_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#repair_action EksNodeGroup#repair_action}.'''
        result = self._values.get("repair_action")
        assert result is not None, "Required property 'repair_action' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksNodeGroupNodeRepairConfigNodeRepairConfigOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupNodeRepairConfigNodeRepairConfigOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e4714b33b50d91099cbc99515b67badbd34ea0617a5f04895da580523fa56d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EksNodeGroupNodeRepairConfigNodeRepairConfigOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6bb0b054108a1bf6a12b1482e312cffbdb11ab2d239adc107a097793b451f03)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EksNodeGroupNodeRepairConfigNodeRepairConfigOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c0cf245bab6b78534693008917bb6271a1a403a4609553f363a161b75d8e17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37fab53cb48b585c0ae8a790f6eefd86cc3e948ecb62d26da5089e4bfb35d56f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b2afff932ffca9e3bc708c232b721ac520d893683352e26d0213f178b0544a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623022df01583f7cf9cbaf58509925bb6447422bbd274a3748f6decc7b0490f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EksNodeGroupNodeRepairConfigNodeRepairConfigOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupNodeRepairConfigNodeRepairConfigOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e132069e089263cd8a53b67b1dc9a2eea41855b36d6a0748577e94cce2db371c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="minRepairWaitTimeMinsInput")
    def min_repair_wait_time_mins_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minRepairWaitTimeMinsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeMonitoringConditionInput")
    def node_monitoring_condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeMonitoringConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeUnhealthyReasonInput")
    def node_unhealthy_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeUnhealthyReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="repairActionInput")
    def repair_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repairActionInput"))

    @builtins.property
    @jsii.member(jsii_name="minRepairWaitTimeMins")
    def min_repair_wait_time_mins(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRepairWaitTimeMins"))

    @min_repair_wait_time_mins.setter
    def min_repair_wait_time_mins(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ce5bbe5bc50e0d4fdef0e143ec86990991e7b87fb531e7915bd2d809279fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRepairWaitTimeMins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeMonitoringCondition")
    def node_monitoring_condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeMonitoringCondition"))

    @node_monitoring_condition.setter
    def node_monitoring_condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370fed2ea819ba02572c4a82ab1881946b13024a4926ea16b624fcad26245747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeMonitoringCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeUnhealthyReason")
    def node_unhealthy_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeUnhealthyReason"))

    @node_unhealthy_reason.setter
    def node_unhealthy_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a61d488bad6d630daec5a120479df574c4ce926f5dd4e5b8dbc58405a2a23036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeUnhealthyReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repairAction")
    def repair_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repairAction"))

    @repair_action.setter
    def repair_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e23fdccb0987c1f0e9203fec563fa16efdc44f095687ae2d97ed257102918428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repairAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9acf24af3e7eec58b9018ce9b241dc7ecba76637d18a5b343d3ea5a53dcabe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EksNodeGroupNodeRepairConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupNodeRepairConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e60c0975a9d5b191dd002c083c3f177b07b2c7a7ad09b2adf4ee869a542bf20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeRepairConfigOverrides")
    def put_node_repair_config_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b745ed8aabec07612f3a45f7065629f52ce1f311d23a42f37e13c3fc04fa8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeRepairConfigOverrides", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetMaxParallelNodesRepairedCount")
    def reset_max_parallel_nodes_repaired_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxParallelNodesRepairedCount", []))

    @jsii.member(jsii_name="resetMaxParallelNodesRepairedPercentage")
    def reset_max_parallel_nodes_repaired_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxParallelNodesRepairedPercentage", []))

    @jsii.member(jsii_name="resetMaxUnhealthyNodeThresholdCount")
    def reset_max_unhealthy_node_threshold_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnhealthyNodeThresholdCount", []))

    @jsii.member(jsii_name="resetMaxUnhealthyNodeThresholdPercentage")
    def reset_max_unhealthy_node_threshold_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnhealthyNodeThresholdPercentage", []))

    @jsii.member(jsii_name="resetNodeRepairConfigOverrides")
    def reset_node_repair_config_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeRepairConfigOverrides", []))

    @builtins.property
    @jsii.member(jsii_name="nodeRepairConfigOverrides")
    def node_repair_config_overrides(
        self,
    ) -> EksNodeGroupNodeRepairConfigNodeRepairConfigOverridesList:
        return typing.cast(EksNodeGroupNodeRepairConfigNodeRepairConfigOverridesList, jsii.get(self, "nodeRepairConfigOverrides"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="maxParallelNodesRepairedCountInput")
    def max_parallel_nodes_repaired_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxParallelNodesRepairedCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxParallelNodesRepairedPercentageInput")
    def max_parallel_nodes_repaired_percentage_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxParallelNodesRepairedPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyNodeThresholdCountInput")
    def max_unhealthy_node_threshold_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnhealthyNodeThresholdCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyNodeThresholdPercentageInput")
    def max_unhealthy_node_threshold_percentage_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnhealthyNodeThresholdPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeRepairConfigOverridesInput")
    def node_repair_config_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides]]], jsii.get(self, "nodeRepairConfigOverridesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cd4142d7992f73d5569e03298f8b3d9eca7c1e22b3fd4de85bb1961409f4e9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxParallelNodesRepairedCount")
    def max_parallel_nodes_repaired_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxParallelNodesRepairedCount"))

    @max_parallel_nodes_repaired_count.setter
    def max_parallel_nodes_repaired_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990aecb7d139996fa42c4d8c96b06a044498d05fc7503ad853a0499c68216237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxParallelNodesRepairedCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxParallelNodesRepairedPercentage")
    def max_parallel_nodes_repaired_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxParallelNodesRepairedPercentage"))

    @max_parallel_nodes_repaired_percentage.setter
    def max_parallel_nodes_repaired_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b74b65a3a53068c816522be2de82ad2d34aeb31ee539adc64eca4af387096cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxParallelNodesRepairedPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyNodeThresholdCount")
    def max_unhealthy_node_threshold_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnhealthyNodeThresholdCount"))

    @max_unhealthy_node_threshold_count.setter
    def max_unhealthy_node_threshold_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a44ee953515362cd747c9ff112717e4c2f83636b4aed72649f8a6b74d9ca5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnhealthyNodeThresholdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyNodeThresholdPercentage")
    def max_unhealthy_node_threshold_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnhealthyNodeThresholdPercentage"))

    @max_unhealthy_node_threshold_percentage.setter
    def max_unhealthy_node_threshold_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f23045695e76c14de0d8389383b277ad56460e7cfc11ed0b82d921fa3061bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnhealthyNodeThresholdPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksNodeGroupNodeRepairConfig]:
        return typing.cast(typing.Optional[EksNodeGroupNodeRepairConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksNodeGroupNodeRepairConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80fa43560c380256cb007cd2b0e03cf2f498208b8c532a7b2e5cbb24b831e90a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupRemoteAccess",
    jsii_struct_bases=[],
    name_mapping={
        "ec2_ssh_key": "ec2SshKey",
        "source_security_group_ids": "sourceSecurityGroupIds",
    },
)
class EksNodeGroupRemoteAccess:
    def __init__(
        self,
        *,
        ec2_ssh_key: typing.Optional[builtins.str] = None,
        source_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ec2_ssh_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#ec2_ssh_key EksNodeGroup#ec2_ssh_key}.
        :param source_security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#source_security_group_ids EksNodeGroup#source_security_group_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc43ad9ce14d9af9af22b67c8e4f75310ca318e3a8d0fabc476c03ad17121012)
            check_type(argname="argument ec2_ssh_key", value=ec2_ssh_key, expected_type=type_hints["ec2_ssh_key"])
            check_type(argname="argument source_security_group_ids", value=source_security_group_ids, expected_type=type_hints["source_security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ec2_ssh_key is not None:
            self._values["ec2_ssh_key"] = ec2_ssh_key
        if source_security_group_ids is not None:
            self._values["source_security_group_ids"] = source_security_group_ids

    @builtins.property
    def ec2_ssh_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#ec2_ssh_key EksNodeGroup#ec2_ssh_key}.'''
        result = self._values.get("ec2_ssh_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#source_security_group_ids EksNodeGroup#source_security_group_ids}.'''
        result = self._values.get("source_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupRemoteAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksNodeGroupRemoteAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupRemoteAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd2fe47dddf12f723d61b0e647ffc3ff6e7c9829a8cb0a3d8cffb1bceb72f7e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEc2SshKey")
    def reset_ec2_ssh_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2SshKey", []))

    @jsii.member(jsii_name="resetSourceSecurityGroupIds")
    def reset_source_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSecurityGroupIds", []))

    @builtins.property
    @jsii.member(jsii_name="ec2SshKeyInput")
    def ec2_ssh_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ec2SshKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSecurityGroupIdsInput")
    def source_security_group_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceSecurityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2SshKey")
    def ec2_ssh_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ec2SshKey"))

    @ec2_ssh_key.setter
    def ec2_ssh_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc806029f175a38c469160b2a971c6d25bdf92476bfc89c387244b62df347119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2SshKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSecurityGroupIds")
    def source_security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceSecurityGroupIds"))

    @source_security_group_ids.setter
    def source_security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa6c7dcc9ec5c41da2bbb51a47ec82ea9bc6443e7d231990cee2bde42f6cd1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSecurityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksNodeGroupRemoteAccess]:
        return typing.cast(typing.Optional[EksNodeGroupRemoteAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksNodeGroupRemoteAccess]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad72c7ff385a8e554975b0a39c36461260d547e4edeef20cb560f50214cb334f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupResources",
    jsii_struct_bases=[],
    name_mapping={},
)
class EksNodeGroupResources:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupResourcesAutoscalingGroups",
    jsii_struct_bases=[],
    name_mapping={},
)
class EksNodeGroupResourcesAutoscalingGroups:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupResourcesAutoscalingGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksNodeGroupResourcesAutoscalingGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupResourcesAutoscalingGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7da07d0ee26f014df1ac5f25db0ff3637f2f69db7e2b1f9c21f411bf878a936a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EksNodeGroupResourcesAutoscalingGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd1b781527ac5d6e24ec00c431060a53bcd0d912b8a5a2931ff1ff525335ab6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EksNodeGroupResourcesAutoscalingGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9acd56b10ba79ec50a96d092cbc0332cad3e4afd40029eb1e979170c525e06eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5880e8be809ebde4c8e99443f0a54c54690ca581a70428843afa2abc885ab3d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78e5003116429b56f8d84727c100b537dcd6f485a7470196a565e41504221e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class EksNodeGroupResourcesAutoscalingGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupResourcesAutoscalingGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6473076e5d93ae66f0c8013129684f43ed3907420fff22dd780782dbea2c7e09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksNodeGroupResourcesAutoscalingGroups]:
        return typing.cast(typing.Optional[EksNodeGroupResourcesAutoscalingGroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EksNodeGroupResourcesAutoscalingGroups],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd92a7bb81d9fe56f6b082114e6767cba2c23c638f7d9a5efbd11845b912004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EksNodeGroupResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5907e71a4d6aea7d5d79adeedabbf87e69f045f88b944cf34f7b87cb82a447ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EksNodeGroupResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67bfeb471d242c56a633c70f86097c30a0757d74ce41cc787aca510560807fb1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EksNodeGroupResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3368303cb572e2b1ffde3750bea6b0a4eb7131acf5d0401ec51b074d499a4f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ccf56dbcd8ee93737638532ad845a04f05d861817a7a66235352e8dc00555b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d90a0019730aba50ff22d738db7e4de8009087a53983b650b7abad1c45ab90f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class EksNodeGroupResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__412da5ac7510a5d729278a690b840f3216c985d063942f48e0061d729440c1ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="autoscalingGroups")
    def autoscaling_groups(self) -> EksNodeGroupResourcesAutoscalingGroupsList:
        return typing.cast(EksNodeGroupResourcesAutoscalingGroupsList, jsii.get(self, "autoscalingGroups"))

    @builtins.property
    @jsii.member(jsii_name="remoteAccessSecurityGroupId")
    def remote_access_security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteAccessSecurityGroupId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksNodeGroupResources]:
        return typing.cast(typing.Optional[EksNodeGroupResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksNodeGroupResources]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b53320bc61edd2071306e0490be6b3c3453a8f71791286f6563e4c18e29483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupScalingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "desired_size": "desiredSize",
        "max_size": "maxSize",
        "min_size": "minSize",
    },
)
class EksNodeGroupScalingConfig:
    def __init__(
        self,
        *,
        desired_size: jsii.Number,
        max_size: jsii.Number,
        min_size: jsii.Number,
    ) -> None:
        '''
        :param desired_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#desired_size EksNodeGroup#desired_size}.
        :param max_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_size EksNodeGroup#max_size}.
        :param min_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#min_size EksNodeGroup#min_size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c151ba68ef01c2863447ee930f88bbbbbdd9e0f02d565af45afef1251c65d19)
            check_type(argname="argument desired_size", value=desired_size, expected_type=type_hints["desired_size"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "desired_size": desired_size,
            "max_size": max_size,
            "min_size": min_size,
        }

    @builtins.property
    def desired_size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#desired_size EksNodeGroup#desired_size}.'''
        result = self._values.get("desired_size")
        assert result is not None, "Required property 'desired_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_size EksNodeGroup#max_size}.'''
        result = self._values.get("max_size")
        assert result is not None, "Required property 'max_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#min_size EksNodeGroup#min_size}.'''
        result = self._values.get("min_size")
        assert result is not None, "Required property 'min_size' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupScalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksNodeGroupScalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupScalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f4d779eff1b8c119ef5e9c6f797fa6323ddff2483364080214e3f23ed8bcbfa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="desiredSizeInput")
    def desired_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "desiredSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSizeInput")
    def max_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="minSizeInput")
    def min_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredSize")
    def desired_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "desiredSize"))

    @desired_size.setter
    def desired_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9ee95b632e899e29c4cf8354daaa5880a6e540f30f825f6ddf1a67cf75b1a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSize")
    def max_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSize"))

    @max_size.setter
    def max_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff22a62a551016dd232ac40c85ebec8f5850c3dc92abc63dc51ced2745392fd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minSize")
    def min_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minSize"))

    @min_size.setter
    def min_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab719de8b6a90ac2a392c669c84221b1ca9712032d2021da0d320d30c61fe106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksNodeGroupScalingConfig]:
        return typing.cast(typing.Optional[EksNodeGroupScalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksNodeGroupScalingConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e3d3997563887e3ee1824127a4500c058ece5236c43ddf81d2d5978ec6d9a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupTaint",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class EksNodeGroupTaint:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#effect EksNodeGroup#effect}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#key EksNodeGroup#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#value EksNodeGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7ffbd61aada4002905c284f0633bc297094f7a8de80c57cef94b290e42b7b1)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effect": effect,
            "key": key,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def effect(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#effect EksNodeGroup#effect}.'''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#key EksNodeGroup#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#value EksNodeGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupTaint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksNodeGroupTaintList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupTaintList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9106fbe288a6323842e50d6927f3e083956082cf47b215333d22059c47b3e804)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EksNodeGroupTaintOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc15b6562588b4ade8df4543811d4702e4c05f920cb4b3ac67d3d65026d5e5b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EksNodeGroupTaintOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6876e84a1ade583d6217609d8c0425c23672a39a4358b357b19519d8076b15fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__965b62d3fef6de6dca311391a428497d525d350def65b9a24abba0bc9601cd28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6e42aa021a38bb4c7afe3ec2e04b9b21a82321c99f1cdfec5df1909e6f44a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EksNodeGroupTaint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EksNodeGroupTaint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EksNodeGroupTaint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857405fee900363faa10aa80dbbbc6256f483eec320b5dc32727e865f3bc1b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EksNodeGroupTaintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupTaintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edb317d757a2253dc87e541bb5e33c0f30c478814a80a13303ac75f50d9b8685)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4f1299f951e0a1193ee67613d63318ad53655ea463ca90d4f111a22c9f139d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6ab538b0c758caeda82bc4f9ecbeeef2050cc89de7e2fe8368456b636cc6e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1343cdccd5e7bfe1a12a3c90334014297debd4c705be5493614312e9c5967f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupTaint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupTaint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupTaint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc774487c04ce68a894dac303bff3d3b727450c0724b412076c5e737c05dbd85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class EksNodeGroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#create EksNodeGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#delete EksNodeGroup#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#update EksNodeGroup#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c405d19043e0d0c22266d2f7c83c84c5399cf968c2dd05f279a51a17cab98b94)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#create EksNodeGroup#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#delete EksNodeGroup#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#update EksNodeGroup#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksNodeGroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2abd533d5b3e48a0e17345f573127693f38e75082bfefac5a37d82a7e802b6c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db13a384be76fe4d50aae2e0d1038a652e882e726f8d717b8a8231ad30851366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9126dbb137cdac25252a1b8948ceb16b60444a36a1932e63de8f6b0222563101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4799f17977bfadf910e2d45ab56b70b4a0df99f98cd06da76146be4246dcd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623b747886b1d5c8511a8d972125cf60d3aa4927393616c885baeeaf8a02ddf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupUpdateConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_unavailable": "maxUnavailable",
        "max_unavailable_percentage": "maxUnavailablePercentage",
        "update_strategy": "updateStrategy",
    },
)
class EksNodeGroupUpdateConfig:
    def __init__(
        self,
        *,
        max_unavailable: typing.Optional[jsii.Number] = None,
        max_unavailable_percentage: typing.Optional[jsii.Number] = None,
        update_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_unavailable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unavailable EksNodeGroup#max_unavailable}.
        :param max_unavailable_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unavailable_percentage EksNodeGroup#max_unavailable_percentage}.
        :param update_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#update_strategy EksNodeGroup#update_strategy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae7e3326d204615f18aacc183ce33f4633867e186d8c2d54b2a455345b3c272)
            check_type(argname="argument max_unavailable", value=max_unavailable, expected_type=type_hints["max_unavailable"])
            check_type(argname="argument max_unavailable_percentage", value=max_unavailable_percentage, expected_type=type_hints["max_unavailable_percentage"])
            check_type(argname="argument update_strategy", value=update_strategy, expected_type=type_hints["update_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_unavailable is not None:
            self._values["max_unavailable"] = max_unavailable
        if max_unavailable_percentage is not None:
            self._values["max_unavailable_percentage"] = max_unavailable_percentage
        if update_strategy is not None:
            self._values["update_strategy"] = update_strategy

    @builtins.property
    def max_unavailable(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unavailable EksNodeGroup#max_unavailable}.'''
        result = self._values.get("max_unavailable")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#max_unavailable_percentage EksNodeGroup#max_unavailable_percentage}.'''
        result = self._values.get("max_unavailable_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def update_strategy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/eks_node_group#update_strategy EksNodeGroup#update_strategy}.'''
        result = self._values.get("update_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodeGroupUpdateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EksNodeGroupUpdateConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.eksNodeGroup.EksNodeGroupUpdateConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9417ed3ac226c29c497c9ab17c3f54d001667d57d288e0e5ea1020aa6b3de13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxUnavailable")
    def reset_max_unavailable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnavailable", []))

    @jsii.member(jsii_name="resetMaxUnavailablePercentage")
    def reset_max_unavailable_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnavailablePercentage", []))

    @jsii.member(jsii_name="resetUpdateStrategy")
    def reset_update_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateStrategy", []))

    @builtins.property
    @jsii.member(jsii_name="maxUnavailableInput")
    def max_unavailable_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnavailableInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnavailablePercentageInput")
    def max_unavailable_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnavailablePercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="updateStrategyInput")
    def update_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnavailable")
    def max_unavailable(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailable"))

    @max_unavailable.setter
    def max_unavailable(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d7695bada46c094a64d9bb6fc01dc3983180ceec44ce16d0ce37da46229095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailablePercentage")
    def max_unavailable_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailablePercentage"))

    @max_unavailable_percentage.setter
    def max_unavailable_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce36d4fd6e64f5946159c9dca40cfdde70077234469d39ffd43ec3cee38f3dff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailablePercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateStrategy")
    def update_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateStrategy"))

    @update_strategy.setter
    def update_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__798f97a0b1cd8582f98a8a209c6e280b3c34e6b95c96864149eba48c5b2c4798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EksNodeGroupUpdateConfig]:
        return typing.cast(typing.Optional[EksNodeGroupUpdateConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EksNodeGroupUpdateConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501fea3167ce6483758ee66332f874c53c2468e196f56f7036f2ae67b25f5682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EksNodeGroup",
    "EksNodeGroupConfig",
    "EksNodeGroupLaunchTemplate",
    "EksNodeGroupLaunchTemplateOutputReference",
    "EksNodeGroupNodeRepairConfig",
    "EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides",
    "EksNodeGroupNodeRepairConfigNodeRepairConfigOverridesList",
    "EksNodeGroupNodeRepairConfigNodeRepairConfigOverridesOutputReference",
    "EksNodeGroupNodeRepairConfigOutputReference",
    "EksNodeGroupRemoteAccess",
    "EksNodeGroupRemoteAccessOutputReference",
    "EksNodeGroupResources",
    "EksNodeGroupResourcesAutoscalingGroups",
    "EksNodeGroupResourcesAutoscalingGroupsList",
    "EksNodeGroupResourcesAutoscalingGroupsOutputReference",
    "EksNodeGroupResourcesList",
    "EksNodeGroupResourcesOutputReference",
    "EksNodeGroupScalingConfig",
    "EksNodeGroupScalingConfigOutputReference",
    "EksNodeGroupTaint",
    "EksNodeGroupTaintList",
    "EksNodeGroupTaintOutputReference",
    "EksNodeGroupTimeouts",
    "EksNodeGroupTimeoutsOutputReference",
    "EksNodeGroupUpdateConfig",
    "EksNodeGroupUpdateConfigOutputReference",
]

publication.publish()

def _typecheckingstub__48461204c8b5196e0df0deec2b4c3c912ac530a335447e23c2d45026693900c9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_name: builtins.str,
    node_role_arn: builtins.str,
    scaling_config: typing.Union[EksNodeGroupScalingConfig, typing.Dict[builtins.str, typing.Any]],
    subnet_ids: typing.Sequence[builtins.str],
    ami_type: typing.Optional[builtins.str] = None,
    capacity_type: typing.Optional[builtins.str] = None,
    disk_size: typing.Optional[jsii.Number] = None,
    force_update_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launch_template: typing.Optional[typing.Union[EksNodeGroupLaunchTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    node_group_name: typing.Optional[builtins.str] = None,
    node_group_name_prefix: typing.Optional[builtins.str] = None,
    node_repair_config: typing.Optional[typing.Union[EksNodeGroupNodeRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    release_version: typing.Optional[builtins.str] = None,
    remote_access: typing.Optional[typing.Union[EksNodeGroupRemoteAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EksNodeGroupTaint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[EksNodeGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_config: typing.Optional[typing.Union[EksNodeGroupUpdateConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__c1122379c8ca39e3707d595fe83e441320f61b72f39cfeed759c64ccda636b04(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0dd258fc63014d1a3032f0b88e893ae52adec552690729bb460617b560acd8a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EksNodeGroupTaint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d6e33e2dcfd9b6b985234b49ef9fe01d09566f27b39656d0c8bf279fe281ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db16e5b2970693f7717c87846e7cdf51d5a9bfe8ae300ca270ad98fbdca49713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c23f62741dc66eaa49229a10e16d79b540aa3895979b50c4381382b50ec111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8632f76cc6768e21362d4c64fff9d3ddaa0e6cad3be3bf54d61cbe5edc50f36b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741d17096ff53769e615cc7818b234d4f4adf8d878fd921be0c21454255eb9bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0310d3450254965d2b58cdb674fe09fb88d693402a824f86c1c9e5ec9ff15f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c930d28d2b6fe8d6b3d11fd2c524b3d8a3e06656f5391b7936f74e77d600dd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b763f59bd8f2f83da4a8356759fb00e8aacd7075026d531fe898eb1cd6b5a7af(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa2ef5d85a87c5ca590ed3637ad14eed7f82ba0957676fe9677d7ba9cebf4c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad78dcf78fd17ac15063b12dff1be54631ba253a17fb6d0da4e8687619cdb8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440afaa81b4c707f65cf06aa5f261ca175427db756f4e946cf31b86ce0df63c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beade79a2af90a8ffe0a9a9a8cd6973c5d8464ee237a4c0446f6065f044590c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c06c8914dbaef1de20b1de87cf572212373effe04ea67c888a8f116e9d15db8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b81ea4493ea6e5dbdfc83eb229d96b9b17b856e1160b8a17c5bba5805205bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d291b6761262fc37c52f9589cb495aefce4556f0c244372932ee23f46942dff(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3b2987a5600a1b356f0aa46a18fcd19d75db3fbf30cb9ea18a82979129adac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb787398634c2f327d93f3d2dfe77cda5fc106ae62ccde0dcca8e4b23dac633(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1801ec0f597f111dac90e5874085cd59c4278b861c272ba57d56a5b6950211(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_name: builtins.str,
    node_role_arn: builtins.str,
    scaling_config: typing.Union[EksNodeGroupScalingConfig, typing.Dict[builtins.str, typing.Any]],
    subnet_ids: typing.Sequence[builtins.str],
    ami_type: typing.Optional[builtins.str] = None,
    capacity_type: typing.Optional[builtins.str] = None,
    disk_size: typing.Optional[jsii.Number] = None,
    force_update_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launch_template: typing.Optional[typing.Union[EksNodeGroupLaunchTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    node_group_name: typing.Optional[builtins.str] = None,
    node_group_name_prefix: typing.Optional[builtins.str] = None,
    node_repair_config: typing.Optional[typing.Union[EksNodeGroupNodeRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    release_version: typing.Optional[builtins.str] = None,
    remote_access: typing.Optional[typing.Union[EksNodeGroupRemoteAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EksNodeGroupTaint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[EksNodeGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_config: typing.Optional[typing.Union[EksNodeGroupUpdateConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145dbe37290467a0aa6f74c4023de8df40b94d5f2101e512426a13c8bbf2884d(
    *,
    version: builtins.str,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195da0acbdf561cb3a4c82add90af8f3cd638768122a78d1c7ada4e0a7a289bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4354f752d733041145917c9b77cddcf45bb184e26e05170e453910f4ff01ff6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e309900de318ed4df1e595dcb582d03102174ee870de3c0655c44af4b10342(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b829022aa8f7ab4a2ceb99ffc65b9e89ef31e81cca86c7eb8e400a451305b5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc396e299c74ef20b76ae6e3cd313b36513a85b28d10786bdb57765b85c9a72(
    value: typing.Optional[EksNodeGroupLaunchTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e2599466a967ddebd58cf5d9c0e327745a93f2b1f61014d796209ff425083b(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_parallel_nodes_repaired_count: typing.Optional[jsii.Number] = None,
    max_parallel_nodes_repaired_percentage: typing.Optional[jsii.Number] = None,
    max_unhealthy_node_threshold_count: typing.Optional[jsii.Number] = None,
    max_unhealthy_node_threshold_percentage: typing.Optional[jsii.Number] = None,
    node_repair_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5387dc65098e3cd79d2cc918b491c1b7938b6919855d057793be3a3fc736b710(
    *,
    min_repair_wait_time_mins: jsii.Number,
    node_monitoring_condition: builtins.str,
    node_unhealthy_reason: builtins.str,
    repair_action: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4714b33b50d91099cbc99515b67badbd34ea0617a5f04895da580523fa56d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6bb0b054108a1bf6a12b1482e312cffbdb11ab2d239adc107a097793b451f03(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c0cf245bab6b78534693008917bb6271a1a403a4609553f363a161b75d8e17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fab53cb48b585c0ae8a790f6eefd86cc3e948ecb62d26da5089e4bfb35d56f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2afff932ffca9e3bc708c232b721ac520d893683352e26d0213f178b0544a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623022df01583f7cf9cbaf58509925bb6447422bbd274a3748f6decc7b0490f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e132069e089263cd8a53b67b1dc9a2eea41855b36d6a0748577e94cce2db371c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ce5bbe5bc50e0d4fdef0e143ec86990991e7b87fb531e7915bd2d809279fc2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370fed2ea819ba02572c4a82ab1881946b13024a4926ea16b624fcad26245747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61d488bad6d630daec5a120479df574c4ce926f5dd4e5b8dbc58405a2a23036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e23fdccb0987c1f0e9203fec563fa16efdc44f095687ae2d97ed257102918428(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9acf24af3e7eec58b9018ce9b241dc7ecba76637d18a5b343d3ea5a53dcabe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e60c0975a9d5b191dd002c083c3f177b07b2c7a7ad09b2adf4ee869a542bf20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b745ed8aabec07612f3a45f7065629f52ce1f311d23a42f37e13c3fc04fa8b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EksNodeGroupNodeRepairConfigNodeRepairConfigOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4142d7992f73d5569e03298f8b3d9eca7c1e22b3fd4de85bb1961409f4e9b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990aecb7d139996fa42c4d8c96b06a044498d05fc7503ad853a0499c68216237(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b74b65a3a53068c816522be2de82ad2d34aeb31ee539adc64eca4af387096cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a44ee953515362cd747c9ff112717e4c2f83636b4aed72649f8a6b74d9ca5a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f23045695e76c14de0d8389383b277ad56460e7cfc11ed0b82d921fa3061bc8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fa43560c380256cb007cd2b0e03cf2f498208b8c532a7b2e5cbb24b831e90a(
    value: typing.Optional[EksNodeGroupNodeRepairConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc43ad9ce14d9af9af22b67c8e4f75310ca318e3a8d0fabc476c03ad17121012(
    *,
    ec2_ssh_key: typing.Optional[builtins.str] = None,
    source_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2fe47dddf12f723d61b0e647ffc3ff6e7c9829a8cb0a3d8cffb1bceb72f7e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc806029f175a38c469160b2a971c6d25bdf92476bfc89c387244b62df347119(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa6c7dcc9ec5c41da2bbb51a47ec82ea9bc6443e7d231990cee2bde42f6cd1e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad72c7ff385a8e554975b0a39c36461260d547e4edeef20cb560f50214cb334f(
    value: typing.Optional[EksNodeGroupRemoteAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da07d0ee26f014df1ac5f25db0ff3637f2f69db7e2b1f9c21f411bf878a936a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd1b781527ac5d6e24ec00c431060a53bcd0d912b8a5a2931ff1ff525335ab6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acd56b10ba79ec50a96d092cbc0332cad3e4afd40029eb1e979170c525e06eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5880e8be809ebde4c8e99443f0a54c54690ca581a70428843afa2abc885ab3d6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e5003116429b56f8d84727c100b537dcd6f485a7470196a565e41504221e2c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6473076e5d93ae66f0c8013129684f43ed3907420fff22dd780782dbea2c7e09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd92a7bb81d9fe56f6b082114e6767cba2c23c638f7d9a5efbd11845b912004(
    value: typing.Optional[EksNodeGroupResourcesAutoscalingGroups],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5907e71a4d6aea7d5d79adeedabbf87e69f045f88b944cf34f7b87cb82a447ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bfeb471d242c56a633c70f86097c30a0757d74ce41cc787aca510560807fb1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3368303cb572e2b1ffde3750bea6b0a4eb7131acf5d0401ec51b074d499a4f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ccf56dbcd8ee93737638532ad845a04f05d861817a7a66235352e8dc00555b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90a0019730aba50ff22d738db7e4de8009087a53983b650b7abad1c45ab90f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412da5ac7510a5d729278a690b840f3216c985d063942f48e0061d729440c1ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b53320bc61edd2071306e0490be6b3c3453a8f71791286f6563e4c18e29483(
    value: typing.Optional[EksNodeGroupResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c151ba68ef01c2863447ee930f88bbbbbdd9e0f02d565af45afef1251c65d19(
    *,
    desired_size: jsii.Number,
    max_size: jsii.Number,
    min_size: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4d779eff1b8c119ef5e9c6f797fa6323ddff2483364080214e3f23ed8bcbfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9ee95b632e899e29c4cf8354daaa5880a6e540f30f825f6ddf1a67cf75b1a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff22a62a551016dd232ac40c85ebec8f5850c3dc92abc63dc51ced2745392fd6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab719de8b6a90ac2a392c669c84221b1ca9712032d2021da0d320d30c61fe106(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e3d3997563887e3ee1824127a4500c058ece5236c43ddf81d2d5978ec6d9a0(
    value: typing.Optional[EksNodeGroupScalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7ffbd61aada4002905c284f0633bc297094f7a8de80c57cef94b290e42b7b1(
    *,
    effect: builtins.str,
    key: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9106fbe288a6323842e50d6927f3e083956082cf47b215333d22059c47b3e804(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc15b6562588b4ade8df4543811d4702e4c05f920cb4b3ac67d3d65026d5e5b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6876e84a1ade583d6217609d8c0425c23672a39a4358b357b19519d8076b15fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965b62d3fef6de6dca311391a428497d525d350def65b9a24abba0bc9601cd28(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e42aa021a38bb4c7afe3ec2e04b9b21a82321c99f1cdfec5df1909e6f44a5d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857405fee900363faa10aa80dbbbc6256f483eec320b5dc32727e865f3bc1b78(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EksNodeGroupTaint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb317d757a2253dc87e541bb5e33c0f30c478814a80a13303ac75f50d9b8685(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4f1299f951e0a1193ee67613d63318ad53655ea463ca90d4f111a22c9f139d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6ab538b0c758caeda82bc4f9ecbeeef2050cc89de7e2fe8368456b636cc6e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1343cdccd5e7bfe1a12a3c90334014297debd4c705be5493614312e9c5967f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc774487c04ce68a894dac303bff3d3b727450c0724b412076c5e737c05dbd85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupTaint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c405d19043e0d0c22266d2f7c83c84c5399cf968c2dd05f279a51a17cab98b94(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abd533d5b3e48a0e17345f573127693f38e75082bfefac5a37d82a7e802b6c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db13a384be76fe4d50aae2e0d1038a652e882e726f8d717b8a8231ad30851366(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9126dbb137cdac25252a1b8948ceb16b60444a36a1932e63de8f6b0222563101(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4799f17977bfadf910e2d45ab56b70b4a0df99f98cd06da76146be4246dcd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623b747886b1d5c8511a8d972125cf60d3aa4927393616c885baeeaf8a02ddf1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EksNodeGroupTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae7e3326d204615f18aacc183ce33f4633867e186d8c2d54b2a455345b3c272(
    *,
    max_unavailable: typing.Optional[jsii.Number] = None,
    max_unavailable_percentage: typing.Optional[jsii.Number] = None,
    update_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9417ed3ac226c29c497c9ab17c3f54d001667d57d288e0e5ea1020aa6b3de13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d7695bada46c094a64d9bb6fc01dc3983180ceec44ce16d0ce37da46229095(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce36d4fd6e64f5946159c9dca40cfdde70077234469d39ffd43ec3cee38f3dff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798f97a0b1cd8582f98a8a209c6e280b3c34e6b95c96864149eba48c5b2c4798(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501fea3167ce6483758ee66332f874c53c2468e196f56f7036f2ae67b25f5682(
    value: typing.Optional[EksNodeGroupUpdateConfig],
) -> None:
    """Type checking stubs"""
    pass
