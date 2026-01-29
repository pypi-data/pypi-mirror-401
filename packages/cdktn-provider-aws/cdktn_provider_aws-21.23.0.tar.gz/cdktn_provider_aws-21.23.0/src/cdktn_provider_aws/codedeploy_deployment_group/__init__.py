r'''
# `aws_codedeploy_deployment_group`

Refer to the Terraform Registry for docs: [`aws_codedeploy_deployment_group`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group).
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


class CodedeployDeploymentGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group aws_codedeploy_deployment_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_name: builtins.str,
        deployment_group_name: builtins.str,
        service_role_arn: builtins.str,
        alarm_configuration: typing.Optional[typing.Union["CodedeployDeploymentGroupAlarmConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_rollback_configuration: typing.Optional[typing.Union["CodedeployDeploymentGroupAutoRollbackConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        blue_green_deployment_config: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        deployment_style: typing.Optional[typing.Union["CodedeployDeploymentGroupDeploymentStyle", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ec2_tag_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ecs_service: typing.Optional[typing.Union["CodedeployDeploymentGroupEcsService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer_info: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        on_premises_instance_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupOnPremisesInstanceTagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        outdated_instances_strategy: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_hook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trigger_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupTriggerConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group aws_codedeploy_deployment_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#app_name CodedeployDeploymentGroup#app_name}.
        :param deployment_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_group_name CodedeployDeploymentGroup#deployment_group_name}.
        :param service_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#service_role_arn CodedeployDeploymentGroup#service_role_arn}.
        :param alarm_configuration: alarm_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#alarm_configuration CodedeployDeploymentGroup#alarm_configuration}
        :param auto_rollback_configuration: auto_rollback_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#auto_rollback_configuration CodedeployDeploymentGroup#auto_rollback_configuration}
        :param autoscaling_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#autoscaling_groups CodedeployDeploymentGroup#autoscaling_groups}.
        :param blue_green_deployment_config: blue_green_deployment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#blue_green_deployment_config CodedeployDeploymentGroup#blue_green_deployment_config}
        :param deployment_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_config_name CodedeployDeploymentGroup#deployment_config_name}.
        :param deployment_style: deployment_style block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_style CodedeployDeploymentGroup#deployment_style}
        :param ec2_tag_filter: ec2_tag_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ec2_tag_filter CodedeployDeploymentGroup#ec2_tag_filter}
        :param ec2_tag_set: ec2_tag_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ec2_tag_set CodedeployDeploymentGroup#ec2_tag_set}
        :param ecs_service: ecs_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ecs_service CodedeployDeploymentGroup#ecs_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#id CodedeployDeploymentGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer_info: load_balancer_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#load_balancer_info CodedeployDeploymentGroup#load_balancer_info}
        :param on_premises_instance_tag_filter: on_premises_instance_tag_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#on_premises_instance_tag_filter CodedeployDeploymentGroup#on_premises_instance_tag_filter}
        :param outdated_instances_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#outdated_instances_strategy CodedeployDeploymentGroup#outdated_instances_strategy}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#region CodedeployDeploymentGroup#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#tags CodedeployDeploymentGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#tags_all CodedeployDeploymentGroup#tags_all}.
        :param termination_hook_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#termination_hook_enabled CodedeployDeploymentGroup#termination_hook_enabled}.
        :param trigger_configuration: trigger_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#trigger_configuration CodedeployDeploymentGroup#trigger_configuration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d10c1172f66162326f2a54948dbdfaf972e553d40d1d2034fa32cd48fe6b618)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CodedeployDeploymentGroupConfig(
            app_name=app_name,
            deployment_group_name=deployment_group_name,
            service_role_arn=service_role_arn,
            alarm_configuration=alarm_configuration,
            auto_rollback_configuration=auto_rollback_configuration,
            autoscaling_groups=autoscaling_groups,
            blue_green_deployment_config=blue_green_deployment_config,
            deployment_config_name=deployment_config_name,
            deployment_style=deployment_style,
            ec2_tag_filter=ec2_tag_filter,
            ec2_tag_set=ec2_tag_set,
            ecs_service=ecs_service,
            id=id,
            load_balancer_info=load_balancer_info,
            on_premises_instance_tag_filter=on_premises_instance_tag_filter,
            outdated_instances_strategy=outdated_instances_strategy,
            region=region,
            tags=tags,
            tags_all=tags_all,
            termination_hook_enabled=termination_hook_enabled,
            trigger_configuration=trigger_configuration,
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
        '''Generates CDKTF code for importing a CodedeployDeploymentGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CodedeployDeploymentGroup to import.
        :param import_from_id: The id of the existing CodedeployDeploymentGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CodedeployDeploymentGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693b2a315a1986e1ebecc09211c03ff195178bb3118e0994809e3f401ed5fc02)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAlarmConfiguration")
    def put_alarm_configuration(
        self,
        *,
        alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param alarms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#alarms CodedeployDeploymentGroup#alarms}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.
        :param ignore_poll_alarm_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ignore_poll_alarm_failure CodedeployDeploymentGroup#ignore_poll_alarm_failure}.
        '''
        value = CodedeployDeploymentGroupAlarmConfiguration(
            alarms=alarms,
            enabled=enabled,
            ignore_poll_alarm_failure=ignore_poll_alarm_failure,
        )

        return typing.cast(None, jsii.invoke(self, "putAlarmConfiguration", [value]))

    @jsii.member(jsii_name="putAutoRollbackConfiguration")
    def put_auto_rollback_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        events: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.
        :param events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#events CodedeployDeploymentGroup#events}.
        '''
        value = CodedeployDeploymentGroupAutoRollbackConfiguration(
            enabled=enabled, events=events
        )

        return typing.cast(None, jsii.invoke(self, "putAutoRollbackConfiguration", [value]))

    @jsii.member(jsii_name="putBlueGreenDeploymentConfig")
    def put_blue_green_deployment_config(
        self,
        *,
        deployment_ready_option: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption", typing.Dict[builtins.str, typing.Any]]] = None,
        green_fleet_provisioning_option: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption", typing.Dict[builtins.str, typing.Any]]] = None,
        terminate_blue_instances_on_deployment_success: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param deployment_ready_option: deployment_ready_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_ready_option CodedeployDeploymentGroup#deployment_ready_option}
        :param green_fleet_provisioning_option: green_fleet_provisioning_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#green_fleet_provisioning_option CodedeployDeploymentGroup#green_fleet_provisioning_option}
        :param terminate_blue_instances_on_deployment_success: terminate_blue_instances_on_deployment_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#terminate_blue_instances_on_deployment_success CodedeployDeploymentGroup#terminate_blue_instances_on_deployment_success}
        '''
        value = CodedeployDeploymentGroupBlueGreenDeploymentConfig(
            deployment_ready_option=deployment_ready_option,
            green_fleet_provisioning_option=green_fleet_provisioning_option,
            terminate_blue_instances_on_deployment_success=terminate_blue_instances_on_deployment_success,
        )

        return typing.cast(None, jsii.invoke(self, "putBlueGreenDeploymentConfig", [value]))

    @jsii.member(jsii_name="putDeploymentStyle")
    def put_deployment_style(
        self,
        *,
        deployment_option: typing.Optional[builtins.str] = None,
        deployment_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_option CodedeployDeploymentGroup#deployment_option}.
        :param deployment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_type CodedeployDeploymentGroup#deployment_type}.
        '''
        value = CodedeployDeploymentGroupDeploymentStyle(
            deployment_option=deployment_option, deployment_type=deployment_type
        )

        return typing.cast(None, jsii.invoke(self, "putDeploymentStyle", [value]))

    @jsii.member(jsii_name="putEc2TagFilter")
    def put_ec2_tag_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71a5c537a5b97604eb87b96dc9d68e356ca98c729fadd334fec4824ae963d04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEc2TagFilter", [value]))

    @jsii.member(jsii_name="putEc2TagSet")
    def put_ec2_tag_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24df7547ab3345227f2e06521233abaa2e6a527d47602b19de6323840c61c285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEc2TagSet", [value]))

    @jsii.member(jsii_name="putEcsService")
    def put_ecs_service(
        self,
        *,
        cluster_name: builtins.str,
        service_name: builtins.str,
    ) -> None:
        '''
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#cluster_name CodedeployDeploymentGroup#cluster_name}.
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#service_name CodedeployDeploymentGroup#service_name}.
        '''
        value = CodedeployDeploymentGroupEcsService(
            cluster_name=cluster_name, service_name=service_name
        )

        return typing.cast(None, jsii.invoke(self, "putEcsService", [value]))

    @jsii.member(jsii_name="putLoadBalancerInfo")
    def put_load_balancer_info(
        self,
        *,
        elb_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoElbInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_group_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_group_pair_info: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param elb_info: elb_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#elb_info CodedeployDeploymentGroup#elb_info}
        :param target_group_info: target_group_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#target_group_info CodedeployDeploymentGroup#target_group_info}
        :param target_group_pair_info: target_group_pair_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#target_group_pair_info CodedeployDeploymentGroup#target_group_pair_info}
        '''
        value = CodedeployDeploymentGroupLoadBalancerInfo(
            elb_info=elb_info,
            target_group_info=target_group_info,
            target_group_pair_info=target_group_pair_info,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancerInfo", [value]))

    @jsii.member(jsii_name="putOnPremisesInstanceTagFilter")
    def put_on_premises_instance_tag_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupOnPremisesInstanceTagFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395ab1400d3d16ed33a15eb7ad0b437ad9b834d74492e25a929c9a056312d3eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOnPremisesInstanceTagFilter", [value]))

    @jsii.member(jsii_name="putTriggerConfiguration")
    def put_trigger_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupTriggerConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e5f93634596baee0963f5f83f741e2dd2d797e50f58c7796697ac234d25c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTriggerConfiguration", [value]))

    @jsii.member(jsii_name="resetAlarmConfiguration")
    def reset_alarm_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmConfiguration", []))

    @jsii.member(jsii_name="resetAutoRollbackConfiguration")
    def reset_auto_rollback_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRollbackConfiguration", []))

    @jsii.member(jsii_name="resetAutoscalingGroups")
    def reset_autoscaling_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingGroups", []))

    @jsii.member(jsii_name="resetBlueGreenDeploymentConfig")
    def reset_blue_green_deployment_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlueGreenDeploymentConfig", []))

    @jsii.member(jsii_name="resetDeploymentConfigName")
    def reset_deployment_config_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentConfigName", []))

    @jsii.member(jsii_name="resetDeploymentStyle")
    def reset_deployment_style(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentStyle", []))

    @jsii.member(jsii_name="resetEc2TagFilter")
    def reset_ec2_tag_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2TagFilter", []))

    @jsii.member(jsii_name="resetEc2TagSet")
    def reset_ec2_tag_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2TagSet", []))

    @jsii.member(jsii_name="resetEcsService")
    def reset_ecs_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcsService", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoadBalancerInfo")
    def reset_load_balancer_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerInfo", []))

    @jsii.member(jsii_name="resetOnPremisesInstanceTagFilter")
    def reset_on_premises_instance_tag_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnPremisesInstanceTagFilter", []))

    @jsii.member(jsii_name="resetOutdatedInstancesStrategy")
    def reset_outdated_instances_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutdatedInstancesStrategy", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTerminationHookEnabled")
    def reset_termination_hook_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationHookEnabled", []))

    @jsii.member(jsii_name="resetTriggerConfiguration")
    def reset_trigger_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerConfiguration", []))

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
    @jsii.member(jsii_name="alarmConfiguration")
    def alarm_configuration(
        self,
    ) -> "CodedeployDeploymentGroupAlarmConfigurationOutputReference":
        return typing.cast("CodedeployDeploymentGroupAlarmConfigurationOutputReference", jsii.get(self, "alarmConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="autoRollbackConfiguration")
    def auto_rollback_configuration(
        self,
    ) -> "CodedeployDeploymentGroupAutoRollbackConfigurationOutputReference":
        return typing.cast("CodedeployDeploymentGroupAutoRollbackConfigurationOutputReference", jsii.get(self, "autoRollbackConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="blueGreenDeploymentConfig")
    def blue_green_deployment_config(
        self,
    ) -> "CodedeployDeploymentGroupBlueGreenDeploymentConfigOutputReference":
        return typing.cast("CodedeployDeploymentGroupBlueGreenDeploymentConfigOutputReference", jsii.get(self, "blueGreenDeploymentConfig"))

    @builtins.property
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computePlatform"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupId")
    def deployment_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupId"))

    @builtins.property
    @jsii.member(jsii_name="deploymentStyle")
    def deployment_style(
        self,
    ) -> "CodedeployDeploymentGroupDeploymentStyleOutputReference":
        return typing.cast("CodedeployDeploymentGroupDeploymentStyleOutputReference", jsii.get(self, "deploymentStyle"))

    @builtins.property
    @jsii.member(jsii_name="ec2TagFilter")
    def ec2_tag_filter(self) -> "CodedeployDeploymentGroupEc2TagFilterList":
        return typing.cast("CodedeployDeploymentGroupEc2TagFilterList", jsii.get(self, "ec2TagFilter"))

    @builtins.property
    @jsii.member(jsii_name="ec2TagSet")
    def ec2_tag_set(self) -> "CodedeployDeploymentGroupEc2TagSetList":
        return typing.cast("CodedeployDeploymentGroupEc2TagSetList", jsii.get(self, "ec2TagSet"))

    @builtins.property
    @jsii.member(jsii_name="ecsService")
    def ecs_service(self) -> "CodedeployDeploymentGroupEcsServiceOutputReference":
        return typing.cast("CodedeployDeploymentGroupEcsServiceOutputReference", jsii.get(self, "ecsService"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInfo")
    def load_balancer_info(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoOutputReference":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoOutputReference", jsii.get(self, "loadBalancerInfo"))

    @builtins.property
    @jsii.member(jsii_name="onPremisesInstanceTagFilter")
    def on_premises_instance_tag_filter(
        self,
    ) -> "CodedeployDeploymentGroupOnPremisesInstanceTagFilterList":
        return typing.cast("CodedeployDeploymentGroupOnPremisesInstanceTagFilterList", jsii.get(self, "onPremisesInstanceTagFilter"))

    @builtins.property
    @jsii.member(jsii_name="triggerConfiguration")
    def trigger_configuration(
        self,
    ) -> "CodedeployDeploymentGroupTriggerConfigurationList":
        return typing.cast("CodedeployDeploymentGroupTriggerConfigurationList", jsii.get(self, "triggerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="alarmConfigurationInput")
    def alarm_configuration_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupAlarmConfiguration"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupAlarmConfiguration"], jsii.get(self, "alarmConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="appNameInput")
    def app_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appNameInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRollbackConfigurationInput")
    def auto_rollback_configuration_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupAutoRollbackConfiguration"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupAutoRollbackConfiguration"], jsii.get(self, "autoRollbackConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingGroupsInput")
    def autoscaling_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "autoscalingGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="blueGreenDeploymentConfigInput")
    def blue_green_deployment_config_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfig"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfig"], jsii.get(self, "blueGreenDeploymentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigNameInput")
    def deployment_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupNameInput")
    def deployment_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentStyleInput")
    def deployment_style_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupDeploymentStyle"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupDeploymentStyle"], jsii.get(self, "deploymentStyleInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2TagFilterInput")
    def ec2_tag_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagFilter"]]], jsii.get(self, "ec2TagFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2TagSetInput")
    def ec2_tag_set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSet"]]], jsii.get(self, "ec2TagSetInput"))

    @builtins.property
    @jsii.member(jsii_name="ecsServiceInput")
    def ecs_service_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupEcsService"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupEcsService"], jsii.get(self, "ecsServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInfoInput")
    def load_balancer_info_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfo"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfo"], jsii.get(self, "loadBalancerInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="onPremisesInstanceTagFilterInput")
    def on_premises_instance_tag_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupOnPremisesInstanceTagFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupOnPremisesInstanceTagFilter"]]], jsii.get(self, "onPremisesInstanceTagFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="outdatedInstancesStrategyInput")
    def outdated_instances_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outdatedInstancesStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArnInput")
    def service_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRoleArnInput"))

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
    @jsii.member(jsii_name="terminationHookEnabledInput")
    def termination_hook_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "terminationHookEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerConfigurationInput")
    def trigger_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupTriggerConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupTriggerConfiguration"]]], jsii.get(self, "triggerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="appName")
    def app_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appName"))

    @app_name.setter
    def app_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbab60d05e49f007b41a34561e5ad027fa2849123d582e720289b5d83abb760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoscalingGroups")
    def autoscaling_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "autoscalingGroups"))

    @autoscaling_groups.setter
    def autoscaling_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262a74ce6beab779f7983f3dc1d96fad1efe3752924ee41d70abb403cb7c04a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalingGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))

    @deployment_config_name.setter
    def deployment_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf98102cb65e07cb21c03d3e65bc20b426fb105c520a74ceeb2be62bb7c5835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentConfigName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))

    @deployment_group_name.setter
    def deployment_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a6928727660f4a7e0371311cd8cc2a75b84e3f84ee185b1af6d4e1c501580f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5271aa21718ccfcc2971b6c7f1795a4713490c88aa6b7018c4544fe2e83f12a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outdatedInstancesStrategy")
    def outdated_instances_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outdatedInstancesStrategy"))

    @outdated_instances_strategy.setter
    def outdated_instances_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88785c15d20579cb2fe09b31a05b12c42a632fd6fee962a06f3a8a3bccdfe64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outdatedInstancesStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6abf3555d4c56ac150a2500ba017c2b8cfe31b92b26e62a30f14e0d7499822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRoleArn"))

    @service_role_arn.setter
    def service_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470eb46955cc3c2ad9d141816f8a4be471fb208a1dcf6ad33e0384b8b0110473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad69b122d4704c3d5effae8b3082b7cc8a2d7927b01048ff242b532b420c936b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b1d24cd41f736ea056259a6d4ea10c00c8cfff45d3f9fb5e17d162bafe1417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationHookEnabled")
    def termination_hook_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "terminationHookEnabled"))

    @termination_hook_enabled.setter
    def termination_hook_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2949553382d198d381455ddf83f246dd66d09381063bfb74f5d4b487ff29cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationHookEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupAlarmConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "alarms": "alarms",
        "enabled": "enabled",
        "ignore_poll_alarm_failure": "ignorePollAlarmFailure",
    },
)
class CodedeployDeploymentGroupAlarmConfiguration:
    def __init__(
        self,
        *,
        alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param alarms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#alarms CodedeployDeploymentGroup#alarms}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.
        :param ignore_poll_alarm_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ignore_poll_alarm_failure CodedeployDeploymentGroup#ignore_poll_alarm_failure}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545fdaa69e97b28488818fe155f237f57d8baf787a1d149ec7ae72cca6778b4d)
            check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument ignore_poll_alarm_failure", value=ignore_poll_alarm_failure, expected_type=type_hints["ignore_poll_alarm_failure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarms is not None:
            self._values["alarms"] = alarms
        if enabled is not None:
            self._values["enabled"] = enabled
        if ignore_poll_alarm_failure is not None:
            self._values["ignore_poll_alarm_failure"] = ignore_poll_alarm_failure

    @builtins.property
    def alarms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#alarms CodedeployDeploymentGroup#alarms}.'''
        result = self._values.get("alarms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ignore_poll_alarm_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ignore_poll_alarm_failure CodedeployDeploymentGroup#ignore_poll_alarm_failure}.'''
        result = self._values.get("ignore_poll_alarm_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupAlarmConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupAlarmConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupAlarmConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74a5363a04f2cb97fc03509c0b4002b2472e559e2db975859f08bf93776bc6e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAlarms")
    def reset_alarms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarms", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetIgnorePollAlarmFailure")
    def reset_ignore_poll_alarm_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnorePollAlarmFailure", []))

    @builtins.property
    @jsii.member(jsii_name="alarmsInput")
    def alarms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "alarmsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ignorePollAlarmFailureInput")
    def ignore_poll_alarm_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignorePollAlarmFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="alarms")
    def alarms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "alarms"))

    @alarms.setter
    def alarms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd2169b7b0f1d3b4b0a9a9383801d93300348874636a640716368aebcd6ba17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarms", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__6604fd9f90baa92aa5643cc8da0f988a4efb5ed8e2cb3917cc59ded89b98645b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignorePollAlarmFailure")
    def ignore_poll_alarm_failure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignorePollAlarmFailure"))

    @ignore_poll_alarm_failure.setter
    def ignore_poll_alarm_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a35a82b561d5ce464323aa6b6e38a24607525811838264bcbed0224a7cc935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignorePollAlarmFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupAlarmConfiguration]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupAlarmConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupAlarmConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5127f3e9452d997c685d170b1d181480782ffbd6fa30c01844dfb90417370af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupAutoRollbackConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "events": "events"},
)
class CodedeployDeploymentGroupAutoRollbackConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        events: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.
        :param events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#events CodedeployDeploymentGroup#events}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a97141cedb4e88483c3382fc5b947484d1b4598989927c9f985a888771774a86)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if events is not None:
            self._values["events"] = events

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#events CodedeployDeploymentGroup#events}.'''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupAutoRollbackConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupAutoRollbackConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupAutoRollbackConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80110b765ccb2cc3e9d6da531926ad29edad9196ddd4318a09d0142215ea964a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEvents")
    def reset_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvents", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventsInput")
    def events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__316d5038a352654b06af578bcadad0d4228fae5c80be6cabb5f4d1d6770e0f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "events"))

    @events.setter
    def events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae300ccfca33b4b7a8cc7e0a4745538271087e2607f12a4719a384c8d77674ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb7e6f03e730153b321e17c00acc290d911e7e30346f33e54c52a96a497f38f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_ready_option": "deploymentReadyOption",
        "green_fleet_provisioning_option": "greenFleetProvisioningOption",
        "terminate_blue_instances_on_deployment_success": "terminateBlueInstancesOnDeploymentSuccess",
    },
)
class CodedeployDeploymentGroupBlueGreenDeploymentConfig:
    def __init__(
        self,
        *,
        deployment_ready_option: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption", typing.Dict[builtins.str, typing.Any]]] = None,
        green_fleet_provisioning_option: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption", typing.Dict[builtins.str, typing.Any]]] = None,
        terminate_blue_instances_on_deployment_success: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param deployment_ready_option: deployment_ready_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_ready_option CodedeployDeploymentGroup#deployment_ready_option}
        :param green_fleet_provisioning_option: green_fleet_provisioning_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#green_fleet_provisioning_option CodedeployDeploymentGroup#green_fleet_provisioning_option}
        :param terminate_blue_instances_on_deployment_success: terminate_blue_instances_on_deployment_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#terminate_blue_instances_on_deployment_success CodedeployDeploymentGroup#terminate_blue_instances_on_deployment_success}
        '''
        if isinstance(deployment_ready_option, dict):
            deployment_ready_option = CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption(**deployment_ready_option)
        if isinstance(green_fleet_provisioning_option, dict):
            green_fleet_provisioning_option = CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption(**green_fleet_provisioning_option)
        if isinstance(terminate_blue_instances_on_deployment_success, dict):
            terminate_blue_instances_on_deployment_success = CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess(**terminate_blue_instances_on_deployment_success)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0a12ba2ef1c9f236210bc56b06da2236fa8ea55f34052d2f74ab1bdec75557)
            check_type(argname="argument deployment_ready_option", value=deployment_ready_option, expected_type=type_hints["deployment_ready_option"])
            check_type(argname="argument green_fleet_provisioning_option", value=green_fleet_provisioning_option, expected_type=type_hints["green_fleet_provisioning_option"])
            check_type(argname="argument terminate_blue_instances_on_deployment_success", value=terminate_blue_instances_on_deployment_success, expected_type=type_hints["terminate_blue_instances_on_deployment_success"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_ready_option is not None:
            self._values["deployment_ready_option"] = deployment_ready_option
        if green_fleet_provisioning_option is not None:
            self._values["green_fleet_provisioning_option"] = green_fleet_provisioning_option
        if terminate_blue_instances_on_deployment_success is not None:
            self._values["terminate_blue_instances_on_deployment_success"] = terminate_blue_instances_on_deployment_success

    @builtins.property
    def deployment_ready_option(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption"]:
        '''deployment_ready_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_ready_option CodedeployDeploymentGroup#deployment_ready_option}
        '''
        result = self._values.get("deployment_ready_option")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption"], result)

    @builtins.property
    def green_fleet_provisioning_option(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption"]:
        '''green_fleet_provisioning_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#green_fleet_provisioning_option CodedeployDeploymentGroup#green_fleet_provisioning_option}
        '''
        result = self._values.get("green_fleet_provisioning_option")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption"], result)

    @builtins.property
    def terminate_blue_instances_on_deployment_success(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess"]:
        '''terminate_blue_instances_on_deployment_success block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#terminate_blue_instances_on_deployment_success CodedeployDeploymentGroup#terminate_blue_instances_on_deployment_success}
        '''
        result = self._values.get("terminate_blue_instances_on_deployment_success")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupBlueGreenDeploymentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption",
    jsii_struct_bases=[],
    name_mapping={
        "action_on_timeout": "actionOnTimeout",
        "wait_time_in_minutes": "waitTimeInMinutes",
    },
)
class CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption:
    def __init__(
        self,
        *,
        action_on_timeout: typing.Optional[builtins.str] = None,
        wait_time_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action_on_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#action_on_timeout CodedeployDeploymentGroup#action_on_timeout}.
        :param wait_time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#wait_time_in_minutes CodedeployDeploymentGroup#wait_time_in_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576a09ac2454f14b39273752b6ae05569129c4dd31b8497e695266ca4026f454)
            check_type(argname="argument action_on_timeout", value=action_on_timeout, expected_type=type_hints["action_on_timeout"])
            check_type(argname="argument wait_time_in_minutes", value=wait_time_in_minutes, expected_type=type_hints["wait_time_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_on_timeout is not None:
            self._values["action_on_timeout"] = action_on_timeout
        if wait_time_in_minutes is not None:
            self._values["wait_time_in_minutes"] = wait_time_in_minutes

    @builtins.property
    def action_on_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#action_on_timeout CodedeployDeploymentGroup#action_on_timeout}.'''
        result = self._values.get("action_on_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_time_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#wait_time_in_minutes CodedeployDeploymentGroup#wait_time_in_minutes}.'''
        result = self._values.get("wait_time_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52f29c579c5063ea008c1f582000195f276338d5c0c1c0050baa33f2220ab4e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActionOnTimeout")
    def reset_action_on_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionOnTimeout", []))

    @jsii.member(jsii_name="resetWaitTimeInMinutes")
    def reset_wait_time_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitTimeInMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="actionOnTimeoutInput")
    def action_on_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionOnTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="waitTimeInMinutesInput")
    def wait_time_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "waitTimeInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="actionOnTimeout")
    def action_on_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionOnTimeout"))

    @action_on_timeout.setter
    def action_on_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8dbe52a6034c2e59758ac00a45d48676ddd4adf282ecb27774cf0d6231c58f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionOnTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitTimeInMinutes")
    def wait_time_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "waitTimeInMinutes"))

    @wait_time_in_minutes.setter
    def wait_time_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54184e0d841efffa151a5ba99d8ca798c0771f7306438b463ef6f87fdf45093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitTimeInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53833ff5161883d91bcdb33c529429eb4ceff13c439f374178647d201eb7c736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption",
    jsii_struct_bases=[],
    name_mapping={"action": "action"},
)
class CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption:
    def __init__(self, *, action: typing.Optional[builtins.str] = None) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ffd1b2b0a504520596fdcb6fad9e343125f8845d7e4e0e2177b1d72226e255d)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62eb68ddc4f1fd6c32b75dc8f645d59bdc5d6285d80e52fd51b2605667db0de8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5946f288f0c15ea50ec832adf719eda43da09e2cd03f9990eb0db9ecc3b48d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a5706f7da6054ca745888c1d35d178499de469eec51ef8ca86f9a4ff4bba05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupBlueGreenDeploymentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac659bf32843b02a1e86e1c27fcfb53661068d83b91ec699b6b5a08989799188)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeploymentReadyOption")
    def put_deployment_ready_option(
        self,
        *,
        action_on_timeout: typing.Optional[builtins.str] = None,
        wait_time_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action_on_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#action_on_timeout CodedeployDeploymentGroup#action_on_timeout}.
        :param wait_time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#wait_time_in_minutes CodedeployDeploymentGroup#wait_time_in_minutes}.
        '''
        value = CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption(
            action_on_timeout=action_on_timeout,
            wait_time_in_minutes=wait_time_in_minutes,
        )

        return typing.cast(None, jsii.invoke(self, "putDeploymentReadyOption", [value]))

    @jsii.member(jsii_name="putGreenFleetProvisioningOption")
    def put_green_fleet_provisioning_option(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.
        '''
        value = CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption(
            action=action
        )

        return typing.cast(None, jsii.invoke(self, "putGreenFleetProvisioningOption", [value]))

    @jsii.member(jsii_name="putTerminateBlueInstancesOnDeploymentSuccess")
    def put_terminate_blue_instances_on_deployment_success(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.
        :param termination_wait_time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#termination_wait_time_in_minutes CodedeployDeploymentGroup#termination_wait_time_in_minutes}.
        '''
        value = CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess(
            action=action,
            termination_wait_time_in_minutes=termination_wait_time_in_minutes,
        )

        return typing.cast(None, jsii.invoke(self, "putTerminateBlueInstancesOnDeploymentSuccess", [value]))

    @jsii.member(jsii_name="resetDeploymentReadyOption")
    def reset_deployment_ready_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentReadyOption", []))

    @jsii.member(jsii_name="resetGreenFleetProvisioningOption")
    def reset_green_fleet_provisioning_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGreenFleetProvisioningOption", []))

    @jsii.member(jsii_name="resetTerminateBlueInstancesOnDeploymentSuccess")
    def reset_terminate_blue_instances_on_deployment_success(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminateBlueInstancesOnDeploymentSuccess", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentReadyOption")
    def deployment_ready_option(
        self,
    ) -> CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionOutputReference:
        return typing.cast(CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionOutputReference, jsii.get(self, "deploymentReadyOption"))

    @builtins.property
    @jsii.member(jsii_name="greenFleetProvisioningOption")
    def green_fleet_provisioning_option(
        self,
    ) -> CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionOutputReference:
        return typing.cast(CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionOutputReference, jsii.get(self, "greenFleetProvisioningOption"))

    @builtins.property
    @jsii.member(jsii_name="terminateBlueInstancesOnDeploymentSuccess")
    def terminate_blue_instances_on_deployment_success(
        self,
    ) -> "CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessOutputReference":
        return typing.cast("CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessOutputReference", jsii.get(self, "terminateBlueInstancesOnDeploymentSuccess"))

    @builtins.property
    @jsii.member(jsii_name="deploymentReadyOptionInput")
    def deployment_ready_option_input(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption], jsii.get(self, "deploymentReadyOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="greenFleetProvisioningOptionInput")
    def green_fleet_provisioning_option_input(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption], jsii.get(self, "greenFleetProvisioningOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="terminateBlueInstancesOnDeploymentSuccessInput")
    def terminate_blue_instances_on_deployment_success_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess"], jsii.get(self, "terminateBlueInstancesOnDeploymentSuccessInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17bd954718ab7d10e434ca761a2740ada279f1edda835227d6dd107455a3eb87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "termination_wait_time_in_minutes": "terminationWaitTimeInMinutes",
    },
)
class CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.
        :param termination_wait_time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#termination_wait_time_in_minutes CodedeployDeploymentGroup#termination_wait_time_in_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2876891a42fbf393c8ae91563c0f981fe768b6b567ce93623d2f171cc17d86b5)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument termination_wait_time_in_minutes", value=termination_wait_time_in_minutes, expected_type=type_hints["termination_wait_time_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if termination_wait_time_in_minutes is not None:
            self._values["termination_wait_time_in_minutes"] = termination_wait_time_in_minutes

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_wait_time_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#termination_wait_time_in_minutes CodedeployDeploymentGroup#termination_wait_time_in_minutes}.'''
        result = self._values.get("termination_wait_time_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f4c0c86aab9046d2e20255db6b6f74a304891fb5bc10339e7b2b6d1c001f436)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetTerminationWaitTimeInMinutes")
    def reset_termination_wait_time_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationWaitTimeInMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationWaitTimeInMinutesInput")
    def termination_wait_time_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "terminationWaitTimeInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2d7f8dbc2a1c328cbe4c69063a9cb82b99fd01b114645d538ead57a04fbba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationWaitTimeInMinutes")
    def termination_wait_time_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminationWaitTimeInMinutes"))

    @termination_wait_time_in_minutes.setter
    def termination_wait_time_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627ea89e25a92943ee8784001dfa5c27a9d807330ccfb5329218bb7f7e037938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationWaitTimeInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef453839d1709de0211b5eac74bfd2119d25b0add181340e7744e20d46c09260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_name": "appName",
        "deployment_group_name": "deploymentGroupName",
        "service_role_arn": "serviceRoleArn",
        "alarm_configuration": "alarmConfiguration",
        "auto_rollback_configuration": "autoRollbackConfiguration",
        "autoscaling_groups": "autoscalingGroups",
        "blue_green_deployment_config": "blueGreenDeploymentConfig",
        "deployment_config_name": "deploymentConfigName",
        "deployment_style": "deploymentStyle",
        "ec2_tag_filter": "ec2TagFilter",
        "ec2_tag_set": "ec2TagSet",
        "ecs_service": "ecsService",
        "id": "id",
        "load_balancer_info": "loadBalancerInfo",
        "on_premises_instance_tag_filter": "onPremisesInstanceTagFilter",
        "outdated_instances_strategy": "outdatedInstancesStrategy",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "termination_hook_enabled": "terminationHookEnabled",
        "trigger_configuration": "triggerConfiguration",
    },
)
class CodedeployDeploymentGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_name: builtins.str,
        deployment_group_name: builtins.str,
        service_role_arn: builtins.str,
        alarm_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAlarmConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_rollback_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAutoRollbackConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        autoscaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        blue_green_deployment_config: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        deployment_style: typing.Optional[typing.Union["CodedeployDeploymentGroupDeploymentStyle", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ec2_tag_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ecs_service: typing.Optional[typing.Union["CodedeployDeploymentGroupEcsService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer_info: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        on_premises_instance_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupOnPremisesInstanceTagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        outdated_instances_strategy: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_hook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trigger_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupTriggerConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#app_name CodedeployDeploymentGroup#app_name}.
        :param deployment_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_group_name CodedeployDeploymentGroup#deployment_group_name}.
        :param service_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#service_role_arn CodedeployDeploymentGroup#service_role_arn}.
        :param alarm_configuration: alarm_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#alarm_configuration CodedeployDeploymentGroup#alarm_configuration}
        :param auto_rollback_configuration: auto_rollback_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#auto_rollback_configuration CodedeployDeploymentGroup#auto_rollback_configuration}
        :param autoscaling_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#autoscaling_groups CodedeployDeploymentGroup#autoscaling_groups}.
        :param blue_green_deployment_config: blue_green_deployment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#blue_green_deployment_config CodedeployDeploymentGroup#blue_green_deployment_config}
        :param deployment_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_config_name CodedeployDeploymentGroup#deployment_config_name}.
        :param deployment_style: deployment_style block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_style CodedeployDeploymentGroup#deployment_style}
        :param ec2_tag_filter: ec2_tag_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ec2_tag_filter CodedeployDeploymentGroup#ec2_tag_filter}
        :param ec2_tag_set: ec2_tag_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ec2_tag_set CodedeployDeploymentGroup#ec2_tag_set}
        :param ecs_service: ecs_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ecs_service CodedeployDeploymentGroup#ecs_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#id CodedeployDeploymentGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer_info: load_balancer_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#load_balancer_info CodedeployDeploymentGroup#load_balancer_info}
        :param on_premises_instance_tag_filter: on_premises_instance_tag_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#on_premises_instance_tag_filter CodedeployDeploymentGroup#on_premises_instance_tag_filter}
        :param outdated_instances_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#outdated_instances_strategy CodedeployDeploymentGroup#outdated_instances_strategy}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#region CodedeployDeploymentGroup#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#tags CodedeployDeploymentGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#tags_all CodedeployDeploymentGroup#tags_all}.
        :param termination_hook_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#termination_hook_enabled CodedeployDeploymentGroup#termination_hook_enabled}.
        :param trigger_configuration: trigger_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#trigger_configuration CodedeployDeploymentGroup#trigger_configuration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(alarm_configuration, dict):
            alarm_configuration = CodedeployDeploymentGroupAlarmConfiguration(**alarm_configuration)
        if isinstance(auto_rollback_configuration, dict):
            auto_rollback_configuration = CodedeployDeploymentGroupAutoRollbackConfiguration(**auto_rollback_configuration)
        if isinstance(blue_green_deployment_config, dict):
            blue_green_deployment_config = CodedeployDeploymentGroupBlueGreenDeploymentConfig(**blue_green_deployment_config)
        if isinstance(deployment_style, dict):
            deployment_style = CodedeployDeploymentGroupDeploymentStyle(**deployment_style)
        if isinstance(ecs_service, dict):
            ecs_service = CodedeployDeploymentGroupEcsService(**ecs_service)
        if isinstance(load_balancer_info, dict):
            load_balancer_info = CodedeployDeploymentGroupLoadBalancerInfo(**load_balancer_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de3e200c635a3dfcf80cca88c25b78d43862898fb71889073cdc4c2e9704d0e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_name", value=app_name, expected_type=type_hints["app_name"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument alarm_configuration", value=alarm_configuration, expected_type=type_hints["alarm_configuration"])
            check_type(argname="argument auto_rollback_configuration", value=auto_rollback_configuration, expected_type=type_hints["auto_rollback_configuration"])
            check_type(argname="argument autoscaling_groups", value=autoscaling_groups, expected_type=type_hints["autoscaling_groups"])
            check_type(argname="argument blue_green_deployment_config", value=blue_green_deployment_config, expected_type=type_hints["blue_green_deployment_config"])
            check_type(argname="argument deployment_config_name", value=deployment_config_name, expected_type=type_hints["deployment_config_name"])
            check_type(argname="argument deployment_style", value=deployment_style, expected_type=type_hints["deployment_style"])
            check_type(argname="argument ec2_tag_filter", value=ec2_tag_filter, expected_type=type_hints["ec2_tag_filter"])
            check_type(argname="argument ec2_tag_set", value=ec2_tag_set, expected_type=type_hints["ec2_tag_set"])
            check_type(argname="argument ecs_service", value=ecs_service, expected_type=type_hints["ecs_service"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument load_balancer_info", value=load_balancer_info, expected_type=type_hints["load_balancer_info"])
            check_type(argname="argument on_premises_instance_tag_filter", value=on_premises_instance_tag_filter, expected_type=type_hints["on_premises_instance_tag_filter"])
            check_type(argname="argument outdated_instances_strategy", value=outdated_instances_strategy, expected_type=type_hints["outdated_instances_strategy"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument termination_hook_enabled", value=termination_hook_enabled, expected_type=type_hints["termination_hook_enabled"])
            check_type(argname="argument trigger_configuration", value=trigger_configuration, expected_type=type_hints["trigger_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_name": app_name,
            "deployment_group_name": deployment_group_name,
            "service_role_arn": service_role_arn,
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
        if alarm_configuration is not None:
            self._values["alarm_configuration"] = alarm_configuration
        if auto_rollback_configuration is not None:
            self._values["auto_rollback_configuration"] = auto_rollback_configuration
        if autoscaling_groups is not None:
            self._values["autoscaling_groups"] = autoscaling_groups
        if blue_green_deployment_config is not None:
            self._values["blue_green_deployment_config"] = blue_green_deployment_config
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name
        if deployment_style is not None:
            self._values["deployment_style"] = deployment_style
        if ec2_tag_filter is not None:
            self._values["ec2_tag_filter"] = ec2_tag_filter
        if ec2_tag_set is not None:
            self._values["ec2_tag_set"] = ec2_tag_set
        if ecs_service is not None:
            self._values["ecs_service"] = ecs_service
        if id is not None:
            self._values["id"] = id
        if load_balancer_info is not None:
            self._values["load_balancer_info"] = load_balancer_info
        if on_premises_instance_tag_filter is not None:
            self._values["on_premises_instance_tag_filter"] = on_premises_instance_tag_filter
        if outdated_instances_strategy is not None:
            self._values["outdated_instances_strategy"] = outdated_instances_strategy
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if termination_hook_enabled is not None:
            self._values["termination_hook_enabled"] = termination_hook_enabled
        if trigger_configuration is not None:
            self._values["trigger_configuration"] = trigger_configuration

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
    def app_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#app_name CodedeployDeploymentGroup#app_name}.'''
        result = self._values.get("app_name")
        assert result is not None, "Required property 'app_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_group_name CodedeployDeploymentGroup#deployment_group_name}.'''
        result = self._values.get("deployment_group_name")
        assert result is not None, "Required property 'deployment_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#service_role_arn CodedeployDeploymentGroup#service_role_arn}.'''
        result = self._values.get("service_role_arn")
        assert result is not None, "Required property 'service_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarm_configuration(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupAlarmConfiguration]:
        '''alarm_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#alarm_configuration CodedeployDeploymentGroup#alarm_configuration}
        '''
        result = self._values.get("alarm_configuration")
        return typing.cast(typing.Optional[CodedeployDeploymentGroupAlarmConfiguration], result)

    @builtins.property
    def auto_rollback_configuration(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration]:
        '''auto_rollback_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#auto_rollback_configuration CodedeployDeploymentGroup#auto_rollback_configuration}
        '''
        result = self._values.get("auto_rollback_configuration")
        return typing.cast(typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration], result)

    @builtins.property
    def autoscaling_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#autoscaling_groups CodedeployDeploymentGroup#autoscaling_groups}.'''
        result = self._values.get("autoscaling_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def blue_green_deployment_config(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig]:
        '''blue_green_deployment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#blue_green_deployment_config CodedeployDeploymentGroup#blue_green_deployment_config}
        '''
        result = self._values.get("blue_green_deployment_config")
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig], result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_config_name CodedeployDeploymentGroup#deployment_config_name}.'''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_style(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupDeploymentStyle"]:
        '''deployment_style block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_style CodedeployDeploymentGroup#deployment_style}
        '''
        result = self._values.get("deployment_style")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupDeploymentStyle"], result)

    @builtins.property
    def ec2_tag_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagFilter"]]]:
        '''ec2_tag_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ec2_tag_filter CodedeployDeploymentGroup#ec2_tag_filter}
        '''
        result = self._values.get("ec2_tag_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagFilter"]]], result)

    @builtins.property
    def ec2_tag_set(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSet"]]]:
        '''ec2_tag_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ec2_tag_set CodedeployDeploymentGroup#ec2_tag_set}
        '''
        result = self._values.get("ec2_tag_set")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSet"]]], result)

    @builtins.property
    def ecs_service(self) -> typing.Optional["CodedeployDeploymentGroupEcsService"]:
        '''ecs_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ecs_service CodedeployDeploymentGroup#ecs_service}
        '''
        result = self._values.get("ecs_service")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupEcsService"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#id CodedeployDeploymentGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_info(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfo"]:
        '''load_balancer_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#load_balancer_info CodedeployDeploymentGroup#load_balancer_info}
        '''
        result = self._values.get("load_balancer_info")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfo"], result)

    @builtins.property
    def on_premises_instance_tag_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupOnPremisesInstanceTagFilter"]]]:
        '''on_premises_instance_tag_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#on_premises_instance_tag_filter CodedeployDeploymentGroup#on_premises_instance_tag_filter}
        '''
        result = self._values.get("on_premises_instance_tag_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupOnPremisesInstanceTagFilter"]]], result)

    @builtins.property
    def outdated_instances_strategy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#outdated_instances_strategy CodedeployDeploymentGroup#outdated_instances_strategy}.'''
        result = self._values.get("outdated_instances_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#region CodedeployDeploymentGroup#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#tags CodedeployDeploymentGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#tags_all CodedeployDeploymentGroup#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_hook_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#termination_hook_enabled CodedeployDeploymentGroup#termination_hook_enabled}.'''
        result = self._values.get("termination_hook_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trigger_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupTriggerConfiguration"]]]:
        '''trigger_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#trigger_configuration CodedeployDeploymentGroup#trigger_configuration}
        '''
        result = self._values.get("trigger_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupTriggerConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupDeploymentStyle",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_option": "deploymentOption",
        "deployment_type": "deploymentType",
    },
)
class CodedeployDeploymentGroupDeploymentStyle:
    def __init__(
        self,
        *,
        deployment_option: typing.Optional[builtins.str] = None,
        deployment_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_option CodedeployDeploymentGroup#deployment_option}.
        :param deployment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_type CodedeployDeploymentGroup#deployment_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92d6cbae4425129fcc51c95cd17076938295e1cb36390e327c62248c904c772)
            check_type(argname="argument deployment_option", value=deployment_option, expected_type=type_hints["deployment_option"])
            check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_option is not None:
            self._values["deployment_option"] = deployment_option
        if deployment_type is not None:
            self._values["deployment_type"] = deployment_type

    @builtins.property
    def deployment_option(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_option CodedeployDeploymentGroup#deployment_option}.'''
        result = self._values.get("deployment_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#deployment_type CodedeployDeploymentGroup#deployment_type}.'''
        result = self._values.get("deployment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupDeploymentStyle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupDeploymentStyleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupDeploymentStyleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11e8f2083e6c8a1adc42c0114f2825b25fa81bd0c49ca9275ed8636652558fe3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeploymentOption")
    def reset_deployment_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentOption", []))

    @jsii.member(jsii_name="resetDeploymentType")
    def reset_deployment_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentType", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentOptionInput")
    def deployment_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentTypeInput")
    def deployment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentOption")
    def deployment_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentOption"))

    @deployment_option.setter
    def deployment_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f2b550e1ba429d16ffc20afebac0329c3c2e766eeca8a7ef1131a8e3c14bc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentType")
    def deployment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentType"))

    @deployment_type.setter
    def deployment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ead77b9f6b1f3f2f5321fa74da5edd21a3c13d58f820d16eeffb601c8d5445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupDeploymentStyle]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupDeploymentStyle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupDeploymentStyle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c15f0f6989b2a7186dec12d563f5d5a412fca06790f202e641de6d44357e56e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagFilter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "type": "type", "value": "value"},
)
class CodedeployDeploymentGroupEc2TagFilter:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea50669ba8953d6806e97c2490d62f1e7bfe74fe2aff7b7827359f99b2af895)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupEc2TagFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupEc2TagFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1cb5cd7ef0fff9f5ff9e9fc03a5a508643f3d57eb86d4d9f40980641303fb60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupEc2TagFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac99b07af15061bfe10bb005213fcebde8b4c055cc130465fcf47d4dbfbfbd15)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupEc2TagFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279c3fa2a030ffa1b33c5dbd9593f22f453ad14d56ca7f1d6d974d842ef3eef1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ced71c0a7f7d3cfd0d6fdce71d8d387a0a6e3a9415490a4a7ba3a675cdf0fc4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc1acdb513d8f2485d33d3aef60c8921d00928a07e6f07d53734d19dd91ea41f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6da961776ab4381bd7c08a5842e43f279bf0c7cda9d7f2667ec6b7457f0c03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupEc2TagFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03efdc40c3a4550707efa4ad72e493c29a16807b53eca43356663826dd69b770)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f6bb9b259b2ded7505231e09201df0d88957cdf9585b9950c8a8e6beec26f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3deb97243abee8ad36ee1d48ce8da1e34b29bccb0eacbdc0a70f32693d8b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2506aac9bcd73156a3eb763d0043879e88f83413a3d2c4b369e717d14340da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0eb58abd78006c7eb003c6e7cb29e0756da2af50b5530d5bacb1d1f27b6755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSet",
    jsii_struct_bases=[],
    name_mapping={"ec2_tag_filter": "ec2TagFilter"},
)
class CodedeployDeploymentGroupEc2TagSet:
    def __init__(
        self,
        *,
        ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagSetEc2TagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ec2_tag_filter: ec2_tag_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ec2_tag_filter CodedeployDeploymentGroup#ec2_tag_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce56a74894a2eb37ce97231faa0623da1becb9edc4406712eb8efa19b9dee7aa)
            check_type(argname="argument ec2_tag_filter", value=ec2_tag_filter, expected_type=type_hints["ec2_tag_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ec2_tag_filter is not None:
            self._values["ec2_tag_filter"] = ec2_tag_filter

    @builtins.property
    def ec2_tag_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSetEc2TagFilter"]]]:
        '''ec2_tag_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#ec2_tag_filter CodedeployDeploymentGroup#ec2_tag_filter}
        '''
        result = self._values.get("ec2_tag_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSetEc2TagFilter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupEc2TagSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSetEc2TagFilter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "type": "type", "value": "value"},
)
class CodedeployDeploymentGroupEc2TagSetEc2TagFilter:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2bf56b371cc45291b6122943fec8b5e78c8f37b5da68903dda03fe86bf2a35)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupEc2TagSetEc2TagFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupEc2TagSetEc2TagFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSetEc2TagFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f38d1435e33867dea4ee862670934ebf859b6d2c520aff9623f57ce54cb8ac60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupEc2TagSetEc2TagFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857ea9e0e837fb3d3da9073ecfbdb39f65c69e6cf01c951c392e25d68858e086)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupEc2TagSetEc2TagFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f8497a9933f43bcb62b97eaea80770c25ecba03d2af3ea8117e7b369493f49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c157802ad85d9e2f8d1382786248a62b353917b0ac818e538c2f57a1cea3c279)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2967b19d3590974f2702e9e1a52201a8557f3d428960a95f75d6b313898c772c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f88cccfdcd25dd0d04198e7eb7c6989e75b1e3944a5d1a5c7055affcb138fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupEc2TagSetEc2TagFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSetEc2TagFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9381c74e50ee2ffe3244b06873b5c8ca388a47f2d2a34ecbb712ebeab085de73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c5c2d55530b62a64156a1ea5ab7c6ccbf298d24492f2242fb032788a638232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7654d4f80b5a8c89db95e5df313aacc3cc1e1cc7ea2e1a9aa7dcc9b12d8b5cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8af59bd90fa6774427f04ebd729e31ee4f9d1557a41ec11e4386fe46aa1e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSetEc2TagFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSetEc2TagFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5955ff303ec3e7d3fae844e43acd1eeec52628ef03ebbad978f531e7afa9ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupEc2TagSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__305e05969ada7bbebcbd0fe9916eca1ddc88ff3e192f5e21602ac86596929f5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupEc2TagSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10337ac56e3fd2cdfca2c5c9a3e0a1f974975e11d95ec1da50b6b4b158bf85d7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupEc2TagSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a73d3e78a3b005eeff559437ca53bb591513a21e1531b4cc306270ea2d90770)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e734c5ff227d1cd2c6fd8566b5905104dc99ef6a1f9c54295b5e352fce860b2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04c5edfe9d80634985a34e3feff123fd7af627a1eead9b896644ff0e90ccc813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe945e669a9e7d54afb11ae892dd546ac574f421d89a8f50919cef3166589a65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupEc2TagSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ebd28b56719a61b7d3871b323b417dbb19876096ff081810a055b8cc274adb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEc2TagFilter")
    def put_ec2_tag_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSetEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878e3bab64d1f74e97d7c004d049fa6cb26a4ae3212288de52915fe3bceb8e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEc2TagFilter", [value]))

    @jsii.member(jsii_name="resetEc2TagFilter")
    def reset_ec2_tag_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2TagFilter", []))

    @builtins.property
    @jsii.member(jsii_name="ec2TagFilter")
    def ec2_tag_filter(self) -> CodedeployDeploymentGroupEc2TagSetEc2TagFilterList:
        return typing.cast(CodedeployDeploymentGroupEc2TagSetEc2TagFilterList, jsii.get(self, "ec2TagFilter"))

    @builtins.property
    @jsii.member(jsii_name="ec2TagFilterInput")
    def ec2_tag_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]], jsii.get(self, "ec2TagFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93ed8d4cd544d8e12446a656b3cb68058c280439f5ae7779f0fad5aa9ac4673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEcsService",
    jsii_struct_bases=[],
    name_mapping={"cluster_name": "clusterName", "service_name": "serviceName"},
)
class CodedeployDeploymentGroupEcsService:
    def __init__(
        self,
        *,
        cluster_name: builtins.str,
        service_name: builtins.str,
    ) -> None:
        '''
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#cluster_name CodedeployDeploymentGroup#cluster_name}.
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#service_name CodedeployDeploymentGroup#service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e61a659bace40c1230ea3501df0256b5a65cc730654dee8c8d0ce8bce14bb7b)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "service_name": service_name,
        }

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#cluster_name CodedeployDeploymentGroup#cluster_name}.'''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#service_name CodedeployDeploymentGroup#service_name}.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupEcsService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupEcsServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEcsServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7629bd668055bf1880b035dcbcefca17a35abab27351c5ed2b6cc45115d22ef1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57870823474b13659a8c40f56d589a0f64b6e395ef0a333ce77cb84dda75b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24ded0d8d800fc784cfca202078766f495bda03b5dda26b6c84815355ae2069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodedeployDeploymentGroupEcsService]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupEcsService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupEcsService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e67627e6bcd77c9f141175bf8bdb3ebd233f8c374622fcd9456a4ae97dd37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfo",
    jsii_struct_bases=[],
    name_mapping={
        "elb_info": "elbInfo",
        "target_group_info": "targetGroupInfo",
        "target_group_pair_info": "targetGroupPairInfo",
    },
)
class CodedeployDeploymentGroupLoadBalancerInfo:
    def __init__(
        self,
        *,
        elb_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoElbInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_group_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_group_pair_info: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param elb_info: elb_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#elb_info CodedeployDeploymentGroup#elb_info}
        :param target_group_info: target_group_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#target_group_info CodedeployDeploymentGroup#target_group_info}
        :param target_group_pair_info: target_group_pair_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#target_group_pair_info CodedeployDeploymentGroup#target_group_pair_info}
        '''
        if isinstance(target_group_pair_info, dict):
            target_group_pair_info = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo(**target_group_pair_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c028bfe0c2152a6ce7615978ea620108fc8c05eba40fa0a71a9f770409d4ebdf)
            check_type(argname="argument elb_info", value=elb_info, expected_type=type_hints["elb_info"])
            check_type(argname="argument target_group_info", value=target_group_info, expected_type=type_hints["target_group_info"])
            check_type(argname="argument target_group_pair_info", value=target_group_pair_info, expected_type=type_hints["target_group_pair_info"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if elb_info is not None:
            self._values["elb_info"] = elb_info
        if target_group_info is not None:
            self._values["target_group_info"] = target_group_info
        if target_group_pair_info is not None:
            self._values["target_group_pair_info"] = target_group_pair_info

    @builtins.property
    def elb_info(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoElbInfo"]]]:
        '''elb_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#elb_info CodedeployDeploymentGroup#elb_info}
        '''
        result = self._values.get("elb_info")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoElbInfo"]]], result)

    @builtins.property
    def target_group_info(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo"]]]:
        '''target_group_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#target_group_info CodedeployDeploymentGroup#target_group_info}
        '''
        result = self._values.get("target_group_info")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo"]]], result)

    @builtins.property
    def target_group_pair_info(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo"]:
        '''target_group_pair_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#target_group_pair_info CodedeployDeploymentGroup#target_group_pair_info}
        '''
        result = self._values.get("target_group_pair_info")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoElbInfo",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class CodedeployDeploymentGroupLoadBalancerInfoElbInfo:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7365538b0b6c647bc19a718c3b6608ef1712707d089dc7d35b8789da1e235bf1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoElbInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoElbInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoElbInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78e006c4760316f43ed62fd428b2c69490094435d35d5d3ed45a79550fbb722f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoElbInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c81483f9c108fbce58e870551116491cd4ecdad44e863dea3796b48e864fbe6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoElbInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f654c45633faab8521c4d90587262e6e7fd3939eec86667f4a80ea511dcb709b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbb9971477de2dc5ffc23bd69975794f256ae44c7d6a3f8be0f32b6eaca42637)
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
            type_hints = typing.get_type_hints(_typecheckingstub__289c0d204f2c537c05a38c89078758774992e869610bccfbfeb368635a980c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0e92f2a0aba148e37c3629a9ec135153d41060a50a67da1712944cf3769df5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupLoadBalancerInfoElbInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoElbInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe1af728c45487f291d9ce90cf71ad32840054f8c73c9eae12038bfa84da0dd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232704bec9ab6a2f756d9acba63aa95db6d79251e1494b5a7d08af24a8ff3470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoElbInfo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoElbInfo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa33c667c7512e893f490f3b36ee5daaaa9ef3909f6194f8dfcec3a0f1869cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupLoadBalancerInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a173c1305e5215820a5f3cfc9bef8c9088ccffcbbd32055d5c251992d0efe4f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putElbInfo")
    def put_elb_info(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoElbInfo, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b7ace797f4c2bac89e14142ec37bf3360220e5fbdfb0a6424853d92e9b1061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElbInfo", [value]))

    @jsii.member(jsii_name="putTargetGroupInfo")
    def put_target_group_info(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__116d55eb957e7b70bfc3af14f7ea5e0d878e05682b4e715f9e656d749e05c3d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetGroupInfo", [value]))

    @jsii.member(jsii_name="putTargetGroupPairInfo")
    def put_target_group_pair_info(
        self,
        *,
        prod_traffic_route: typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute", typing.Dict[builtins.str, typing.Any]],
        target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
        test_traffic_route: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param prod_traffic_route: prod_traffic_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#prod_traffic_route CodedeployDeploymentGroup#prod_traffic_route}
        :param target_group: target_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#target_group CodedeployDeploymentGroup#target_group}
        :param test_traffic_route: test_traffic_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#test_traffic_route CodedeployDeploymentGroup#test_traffic_route}
        '''
        value = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo(
            prod_traffic_route=prod_traffic_route,
            target_group=target_group,
            test_traffic_route=test_traffic_route,
        )

        return typing.cast(None, jsii.invoke(self, "putTargetGroupPairInfo", [value]))

    @jsii.member(jsii_name="resetElbInfo")
    def reset_elb_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElbInfo", []))

    @jsii.member(jsii_name="resetTargetGroupInfo")
    def reset_target_group_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetGroupInfo", []))

    @jsii.member(jsii_name="resetTargetGroupPairInfo")
    def reset_target_group_pair_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetGroupPairInfo", []))

    @builtins.property
    @jsii.member(jsii_name="elbInfo")
    def elb_info(self) -> CodedeployDeploymentGroupLoadBalancerInfoElbInfoList:
        return typing.cast(CodedeployDeploymentGroupLoadBalancerInfoElbInfoList, jsii.get(self, "elbInfo"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupInfo")
    def target_group_info(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoList":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoList", jsii.get(self, "targetGroupInfo"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupPairInfo")
    def target_group_pair_info(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoOutputReference":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoOutputReference", jsii.get(self, "targetGroupPairInfo"))

    @builtins.property
    @jsii.member(jsii_name="elbInfoInput")
    def elb_info_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]], jsii.get(self, "elbInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupInfoInput")
    def target_group_info_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo"]]], jsii.get(self, "targetGroupInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupPairInfoInput")
    def target_group_pair_info_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo"], jsii.get(self, "targetGroupPairInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupLoadBalancerInfo]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupLoadBalancerInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8057d0a7544d2aab33db25af7f51b54d5b4ec533affead0f6317ceab08667d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975f45258e5e760f46652ee79811edd5720779ccf107bf9b083caf273c2e2f31)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58eece04d18f81be194174ea4a0b75e3be429a35f97406333ff2f8ce419c3de9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188821875386099a248d53b9593c22f7c6b53e4ba81ec6899bbbc7a4e47c1b40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c59eb7ae28a89298b89aa9edb85ba311cb4ab466737d0257fb4cbe342b13268)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bb259ae03176dd8c447e7dee6225ca66ee2a1431cdedbfc04cec3e8238bd756)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c710c0ab762a86842f0a95d0475d89b9aaa0958f1f1cddedcf8c36a4c555b427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e3de471c122d127d63cfc78422b72cbac3e9301812a75077a43b6dd108dec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bc448ec46c37e32925c98ae098f3f7c452bf3f4b03575384cfaac0485f91393)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a60edb7d161a1c1c3dc630874bebaf907da7c54a3cd3271eff8eeef706b5872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a06a53eb52df4fc8605635de8390b92a846268f694b94da689ef096999d28bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo",
    jsii_struct_bases=[],
    name_mapping={
        "prod_traffic_route": "prodTrafficRoute",
        "target_group": "targetGroup",
        "test_traffic_route": "testTrafficRoute",
    },
)
class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo:
    def __init__(
        self,
        *,
        prod_traffic_route: typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute", typing.Dict[builtins.str, typing.Any]],
        target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
        test_traffic_route: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param prod_traffic_route: prod_traffic_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#prod_traffic_route CodedeployDeploymentGroup#prod_traffic_route}
        :param target_group: target_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#target_group CodedeployDeploymentGroup#target_group}
        :param test_traffic_route: test_traffic_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#test_traffic_route CodedeployDeploymentGroup#test_traffic_route}
        '''
        if isinstance(prod_traffic_route, dict):
            prod_traffic_route = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute(**prod_traffic_route)
        if isinstance(test_traffic_route, dict):
            test_traffic_route = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute(**test_traffic_route)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937d5d120ead557f9e322fddcc42924838cb2368dc1d17f2454fecd19289750b)
            check_type(argname="argument prod_traffic_route", value=prod_traffic_route, expected_type=type_hints["prod_traffic_route"])
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
            check_type(argname="argument test_traffic_route", value=test_traffic_route, expected_type=type_hints["test_traffic_route"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prod_traffic_route": prod_traffic_route,
            "target_group": target_group,
        }
        if test_traffic_route is not None:
            self._values["test_traffic_route"] = test_traffic_route

    @builtins.property
    def prod_traffic_route(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute":
        '''prod_traffic_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#prod_traffic_route CodedeployDeploymentGroup#prod_traffic_route}
        '''
        result = self._values.get("prod_traffic_route")
        assert result is not None, "Required property 'prod_traffic_route' is missing"
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute", result)

    @builtins.property
    def target_group(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup"]]:
        '''target_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#target_group CodedeployDeploymentGroup#target_group}
        '''
        result = self._values.get("target_group")
        assert result is not None, "Required property 'target_group' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup"]], result)

    @builtins.property
    def test_traffic_route(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute"]:
        '''test_traffic_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#test_traffic_route CodedeployDeploymentGroup#test_traffic_route}
        '''
        result = self._values.get("test_traffic_route")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c922589089bb99de235238f0048c0d346bb61c3d8f327c617acbf028ebb8ec1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProdTrafficRoute")
    def put_prod_traffic_route(
        self,
        *,
        listener_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param listener_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.
        '''
        value = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute(
            listener_arns=listener_arns
        )

        return typing.cast(None, jsii.invoke(self, "putProdTrafficRoute", [value]))

    @jsii.member(jsii_name="putTargetGroup")
    def put_target_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ea17076fab90fa71f2493dbd3bffe655413d3c28449630cdb3cc177c36d94d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetGroup", [value]))

    @jsii.member(jsii_name="putTestTrafficRoute")
    def put_test_traffic_route(
        self,
        *,
        listener_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param listener_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.
        '''
        value = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute(
            listener_arns=listener_arns
        )

        return typing.cast(None, jsii.invoke(self, "putTestTrafficRoute", [value]))

    @jsii.member(jsii_name="resetTestTrafficRoute")
    def reset_test_traffic_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestTrafficRoute", []))

    @builtins.property
    @jsii.member(jsii_name="prodTrafficRoute")
    def prod_traffic_route(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteOutputReference":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteOutputReference", jsii.get(self, "prodTrafficRoute"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupList":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupList", jsii.get(self, "targetGroup"))

    @builtins.property
    @jsii.member(jsii_name="testTrafficRoute")
    def test_traffic_route(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRouteOutputReference":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRouteOutputReference", jsii.get(self, "testTrafficRoute"))

    @builtins.property
    @jsii.member(jsii_name="prodTrafficRouteInput")
    def prod_traffic_route_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute"], jsii.get(self, "prodTrafficRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupInput")
    def target_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup"]]], jsii.get(self, "targetGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="testTrafficRouteInput")
    def test_traffic_route_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute"], jsii.get(self, "testTrafficRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c24661519253cd7118a75976c42e908112ba9535bb3ffae6bd15f51e8a7e84ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute",
    jsii_struct_bases=[],
    name_mapping={"listener_arns": "listenerArns"},
)
class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute:
    def __init__(self, *, listener_arns: typing.Sequence[builtins.str]) -> None:
        '''
        :param listener_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5feaf6683c7cbb06bdebfdd0cd7df87754e1eab352f038e2cb8ada71ae0c30f)
            check_type(argname="argument listener_arns", value=listener_arns, expected_type=type_hints["listener_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "listener_arns": listener_arns,
        }

    @builtins.property
    def listener_arns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.'''
        result = self._values.get("listener_arns")
        assert result is not None, "Required property 'listener_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__100576b1dd09387aa2fbd634396b2cfcf595b534c61737aa8b1d6328f3c6f8af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="listenerArnsInput")
    def listener_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "listenerArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="listenerArns")
    def listener_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "listenerArns"))

    @listener_arns.setter
    def listener_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf566306901a518be7f9bb645636288a198be0f903b37073e72a6e441f1f8bb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listenerArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c85d421faa12623265661f7d5ab47af142d6556ee9501d51860533e58d73a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a277d974598ac8ec1dfa6b2d0551c445c2a91a1a6dbe7415d6b7ddebde99c9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__887e204aca487b1fd493a2391903ce6a258d71b8d57e1b644ab716af2b0aec99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7937cb025d969bda3a9bfddb693f96f6b88e805c621d553be1c23fb9d12d651)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75506510341817292f85b19bb4f0382325e855bdcdc8dab504ddf12ef07da0c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__924bbf498324bfeae9d9c8000d2456519d1ce541546b04816bd92e7c274f138e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83c8f85e5ae51080d6689b71ae198990e23ec9b61124d0aa30f2873aa9a2bdf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5605ceb9b80c0058600f7ba6219fe4d1e4e0af4c1ec97d1995eba105e5a6be3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7cadbf2ef6b0c71f499b6675e75dc5a07a18374920d4d07cd4b23e70e2d1000)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f55e1cf4d127a2c1ea7d110789b58bb17d6a4ed970f8b9bb91807285088f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd86583df6e761e95cf61762cfdf45c64598ad6a40ecefc9bcce51d97d09a94d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute",
    jsii_struct_bases=[],
    name_mapping={"listener_arns": "listenerArns"},
)
class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute:
    def __init__(self, *, listener_arns: typing.Sequence[builtins.str]) -> None:
        '''
        :param listener_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd95086220e0c2cf5f4c9ae8a671f584239727452c4a92cd75888ab253d4232)
            check_type(argname="argument listener_arns", value=listener_arns, expected_type=type_hints["listener_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "listener_arns": listener_arns,
        }

    @builtins.property
    def listener_arns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.'''
        result = self._values.get("listener_arns")
        assert result is not None, "Required property 'listener_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c050687677be8c57ca68b3072d5729062a0412c58b49c380f1cb8e140e3c5c3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="listenerArnsInput")
    def listener_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "listenerArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="listenerArns")
    def listener_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "listenerArns"))

    @listener_arns.setter
    def listener_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e9395dea77a2adba7fd7fdb8b2139c5887ce119371c3d1e381725589b8abd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listenerArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df99a5351b5010977c40b82944e21a470a5c6691ee4226b9d6fbdf5fe8ffac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupOnPremisesInstanceTagFilter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "type": "type", "value": "value"},
)
class CodedeployDeploymentGroupOnPremisesInstanceTagFilter:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db32f16ee7ab3396af096432fb8b3166639b2a63c26be62687133727ff712d8)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupOnPremisesInstanceTagFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupOnPremisesInstanceTagFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupOnPremisesInstanceTagFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da20b0aab92da8ebf5f3ec73385f4130c980f27bd9adb22846b1dcc158d0eba5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupOnPremisesInstanceTagFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1794872ee6995db46fbf40a3c3f7e31472cc8534feb69c82f1f9b54dac8bbc71)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupOnPremisesInstanceTagFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2dc90395d69dbfac3315840ab4b1d79a1f4d7392331fdaa51a96952006caa6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3bace816e3ef7ec2a0abcd57675a16a214664d86309c9f1918c8b081175974c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ace389eec5a4c52b0e7cf728fe8ebf136a8f9d43c0f35ddad3b4f507e5823df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupOnPremisesInstanceTagFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupOnPremisesInstanceTagFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupOnPremisesInstanceTagFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84671b1bd90be390a9fb3e8d00cd56450c7ce6aca96a47a13757d515b5532ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupOnPremisesInstanceTagFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupOnPremisesInstanceTagFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7df1403af7af7626e9fa39a7bd9d26ce5c7e351892c8978927a8241d0a42040)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b12a36eff8f5efcb644fb8bb0741429f661dfd2a001f61c40de478b0c79c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade7a378f7a4a097ec2aa211f73c4d1d8266ac8a8c6677c69edcae60361cea41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db4d7c357bdd4d2680600ce48164e6945071e9992d78bd88f00211fc5fb7785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupOnPremisesInstanceTagFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupOnPremisesInstanceTagFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupOnPremisesInstanceTagFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b30becaf6534ec2316c9761917517ee8d98bcbb3d51f3ab18aa046049f9e0e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupTriggerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "trigger_events": "triggerEvents",
        "trigger_name": "triggerName",
        "trigger_target_arn": "triggerTargetArn",
    },
)
class CodedeployDeploymentGroupTriggerConfiguration:
    def __init__(
        self,
        *,
        trigger_events: typing.Sequence[builtins.str],
        trigger_name: builtins.str,
        trigger_target_arn: builtins.str,
    ) -> None:
        '''
        :param trigger_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#trigger_events CodedeployDeploymentGroup#trigger_events}.
        :param trigger_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#trigger_name CodedeployDeploymentGroup#trigger_name}.
        :param trigger_target_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#trigger_target_arn CodedeployDeploymentGroup#trigger_target_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad2f313e306c023057ce732d1a091eec5089dc32d83ed9e8ce9a400484538ff)
            check_type(argname="argument trigger_events", value=trigger_events, expected_type=type_hints["trigger_events"])
            check_type(argname="argument trigger_name", value=trigger_name, expected_type=type_hints["trigger_name"])
            check_type(argname="argument trigger_target_arn", value=trigger_target_arn, expected_type=type_hints["trigger_target_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trigger_events": trigger_events,
            "trigger_name": trigger_name,
            "trigger_target_arn": trigger_target_arn,
        }

    @builtins.property
    def trigger_events(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#trigger_events CodedeployDeploymentGroup#trigger_events}.'''
        result = self._values.get("trigger_events")
        assert result is not None, "Required property 'trigger_events' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def trigger_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#trigger_name CodedeployDeploymentGroup#trigger_name}.'''
        result = self._values.get("trigger_name")
        assert result is not None, "Required property 'trigger_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_target_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codedeploy_deployment_group#trigger_target_arn CodedeployDeploymentGroup#trigger_target_arn}.'''
        result = self._values.get("trigger_target_arn")
        assert result is not None, "Required property 'trigger_target_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupTriggerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupTriggerConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupTriggerConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40f906c476a7d13836c3329964d2b278947c829fd58000f3e350771340315786)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupTriggerConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1afc7c8858e657d9fb52df58de379827bbada92a46c605f695886e80bd4b4203)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupTriggerConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11db513ce9b7021c589b3a70d00a81b978ce4ac6f568fc1efa876db11d7342fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6fe06f7091b4bb9ec6c310d1b6407217bc21949204b54556b806c20f87424b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9202ba45f27121964aec23c4d6c9cca891e44a10e70112191b5f877678e1fe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupTriggerConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupTriggerConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupTriggerConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3bf383e6b47466da225824b130939c8e482b6d15d0d1133048c143f1893555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupTriggerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupTriggerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cab6e829ad66a96095a81fbb2d674d27afb208bbdde51b404aa74a5b12a967bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="triggerEventsInput")
    def trigger_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggerEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerNameInput")
    def trigger_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerTargetArnInput")
    def trigger_target_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerTargetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerEvents")
    def trigger_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerEvents"))

    @trigger_events.setter
    def trigger_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076dab3bffdc45397f763a684e2723cef6253f290886db58fe3e6839018c7af3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerName")
    def trigger_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerName"))

    @trigger_name.setter
    def trigger_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9546cf2bddd110f57d31b4a42445633d941bdc920a0d7faac375c80ee038bfe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerTargetArn")
    def trigger_target_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerTargetArn"))

    @trigger_target_arn.setter
    def trigger_target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38040910444e606510873d62d2bcb39b2966dd4255aff12bb74b7aa153ef5a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerTargetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupTriggerConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupTriggerConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupTriggerConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a9363e4003a22a9e0ef82ddeea144f09721144c66f0ed36bc02f4b910e879f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CodedeployDeploymentGroup",
    "CodedeployDeploymentGroupAlarmConfiguration",
    "CodedeployDeploymentGroupAlarmConfigurationOutputReference",
    "CodedeployDeploymentGroupAutoRollbackConfiguration",
    "CodedeployDeploymentGroupAutoRollbackConfigurationOutputReference",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfig",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionOutputReference",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionOutputReference",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigOutputReference",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessOutputReference",
    "CodedeployDeploymentGroupConfig",
    "CodedeployDeploymentGroupDeploymentStyle",
    "CodedeployDeploymentGroupDeploymentStyleOutputReference",
    "CodedeployDeploymentGroupEc2TagFilter",
    "CodedeployDeploymentGroupEc2TagFilterList",
    "CodedeployDeploymentGroupEc2TagFilterOutputReference",
    "CodedeployDeploymentGroupEc2TagSet",
    "CodedeployDeploymentGroupEc2TagSetEc2TagFilter",
    "CodedeployDeploymentGroupEc2TagSetEc2TagFilterList",
    "CodedeployDeploymentGroupEc2TagSetEc2TagFilterOutputReference",
    "CodedeployDeploymentGroupEc2TagSetList",
    "CodedeployDeploymentGroupEc2TagSetOutputReference",
    "CodedeployDeploymentGroupEcsService",
    "CodedeployDeploymentGroupEcsServiceOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfo",
    "CodedeployDeploymentGroupLoadBalancerInfoElbInfo",
    "CodedeployDeploymentGroupLoadBalancerInfoElbInfoList",
    "CodedeployDeploymentGroupLoadBalancerInfoElbInfoOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoList",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupList",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRouteOutputReference",
    "CodedeployDeploymentGroupOnPremisesInstanceTagFilter",
    "CodedeployDeploymentGroupOnPremisesInstanceTagFilterList",
    "CodedeployDeploymentGroupOnPremisesInstanceTagFilterOutputReference",
    "CodedeployDeploymentGroupTriggerConfiguration",
    "CodedeployDeploymentGroupTriggerConfigurationList",
    "CodedeployDeploymentGroupTriggerConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__6d10c1172f66162326f2a54948dbdfaf972e553d40d1d2034fa32cd48fe6b618(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_name: builtins.str,
    deployment_group_name: builtins.str,
    service_role_arn: builtins.str,
    alarm_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAlarmConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_rollback_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAutoRollbackConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    autoscaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    blue_green_deployment_config: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_config_name: typing.Optional[builtins.str] = None,
    deployment_style: typing.Optional[typing.Union[CodedeployDeploymentGroupDeploymentStyle, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ec2_tag_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ecs_service: typing.Optional[typing.Union[CodedeployDeploymentGroupEcsService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer_info: typing.Optional[typing.Union[CodedeployDeploymentGroupLoadBalancerInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    on_premises_instance_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupOnPremisesInstanceTagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    outdated_instances_strategy: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_hook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trigger_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupTriggerConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__693b2a315a1986e1ebecc09211c03ff195178bb3118e0994809e3f401ed5fc02(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71a5c537a5b97604eb87b96dc9d68e356ca98c729fadd334fec4824ae963d04(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24df7547ab3345227f2e06521233abaa2e6a527d47602b19de6323840c61c285(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395ab1400d3d16ed33a15eb7ad0b437ad9b834d74492e25a929c9a056312d3eb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupOnPremisesInstanceTagFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e5f93634596baee0963f5f83f741e2dd2d797e50f58c7796697ac234d25c3c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupTriggerConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbab60d05e49f007b41a34561e5ad027fa2849123d582e720289b5d83abb760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262a74ce6beab779f7983f3dc1d96fad1efe3752924ee41d70abb403cb7c04a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf98102cb65e07cb21c03d3e65bc20b426fb105c520a74ceeb2be62bb7c5835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a6928727660f4a7e0371311cd8cc2a75b84e3f84ee185b1af6d4e1c501580f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5271aa21718ccfcc2971b6c7f1795a4713490c88aa6b7018c4544fe2e83f12a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88785c15d20579cb2fe09b31a05b12c42a632fd6fee962a06f3a8a3bccdfe64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6abf3555d4c56ac150a2500ba017c2b8cfe31b92b26e62a30f14e0d7499822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470eb46955cc3c2ad9d141816f8a4be471fb208a1dcf6ad33e0384b8b0110473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad69b122d4704c3d5effae8b3082b7cc8a2d7927b01048ff242b532b420c936b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b1d24cd41f736ea056259a6d4ea10c00c8cfff45d3f9fb5e17d162bafe1417(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2949553382d198d381455ddf83f246dd66d09381063bfb74f5d4b487ff29cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545fdaa69e97b28488818fe155f237f57d8baf787a1d149ec7ae72cca6778b4d(
    *,
    alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a5363a04f2cb97fc03509c0b4002b2472e559e2db975859f08bf93776bc6e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd2169b7b0f1d3b4b0a9a9383801d93300348874636a640716368aebcd6ba17(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6604fd9f90baa92aa5643cc8da0f988a4efb5ed8e2cb3917cc59ded89b98645b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a35a82b561d5ce464323aa6b6e38a24607525811838264bcbed0224a7cc935(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5127f3e9452d997c685d170b1d181480782ffbd6fa30c01844dfb90417370af(
    value: typing.Optional[CodedeployDeploymentGroupAlarmConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97141cedb4e88483c3382fc5b947484d1b4598989927c9f985a888771774a86(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80110b765ccb2cc3e9d6da531926ad29edad9196ddd4318a09d0142215ea964a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316d5038a352654b06af578bcadad0d4228fae5c80be6cabb5f4d1d6770e0f6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae300ccfca33b4b7a8cc7e0a4745538271087e2607f12a4719a384c8d77674ab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb7e6f03e730153b321e17c00acc290d911e7e30346f33e54c52a96a497f38f(
    value: typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0a12ba2ef1c9f236210bc56b06da2236fa8ea55f34052d2f74ab1bdec75557(
    *,
    deployment_ready_option: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption, typing.Dict[builtins.str, typing.Any]]] = None,
    green_fleet_provisioning_option: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption, typing.Dict[builtins.str, typing.Any]]] = None,
    terminate_blue_instances_on_deployment_success: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576a09ac2454f14b39273752b6ae05569129c4dd31b8497e695266ca4026f454(
    *,
    action_on_timeout: typing.Optional[builtins.str] = None,
    wait_time_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f29c579c5063ea008c1f582000195f276338d5c0c1c0050baa33f2220ab4e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8dbe52a6034c2e59758ac00a45d48676ddd4adf282ecb27774cf0d6231c58f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54184e0d841efffa151a5ba99d8ca798c0771f7306438b463ef6f87fdf45093(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53833ff5161883d91bcdb33c529429eb4ceff13c439f374178647d201eb7c736(
    value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ffd1b2b0a504520596fdcb6fad9e343125f8845d7e4e0e2177b1d72226e255d(
    *,
    action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62eb68ddc4f1fd6c32b75dc8f645d59bdc5d6285d80e52fd51b2605667db0de8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5946f288f0c15ea50ec832adf719eda43da09e2cd03f9990eb0db9ecc3b48d1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a5706f7da6054ca745888c1d35d178499de469eec51ef8ca86f9a4ff4bba05(
    value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac659bf32843b02a1e86e1c27fcfb53661068d83b91ec699b6b5a08989799188(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17bd954718ab7d10e434ca761a2740ada279f1edda835227d6dd107455a3eb87(
    value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2876891a42fbf393c8ae91563c0f981fe768b6b567ce93623d2f171cc17d86b5(
    *,
    action: typing.Optional[builtins.str] = None,
    termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4c0c86aab9046d2e20255db6b6f74a304891fb5bc10339e7b2b6d1c001f436(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2d7f8dbc2a1c328cbe4c69063a9cb82b99fd01b114645d538ead57a04fbba6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627ea89e25a92943ee8784001dfa5c27a9d807330ccfb5329218bb7f7e037938(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef453839d1709de0211b5eac74bfd2119d25b0add181340e7744e20d46c09260(
    value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de3e200c635a3dfcf80cca88c25b78d43862898fb71889073cdc4c2e9704d0e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_name: builtins.str,
    deployment_group_name: builtins.str,
    service_role_arn: builtins.str,
    alarm_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAlarmConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_rollback_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAutoRollbackConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    autoscaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    blue_green_deployment_config: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_config_name: typing.Optional[builtins.str] = None,
    deployment_style: typing.Optional[typing.Union[CodedeployDeploymentGroupDeploymentStyle, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ec2_tag_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ecs_service: typing.Optional[typing.Union[CodedeployDeploymentGroupEcsService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer_info: typing.Optional[typing.Union[CodedeployDeploymentGroupLoadBalancerInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    on_premises_instance_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupOnPremisesInstanceTagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    outdated_instances_strategy: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_hook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trigger_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupTriggerConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92d6cbae4425129fcc51c95cd17076938295e1cb36390e327c62248c904c772(
    *,
    deployment_option: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e8f2083e6c8a1adc42c0114f2825b25fa81bd0c49ca9275ed8636652558fe3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f2b550e1ba429d16ffc20afebac0329c3c2e766eeca8a7ef1131a8e3c14bc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ead77b9f6b1f3f2f5321fa74da5edd21a3c13d58f820d16eeffb601c8d5445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c15f0f6989b2a7186dec12d563f5d5a412fca06790f202e641de6d44357e56e(
    value: typing.Optional[CodedeployDeploymentGroupDeploymentStyle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea50669ba8953d6806e97c2490d62f1e7bfe74fe2aff7b7827359f99b2af895(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1cb5cd7ef0fff9f5ff9e9fc03a5a508643f3d57eb86d4d9f40980641303fb60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac99b07af15061bfe10bb005213fcebde8b4c055cc130465fcf47d4dbfbfbd15(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279c3fa2a030ffa1b33c5dbd9593f22f453ad14d56ca7f1d6d974d842ef3eef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced71c0a7f7d3cfd0d6fdce71d8d387a0a6e3a9415490a4a7ba3a675cdf0fc4c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1acdb513d8f2485d33d3aef60c8921d00928a07e6f07d53734d19dd91ea41f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6da961776ab4381bd7c08a5842e43f279bf0c7cda9d7f2667ec6b7457f0c03(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03efdc40c3a4550707efa4ad72e493c29a16807b53eca43356663826dd69b770(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f6bb9b259b2ded7505231e09201df0d88957cdf9585b9950c8a8e6beec26f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3deb97243abee8ad36ee1d48ce8da1e34b29bccb0eacbdc0a70f32693d8b51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2506aac9bcd73156a3eb763d0043879e88f83413a3d2c4b369e717d14340da6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0eb58abd78006c7eb003c6e7cb29e0756da2af50b5530d5bacb1d1f27b6755(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce56a74894a2eb37ce97231faa0623da1becb9edc4406712eb8efa19b9dee7aa(
    *,
    ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSetEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2bf56b371cc45291b6122943fec8b5e78c8f37b5da68903dda03fe86bf2a35(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38d1435e33867dea4ee862670934ebf859b6d2c520aff9623f57ce54cb8ac60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857ea9e0e837fb3d3da9073ecfbdb39f65c69e6cf01c951c392e25d68858e086(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f8497a9933f43bcb62b97eaea80770c25ecba03d2af3ea8117e7b369493f49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c157802ad85d9e2f8d1382786248a62b353917b0ac818e538c2f57a1cea3c279(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2967b19d3590974f2702e9e1a52201a8557f3d428960a95f75d6b313898c772c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f88cccfdcd25dd0d04198e7eb7c6989e75b1e3944a5d1a5c7055affcb138fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9381c74e50ee2ffe3244b06873b5c8ca388a47f2d2a34ecbb712ebeab085de73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c5c2d55530b62a64156a1ea5ab7c6ccbf298d24492f2242fb032788a638232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7654d4f80b5a8c89db95e5df313aacc3cc1e1cc7ea2e1a9aa7dcc9b12d8b5cd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8af59bd90fa6774427f04ebd729e31ee4f9d1557a41ec11e4386fe46aa1e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5955ff303ec3e7d3fae844e43acd1eeec52628ef03ebbad978f531e7afa9ade(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSetEc2TagFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305e05969ada7bbebcbd0fe9916eca1ddc88ff3e192f5e21602ac86596929f5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10337ac56e3fd2cdfca2c5c9a3e0a1f974975e11d95ec1da50b6b4b158bf85d7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a73d3e78a3b005eeff559437ca53bb591513a21e1531b4cc306270ea2d90770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e734c5ff227d1cd2c6fd8566b5905104dc99ef6a1f9c54295b5e352fce860b2a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c5edfe9d80634985a34e3feff123fd7af627a1eead9b896644ff0e90ccc813(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe945e669a9e7d54afb11ae892dd546ac574f421d89a8f50919cef3166589a65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ebd28b56719a61b7d3871b323b417dbb19876096ff081810a055b8cc274adb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878e3bab64d1f74e97d7c004d049fa6cb26a4ae3212288de52915fe3bceb8e66(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSetEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93ed8d4cd544d8e12446a656b3cb68058c280439f5ae7779f0fad5aa9ac4673(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e61a659bace40c1230ea3501df0256b5a65cc730654dee8c8d0ce8bce14bb7b(
    *,
    cluster_name: builtins.str,
    service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7629bd668055bf1880b035dcbcefca17a35abab27351c5ed2b6cc45115d22ef1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57870823474b13659a8c40f56d589a0f64b6e395ef0a333ce77cb84dda75b3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24ded0d8d800fc784cfca202078766f495bda03b5dda26b6c84815355ae2069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e67627e6bcd77c9f141175bf8bdb3ebd233f8c374622fcd9456a4ae97dd37e(
    value: typing.Optional[CodedeployDeploymentGroupEcsService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c028bfe0c2152a6ce7615978ea620108fc8c05eba40fa0a71a9f770409d4ebdf(
    *,
    elb_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoElbInfo, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_group_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_group_pair_info: typing.Optional[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7365538b0b6c647bc19a718c3b6608ef1712707d089dc7d35b8789da1e235bf1(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e006c4760316f43ed62fd428b2c69490094435d35d5d3ed45a79550fbb722f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c81483f9c108fbce58e870551116491cd4ecdad44e863dea3796b48e864fbe6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f654c45633faab8521c4d90587262e6e7fd3939eec86667f4a80ea511dcb709b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb9971477de2dc5ffc23bd69975794f256ae44c7d6a3f8be0f32b6eaca42637(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289c0d204f2c537c05a38c89078758774992e869610bccfbfeb368635a980c11(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0e92f2a0aba148e37c3629a9ec135153d41060a50a67da1712944cf3769df5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1af728c45487f291d9ce90cf71ad32840054f8c73c9eae12038bfa84da0dd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232704bec9ab6a2f756d9acba63aa95db6d79251e1494b5a7d08af24a8ff3470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa33c667c7512e893f490f3b36ee5daaaa9ef3909f6194f8dfcec3a0f1869cef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoElbInfo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a173c1305e5215820a5f3cfc9bef8c9088ccffcbbd32055d5c251992d0efe4f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b7ace797f4c2bac89e14142ec37bf3360220e5fbdfb0a6424853d92e9b1061(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoElbInfo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116d55eb957e7b70bfc3af14f7ea5e0d878e05682b4e715f9e656d749e05c3d8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8057d0a7544d2aab33db25af7f51b54d5b4ec533affead0f6317ceab08667d1(
    value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975f45258e5e760f46652ee79811edd5720779ccf107bf9b083caf273c2e2f31(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58eece04d18f81be194174ea4a0b75e3be429a35f97406333ff2f8ce419c3de9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188821875386099a248d53b9593c22f7c6b53e4ba81ec6899bbbc7a4e47c1b40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c59eb7ae28a89298b89aa9edb85ba311cb4ab466737d0257fb4cbe342b13268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb259ae03176dd8c447e7dee6225ca66ee2a1431cdedbfc04cec3e8238bd756(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c710c0ab762a86842f0a95d0475d89b9aaa0958f1f1cddedcf8c36a4c555b427(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e3de471c122d127d63cfc78422b72cbac3e9301812a75077a43b6dd108dec5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc448ec46c37e32925c98ae098f3f7c452bf3f4b03575384cfaac0485f91393(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a60edb7d161a1c1c3dc630874bebaf907da7c54a3cd3271eff8eeef706b5872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a06a53eb52df4fc8605635de8390b92a846268f694b94da689ef096999d28bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937d5d120ead557f9e322fddcc42924838cb2368dc1d17f2454fecd19289750b(
    *,
    prod_traffic_route: typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute, typing.Dict[builtins.str, typing.Any]],
    target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
    test_traffic_route: typing.Optional[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c922589089bb99de235238f0048c0d346bb61c3d8f327c617acbf028ebb8ec1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ea17076fab90fa71f2493dbd3bffe655413d3c28449630cdb3cc177c36d94d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24661519253cd7118a75976c42e908112ba9535bb3ffae6bd15f51e8a7e84ba(
    value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5feaf6683c7cbb06bdebfdd0cd7df87754e1eab352f038e2cb8ada71ae0c30f(
    *,
    listener_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100576b1dd09387aa2fbd634396b2cfcf595b534c61737aa8b1d6328f3c6f8af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf566306901a518be7f9bb645636288a198be0f903b37073e72a6e441f1f8bb2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c85d421faa12623265661f7d5ab47af142d6556ee9501d51860533e58d73a8(
    value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a277d974598ac8ec1dfa6b2d0551c445c2a91a1a6dbe7415d6b7ddebde99c9(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887e204aca487b1fd493a2391903ce6a258d71b8d57e1b644ab716af2b0aec99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7937cb025d969bda3a9bfddb693f96f6b88e805c621d553be1c23fb9d12d651(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75506510341817292f85b19bb4f0382325e855bdcdc8dab504ddf12ef07da0c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924bbf498324bfeae9d9c8000d2456519d1ce541546b04816bd92e7c274f138e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c8f85e5ae51080d6689b71ae198990e23ec9b61124d0aa30f2873aa9a2bdf7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5605ceb9b80c0058600f7ba6219fe4d1e4e0af4c1ec97d1995eba105e5a6be3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7cadbf2ef6b0c71f499b6675e75dc5a07a18374920d4d07cd4b23e70e2d1000(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f55e1cf4d127a2c1ea7d110789b58bb17d6a4ed970f8b9bb91807285088f1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd86583df6e761e95cf61762cfdf45c64598ad6a40ecefc9bcce51d97d09a94d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd95086220e0c2cf5f4c9ae8a671f584239727452c4a92cd75888ab253d4232(
    *,
    listener_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c050687677be8c57ca68b3072d5729062a0412c58b49c380f1cb8e140e3c5c3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e9395dea77a2adba7fd7fdb8b2139c5887ce119371c3d1e381725589b8abd1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df99a5351b5010977c40b82944e21a470a5c6691ee4226b9d6fbdf5fe8ffac4(
    value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db32f16ee7ab3396af096432fb8b3166639b2a63c26be62687133727ff712d8(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da20b0aab92da8ebf5f3ec73385f4130c980f27bd9adb22846b1dcc158d0eba5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1794872ee6995db46fbf40a3c3f7e31472cc8534feb69c82f1f9b54dac8bbc71(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2dc90395d69dbfac3315840ab4b1d79a1f4d7392331fdaa51a96952006caa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bace816e3ef7ec2a0abcd57675a16a214664d86309c9f1918c8b081175974c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace389eec5a4c52b0e7cf728fe8ebf136a8f9d43c0f35ddad3b4f507e5823df6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84671b1bd90be390a9fb3e8d00cd56450c7ce6aca96a47a13757d515b5532ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupOnPremisesInstanceTagFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7df1403af7af7626e9fa39a7bd9d26ce5c7e351892c8978927a8241d0a42040(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b12a36eff8f5efcb644fb8bb0741429f661dfd2a001f61c40de478b0c79c02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade7a378f7a4a097ec2aa211f73c4d1d8266ac8a8c6677c69edcae60361cea41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db4d7c357bdd4d2680600ce48164e6945071e9992d78bd88f00211fc5fb7785(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b30becaf6534ec2316c9761917517ee8d98bcbb3d51f3ab18aa046049f9e0e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupOnPremisesInstanceTagFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad2f313e306c023057ce732d1a091eec5089dc32d83ed9e8ce9a400484538ff(
    *,
    trigger_events: typing.Sequence[builtins.str],
    trigger_name: builtins.str,
    trigger_target_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f906c476a7d13836c3329964d2b278947c829fd58000f3e350771340315786(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afc7c8858e657d9fb52df58de379827bbada92a46c605f695886e80bd4b4203(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11db513ce9b7021c589b3a70d00a81b978ce4ac6f568fc1efa876db11d7342fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fe06f7091b4bb9ec6c310d1b6407217bc21949204b54556b806c20f87424b1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9202ba45f27121964aec23c4d6c9cca891e44a10e70112191b5f877678e1fe4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3bf383e6b47466da225824b130939c8e482b6d15d0d1133048c143f1893555(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupTriggerConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab6e829ad66a96095a81fbb2d674d27afb208bbdde51b404aa74a5b12a967bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076dab3bffdc45397f763a684e2723cef6253f290886db58fe3e6839018c7af3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9546cf2bddd110f57d31b4a42445633d941bdc920a0d7faac375c80ee038bfe4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38040910444e606510873d62d2bcb39b2966dd4255aff12bb74b7aa153ef5a6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a9363e4003a22a9e0ef82ddeea144f09721144c66f0ed36bc02f4b910e879f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupTriggerConfiguration]],
) -> None:
    """Type checking stubs"""
    pass
