r'''
# `aws_ssm_maintenance_window_task`

Refer to the Terraform Registry for docs: [`aws_ssm_maintenance_window_task`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task).
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


class SsmMaintenanceWindowTask(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTask",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task aws_ssm_maintenance_window_task}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        task_arn: builtins.str,
        task_type: builtins.str,
        window_id: builtins.str,
        cutoff_behavior: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_concurrency: typing.Optional[builtins.str] = None,
        max_errors: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmMaintenanceWindowTaskTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        task_invocation_parameters: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task aws_ssm_maintenance_window_task} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param task_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#task_arn SsmMaintenanceWindowTask#task_arn}.
        :param task_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#task_type SsmMaintenanceWindowTask#task_type}.
        :param window_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#window_id SsmMaintenanceWindowTask#window_id}.
        :param cutoff_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cutoff_behavior SsmMaintenanceWindowTask#cutoff_behavior}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#description SsmMaintenanceWindowTask#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#id SsmMaintenanceWindowTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#max_concurrency SsmMaintenanceWindowTask#max_concurrency}.
        :param max_errors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#max_errors SsmMaintenanceWindowTask#max_errors}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#name SsmMaintenanceWindowTask#name}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#priority SsmMaintenanceWindowTask#priority}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#region SsmMaintenanceWindowTask#region}
        :param service_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#service_role_arn SsmMaintenanceWindowTask#service_role_arn}.
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#targets SsmMaintenanceWindowTask#targets}
        :param task_invocation_parameters: task_invocation_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#task_invocation_parameters SsmMaintenanceWindowTask#task_invocation_parameters}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb7ab99391380e3804313e28d6cb96993f9bf4931bb43ca90354fe9f017d496)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SsmMaintenanceWindowTaskConfig(
            task_arn=task_arn,
            task_type=task_type,
            window_id=window_id,
            cutoff_behavior=cutoff_behavior,
            description=description,
            id=id,
            max_concurrency=max_concurrency,
            max_errors=max_errors,
            name=name,
            priority=priority,
            region=region,
            service_role_arn=service_role_arn,
            targets=targets,
            task_invocation_parameters=task_invocation_parameters,
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
        '''Generates CDKTF code for importing a SsmMaintenanceWindowTask resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SsmMaintenanceWindowTask to import.
        :param import_from_id: The id of the existing SsmMaintenanceWindowTask that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SsmMaintenanceWindowTask to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d34dd7779e1348df2fc217c062c3c48ac7ae45a03b6605a46bb75b6423dbf9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTargets")
    def put_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmMaintenanceWindowTaskTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3343b3b19da39a9cc60e9f798e203ca33c329379c8e9f5e235bc533068b473f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargets", [value]))

    @jsii.member(jsii_name="putTaskInvocationParameters")
    def put_task_invocation_parameters(
        self,
        *,
        automation_parameters: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_parameters: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        run_command_parameters: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        step_functions_parameters: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param automation_parameters: automation_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#automation_parameters SsmMaintenanceWindowTask#automation_parameters}
        :param lambda_parameters: lambda_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#lambda_parameters SsmMaintenanceWindowTask#lambda_parameters}
        :param run_command_parameters: run_command_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#run_command_parameters SsmMaintenanceWindowTask#run_command_parameters}
        :param step_functions_parameters: step_functions_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#step_functions_parameters SsmMaintenanceWindowTask#step_functions_parameters}
        '''
        value = SsmMaintenanceWindowTaskTaskInvocationParameters(
            automation_parameters=automation_parameters,
            lambda_parameters=lambda_parameters,
            run_command_parameters=run_command_parameters,
            step_functions_parameters=step_functions_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putTaskInvocationParameters", [value]))

    @jsii.member(jsii_name="resetCutoffBehavior")
    def reset_cutoff_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCutoffBehavior", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxConcurrency")
    def reset_max_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrency", []))

    @jsii.member(jsii_name="resetMaxErrors")
    def reset_max_errors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxErrors", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetServiceRoleArn")
    def reset_service_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceRoleArn", []))

    @jsii.member(jsii_name="resetTargets")
    def reset_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargets", []))

    @jsii.member(jsii_name="resetTaskInvocationParameters")
    def reset_task_invocation_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskInvocationParameters", []))

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
    @jsii.member(jsii_name="targets")
    def targets(self) -> "SsmMaintenanceWindowTaskTargetsList":
        return typing.cast("SsmMaintenanceWindowTaskTargetsList", jsii.get(self, "targets"))

    @builtins.property
    @jsii.member(jsii_name="taskInvocationParameters")
    def task_invocation_parameters(
        self,
    ) -> "SsmMaintenanceWindowTaskTaskInvocationParametersOutputReference":
        return typing.cast("SsmMaintenanceWindowTaskTaskInvocationParametersOutputReference", jsii.get(self, "taskInvocationParameters"))

    @builtins.property
    @jsii.member(jsii_name="windowTaskId")
    def window_task_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "windowTaskId"))

    @builtins.property
    @jsii.member(jsii_name="cutoffBehaviorInput")
    def cutoff_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cutoffBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrencyInput")
    def max_concurrency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxErrorsInput")
    def max_errors_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxErrorsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArnInput")
    def service_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetsInput")
    def targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTargets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTargets"]]], jsii.get(self, "targetsInput"))

    @builtins.property
    @jsii.member(jsii_name="taskArnInput")
    def task_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskArnInput"))

    @builtins.property
    @jsii.member(jsii_name="taskInvocationParametersInput")
    def task_invocation_parameters_input(
        self,
    ) -> typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParameters"]:
        return typing.cast(typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParameters"], jsii.get(self, "taskInvocationParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="taskTypeInput")
    def task_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="windowIdInput")
    def window_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "windowIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cutoffBehavior")
    def cutoff_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cutoffBehavior"))

    @cutoff_behavior.setter
    def cutoff_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a54f7324b1d496603225c9af5fdaf5621ab17fb634891187ac1f7571211b2fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cutoffBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0fee139723dc46be994b33dc34787814166a8d6a407e0c735cc621b0c13843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8ae1983e19b4f1f6f278ec828a0ccacc6d114a906adb9d1a925725972ffe9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConcurrency")
    def max_concurrency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxConcurrency"))

    @max_concurrency.setter
    def max_concurrency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4f37e642fbb7b85314be84618d97db956477236c1060ac9edb29ea8d8aad10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxErrors")
    def max_errors(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxErrors"))

    @max_errors.setter
    def max_errors(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8969ee2efddedf1410637bf90a952c8c1b91ac0a89d197ed5b9768e1e1dc69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b40dac9a5a0b630880ccfce8b242640542928cadd69358b46e2683f2ce7438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa28ebc3a8389239df8937d8e94addc900f7b145035d114eab02ef8e8c36ef59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deeda67339543132cf7b5b439b3ab2ae093ffe96ee121b2d08a5a728461d46f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRoleArn"))

    @service_role_arn.setter
    def service_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6224f232ece0e24b340f5d761aa45c1256cfb571f6ef5032006d181b36c72bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskArn")
    def task_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskArn"))

    @task_arn.setter
    def task_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a7dcc2ff0e20fb42ad8c7cf3e5096878c6efd1c359275e5e4e240b7de188af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskType")
    def task_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskType"))

    @task_type.setter
    def task_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812c38005cfad35a2b6c513b8abc51af8986a6c05401a7fca9aa0c70ce12b767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowId")
    def window_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "windowId"))

    @window_id.setter
    def window_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa91cb12c946e9c8bd579972a11cb9df8bb7753c9118ee143f8709ff986f6713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "task_arn": "taskArn",
        "task_type": "taskType",
        "window_id": "windowId",
        "cutoff_behavior": "cutoffBehavior",
        "description": "description",
        "id": "id",
        "max_concurrency": "maxConcurrency",
        "max_errors": "maxErrors",
        "name": "name",
        "priority": "priority",
        "region": "region",
        "service_role_arn": "serviceRoleArn",
        "targets": "targets",
        "task_invocation_parameters": "taskInvocationParameters",
    },
)
class SsmMaintenanceWindowTaskConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        task_arn: builtins.str,
        task_type: builtins.str,
        window_id: builtins.str,
        cutoff_behavior: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_concurrency: typing.Optional[builtins.str] = None,
        max_errors: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmMaintenanceWindowTaskTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        task_invocation_parameters: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param task_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#task_arn SsmMaintenanceWindowTask#task_arn}.
        :param task_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#task_type SsmMaintenanceWindowTask#task_type}.
        :param window_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#window_id SsmMaintenanceWindowTask#window_id}.
        :param cutoff_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cutoff_behavior SsmMaintenanceWindowTask#cutoff_behavior}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#description SsmMaintenanceWindowTask#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#id SsmMaintenanceWindowTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#max_concurrency SsmMaintenanceWindowTask#max_concurrency}.
        :param max_errors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#max_errors SsmMaintenanceWindowTask#max_errors}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#name SsmMaintenanceWindowTask#name}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#priority SsmMaintenanceWindowTask#priority}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#region SsmMaintenanceWindowTask#region}
        :param service_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#service_role_arn SsmMaintenanceWindowTask#service_role_arn}.
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#targets SsmMaintenanceWindowTask#targets}
        :param task_invocation_parameters: task_invocation_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#task_invocation_parameters SsmMaintenanceWindowTask#task_invocation_parameters}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(task_invocation_parameters, dict):
            task_invocation_parameters = SsmMaintenanceWindowTaskTaskInvocationParameters(**task_invocation_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d284cd95ff0fe929fc8fc8eed6ece652b91781e5a92eb70d70d1d3af914fe992)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument task_arn", value=task_arn, expected_type=type_hints["task_arn"])
            check_type(argname="argument task_type", value=task_type, expected_type=type_hints["task_type"])
            check_type(argname="argument window_id", value=window_id, expected_type=type_hints["window_id"])
            check_type(argname="argument cutoff_behavior", value=cutoff_behavior, expected_type=type_hints["cutoff_behavior"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_concurrency", value=max_concurrency, expected_type=type_hints["max_concurrency"])
            check_type(argname="argument max_errors", value=max_errors, expected_type=type_hints["max_errors"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument task_invocation_parameters", value=task_invocation_parameters, expected_type=type_hints["task_invocation_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_arn": task_arn,
            "task_type": task_type,
            "window_id": window_id,
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
        if cutoff_behavior is not None:
            self._values["cutoff_behavior"] = cutoff_behavior
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if max_concurrency is not None:
            self._values["max_concurrency"] = max_concurrency
        if max_errors is not None:
            self._values["max_errors"] = max_errors
        if name is not None:
            self._values["name"] = name
        if priority is not None:
            self._values["priority"] = priority
        if region is not None:
            self._values["region"] = region
        if service_role_arn is not None:
            self._values["service_role_arn"] = service_role_arn
        if targets is not None:
            self._values["targets"] = targets
        if task_invocation_parameters is not None:
            self._values["task_invocation_parameters"] = task_invocation_parameters

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
    def task_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#task_arn SsmMaintenanceWindowTask#task_arn}.'''
        result = self._values.get("task_arn")
        assert result is not None, "Required property 'task_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#task_type SsmMaintenanceWindowTask#task_type}.'''
        result = self._values.get("task_type")
        assert result is not None, "Required property 'task_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def window_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#window_id SsmMaintenanceWindowTask#window_id}.'''
        result = self._values.get("window_id")
        assert result is not None, "Required property 'window_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cutoff_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cutoff_behavior SsmMaintenanceWindowTask#cutoff_behavior}.'''
        result = self._values.get("cutoff_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#description SsmMaintenanceWindowTask#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#id SsmMaintenanceWindowTask#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#max_concurrency SsmMaintenanceWindowTask#max_concurrency}.'''
        result = self._values.get("max_concurrency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_errors(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#max_errors SsmMaintenanceWindowTask#max_errors}.'''
        result = self._values.get("max_errors")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#name SsmMaintenanceWindowTask#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#priority SsmMaintenanceWindowTask#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#region SsmMaintenanceWindowTask#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#service_role_arn SsmMaintenanceWindowTask#service_role_arn}.'''
        result = self._values.get("service_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTargets"]]]:
        '''targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#targets SsmMaintenanceWindowTask#targets}
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTargets"]]], result)

    @builtins.property
    def task_invocation_parameters(
        self,
    ) -> typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParameters"]:
        '''task_invocation_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#task_invocation_parameters SsmMaintenanceWindowTask#task_invocation_parameters}
        '''
        result = self._values.get("task_invocation_parameters")
        return typing.cast(typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTargets",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class SsmMaintenanceWindowTaskTargets:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#key SsmMaintenanceWindowTask#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#values SsmMaintenanceWindowTask#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afdd6d6b4cc051073b3be8a3e0cd07912171984d9f4abc0e07c5e68f29d5d328)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#key SsmMaintenanceWindowTask#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#values SsmMaintenanceWindowTask#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmMaintenanceWindowTaskTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__167b885d6f956ef827742ae90082a9f985b701ea5c5914a066555978213596df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmMaintenanceWindowTaskTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b347d538c7d70a81f77b7cc6687d6753cdcdd1055b4b0ad5d3cf87eaee4d0a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmMaintenanceWindowTaskTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672237d6994ce80f06a6177c1b7d48d50d69115c81ce9234d12ecff6acad5749)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4d2ee32bed448db0c525b7832db61de358db1fb1c518c653fa5254bfe7bcba5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__965751a22a39c3142fd8630e446dd2a3d2ff974e1f2929468d8c59c2f59f998a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de84b55a77ce6ac9cac7f31310d04bb179104a3ef9e031926e2916de1ff63213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmMaintenanceWindowTaskTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__444fb1076bbb853416bbecfc3bb6dca658a9d1ba10363ce9b785743eca730e16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6a0ddef6dc643f7492c785f99a0645987b40a37c24731f64a5fa3197d74f11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d0eaedb93e1d6ce6340db986a18a7244ee2fad165fd556f76934cabf4f5868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1198e50d0ec195fcdf77dec4a6ab18da34d675e8e4c97a72fa8f54f631c3d690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParameters",
    jsii_struct_bases=[],
    name_mapping={
        "automation_parameters": "automationParameters",
        "lambda_parameters": "lambdaParameters",
        "run_command_parameters": "runCommandParameters",
        "step_functions_parameters": "stepFunctionsParameters",
    },
)
class SsmMaintenanceWindowTaskTaskInvocationParameters:
    def __init__(
        self,
        *,
        automation_parameters: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_parameters: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        run_command_parameters: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        step_functions_parameters: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param automation_parameters: automation_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#automation_parameters SsmMaintenanceWindowTask#automation_parameters}
        :param lambda_parameters: lambda_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#lambda_parameters SsmMaintenanceWindowTask#lambda_parameters}
        :param run_command_parameters: run_command_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#run_command_parameters SsmMaintenanceWindowTask#run_command_parameters}
        :param step_functions_parameters: step_functions_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#step_functions_parameters SsmMaintenanceWindowTask#step_functions_parameters}
        '''
        if isinstance(automation_parameters, dict):
            automation_parameters = SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters(**automation_parameters)
        if isinstance(lambda_parameters, dict):
            lambda_parameters = SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters(**lambda_parameters)
        if isinstance(run_command_parameters, dict):
            run_command_parameters = SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters(**run_command_parameters)
        if isinstance(step_functions_parameters, dict):
            step_functions_parameters = SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters(**step_functions_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__717af68e334e5f42b169a44bb23ffe2c82395044f8ab0008fea93b72b409470b)
            check_type(argname="argument automation_parameters", value=automation_parameters, expected_type=type_hints["automation_parameters"])
            check_type(argname="argument lambda_parameters", value=lambda_parameters, expected_type=type_hints["lambda_parameters"])
            check_type(argname="argument run_command_parameters", value=run_command_parameters, expected_type=type_hints["run_command_parameters"])
            check_type(argname="argument step_functions_parameters", value=step_functions_parameters, expected_type=type_hints["step_functions_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automation_parameters is not None:
            self._values["automation_parameters"] = automation_parameters
        if lambda_parameters is not None:
            self._values["lambda_parameters"] = lambda_parameters
        if run_command_parameters is not None:
            self._values["run_command_parameters"] = run_command_parameters
        if step_functions_parameters is not None:
            self._values["step_functions_parameters"] = step_functions_parameters

    @builtins.property
    def automation_parameters(
        self,
    ) -> typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters"]:
        '''automation_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#automation_parameters SsmMaintenanceWindowTask#automation_parameters}
        '''
        result = self._values.get("automation_parameters")
        return typing.cast(typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters"], result)

    @builtins.property
    def lambda_parameters(
        self,
    ) -> typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters"]:
        '''lambda_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#lambda_parameters SsmMaintenanceWindowTask#lambda_parameters}
        '''
        result = self._values.get("lambda_parameters")
        return typing.cast(typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters"], result)

    @builtins.property
    def run_command_parameters(
        self,
    ) -> typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters"]:
        '''run_command_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#run_command_parameters SsmMaintenanceWindowTask#run_command_parameters}
        '''
        result = self._values.get("run_command_parameters")
        return typing.cast(typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters"], result)

    @builtins.property
    def step_functions_parameters(
        self,
    ) -> typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters"]:
        '''step_functions_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#step_functions_parameters SsmMaintenanceWindowTask#step_functions_parameters}
        '''
        result = self._values.get("step_functions_parameters")
        return typing.cast(typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskTaskInvocationParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters",
    jsii_struct_bases=[],
    name_mapping={"document_version": "documentVersion", "parameter": "parameter"},
)
class SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters:
    def __init__(
        self,
        *,
        document_version: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param document_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_version SsmMaintenanceWindowTask#document_version}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#parameter SsmMaintenanceWindowTask#parameter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef6f18c7a05aef5f3aa7bcab403a274dbb7ef87228c298c7f12a56d71b7777d)
            check_type(argname="argument document_version", value=document_version, expected_type=type_hints["document_version"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if document_version is not None:
            self._values["document_version"] = document_version
        if parameter is not None:
            self._values["parameter"] = parameter

    @builtins.property
    def document_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_version SsmMaintenanceWindowTask#document_version}.'''
        result = self._values.get("document_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#parameter SsmMaintenanceWindowTask#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dd14f71b482e156f4717e39b81a92d42a265ce17475ae6ae3aa0f23c879eb81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e57de40300ccbed639d2f758feef77413b45a818ae5858a8207f807dc2d8ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameter", [value]))

    @jsii.member(jsii_name="resetDocumentVersion")
    def reset_document_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentVersion", []))

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(
        self,
    ) -> "SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameterList":
        return typing.cast("SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="documentVersionInput")
    def document_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="documentVersion")
    def document_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentVersion"))

    @document_version.setter
    def document_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c776cf5e3b5d4f0db364e30d6912894b11fbb5974190ca7b508025922105b8e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb4be55e7536b258db6b2a527f83ffcbf98a3a3d0e6e16eed970fbc27aa34d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#name SsmMaintenanceWindowTask#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#values SsmMaintenanceWindowTask#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73162cbee48f8a6b6246cbb8bbace6135e1e801c6cc514bdb27127088bcb6843)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#name SsmMaintenanceWindowTask#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#values SsmMaintenanceWindowTask#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6188b3cecc7f0167f717b93ddced62bb5ac924b489a6e56d88019bed510a12cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760e9feb5732774752554447c16f7cd1a6a7ff87baf54a4a4dd71af7de926685)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55eb5d24b47072225d02c89226b6e3fb7c36e40c450e34aab993ed0470141e11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62c8ced5363e0c096511e4e191efb9ed547517468591bebd47ea8064790b31a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__247010e1cd5e5d843ac3e14d04a11ed6617933ad1fced9d968685e678de293c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dacdbf163daee5d2784077e792b3291e14213793813629d207844ddfb1d72012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70f7ccec83e108ea8b50a72ef4d1a9f0ec36ab7a05dcec76e94f5506fd3e5363)
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
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a6fc62205ebc4e61589f124b8db1d81534ff54f95169dc4b25c6390fa68416c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827360fb3ccb204d4ef2480a4bc3df08dbb429c5e24374cdb15282250c68c101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e437affc10c5c40722e573da89d17bff196c7755bbbc783f1db6a8a246b29795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters",
    jsii_struct_bases=[],
    name_mapping={
        "client_context": "clientContext",
        "payload": "payload",
        "qualifier": "qualifier",
    },
)
class SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters:
    def __init__(
        self,
        *,
        client_context: typing.Optional[builtins.str] = None,
        payload: typing.Optional[builtins.str] = None,
        qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#client_context SsmMaintenanceWindowTask#client_context}.
        :param payload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#payload SsmMaintenanceWindowTask#payload}.
        :param qualifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#qualifier SsmMaintenanceWindowTask#qualifier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081ae97c11ad1dc020f87a4ecc8f51d322ea58f7839971e4dab2885cfe1ed761)
            check_type(argname="argument client_context", value=client_context, expected_type=type_hints["client_context"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_context is not None:
            self._values["client_context"] = client_context
        if payload is not None:
            self._values["payload"] = payload
        if qualifier is not None:
            self._values["qualifier"] = qualifier

    @builtins.property
    def client_context(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#client_context SsmMaintenanceWindowTask#client_context}.'''
        result = self._values.get("client_context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#payload SsmMaintenanceWindowTask#payload}.'''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qualifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#qualifier SsmMaintenanceWindowTask#qualifier}.'''
        result = self._values.get("qualifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__760ad880a4a90a14e636bba172ebc82c33e63eb04a9a8afbb40589f67b7f6cdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientContext")
    def reset_client_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientContext", []))

    @jsii.member(jsii_name="resetPayload")
    def reset_payload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayload", []))

    @jsii.member(jsii_name="resetQualifier")
    def reset_qualifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQualifier", []))

    @builtins.property
    @jsii.member(jsii_name="clientContextInput")
    def client_context_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientContextInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadInput")
    def payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadInput"))

    @builtins.property
    @jsii.member(jsii_name="qualifierInput")
    def qualifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qualifierInput"))

    @builtins.property
    @jsii.member(jsii_name="clientContext")
    def client_context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientContext"))

    @client_context.setter
    def client_context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9703b184615971b9d5ee31cb9c517f2939d02ee3397a4007a574922c1a1481da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientContext", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd0ae4255d93e5cd00c8232c89c90ba802d342c631e74424cef2206b734a0db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qualifier"))

    @qualifier.setter
    def qualifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e95cc2452185d9aa9fc6cedb1893fc55f062f07727d41049d58a42194ecf722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4374f6ef80ca565490157d6aced4abc76c8147ff8f6d0fac136c69f9bda97a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmMaintenanceWindowTaskTaskInvocationParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfa0ef91e0adb4c90aca6d007a18d57c2a54619c1a0979b98b2551914de1976f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutomationParameters")
    def put_automation_parameters(
        self,
        *,
        document_version: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param document_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_version SsmMaintenanceWindowTask#document_version}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#parameter SsmMaintenanceWindowTask#parameter}
        '''
        value = SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters(
            document_version=document_version, parameter=parameter
        )

        return typing.cast(None, jsii.invoke(self, "putAutomationParameters", [value]))

    @jsii.member(jsii_name="putLambdaParameters")
    def put_lambda_parameters(
        self,
        *,
        client_context: typing.Optional[builtins.str] = None,
        payload: typing.Optional[builtins.str] = None,
        qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#client_context SsmMaintenanceWindowTask#client_context}.
        :param payload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#payload SsmMaintenanceWindowTask#payload}.
        :param qualifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#qualifier SsmMaintenanceWindowTask#qualifier}.
        '''
        value = SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters(
            client_context=client_context, payload=payload, qualifier=qualifier
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaParameters", [value]))

    @jsii.member(jsii_name="putRunCommandParameters")
    def put_run_command_parameters(
        self,
        *,
        cloudwatch_config: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        comment: typing.Optional[builtins.str] = None,
        document_hash: typing.Optional[builtins.str] = None,
        document_hash_type: typing.Optional[builtins.str] = None,
        document_version: typing.Optional[builtins.str] = None,
        notification_config: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        output_s3_bucket: typing.Optional[builtins.str] = None,
        output_s3_key_prefix: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cloudwatch_config: cloudwatch_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cloudwatch_config SsmMaintenanceWindowTask#cloudwatch_config}
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#comment SsmMaintenanceWindowTask#comment}.
        :param document_hash: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_hash SsmMaintenanceWindowTask#document_hash}.
        :param document_hash_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_hash_type SsmMaintenanceWindowTask#document_hash_type}.
        :param document_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_version SsmMaintenanceWindowTask#document_version}.
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_config SsmMaintenanceWindowTask#notification_config}
        :param output_s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#output_s3_bucket SsmMaintenanceWindowTask#output_s3_bucket}.
        :param output_s3_key_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#output_s3_key_prefix SsmMaintenanceWindowTask#output_s3_key_prefix}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#parameter SsmMaintenanceWindowTask#parameter}
        :param service_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#service_role_arn SsmMaintenanceWindowTask#service_role_arn}.
        :param timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#timeout_seconds SsmMaintenanceWindowTask#timeout_seconds}.
        '''
        value = SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters(
            cloudwatch_config=cloudwatch_config,
            comment=comment,
            document_hash=document_hash,
            document_hash_type=document_hash_type,
            document_version=document_version,
            notification_config=notification_config,
            output_s3_bucket=output_s3_bucket,
            output_s3_key_prefix=output_s3_key_prefix,
            parameter=parameter,
            service_role_arn=service_role_arn,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putRunCommandParameters", [value]))

    @jsii.member(jsii_name="putStepFunctionsParameters")
    def put_step_functions_parameters(
        self,
        *,
        input: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#input SsmMaintenanceWindowTask#input}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#name SsmMaintenanceWindowTask#name}.
        '''
        value = SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters(
            input=input, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putStepFunctionsParameters", [value]))

    @jsii.member(jsii_name="resetAutomationParameters")
    def reset_automation_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomationParameters", []))

    @jsii.member(jsii_name="resetLambdaParameters")
    def reset_lambda_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaParameters", []))

    @jsii.member(jsii_name="resetRunCommandParameters")
    def reset_run_command_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunCommandParameters", []))

    @jsii.member(jsii_name="resetStepFunctionsParameters")
    def reset_step_functions_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStepFunctionsParameters", []))

    @builtins.property
    @jsii.member(jsii_name="automationParameters")
    def automation_parameters(
        self,
    ) -> SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersOutputReference:
        return typing.cast(SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersOutputReference, jsii.get(self, "automationParameters"))

    @builtins.property
    @jsii.member(jsii_name="lambdaParameters")
    def lambda_parameters(
        self,
    ) -> SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParametersOutputReference:
        return typing.cast(SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParametersOutputReference, jsii.get(self, "lambdaParameters"))

    @builtins.property
    @jsii.member(jsii_name="runCommandParameters")
    def run_command_parameters(
        self,
    ) -> "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersOutputReference":
        return typing.cast("SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersOutputReference", jsii.get(self, "runCommandParameters"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctionsParameters")
    def step_functions_parameters(
        self,
    ) -> "SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParametersOutputReference":
        return typing.cast("SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParametersOutputReference", jsii.get(self, "stepFunctionsParameters"))

    @builtins.property
    @jsii.member(jsii_name="automationParametersInput")
    def automation_parameters_input(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters], jsii.get(self, "automationParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaParametersInput")
    def lambda_parameters_input(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters], jsii.get(self, "lambdaParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="runCommandParametersInput")
    def run_command_parameters_input(
        self,
    ) -> typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters"]:
        return typing.cast(typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters"], jsii.get(self, "runCommandParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctionsParametersInput")
    def step_functions_parameters_input(
        self,
    ) -> typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters"]:
        return typing.cast(typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters"], jsii.get(self, "stepFunctionsParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParameters]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2de17ee05763ceb1882a5265f6147c69c40e3af376e439d658160fff7b7437f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_config": "cloudwatchConfig",
        "comment": "comment",
        "document_hash": "documentHash",
        "document_hash_type": "documentHashType",
        "document_version": "documentVersion",
        "notification_config": "notificationConfig",
        "output_s3_bucket": "outputS3Bucket",
        "output_s3_key_prefix": "outputS3KeyPrefix",
        "parameter": "parameter",
        "service_role_arn": "serviceRoleArn",
        "timeout_seconds": "timeoutSeconds",
    },
)
class SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters:
    def __init__(
        self,
        *,
        cloudwatch_config: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        comment: typing.Optional[builtins.str] = None,
        document_hash: typing.Optional[builtins.str] = None,
        document_hash_type: typing.Optional[builtins.str] = None,
        document_version: typing.Optional[builtins.str] = None,
        notification_config: typing.Optional[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        output_s3_bucket: typing.Optional[builtins.str] = None,
        output_s3_key_prefix: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cloudwatch_config: cloudwatch_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cloudwatch_config SsmMaintenanceWindowTask#cloudwatch_config}
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#comment SsmMaintenanceWindowTask#comment}.
        :param document_hash: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_hash SsmMaintenanceWindowTask#document_hash}.
        :param document_hash_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_hash_type SsmMaintenanceWindowTask#document_hash_type}.
        :param document_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_version SsmMaintenanceWindowTask#document_version}.
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_config SsmMaintenanceWindowTask#notification_config}
        :param output_s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#output_s3_bucket SsmMaintenanceWindowTask#output_s3_bucket}.
        :param output_s3_key_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#output_s3_key_prefix SsmMaintenanceWindowTask#output_s3_key_prefix}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#parameter SsmMaintenanceWindowTask#parameter}
        :param service_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#service_role_arn SsmMaintenanceWindowTask#service_role_arn}.
        :param timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#timeout_seconds SsmMaintenanceWindowTask#timeout_seconds}.
        '''
        if isinstance(cloudwatch_config, dict):
            cloudwatch_config = SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig(**cloudwatch_config)
        if isinstance(notification_config, dict):
            notification_config = SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig(**notification_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9be3c1d613e3858e6dec8b88768f387053a1918144e100ce451af607472657)
            check_type(argname="argument cloudwatch_config", value=cloudwatch_config, expected_type=type_hints["cloudwatch_config"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument document_hash", value=document_hash, expected_type=type_hints["document_hash"])
            check_type(argname="argument document_hash_type", value=document_hash_type, expected_type=type_hints["document_hash_type"])
            check_type(argname="argument document_version", value=document_version, expected_type=type_hints["document_version"])
            check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
            check_type(argname="argument output_s3_bucket", value=output_s3_bucket, expected_type=type_hints["output_s3_bucket"])
            check_type(argname="argument output_s3_key_prefix", value=output_s3_key_prefix, expected_type=type_hints["output_s3_key_prefix"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_config is not None:
            self._values["cloudwatch_config"] = cloudwatch_config
        if comment is not None:
            self._values["comment"] = comment
        if document_hash is not None:
            self._values["document_hash"] = document_hash
        if document_hash_type is not None:
            self._values["document_hash_type"] = document_hash_type
        if document_version is not None:
            self._values["document_version"] = document_version
        if notification_config is not None:
            self._values["notification_config"] = notification_config
        if output_s3_bucket is not None:
            self._values["output_s3_bucket"] = output_s3_bucket
        if output_s3_key_prefix is not None:
            self._values["output_s3_key_prefix"] = output_s3_key_prefix
        if parameter is not None:
            self._values["parameter"] = parameter
        if service_role_arn is not None:
            self._values["service_role_arn"] = service_role_arn
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def cloudwatch_config(
        self,
    ) -> typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig"]:
        '''cloudwatch_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cloudwatch_config SsmMaintenanceWindowTask#cloudwatch_config}
        '''
        result = self._values.get("cloudwatch_config")
        return typing.cast(typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig"], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#comment SsmMaintenanceWindowTask#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_hash(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_hash SsmMaintenanceWindowTask#document_hash}.'''
        result = self._values.get("document_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_hash_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_hash_type SsmMaintenanceWindowTask#document_hash_type}.'''
        result = self._values.get("document_hash_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#document_version SsmMaintenanceWindowTask#document_version}.'''
        result = self._values.get("document_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_config SsmMaintenanceWindowTask#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig"], result)

    @builtins.property
    def output_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#output_s3_bucket SsmMaintenanceWindowTask#output_s3_bucket}.'''
        result = self._values.get("output_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_s3_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#output_s3_key_prefix SsmMaintenanceWindowTask#output_s3_key_prefix}.'''
        result = self._values.get("output_s3_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#parameter SsmMaintenanceWindowTask#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter"]]], result)

    @builtins.property
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#service_role_arn SsmMaintenanceWindowTask#service_role_arn}.'''
        result = self._values.get("service_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#timeout_seconds SsmMaintenanceWindowTask#timeout_seconds}.'''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_log_group_name": "cloudwatchLogGroupName",
        "cloudwatch_output_enabled": "cloudwatchOutputEnabled",
    },
)
class SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig:
    def __init__(
        self,
        *,
        cloudwatch_log_group_name: typing.Optional[builtins.str] = None,
        cloudwatch_output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cloudwatch_log_group_name SsmMaintenanceWindowTask#cloudwatch_log_group_name}.
        :param cloudwatch_output_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cloudwatch_output_enabled SsmMaintenanceWindowTask#cloudwatch_output_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2adaa9bd6e2ae543ed02112cda7a1e0dba55b7e42a5a238b1d95f9cf2a2e987c)
            check_type(argname="argument cloudwatch_log_group_name", value=cloudwatch_log_group_name, expected_type=type_hints["cloudwatch_log_group_name"])
            check_type(argname="argument cloudwatch_output_enabled", value=cloudwatch_output_enabled, expected_type=type_hints["cloudwatch_output_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_log_group_name is not None:
            self._values["cloudwatch_log_group_name"] = cloudwatch_log_group_name
        if cloudwatch_output_enabled is not None:
            self._values["cloudwatch_output_enabled"] = cloudwatch_output_enabled

    @builtins.property
    def cloudwatch_log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cloudwatch_log_group_name SsmMaintenanceWindowTask#cloudwatch_log_group_name}.'''
        result = self._values.get("cloudwatch_log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatch_output_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cloudwatch_output_enabled SsmMaintenanceWindowTask#cloudwatch_output_enabled}.'''
        result = self._values.get("cloudwatch_output_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27a01533dd9b6cf75847c6beb9d80220f94dace3b73b3b8e730e7eb79bb356f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCloudwatchLogGroupName")
    def reset_cloudwatch_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogGroupName", []))

    @jsii.member(jsii_name="resetCloudwatchOutputEnabled")
    def reset_cloudwatch_output_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchOutputEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogGroupNameInput")
    def cloudwatch_log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchLogGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchOutputEnabledInput")
    def cloudwatch_output_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cloudwatchOutputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogGroupName")
    def cloudwatch_log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchLogGroupName"))

    @cloudwatch_log_group_name.setter
    def cloudwatch_log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a037fe3f446fab82c2199878bceab62cbf23a132a55b5b9b89b41731f296c423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchLogGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudwatchOutputEnabled")
    def cloudwatch_output_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cloudwatchOutputEnabled"))

    @cloudwatch_output_enabled.setter
    def cloudwatch_output_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83dfadd3843c8274d5cf42b1ec24764e2a66af6bcbed8cd0eae76b3f4537af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchOutputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8264b3b3fd0a8f5bce4954535279535283c95302ba5fafc60402a00849ff7e51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "notification_arn": "notificationArn",
        "notification_events": "notificationEvents",
        "notification_type": "notificationType",
    },
)
class SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig:
    def __init__(
        self,
        *,
        notification_arn: typing.Optional[builtins.str] = None,
        notification_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        notification_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param notification_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_arn SsmMaintenanceWindowTask#notification_arn}.
        :param notification_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_events SsmMaintenanceWindowTask#notification_events}.
        :param notification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_type SsmMaintenanceWindowTask#notification_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0403c2189942b834978130ce4599e5c26ad9c65422c4d6d0d67d95a0f3eb20)
            check_type(argname="argument notification_arn", value=notification_arn, expected_type=type_hints["notification_arn"])
            check_type(argname="argument notification_events", value=notification_events, expected_type=type_hints["notification_events"])
            check_type(argname="argument notification_type", value=notification_type, expected_type=type_hints["notification_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if notification_arn is not None:
            self._values["notification_arn"] = notification_arn
        if notification_events is not None:
            self._values["notification_events"] = notification_events
        if notification_type is not None:
            self._values["notification_type"] = notification_type

    @builtins.property
    def notification_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_arn SsmMaintenanceWindowTask#notification_arn}.'''
        result = self._values.get("notification_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_events SsmMaintenanceWindowTask#notification_events}.'''
        result = self._values.get("notification_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def notification_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_type SsmMaintenanceWindowTask#notification_type}.'''
        result = self._values.get("notification_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f79646759bafcf0753cd61159c0914e085aa996148f65bffcc681152f421661)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNotificationArn")
    def reset_notification_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationArn", []))

    @jsii.member(jsii_name="resetNotificationEvents")
    def reset_notification_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationEvents", []))

    @jsii.member(jsii_name="resetNotificationType")
    def reset_notification_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationType", []))

    @builtins.property
    @jsii.member(jsii_name="notificationArnInput")
    def notification_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationEventsInput")
    def notification_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationTypeInput")
    def notification_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationArn")
    def notification_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationArn"))

    @notification_arn.setter
    def notification_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ac0035912a6128c2bfcd7ad2101b3bdca80a389c5dc26d081193ea1c808dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationEvents")
    def notification_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notificationEvents"))

    @notification_events.setter
    def notification_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6435db504e7f7c89a9df626245105bedd931d6cac53ca9ed81bee3ef8c1296c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationType")
    def notification_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationType"))

    @notification_type.setter
    def notification_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fa3a2fa3997311b782516c5d7c5ed843a2b9eb8d55536cbe65ff310b636e6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f89c15811df4dd9f7fe4a9ef5e21c0526dae630c264b3af9d722a8e32ea171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f71006cc968705c5f6ae56b6a558ce3b19900b8e3ef909f7d39c0a18c99e8e9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchConfig")
    def put_cloudwatch_config(
        self,
        *,
        cloudwatch_log_group_name: typing.Optional[builtins.str] = None,
        cloudwatch_output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cloudwatch_log_group_name SsmMaintenanceWindowTask#cloudwatch_log_group_name}.
        :param cloudwatch_output_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#cloudwatch_output_enabled SsmMaintenanceWindowTask#cloudwatch_output_enabled}.
        '''
        value = SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig(
            cloudwatch_log_group_name=cloudwatch_log_group_name,
            cloudwatch_output_enabled=cloudwatch_output_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchConfig", [value]))

    @jsii.member(jsii_name="putNotificationConfig")
    def put_notification_config(
        self,
        *,
        notification_arn: typing.Optional[builtins.str] = None,
        notification_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        notification_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param notification_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_arn SsmMaintenanceWindowTask#notification_arn}.
        :param notification_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_events SsmMaintenanceWindowTask#notification_events}.
        :param notification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#notification_type SsmMaintenanceWindowTask#notification_type}.
        '''
        value = SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig(
            notification_arn=notification_arn,
            notification_events=notification_events,
            notification_type=notification_type,
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationConfig", [value]))

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1587020a72c7844cd5faff53b2196ffc1b24f8e73e84c55b9de2ea04dc4ac32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameter", [value]))

    @jsii.member(jsii_name="resetCloudwatchConfig")
    def reset_cloudwatch_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchConfig", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetDocumentHash")
    def reset_document_hash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentHash", []))

    @jsii.member(jsii_name="resetDocumentHashType")
    def reset_document_hash_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentHashType", []))

    @jsii.member(jsii_name="resetDocumentVersion")
    def reset_document_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentVersion", []))

    @jsii.member(jsii_name="resetNotificationConfig")
    def reset_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfig", []))

    @jsii.member(jsii_name="resetOutputS3Bucket")
    def reset_output_s3_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputS3Bucket", []))

    @jsii.member(jsii_name="resetOutputS3KeyPrefix")
    def reset_output_s3_key_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputS3KeyPrefix", []))

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @jsii.member(jsii_name="resetServiceRoleArn")
    def reset_service_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceRoleArn", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchConfig")
    def cloudwatch_config(
        self,
    ) -> SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfigOutputReference:
        return typing.cast(SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfigOutputReference, jsii.get(self, "cloudwatchConfig"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfigOutputReference:
        return typing.cast(SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfigOutputReference, jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(
        self,
    ) -> "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameterList":
        return typing.cast("SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchConfigInput")
    def cloudwatch_config_input(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig], jsii.get(self, "cloudwatchConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="documentHashInput")
    def document_hash_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentHashInput"))

    @builtins.property
    @jsii.member(jsii_name="documentHashTypeInput")
    def document_hash_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentHashTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="documentVersionInput")
    def document_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="outputS3BucketInput")
    def output_s3_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputS3BucketInput"))

    @builtins.property
    @jsii.member(jsii_name="outputS3KeyPrefixInput")
    def output_s3_key_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputS3KeyPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArnInput")
    def service_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__893a0a83ed2346eb7f015c42f7190c6fedb51bc2020ea557992530a527c54da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentHash")
    def document_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentHash"))

    @document_hash.setter
    def document_hash(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__461699f757c2355093575f94ec43ba0871704c8aa9a38a7fad7a33e07595dfca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentHash", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentHashType")
    def document_hash_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentHashType"))

    @document_hash_type.setter
    def document_hash_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fb7e7c0a52686b55bef457a135ef3dc83e5e2535cbedb3d26687adbd593aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentHashType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentVersion")
    def document_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentVersion"))

    @document_version.setter
    def document_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0547b8864787a35d3cf90e9aff6fa94d6ca9e58fbae1374c2417f16259303b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputS3Bucket")
    def output_s3_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputS3Bucket"))

    @output_s3_bucket.setter
    def output_s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ff236b5530bc911b8ad0ff8f66ac252d9c06ec8328bba7466730f7c2957154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputS3Bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputS3KeyPrefix")
    def output_s3_key_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputS3KeyPrefix"))

    @output_s3_key_prefix.setter
    def output_s3_key_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d032ec1aebe93ed5883c6274645a5c3a5989e11c7d0f488b034f1c7d7dfe5007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputS3KeyPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRoleArn"))

    @service_role_arn.setter
    def service_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad03aa9c267effe6bfb914b6292e8d1b6dd540d9905650311319469f3126b3c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96083f432b1ba013c01f833fb51d2485bbe9d6f3546bb97adcaedbdb0940639d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d692d99f25cfa8f1f61c530cbf2392641091704c443982016b789492b13921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#name SsmMaintenanceWindowTask#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#values SsmMaintenanceWindowTask#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e99f7138f6db277c86b4b36e921416bf30ce33e0f52a22523d8854c8ca36e60)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#name SsmMaintenanceWindowTask#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#values SsmMaintenanceWindowTask#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a066675b1647b54c3abe86fe65aaebc68b7cd6a2d1117971aeb09e642f69d3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560ba6f321241de9bea74e066f7d8f01a4047808e5eae4ff595375c7c4c59d26)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebca804babaeef60a1ac3a899489b89a9c0f4adf045633b379b5e8a36c0a4cf4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbc5041525fb71ba581b126ce4700833aa0edbfb2211498d998d1ae47943afd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__578ee5fec0a1372ff7bf0e2ba141298db99b45ddb7ccaed1e5a0cd29374d8509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d84898cdc6abc57d4582b77ffec5e8c95e0eaacbc88a89fe45ce8a38e62576e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aba0a4d3584a107e8d047dd66849b68c1d1d66794b7dd1a9490ac23e5d09015)
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
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09499346583a347eb42c72a237d794811f5e51e7e46304ac5e1ef4c6f9395326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71c3967dac37bf5712b116c9cc690c4639d4169f4405d85190ed155af5031ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce50009df5c23a22721760fe8bd5df0075bd92a3ec2ca888e7ded8ea1587903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters",
    jsii_struct_bases=[],
    name_mapping={"input": "input", "name": "name"},
)
class SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters:
    def __init__(
        self,
        *,
        input: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#input SsmMaintenanceWindowTask#input}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#name SsmMaintenanceWindowTask#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361a76427ba83624e62f19ffa4624034b172c888a4137d77775ea4c6b78db127)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input is not None:
            self._values["input"] = input
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def input(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#input SsmMaintenanceWindowTask#input}.'''
        result = self._values.get("input")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/ssm_maintenance_window_task#name SsmMaintenanceWindowTask#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.ssmMaintenanceWindowTask.SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7ebec7426e66190fa2215383c18b2cee24843233099e0200f4ff8311cb44a8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInput")
    def reset_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInput", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="inputInput")
    def input_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "input"))

    @input.setter
    def input(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f1421d2e247096972a2007b1495c05aac9101a5dbc105efffa41d152d2b261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "input", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ab1b37427716b65d98128693399ac03ca03754707ad801b69a2c98489709e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters]:
        return typing.cast(typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538f3494e65972b8642c2b8afcc713db32de5c0d13c666819bad92506bcb56c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SsmMaintenanceWindowTask",
    "SsmMaintenanceWindowTaskConfig",
    "SsmMaintenanceWindowTaskTargets",
    "SsmMaintenanceWindowTaskTargetsList",
    "SsmMaintenanceWindowTaskTargetsOutputReference",
    "SsmMaintenanceWindowTaskTaskInvocationParameters",
    "SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters",
    "SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersOutputReference",
    "SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter",
    "SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameterList",
    "SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameterOutputReference",
    "SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters",
    "SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParametersOutputReference",
    "SsmMaintenanceWindowTaskTaskInvocationParametersOutputReference",
    "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters",
    "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig",
    "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfigOutputReference",
    "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig",
    "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfigOutputReference",
    "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersOutputReference",
    "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter",
    "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameterList",
    "SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameterOutputReference",
    "SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters",
    "SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParametersOutputReference",
]

publication.publish()

def _typecheckingstub__dfb7ab99391380e3804313e28d6cb96993f9bf4931bb43ca90354fe9f017d496(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    task_arn: builtins.str,
    task_type: builtins.str,
    window_id: builtins.str,
    cutoff_behavior: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_concurrency: typing.Optional[builtins.str] = None,
    max_errors: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmMaintenanceWindowTaskTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    task_invocation_parameters: typing.Optional[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParameters, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__98d34dd7779e1348df2fc217c062c3c48ac7ae45a03b6605a46bb75b6423dbf9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3343b3b19da39a9cc60e9f798e203ca33c329379c8e9f5e235bc533068b473f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmMaintenanceWindowTaskTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a54f7324b1d496603225c9af5fdaf5621ab17fb634891187ac1f7571211b2fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0fee139723dc46be994b33dc34787814166a8d6a407e0c735cc621b0c13843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8ae1983e19b4f1f6f278ec828a0ccacc6d114a906adb9d1a925725972ffe9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4f37e642fbb7b85314be84618d97db956477236c1060ac9edb29ea8d8aad10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8969ee2efddedf1410637bf90a952c8c1b91ac0a89d197ed5b9768e1e1dc69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b40dac9a5a0b630880ccfce8b242640542928cadd69358b46e2683f2ce7438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa28ebc3a8389239df8937d8e94addc900f7b145035d114eab02ef8e8c36ef59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deeda67339543132cf7b5b439b3ab2ae093ffe96ee121b2d08a5a728461d46f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6224f232ece0e24b340f5d761aa45c1256cfb571f6ef5032006d181b36c72bd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7dcc2ff0e20fb42ad8c7cf3e5096878c6efd1c359275e5e4e240b7de188af9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812c38005cfad35a2b6c513b8abc51af8986a6c05401a7fca9aa0c70ce12b767(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa91cb12c946e9c8bd579972a11cb9df8bb7753c9118ee143f8709ff986f6713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d284cd95ff0fe929fc8fc8eed6ece652b91781e5a92eb70d70d1d3af914fe992(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    task_arn: builtins.str,
    task_type: builtins.str,
    window_id: builtins.str,
    cutoff_behavior: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_concurrency: typing.Optional[builtins.str] = None,
    max_errors: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmMaintenanceWindowTaskTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    task_invocation_parameters: typing.Optional[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdd6d6b4cc051073b3be8a3e0cd07912171984d9f4abc0e07c5e68f29d5d328(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167b885d6f956ef827742ae90082a9f985b701ea5c5914a066555978213596df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b347d538c7d70a81f77b7cc6687d6753cdcdd1055b4b0ad5d3cf87eaee4d0a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672237d6994ce80f06a6177c1b7d48d50d69115c81ce9234d12ecff6acad5749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d2ee32bed448db0c525b7832db61de358db1fb1c518c653fa5254bfe7bcba5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965751a22a39c3142fd8630e446dd2a3d2ff974e1f2929468d8c59c2f59f998a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de84b55a77ce6ac9cac7f31310d04bb179104a3ef9e031926e2916de1ff63213(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444fb1076bbb853416bbecfc3bb6dca658a9d1ba10363ce9b785743eca730e16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a0ddef6dc643f7492c785f99a0645987b40a37c24731f64a5fa3197d74f11b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d0eaedb93e1d6ce6340db986a18a7244ee2fad165fd556f76934cabf4f5868(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1198e50d0ec195fcdf77dec4a6ab18da34d675e8e4c97a72fa8f54f631c3d690(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTargets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717af68e334e5f42b169a44bb23ffe2c82395044f8ab0008fea93b72b409470b(
    *,
    automation_parameters: typing.Optional[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_parameters: typing.Optional[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    run_command_parameters: typing.Optional[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    step_functions_parameters: typing.Optional[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef6f18c7a05aef5f3aa7bcab403a274dbb7ef87228c298c7f12a56d71b7777d(
    *,
    document_version: typing.Optional[builtins.str] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd14f71b482e156f4717e39b81a92d42a265ce17475ae6ae3aa0f23c879eb81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e57de40300ccbed639d2f758feef77413b45a818ae5858a8207f807dc2d8ba9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c776cf5e3b5d4f0db364e30d6912894b11fbb5974190ca7b508025922105b8e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb4be55e7536b258db6b2a527f83ffcbf98a3a3d0e6e16eed970fbc27aa34d1(
    value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73162cbee48f8a6b6246cbb8bbace6135e1e801c6cc514bdb27127088bcb6843(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6188b3cecc7f0167f717b93ddced62bb5ac924b489a6e56d88019bed510a12cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760e9feb5732774752554447c16f7cd1a6a7ff87baf54a4a4dd71af7de926685(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55eb5d24b47072225d02c89226b6e3fb7c36e40c450e34aab993ed0470141e11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c8ced5363e0c096511e4e191efb9ed547517468591bebd47ea8064790b31a3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247010e1cd5e5d843ac3e14d04a11ed6617933ad1fced9d968685e678de293c2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacdbf163daee5d2784077e792b3291e14213793813629d207844ddfb1d72012(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f7ccec83e108ea8b50a72ef4d1a9f0ec36ab7a05dcec76e94f5506fd3e5363(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a6fc62205ebc4e61589f124b8db1d81534ff54f95169dc4b25c6390fa68416c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827360fb3ccb204d4ef2480a4bc3df08dbb429c5e24374cdb15282250c68c101(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e437affc10c5c40722e573da89d17bff196c7755bbbc783f1db6a8a246b29795(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTaskInvocationParametersAutomationParametersParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081ae97c11ad1dc020f87a4ecc8f51d322ea58f7839971e4dab2885cfe1ed761(
    *,
    client_context: typing.Optional[builtins.str] = None,
    payload: typing.Optional[builtins.str] = None,
    qualifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760ad880a4a90a14e636bba172ebc82c33e63eb04a9a8afbb40589f67b7f6cdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9703b184615971b9d5ee31cb9c517f2939d02ee3397a4007a574922c1a1481da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd0ae4255d93e5cd00c8232c89c90ba802d342c631e74424cef2206b734a0db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e95cc2452185d9aa9fc6cedb1893fc55f062f07727d41049d58a42194ecf722(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4374f6ef80ca565490157d6aced4abc76c8147ff8f6d0fac136c69f9bda97a(
    value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersLambdaParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa0ef91e0adb4c90aca6d007a18d57c2a54619c1a0979b98b2551914de1976f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2de17ee05763ceb1882a5265f6147c69c40e3af376e439d658160fff7b7437f(
    value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9be3c1d613e3858e6dec8b88768f387053a1918144e100ce451af607472657(
    *,
    cloudwatch_config: typing.Optional[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    comment: typing.Optional[builtins.str] = None,
    document_hash: typing.Optional[builtins.str] = None,
    document_hash_type: typing.Optional[builtins.str] = None,
    document_version: typing.Optional[builtins.str] = None,
    notification_config: typing.Optional[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    output_s3_bucket: typing.Optional[builtins.str] = None,
    output_s3_key_prefix: typing.Optional[builtins.str] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2adaa9bd6e2ae543ed02112cda7a1e0dba55b7e42a5a238b1d95f9cf2a2e987c(
    *,
    cloudwatch_log_group_name: typing.Optional[builtins.str] = None,
    cloudwatch_output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a01533dd9b6cf75847c6beb9d80220f94dace3b73b3b8e730e7eb79bb356f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a037fe3f446fab82c2199878bceab62cbf23a132a55b5b9b89b41731f296c423(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83dfadd3843c8274d5cf42b1ec24764e2a66af6bcbed8cd0eae76b3f4537af9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8264b3b3fd0a8f5bce4954535279535283c95302ba5fafc60402a00849ff7e51(
    value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersCloudwatchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0403c2189942b834978130ce4599e5c26ad9c65422c4d6d0d67d95a0f3eb20(
    *,
    notification_arn: typing.Optional[builtins.str] = None,
    notification_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    notification_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f79646759bafcf0753cd61159c0914e085aa996148f65bffcc681152f421661(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ac0035912a6128c2bfcd7ad2101b3bdca80a389c5dc26d081193ea1c808dee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6435db504e7f7c89a9df626245105bedd931d6cac53ca9ed81bee3ef8c1296c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fa3a2fa3997311b782516c5d7c5ed843a2b9eb8d55536cbe65ff310b636e6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f89c15811df4dd9f7fe4a9ef5e21c0526dae630c264b3af9d722a8e32ea171(
    value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71006cc968705c5f6ae56b6a558ce3b19900b8e3ef909f7d39c0a18c99e8e9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1587020a72c7844cd5faff53b2196ffc1b24f8e73e84c55b9de2ea04dc4ac32(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893a0a83ed2346eb7f015c42f7190c6fedb51bc2020ea557992530a527c54da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461699f757c2355093575f94ec43ba0871704c8aa9a38a7fad7a33e07595dfca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fb7e7c0a52686b55bef457a135ef3dc83e5e2535cbedb3d26687adbd593aee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0547b8864787a35d3cf90e9aff6fa94d6ca9e58fbae1374c2417f16259303b3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ff236b5530bc911b8ad0ff8f66ac252d9c06ec8328bba7466730f7c2957154(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d032ec1aebe93ed5883c6274645a5c3a5989e11c7d0f488b034f1c7d7dfe5007(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad03aa9c267effe6bfb914b6292e8d1b6dd540d9905650311319469f3126b3c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96083f432b1ba013c01f833fb51d2485bbe9d6f3546bb97adcaedbdb0940639d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d692d99f25cfa8f1f61c530cbf2392641091704c443982016b789492b13921(
    value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e99f7138f6db277c86b4b36e921416bf30ce33e0f52a22523d8854c8ca36e60(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a066675b1647b54c3abe86fe65aaebc68b7cd6a2d1117971aeb09e642f69d3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560ba6f321241de9bea74e066f7d8f01a4047808e5eae4ff595375c7c4c59d26(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebca804babaeef60a1ac3a899489b89a9c0f4adf045633b379b5e8a36c0a4cf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc5041525fb71ba581b126ce4700833aa0edbfb2211498d998d1ae47943afd3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578ee5fec0a1372ff7bf0e2ba141298db99b45ddb7ccaed1e5a0cd29374d8509(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d84898cdc6abc57d4582b77ffec5e8c95e0eaacbc88a89fe45ce8a38e62576e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aba0a4d3584a107e8d047dd66849b68c1d1d66794b7dd1a9490ac23e5d09015(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09499346583a347eb42c72a237d794811f5e51e7e46304ac5e1ef4c6f9395326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71c3967dac37bf5712b116c9cc690c4639d4169f4405d85190ed155af5031ae(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce50009df5c23a22721760fe8bd5df0075bd92a3ec2ca888e7ded8ea1587903(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SsmMaintenanceWindowTaskTaskInvocationParametersRunCommandParametersParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361a76427ba83624e62f19ffa4624034b172c888a4137d77775ea4c6b78db127(
    *,
    input: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ebec7426e66190fa2215383c18b2cee24843233099e0200f4ff8311cb44a8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f1421d2e247096972a2007b1495c05aac9101a5dbc105efffa41d152d2b261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ab1b37427716b65d98128693399ac03ca03754707ad801b69a2c98489709e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538f3494e65972b8642c2b8afcc713db32de5c0d13c666819bad92506bcb56c5(
    value: typing.Optional[SsmMaintenanceWindowTaskTaskInvocationParametersStepFunctionsParameters],
) -> None:
    """Type checking stubs"""
    pass
