r'''
# `aws_batch_compute_environment`

Refer to the Terraform Registry for docs: [`aws_batch_compute_environment`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment).
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


class BatchComputeEnvironment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment aws_batch_compute_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        type: builtins.str,
        compute_resources: typing.Optional[typing.Union["BatchComputeEnvironmentComputeResources", typing.Dict[builtins.str, typing.Any]]] = None,
        eks_configuration: typing.Optional[typing.Union["BatchComputeEnvironmentEksConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        update_policy: typing.Optional[typing.Union["BatchComputeEnvironmentUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment aws_batch_compute_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#type BatchComputeEnvironment#type}.
        :param compute_resources: compute_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#compute_resources BatchComputeEnvironment#compute_resources}
        :param eks_configuration: eks_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#eks_configuration BatchComputeEnvironment#eks_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#id BatchComputeEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#name BatchComputeEnvironment#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#name_prefix BatchComputeEnvironment#name_prefix}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#region BatchComputeEnvironment#region}
        :param service_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#service_role BatchComputeEnvironment#service_role}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#state BatchComputeEnvironment#state}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#tags BatchComputeEnvironment#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#tags_all BatchComputeEnvironment#tags_all}.
        :param update_policy: update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#update_policy BatchComputeEnvironment#update_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74bf1a04c3638482241fa2f57d0efe7b5bca6bb4105de3cfe196efbc825fd31f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BatchComputeEnvironmentConfig(
            type=type,
            compute_resources=compute_resources,
            eks_configuration=eks_configuration,
            id=id,
            name=name,
            name_prefix=name_prefix,
            region=region,
            service_role=service_role,
            state=state,
            tags=tags,
            tags_all=tags_all,
            update_policy=update_policy,
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
        '''Generates CDKTF code for importing a BatchComputeEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BatchComputeEnvironment to import.
        :param import_from_id: The id of the existing BatchComputeEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BatchComputeEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ca14fa3e1c6a03896819a2ed929503416355f073db2b77b0a8f00eba806341)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putComputeResources")
    def put_compute_resources(
        self,
        *,
        max_vcpus: jsii.Number,
        subnets: typing.Sequence[builtins.str],
        type: builtins.str,
        allocation_strategy: typing.Optional[builtins.str] = None,
        bid_percentage: typing.Optional[jsii.Number] = None,
        desired_vcpus: typing.Optional[jsii.Number] = None,
        ec2_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchComputeEnvironmentComputeResourcesEc2Configuration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ec2_key_pair: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        instance_role: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        launch_template: typing.Optional[typing.Union["BatchComputeEnvironmentComputeResourcesLaunchTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        min_vcpus: typing.Optional[jsii.Number] = None,
        placement_group: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        spot_iam_fleet_role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param max_vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#max_vcpus BatchComputeEnvironment#max_vcpus}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#subnets BatchComputeEnvironment#subnets}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#type BatchComputeEnvironment#type}.
        :param allocation_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#allocation_strategy BatchComputeEnvironment#allocation_strategy}.
        :param bid_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#bid_percentage BatchComputeEnvironment#bid_percentage}.
        :param desired_vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#desired_vcpus BatchComputeEnvironment#desired_vcpus}.
        :param ec2_configuration: ec2_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#ec2_configuration BatchComputeEnvironment#ec2_configuration}
        :param ec2_key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#ec2_key_pair BatchComputeEnvironment#ec2_key_pair}.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#image_id BatchComputeEnvironment#image_id}.
        :param instance_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#instance_role BatchComputeEnvironment#instance_role}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#instance_type BatchComputeEnvironment#instance_type}.
        :param launch_template: launch_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#launch_template BatchComputeEnvironment#launch_template}
        :param min_vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#min_vcpus BatchComputeEnvironment#min_vcpus}.
        :param placement_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#placement_group BatchComputeEnvironment#placement_group}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#security_group_ids BatchComputeEnvironment#security_group_ids}.
        :param spot_iam_fleet_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#spot_iam_fleet_role BatchComputeEnvironment#spot_iam_fleet_role}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#tags BatchComputeEnvironment#tags}.
        '''
        value = BatchComputeEnvironmentComputeResources(
            max_vcpus=max_vcpus,
            subnets=subnets,
            type=type,
            allocation_strategy=allocation_strategy,
            bid_percentage=bid_percentage,
            desired_vcpus=desired_vcpus,
            ec2_configuration=ec2_configuration,
            ec2_key_pair=ec2_key_pair,
            image_id=image_id,
            instance_role=instance_role,
            instance_type=instance_type,
            launch_template=launch_template,
            min_vcpus=min_vcpus,
            placement_group=placement_group,
            security_group_ids=security_group_ids,
            spot_iam_fleet_role=spot_iam_fleet_role,
            tags=tags,
        )

        return typing.cast(None, jsii.invoke(self, "putComputeResources", [value]))

    @jsii.member(jsii_name="putEksConfiguration")
    def put_eks_configuration(
        self,
        *,
        eks_cluster_arn: builtins.str,
        kubernetes_namespace: builtins.str,
    ) -> None:
        '''
        :param eks_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#eks_cluster_arn BatchComputeEnvironment#eks_cluster_arn}.
        :param kubernetes_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#kubernetes_namespace BatchComputeEnvironment#kubernetes_namespace}.
        '''
        value = BatchComputeEnvironmentEksConfiguration(
            eks_cluster_arn=eks_cluster_arn, kubernetes_namespace=kubernetes_namespace
        )

        return typing.cast(None, jsii.invoke(self, "putEksConfiguration", [value]))

    @jsii.member(jsii_name="putUpdatePolicy")
    def put_update_policy(
        self,
        *,
        job_execution_timeout_minutes: typing.Optional[jsii.Number] = None,
        terminate_jobs_on_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param job_execution_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#job_execution_timeout_minutes BatchComputeEnvironment#job_execution_timeout_minutes}.
        :param terminate_jobs_on_update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#terminate_jobs_on_update BatchComputeEnvironment#terminate_jobs_on_update}.
        '''
        value = BatchComputeEnvironmentUpdatePolicy(
            job_execution_timeout_minutes=job_execution_timeout_minutes,
            terminate_jobs_on_update=terminate_jobs_on_update,
        )

        return typing.cast(None, jsii.invoke(self, "putUpdatePolicy", [value]))

    @jsii.member(jsii_name="resetComputeResources")
    def reset_compute_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeResources", []))

    @jsii.member(jsii_name="resetEksConfiguration")
    def reset_eks_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEksConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetServiceRole")
    def reset_service_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceRole", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetUpdatePolicy")
    def reset_update_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatePolicy", []))

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
    @jsii.member(jsii_name="computeResources")
    def compute_resources(
        self,
    ) -> "BatchComputeEnvironmentComputeResourcesOutputReference":
        return typing.cast("BatchComputeEnvironmentComputeResourcesOutputReference", jsii.get(self, "computeResources"))

    @builtins.property
    @jsii.member(jsii_name="ecsClusterArn")
    def ecs_cluster_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ecsClusterArn"))

    @builtins.property
    @jsii.member(jsii_name="eksConfiguration")
    def eks_configuration(
        self,
    ) -> "BatchComputeEnvironmentEksConfigurationOutputReference":
        return typing.cast("BatchComputeEnvironmentEksConfigurationOutputReference", jsii.get(self, "eksConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusReason"))

    @builtins.property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> "BatchComputeEnvironmentUpdatePolicyOutputReference":
        return typing.cast("BatchComputeEnvironmentUpdatePolicyOutputReference", jsii.get(self, "updatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="computeResourcesInput")
    def compute_resources_input(
        self,
    ) -> typing.Optional["BatchComputeEnvironmentComputeResources"]:
        return typing.cast(typing.Optional["BatchComputeEnvironmentComputeResources"], jsii.get(self, "computeResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="eksConfigurationInput")
    def eks_configuration_input(
        self,
    ) -> typing.Optional["BatchComputeEnvironmentEksConfiguration"]:
        return typing.cast(typing.Optional["BatchComputeEnvironmentEksConfiguration"], jsii.get(self, "eksConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRoleInput")
    def service_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

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
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="updatePolicyInput")
    def update_policy_input(
        self,
    ) -> typing.Optional["BatchComputeEnvironmentUpdatePolicy"]:
        return typing.cast(typing.Optional["BatchComputeEnvironmentUpdatePolicy"], jsii.get(self, "updatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702dcb79028a3926a4b3fb43c0eaba6b31f2721061af72b01cb27c78f212168d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf39b4652ee87cedb9b012014ca854e78d13a4d66c61fe362c1e13b8945a590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223a49a662e1632d904c8f9e3aeca685e7618a931c761e221d7e1f05e5e50179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f593fc54ea2ea8aa03c77d111ac2cb88c0a3a06fea5ab8a1655fa94be9829a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRole"))

    @service_role.setter
    def service_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c56d0bcc8f66aab39f7b28236ed83b1a109a92f9f8365b87d0ea870ee09f3a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8454bb31f3970ada04d1c6e0971b4b78a168123fc79fe9c86c8cb994eb64a1bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed6bbfb741da18d3c3c1c38f2be0921858efe72cde69529581c1755ca02c7ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e885b1d0106d1646c51968653f33b233475e7b0bab2fdba8eaef6038ff227932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41fed8acd483085b559d8beb4721e583545d9fd53a07efe421810e86e300b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentComputeResources",
    jsii_struct_bases=[],
    name_mapping={
        "max_vcpus": "maxVcpus",
        "subnets": "subnets",
        "type": "type",
        "allocation_strategy": "allocationStrategy",
        "bid_percentage": "bidPercentage",
        "desired_vcpus": "desiredVcpus",
        "ec2_configuration": "ec2Configuration",
        "ec2_key_pair": "ec2KeyPair",
        "image_id": "imageId",
        "instance_role": "instanceRole",
        "instance_type": "instanceType",
        "launch_template": "launchTemplate",
        "min_vcpus": "minVcpus",
        "placement_group": "placementGroup",
        "security_group_ids": "securityGroupIds",
        "spot_iam_fleet_role": "spotIamFleetRole",
        "tags": "tags",
    },
)
class BatchComputeEnvironmentComputeResources:
    def __init__(
        self,
        *,
        max_vcpus: jsii.Number,
        subnets: typing.Sequence[builtins.str],
        type: builtins.str,
        allocation_strategy: typing.Optional[builtins.str] = None,
        bid_percentage: typing.Optional[jsii.Number] = None,
        desired_vcpus: typing.Optional[jsii.Number] = None,
        ec2_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchComputeEnvironmentComputeResourcesEc2Configuration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ec2_key_pair: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        instance_role: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        launch_template: typing.Optional[typing.Union["BatchComputeEnvironmentComputeResourcesLaunchTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        min_vcpus: typing.Optional[jsii.Number] = None,
        placement_group: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        spot_iam_fleet_role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param max_vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#max_vcpus BatchComputeEnvironment#max_vcpus}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#subnets BatchComputeEnvironment#subnets}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#type BatchComputeEnvironment#type}.
        :param allocation_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#allocation_strategy BatchComputeEnvironment#allocation_strategy}.
        :param bid_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#bid_percentage BatchComputeEnvironment#bid_percentage}.
        :param desired_vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#desired_vcpus BatchComputeEnvironment#desired_vcpus}.
        :param ec2_configuration: ec2_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#ec2_configuration BatchComputeEnvironment#ec2_configuration}
        :param ec2_key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#ec2_key_pair BatchComputeEnvironment#ec2_key_pair}.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#image_id BatchComputeEnvironment#image_id}.
        :param instance_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#instance_role BatchComputeEnvironment#instance_role}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#instance_type BatchComputeEnvironment#instance_type}.
        :param launch_template: launch_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#launch_template BatchComputeEnvironment#launch_template}
        :param min_vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#min_vcpus BatchComputeEnvironment#min_vcpus}.
        :param placement_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#placement_group BatchComputeEnvironment#placement_group}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#security_group_ids BatchComputeEnvironment#security_group_ids}.
        :param spot_iam_fleet_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#spot_iam_fleet_role BatchComputeEnvironment#spot_iam_fleet_role}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#tags BatchComputeEnvironment#tags}.
        '''
        if isinstance(launch_template, dict):
            launch_template = BatchComputeEnvironmentComputeResourcesLaunchTemplate(**launch_template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c44c6e267dd68ee8f622889d87e66fb165cb3801db357957cd256e5db0e5690)
            check_type(argname="argument max_vcpus", value=max_vcpus, expected_type=type_hints["max_vcpus"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
            check_type(argname="argument bid_percentage", value=bid_percentage, expected_type=type_hints["bid_percentage"])
            check_type(argname="argument desired_vcpus", value=desired_vcpus, expected_type=type_hints["desired_vcpus"])
            check_type(argname="argument ec2_configuration", value=ec2_configuration, expected_type=type_hints["ec2_configuration"])
            check_type(argname="argument ec2_key_pair", value=ec2_key_pair, expected_type=type_hints["ec2_key_pair"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument min_vcpus", value=min_vcpus, expected_type=type_hints["min_vcpus"])
            check_type(argname="argument placement_group", value=placement_group, expected_type=type_hints["placement_group"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument spot_iam_fleet_role", value=spot_iam_fleet_role, expected_type=type_hints["spot_iam_fleet_role"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_vcpus": max_vcpus,
            "subnets": subnets,
            "type": type,
        }
        if allocation_strategy is not None:
            self._values["allocation_strategy"] = allocation_strategy
        if bid_percentage is not None:
            self._values["bid_percentage"] = bid_percentage
        if desired_vcpus is not None:
            self._values["desired_vcpus"] = desired_vcpus
        if ec2_configuration is not None:
            self._values["ec2_configuration"] = ec2_configuration
        if ec2_key_pair is not None:
            self._values["ec2_key_pair"] = ec2_key_pair
        if image_id is not None:
            self._values["image_id"] = image_id
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if min_vcpus is not None:
            self._values["min_vcpus"] = min_vcpus
        if placement_group is not None:
            self._values["placement_group"] = placement_group
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if spot_iam_fleet_role is not None:
            self._values["spot_iam_fleet_role"] = spot_iam_fleet_role
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def max_vcpus(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#max_vcpus BatchComputeEnvironment#max_vcpus}.'''
        result = self._values.get("max_vcpus")
        assert result is not None, "Required property 'max_vcpus' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#subnets BatchComputeEnvironment#subnets}.'''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#type BatchComputeEnvironment#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allocation_strategy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#allocation_strategy BatchComputeEnvironment#allocation_strategy}.'''
        result = self._values.get("allocation_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bid_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#bid_percentage BatchComputeEnvironment#bid_percentage}.'''
        result = self._values.get("bid_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def desired_vcpus(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#desired_vcpus BatchComputeEnvironment#desired_vcpus}.'''
        result = self._values.get("desired_vcpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ec2_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchComputeEnvironmentComputeResourcesEc2Configuration"]]]:
        '''ec2_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#ec2_configuration BatchComputeEnvironment#ec2_configuration}
        '''
        result = self._values.get("ec2_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchComputeEnvironmentComputeResourcesEc2Configuration"]]], result)

    @builtins.property
    def ec2_key_pair(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#ec2_key_pair BatchComputeEnvironment#ec2_key_pair}.'''
        result = self._values.get("ec2_key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#image_id BatchComputeEnvironment#image_id}.'''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#instance_role BatchComputeEnvironment#instance_role}.'''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#instance_type BatchComputeEnvironment#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def launch_template(
        self,
    ) -> typing.Optional["BatchComputeEnvironmentComputeResourcesLaunchTemplate"]:
        '''launch_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#launch_template BatchComputeEnvironment#launch_template}
        '''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional["BatchComputeEnvironmentComputeResourcesLaunchTemplate"], result)

    @builtins.property
    def min_vcpus(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#min_vcpus BatchComputeEnvironment#min_vcpus}.'''
        result = self._values.get("min_vcpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#placement_group BatchComputeEnvironment#placement_group}.'''
        result = self._values.get("placement_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#security_group_ids BatchComputeEnvironment#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def spot_iam_fleet_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#spot_iam_fleet_role BatchComputeEnvironment#spot_iam_fleet_role}.'''
        result = self._values.get("spot_iam_fleet_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#tags BatchComputeEnvironment#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchComputeEnvironmentComputeResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentComputeResourcesEc2Configuration",
    jsii_struct_bases=[],
    name_mapping={
        "image_id_override": "imageIdOverride",
        "image_kubernetes_version": "imageKubernetesVersion",
        "image_type": "imageType",
    },
)
class BatchComputeEnvironmentComputeResourcesEc2Configuration:
    def __init__(
        self,
        *,
        image_id_override: typing.Optional[builtins.str] = None,
        image_kubernetes_version: typing.Optional[builtins.str] = None,
        image_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_id_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#image_id_override BatchComputeEnvironment#image_id_override}.
        :param image_kubernetes_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#image_kubernetes_version BatchComputeEnvironment#image_kubernetes_version}.
        :param image_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#image_type BatchComputeEnvironment#image_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff628c5756ea83601cef71f16a4b33457971a288c8d51e9c2e00107f3b2001ea)
            check_type(argname="argument image_id_override", value=image_id_override, expected_type=type_hints["image_id_override"])
            check_type(argname="argument image_kubernetes_version", value=image_kubernetes_version, expected_type=type_hints["image_kubernetes_version"])
            check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image_id_override is not None:
            self._values["image_id_override"] = image_id_override
        if image_kubernetes_version is not None:
            self._values["image_kubernetes_version"] = image_kubernetes_version
        if image_type is not None:
            self._values["image_type"] = image_type

    @builtins.property
    def image_id_override(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#image_id_override BatchComputeEnvironment#image_id_override}.'''
        result = self._values.get("image_id_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_kubernetes_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#image_kubernetes_version BatchComputeEnvironment#image_kubernetes_version}.'''
        result = self._values.get("image_kubernetes_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#image_type BatchComputeEnvironment#image_type}.'''
        result = self._values.get("image_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchComputeEnvironmentComputeResourcesEc2Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchComputeEnvironmentComputeResourcesEc2ConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentComputeResourcesEc2ConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b986c560564e31197f8a43639acc98a82f8098902617c8e17b0aed22f525143)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BatchComputeEnvironmentComputeResourcesEc2ConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f8dcaa664a8a44350d7762bfc8e2116e6acee3960b049e5a02c8d195941077)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchComputeEnvironmentComputeResourcesEc2ConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338d36e8b253e3e24bea1959e146d39cfc30aefa716ac5757ce7e7fada04b2bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0b3ce2a601d944e3fb5cca17d1c87f96700dec01d14aeec428477745929be09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3ffce9f39ba9f83c321fb003cbca698e6cf427ed67045fccc12bac9b977116c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchComputeEnvironmentComputeResourcesEc2Configuration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchComputeEnvironmentComputeResourcesEc2Configuration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchComputeEnvironmentComputeResourcesEc2Configuration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2d4015a653cb355670349e42f3b7955f54ec9fc658bccea16656014d176d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchComputeEnvironmentComputeResourcesEc2ConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentComputeResourcesEc2ConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48a380ee76ad2cedc6e7c3826a72210fdaf9dbaf6a80d20c75b8d2a54c9d1824)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetImageIdOverride")
    def reset_image_id_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageIdOverride", []))

    @jsii.member(jsii_name="resetImageKubernetesVersion")
    def reset_image_kubernetes_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageKubernetesVersion", []))

    @jsii.member(jsii_name="resetImageType")
    def reset_image_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageType", []))

    @builtins.property
    @jsii.member(jsii_name="imageIdOverrideInput")
    def image_id_override_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageIdOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="imageKubernetesVersionInput")
    def image_kubernetes_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageKubernetesVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTypeInput")
    def image_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="imageIdOverride")
    def image_id_override(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageIdOverride"))

    @image_id_override.setter
    def image_id_override(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f395d6287b77d4b5dd1302540bbe54249231e25c11f09af10ab88785135a970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageIdOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageKubernetesVersion")
    def image_kubernetes_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageKubernetesVersion"))

    @image_kubernetes_version.setter
    def image_kubernetes_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78094df28b43abb366007786493e3eb909bcea3fcc8fe7f1223db1dcc29adbf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageKubernetesVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageType")
    def image_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageType"))

    @image_type.setter
    def image_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e861d41029a735c958c67d2fae7375cad66a2856afbf887658f99bde4c59f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchComputeEnvironmentComputeResourcesEc2Configuration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchComputeEnvironmentComputeResourcesEc2Configuration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchComputeEnvironmentComputeResourcesEc2Configuration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd736fe4ba12dcc0ec74a6354a5988d2faac99e60967c0124c817689aa9e8b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentComputeResourcesLaunchTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "launch_template_id": "launchTemplateId",
        "launch_template_name": "launchTemplateName",
        "version": "version",
    },
)
class BatchComputeEnvironmentComputeResourcesLaunchTemplate:
    def __init__(
        self,
        *,
        launch_template_id: typing.Optional[builtins.str] = None,
        launch_template_name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param launch_template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#launch_template_id BatchComputeEnvironment#launch_template_id}.
        :param launch_template_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#launch_template_name BatchComputeEnvironment#launch_template_name}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#version BatchComputeEnvironment#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beeca115512b7ec394440b932ac30f26a7d6a2b95291de04460ecd265c9789b8)
            check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
            check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if launch_template_id is not None:
            self._values["launch_template_id"] = launch_template_id
        if launch_template_name is not None:
            self._values["launch_template_name"] = launch_template_name
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def launch_template_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#launch_template_id BatchComputeEnvironment#launch_template_id}.'''
        result = self._values.get("launch_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_template_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#launch_template_name BatchComputeEnvironment#launch_template_name}.'''
        result = self._values.get("launch_template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#version BatchComputeEnvironment#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchComputeEnvironmentComputeResourcesLaunchTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchComputeEnvironmentComputeResourcesLaunchTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentComputeResourcesLaunchTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54315ce30e7bd999699ac77b3de93815afa281147d157ea8e78e760b7b3563fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLaunchTemplateId")
    def reset_launch_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchTemplateId", []))

    @jsii.member(jsii_name="resetLaunchTemplateName")
    def reset_launch_template_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchTemplateName", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateIdInput")
    def launch_template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateNameInput")
    def launch_template_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateId")
    def launch_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchTemplateId"))

    @launch_template_id.setter
    def launch_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e116201523ee89dd11cbbdc454ddec2c2e98fd0c8b79cf862446baec1bfbd0e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchTemplateName")
    def launch_template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchTemplateName"))

    @launch_template_name.setter
    def launch_template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef7ab2487d423bf0f27caa4c54e06307b6a00d9e7557b7a77940f63e3b3e217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25bc9fafe30ce385f5d034434d83c83f1bfaa787d12a21fcb9205e5034d2bf15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BatchComputeEnvironmentComputeResourcesLaunchTemplate]:
        return typing.cast(typing.Optional[BatchComputeEnvironmentComputeResourcesLaunchTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchComputeEnvironmentComputeResourcesLaunchTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac45e9474b5612496f82a8df1a41132e3832c79328613c2922643811fd82848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchComputeEnvironmentComputeResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentComputeResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23e2dbab5f0d45ff267024300508c13f823c2819480f4b1b37eabf7467db43f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEc2Configuration")
    def put_ec2_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchComputeEnvironmentComputeResourcesEc2Configuration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d836fcc42f6ad85c3586e4132cce05939638691ca27ec98f341dbcd72dd53eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEc2Configuration", [value]))

    @jsii.member(jsii_name="putLaunchTemplate")
    def put_launch_template(
        self,
        *,
        launch_template_id: typing.Optional[builtins.str] = None,
        launch_template_name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param launch_template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#launch_template_id BatchComputeEnvironment#launch_template_id}.
        :param launch_template_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#launch_template_name BatchComputeEnvironment#launch_template_name}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#version BatchComputeEnvironment#version}.
        '''
        value = BatchComputeEnvironmentComputeResourcesLaunchTemplate(
            launch_template_id=launch_template_id,
            launch_template_name=launch_template_name,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putLaunchTemplate", [value]))

    @jsii.member(jsii_name="resetAllocationStrategy")
    def reset_allocation_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocationStrategy", []))

    @jsii.member(jsii_name="resetBidPercentage")
    def reset_bid_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBidPercentage", []))

    @jsii.member(jsii_name="resetDesiredVcpus")
    def reset_desired_vcpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredVcpus", []))

    @jsii.member(jsii_name="resetEc2Configuration")
    def reset_ec2_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2Configuration", []))

    @jsii.member(jsii_name="resetEc2KeyPair")
    def reset_ec2_key_pair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2KeyPair", []))

    @jsii.member(jsii_name="resetImageId")
    def reset_image_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageId", []))

    @jsii.member(jsii_name="resetInstanceRole")
    def reset_instance_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceRole", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLaunchTemplate")
    def reset_launch_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchTemplate", []))

    @jsii.member(jsii_name="resetMinVcpus")
    def reset_min_vcpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinVcpus", []))

    @jsii.member(jsii_name="resetPlacementGroup")
    def reset_placement_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementGroup", []))

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSpotIamFleetRole")
    def reset_spot_iam_fleet_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotIamFleetRole", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="ec2Configuration")
    def ec2_configuration(
        self,
    ) -> BatchComputeEnvironmentComputeResourcesEc2ConfigurationList:
        return typing.cast(BatchComputeEnvironmentComputeResourcesEc2ConfigurationList, jsii.get(self, "ec2Configuration"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(
        self,
    ) -> BatchComputeEnvironmentComputeResourcesLaunchTemplateOutputReference:
        return typing.cast(BatchComputeEnvironmentComputeResourcesLaunchTemplateOutputReference, jsii.get(self, "launchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="allocationStrategyInput")
    def allocation_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allocationStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="bidPercentageInput")
    def bid_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bidPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredVcpusInput")
    def desired_vcpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "desiredVcpusInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2ConfigurationInput")
    def ec2_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchComputeEnvironmentComputeResourcesEc2Configuration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchComputeEnvironmentComputeResourcesEc2Configuration]]], jsii.get(self, "ec2ConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2KeyPairInput")
    def ec2_key_pair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ec2KeyPairInput"))

    @builtins.property
    @jsii.member(jsii_name="imageIdInput")
    def image_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceRoleInput")
    def instance_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplateInput")
    def launch_template_input(
        self,
    ) -> typing.Optional[BatchComputeEnvironmentComputeResourcesLaunchTemplate]:
        return typing.cast(typing.Optional[BatchComputeEnvironmentComputeResourcesLaunchTemplate], jsii.get(self, "launchTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="maxVcpusInput")
    def max_vcpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxVcpusInput"))

    @builtins.property
    @jsii.member(jsii_name="minVcpusInput")
    def min_vcpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minVcpusInput"))

    @builtins.property
    @jsii.member(jsii_name="placementGroupInput")
    def placement_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "placementGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="spotIamFleetRoleInput")
    def spot_iam_fleet_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spotIamFleetRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="allocationStrategy")
    def allocation_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allocationStrategy"))

    @allocation_strategy.setter
    def allocation_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f25ebf1a6d2b093077b02806b47d46ffb35debdcaa20a1d13b89e2df4f1c284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocationStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bidPercentage")
    def bid_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bidPercentage"))

    @bid_percentage.setter
    def bid_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c9a45dd69eff22844721c6f1d02af1c023dc434a390e0531cfa1d824cbfc8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bidPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="desiredVcpus")
    def desired_vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "desiredVcpus"))

    @desired_vcpus.setter
    def desired_vcpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f5be95e725074d8a95bb94a2856894a2c8f86672fc4af38ac4e3b578c58762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredVcpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ec2KeyPair")
    def ec2_key_pair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ec2KeyPair"))

    @ec2_key_pair.setter
    def ec2_key_pair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d5467728bf9c7013448c7725b68492fb7f133a40dfc136782a8a32f1ae4a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2KeyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageId"))

    @image_id.setter
    def image_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59215388a496dc2f4431f0834ddb1cf70e18fe3608dd386495ed68df4dde4859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceRole")
    def instance_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceRole"))

    @instance_role.setter
    def instance_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efaa49b92ea9ab7181d9f62abcd2ec787fa30982fb1bc0b93171fb92c2571416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed47fa9e0d99cfcd88644e7a314d410a1065f4b5af0ee2fcdf369d445fe9c2d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxVcpus")
    def max_vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxVcpus"))

    @max_vcpus.setter
    def max_vcpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33600bf0773b30d7c89eccf728bc76c4a5fd900fdb8d5e145ce56cb69ef4e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxVcpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minVcpus")
    def min_vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minVcpus"))

    @min_vcpus.setter
    def min_vcpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e27abd9e158f83de4d5c0387dba4be643637c19de25f5c4fd67e7b1dc8c4221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minVcpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="placementGroup")
    def placement_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "placementGroup"))

    @placement_group.setter
    def placement_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ef12fe6cccdd0e2910a06ed8b76d4584a5f197570abecff0da9315bdfa276d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "placementGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de52b9d27bee8c289fae4495d1979c1bf6cc0958539bf0f6714429548aa29ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spotIamFleetRole")
    def spot_iam_fleet_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spotIamFleetRole"))

    @spot_iam_fleet_role.setter
    def spot_iam_fleet_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0bbdc82ccb641f956b854c2db8a8f54440caa11d0ae3ee4789675cb3556444a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotIamFleetRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a38368c13260039c09387fbb35d9e11a537990942580ddb9177a498f4fbe480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383734ebe8809d7eea878f93f25aa8dc0f57adf117461fea1a7f4b7e506be698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8449c9765de33a76a1fe1ff96868c5a7df069a13d5dc807afa7ad4def3897815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BatchComputeEnvironmentComputeResources]:
        return typing.cast(typing.Optional[BatchComputeEnvironmentComputeResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchComputeEnvironmentComputeResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55cb0a066d8b59bbc1d1ff095253563eb641b4fee2df52fb203ace9eaf538a67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "type": "type",
        "compute_resources": "computeResources",
        "eks_configuration": "eksConfiguration",
        "id": "id",
        "name": "name",
        "name_prefix": "namePrefix",
        "region": "region",
        "service_role": "serviceRole",
        "state": "state",
        "tags": "tags",
        "tags_all": "tagsAll",
        "update_policy": "updatePolicy",
    },
)
class BatchComputeEnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        type: builtins.str,
        compute_resources: typing.Optional[typing.Union[BatchComputeEnvironmentComputeResources, typing.Dict[builtins.str, typing.Any]]] = None,
        eks_configuration: typing.Optional[typing.Union["BatchComputeEnvironmentEksConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        update_policy: typing.Optional[typing.Union["BatchComputeEnvironmentUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#type BatchComputeEnvironment#type}.
        :param compute_resources: compute_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#compute_resources BatchComputeEnvironment#compute_resources}
        :param eks_configuration: eks_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#eks_configuration BatchComputeEnvironment#eks_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#id BatchComputeEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#name BatchComputeEnvironment#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#name_prefix BatchComputeEnvironment#name_prefix}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#region BatchComputeEnvironment#region}
        :param service_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#service_role BatchComputeEnvironment#service_role}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#state BatchComputeEnvironment#state}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#tags BatchComputeEnvironment#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#tags_all BatchComputeEnvironment#tags_all}.
        :param update_policy: update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#update_policy BatchComputeEnvironment#update_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(compute_resources, dict):
            compute_resources = BatchComputeEnvironmentComputeResources(**compute_resources)
        if isinstance(eks_configuration, dict):
            eks_configuration = BatchComputeEnvironmentEksConfiguration(**eks_configuration)
        if isinstance(update_policy, dict):
            update_policy = BatchComputeEnvironmentUpdatePolicy(**update_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd9e690934c6835098539167540848ed2525030cc3098c829a97b7c221f20e0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument compute_resources", value=compute_resources, expected_type=type_hints["compute_resources"])
            check_type(argname="argument eks_configuration", value=eks_configuration, expected_type=type_hints["eks_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument update_policy", value=update_policy, expected_type=type_hints["update_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if compute_resources is not None:
            self._values["compute_resources"] = compute_resources
        if eks_configuration is not None:
            self._values["eks_configuration"] = eks_configuration
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if region is not None:
            self._values["region"] = region
        if service_role is not None:
            self._values["service_role"] = service_role
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if update_policy is not None:
            self._values["update_policy"] = update_policy

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
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#type BatchComputeEnvironment#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_resources(
        self,
    ) -> typing.Optional[BatchComputeEnvironmentComputeResources]:
        '''compute_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#compute_resources BatchComputeEnvironment#compute_resources}
        '''
        result = self._values.get("compute_resources")
        return typing.cast(typing.Optional[BatchComputeEnvironmentComputeResources], result)

    @builtins.property
    def eks_configuration(
        self,
    ) -> typing.Optional["BatchComputeEnvironmentEksConfiguration"]:
        '''eks_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#eks_configuration BatchComputeEnvironment#eks_configuration}
        '''
        result = self._values.get("eks_configuration")
        return typing.cast(typing.Optional["BatchComputeEnvironmentEksConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#id BatchComputeEnvironment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#name BatchComputeEnvironment#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#name_prefix BatchComputeEnvironment#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#region BatchComputeEnvironment#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#service_role BatchComputeEnvironment#service_role}.'''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#state BatchComputeEnvironment#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#tags BatchComputeEnvironment#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#tags_all BatchComputeEnvironment#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def update_policy(self) -> typing.Optional["BatchComputeEnvironmentUpdatePolicy"]:
        '''update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#update_policy BatchComputeEnvironment#update_policy}
        '''
        result = self._values.get("update_policy")
        return typing.cast(typing.Optional["BatchComputeEnvironmentUpdatePolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchComputeEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentEksConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "eks_cluster_arn": "eksClusterArn",
        "kubernetes_namespace": "kubernetesNamespace",
    },
)
class BatchComputeEnvironmentEksConfiguration:
    def __init__(
        self,
        *,
        eks_cluster_arn: builtins.str,
        kubernetes_namespace: builtins.str,
    ) -> None:
        '''
        :param eks_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#eks_cluster_arn BatchComputeEnvironment#eks_cluster_arn}.
        :param kubernetes_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#kubernetes_namespace BatchComputeEnvironment#kubernetes_namespace}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd56642b0ca0ffd2704d2ec2b7ba2fe14b43b408359619d51491d6de457524ea)
            check_type(argname="argument eks_cluster_arn", value=eks_cluster_arn, expected_type=type_hints["eks_cluster_arn"])
            check_type(argname="argument kubernetes_namespace", value=kubernetes_namespace, expected_type=type_hints["kubernetes_namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "eks_cluster_arn": eks_cluster_arn,
            "kubernetes_namespace": kubernetes_namespace,
        }

    @builtins.property
    def eks_cluster_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#eks_cluster_arn BatchComputeEnvironment#eks_cluster_arn}.'''
        result = self._values.get("eks_cluster_arn")
        assert result is not None, "Required property 'eks_cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kubernetes_namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#kubernetes_namespace BatchComputeEnvironment#kubernetes_namespace}.'''
        result = self._values.get("kubernetes_namespace")
        assert result is not None, "Required property 'kubernetes_namespace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchComputeEnvironmentEksConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchComputeEnvironmentEksConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentEksConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bee93b92f8e582f34590c4f1c05de0416f29a3a33f669060af81499926aa2a32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eksClusterArnInput")
    def eks_cluster_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eksClusterArnInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesNamespaceInput")
    def kubernetes_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="eksClusterArn")
    def eks_cluster_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eksClusterArn"))

    @eks_cluster_arn.setter
    def eks_cluster_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a238635cdd1d1bea1144f408ced7946c2a2e4ffef46590ff8db953ca79aac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eksClusterArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesNamespace")
    def kubernetes_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesNamespace"))

    @kubernetes_namespace.setter
    def kubernetes_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198906c47255e654898b97f7cbb1e88810a3a5dda75146fb621bc58ec0be62f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BatchComputeEnvironmentEksConfiguration]:
        return typing.cast(typing.Optional[BatchComputeEnvironmentEksConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchComputeEnvironmentEksConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97343d9c643671c972089a154ef97427360104a90588ab96f15b40f942a083b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "job_execution_timeout_minutes": "jobExecutionTimeoutMinutes",
        "terminate_jobs_on_update": "terminateJobsOnUpdate",
    },
)
class BatchComputeEnvironmentUpdatePolicy:
    def __init__(
        self,
        *,
        job_execution_timeout_minutes: typing.Optional[jsii.Number] = None,
        terminate_jobs_on_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param job_execution_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#job_execution_timeout_minutes BatchComputeEnvironment#job_execution_timeout_minutes}.
        :param terminate_jobs_on_update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#terminate_jobs_on_update BatchComputeEnvironment#terminate_jobs_on_update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c325848c3de7509b5a9b611ab672981e60a7ecdd9a34852339b61e6f1defc2bd)
            check_type(argname="argument job_execution_timeout_minutes", value=job_execution_timeout_minutes, expected_type=type_hints["job_execution_timeout_minutes"])
            check_type(argname="argument terminate_jobs_on_update", value=terminate_jobs_on_update, expected_type=type_hints["terminate_jobs_on_update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_execution_timeout_minutes is not None:
            self._values["job_execution_timeout_minutes"] = job_execution_timeout_minutes
        if terminate_jobs_on_update is not None:
            self._values["terminate_jobs_on_update"] = terminate_jobs_on_update

    @builtins.property
    def job_execution_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#job_execution_timeout_minutes BatchComputeEnvironment#job_execution_timeout_minutes}.'''
        result = self._values.get("job_execution_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def terminate_jobs_on_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/batch_compute_environment#terminate_jobs_on_update BatchComputeEnvironment#terminate_jobs_on_update}.'''
        result = self._values.get("terminate_jobs_on_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchComputeEnvironmentUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchComputeEnvironmentUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.batchComputeEnvironment.BatchComputeEnvironmentUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec075ccee38bec0bc6719e92aa2b51f73e7d94f9d1cbfc87e43f009002fb172f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetJobExecutionTimeoutMinutes")
    def reset_job_execution_timeout_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobExecutionTimeoutMinutes", []))

    @jsii.member(jsii_name="resetTerminateJobsOnUpdate")
    def reset_terminate_jobs_on_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminateJobsOnUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="jobExecutionTimeoutMinutesInput")
    def job_execution_timeout_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jobExecutionTimeoutMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="terminateJobsOnUpdateInput")
    def terminate_jobs_on_update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "terminateJobsOnUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="jobExecutionTimeoutMinutes")
    def job_execution_timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jobExecutionTimeoutMinutes"))

    @job_execution_timeout_minutes.setter
    def job_execution_timeout_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b875f4b005f178f93c9ddee93aec1b2eb1ce4133cbcb7bd8062b8bf09bcb58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobExecutionTimeoutMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminateJobsOnUpdate")
    def terminate_jobs_on_update(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "terminateJobsOnUpdate"))

    @terminate_jobs_on_update.setter
    def terminate_jobs_on_update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f9461f61781e99c4834cfb2205f8a8d63ae5d3682bb0b4b85dbb589cf89379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminateJobsOnUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchComputeEnvironmentUpdatePolicy]:
        return typing.cast(typing.Optional[BatchComputeEnvironmentUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchComputeEnvironmentUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3ab7f539f7122aae5b390408a5f29e83ecc33b655e62f55441d4fac5e55d2a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BatchComputeEnvironment",
    "BatchComputeEnvironmentComputeResources",
    "BatchComputeEnvironmentComputeResourcesEc2Configuration",
    "BatchComputeEnvironmentComputeResourcesEc2ConfigurationList",
    "BatchComputeEnvironmentComputeResourcesEc2ConfigurationOutputReference",
    "BatchComputeEnvironmentComputeResourcesLaunchTemplate",
    "BatchComputeEnvironmentComputeResourcesLaunchTemplateOutputReference",
    "BatchComputeEnvironmentComputeResourcesOutputReference",
    "BatchComputeEnvironmentConfig",
    "BatchComputeEnvironmentEksConfiguration",
    "BatchComputeEnvironmentEksConfigurationOutputReference",
    "BatchComputeEnvironmentUpdatePolicy",
    "BatchComputeEnvironmentUpdatePolicyOutputReference",
]

publication.publish()

def _typecheckingstub__74bf1a04c3638482241fa2f57d0efe7b5bca6bb4105de3cfe196efbc825fd31f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    type: builtins.str,
    compute_resources: typing.Optional[typing.Union[BatchComputeEnvironmentComputeResources, typing.Dict[builtins.str, typing.Any]]] = None,
    eks_configuration: typing.Optional[typing.Union[BatchComputeEnvironmentEksConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    update_policy: typing.Optional[typing.Union[BatchComputeEnvironmentUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__98ca14fa3e1c6a03896819a2ed929503416355f073db2b77b0a8f00eba806341(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702dcb79028a3926a4b3fb43c0eaba6b31f2721061af72b01cb27c78f212168d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf39b4652ee87cedb9b012014ca854e78d13a4d66c61fe362c1e13b8945a590(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223a49a662e1632d904c8f9e3aeca685e7618a931c761e221d7e1f05e5e50179(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f593fc54ea2ea8aa03c77d111ac2cb88c0a3a06fea5ab8a1655fa94be9829a71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c56d0bcc8f66aab39f7b28236ed83b1a109a92f9f8365b87d0ea870ee09f3a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8454bb31f3970ada04d1c6e0971b4b78a168123fc79fe9c86c8cb994eb64a1bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed6bbfb741da18d3c3c1c38f2be0921858efe72cde69529581c1755ca02c7ba(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e885b1d0106d1646c51968653f33b233475e7b0bab2fdba8eaef6038ff227932(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41fed8acd483085b559d8beb4721e583545d9fd53a07efe421810e86e300b85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c44c6e267dd68ee8f622889d87e66fb165cb3801db357957cd256e5db0e5690(
    *,
    max_vcpus: jsii.Number,
    subnets: typing.Sequence[builtins.str],
    type: builtins.str,
    allocation_strategy: typing.Optional[builtins.str] = None,
    bid_percentage: typing.Optional[jsii.Number] = None,
    desired_vcpus: typing.Optional[jsii.Number] = None,
    ec2_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchComputeEnvironmentComputeResourcesEc2Configuration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ec2_key_pair: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    instance_role: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_template: typing.Optional[typing.Union[BatchComputeEnvironmentComputeResourcesLaunchTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    min_vcpus: typing.Optional[jsii.Number] = None,
    placement_group: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_iam_fleet_role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff628c5756ea83601cef71f16a4b33457971a288c8d51e9c2e00107f3b2001ea(
    *,
    image_id_override: typing.Optional[builtins.str] = None,
    image_kubernetes_version: typing.Optional[builtins.str] = None,
    image_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b986c560564e31197f8a43639acc98a82f8098902617c8e17b0aed22f525143(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f8dcaa664a8a44350d7762bfc8e2116e6acee3960b049e5a02c8d195941077(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338d36e8b253e3e24bea1959e146d39cfc30aefa716ac5757ce7e7fada04b2bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b3ce2a601d944e3fb5cca17d1c87f96700dec01d14aeec428477745929be09(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ffce9f39ba9f83c321fb003cbca698e6cf427ed67045fccc12bac9b977116c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2d4015a653cb355670349e42f3b7955f54ec9fc658bccea16656014d176d46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchComputeEnvironmentComputeResourcesEc2Configuration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a380ee76ad2cedc6e7c3826a72210fdaf9dbaf6a80d20c75b8d2a54c9d1824(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f395d6287b77d4b5dd1302540bbe54249231e25c11f09af10ab88785135a970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78094df28b43abb366007786493e3eb909bcea3fcc8fe7f1223db1dcc29adbf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e861d41029a735c958c67d2fae7375cad66a2856afbf887658f99bde4c59f53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd736fe4ba12dcc0ec74a6354a5988d2faac99e60967c0124c817689aa9e8b0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchComputeEnvironmentComputeResourcesEc2Configuration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beeca115512b7ec394440b932ac30f26a7d6a2b95291de04460ecd265c9789b8(
    *,
    launch_template_id: typing.Optional[builtins.str] = None,
    launch_template_name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54315ce30e7bd999699ac77b3de93815afa281147d157ea8e78e760b7b3563fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e116201523ee89dd11cbbdc454ddec2c2e98fd0c8b79cf862446baec1bfbd0e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef7ab2487d423bf0f27caa4c54e06307b6a00d9e7557b7a77940f63e3b3e217(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25bc9fafe30ce385f5d034434d83c83f1bfaa787d12a21fcb9205e5034d2bf15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac45e9474b5612496f82a8df1a41132e3832c79328613c2922643811fd82848(
    value: typing.Optional[BatchComputeEnvironmentComputeResourcesLaunchTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e2dbab5f0d45ff267024300508c13f823c2819480f4b1b37eabf7467db43f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d836fcc42f6ad85c3586e4132cce05939638691ca27ec98f341dbcd72dd53eae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchComputeEnvironmentComputeResourcesEc2Configuration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f25ebf1a6d2b093077b02806b47d46ffb35debdcaa20a1d13b89e2df4f1c284(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c9a45dd69eff22844721c6f1d02af1c023dc434a390e0531cfa1d824cbfc8f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f5be95e725074d8a95bb94a2856894a2c8f86672fc4af38ac4e3b578c58762(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d5467728bf9c7013448c7725b68492fb7f133a40dfc136782a8a32f1ae4a3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59215388a496dc2f4431f0834ddb1cf70e18fe3608dd386495ed68df4dde4859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efaa49b92ea9ab7181d9f62abcd2ec787fa30982fb1bc0b93171fb92c2571416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed47fa9e0d99cfcd88644e7a314d410a1065f4b5af0ee2fcdf369d445fe9c2d3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33600bf0773b30d7c89eccf728bc76c4a5fd900fdb8d5e145ce56cb69ef4e63(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e27abd9e158f83de4d5c0387dba4be643637c19de25f5c4fd67e7b1dc8c4221(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ef12fe6cccdd0e2910a06ed8b76d4584a5f197570abecff0da9315bdfa276d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de52b9d27bee8c289fae4495d1979c1bf6cc0958539bf0f6714429548aa29ef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bbdc82ccb641f956b854c2db8a8f54440caa11d0ae3ee4789675cb3556444a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a38368c13260039c09387fbb35d9e11a537990942580ddb9177a498f4fbe480(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383734ebe8809d7eea878f93f25aa8dc0f57adf117461fea1a7f4b7e506be698(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8449c9765de33a76a1fe1ff96868c5a7df069a13d5dc807afa7ad4def3897815(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55cb0a066d8b59bbc1d1ff095253563eb641b4fee2df52fb203ace9eaf538a67(
    value: typing.Optional[BatchComputeEnvironmentComputeResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd9e690934c6835098539167540848ed2525030cc3098c829a97b7c221f20e0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: builtins.str,
    compute_resources: typing.Optional[typing.Union[BatchComputeEnvironmentComputeResources, typing.Dict[builtins.str, typing.Any]]] = None,
    eks_configuration: typing.Optional[typing.Union[BatchComputeEnvironmentEksConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    update_policy: typing.Optional[typing.Union[BatchComputeEnvironmentUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd56642b0ca0ffd2704d2ec2b7ba2fe14b43b408359619d51491d6de457524ea(
    *,
    eks_cluster_arn: builtins.str,
    kubernetes_namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee93b92f8e582f34590c4f1c05de0416f29a3a33f669060af81499926aa2a32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a238635cdd1d1bea1144f408ced7946c2a2e4ffef46590ff8db953ca79aac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198906c47255e654898b97f7cbb1e88810a3a5dda75146fb621bc58ec0be62f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97343d9c643671c972089a154ef97427360104a90588ab96f15b40f942a083b7(
    value: typing.Optional[BatchComputeEnvironmentEksConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c325848c3de7509b5a9b611ab672981e60a7ecdd9a34852339b61e6f1defc2bd(
    *,
    job_execution_timeout_minutes: typing.Optional[jsii.Number] = None,
    terminate_jobs_on_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec075ccee38bec0bc6719e92aa2b51f73e7d94f9d1cbfc87e43f009002fb172f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b875f4b005f178f93c9ddee93aec1b2eb1ce4133cbcb7bd8062b8bf09bcb58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f9461f61781e99c4834cfb2205f8a8d63ae5d3682bb0b4b85dbb589cf89379(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ab7f539f7122aae5b390408a5f29e83ecc33b655e62f55441d4fac5e55d2a1(
    value: typing.Optional[BatchComputeEnvironmentUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass
