r'''
# `aws_finspace_kx_cluster`

Refer to the Terraform Registry for docs: [`aws_finspace_kx_cluster`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster).
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


class FinspaceKxCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster aws_finspace_kx_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        az_mode: builtins.str,
        environment_id: builtins.str,
        name: builtins.str,
        release_label: builtins.str,
        type: builtins.str,
        vpc_configuration: typing.Union["FinspaceKxClusterVpcConfiguration", typing.Dict[builtins.str, typing.Any]],
        auto_scaling_configuration: typing.Optional[typing.Union["FinspaceKxClusterAutoScalingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        availability_zone_id: typing.Optional[builtins.str] = None,
        cache_storage_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FinspaceKxClusterCacheStorageConfigurations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        capacity_configuration: typing.Optional[typing.Union["FinspaceKxClusterCapacityConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        code: typing.Optional[typing.Union["FinspaceKxClusterCode", typing.Dict[builtins.str, typing.Any]]] = None,
        command_line_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        database: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FinspaceKxClusterDatabase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initialization_script: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        savedown_storage_configuration: typing.Optional[typing.Union["FinspaceKxClusterSavedownStorageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        scaling_group_configuration: typing.Optional[typing.Union["FinspaceKxClusterScalingGroupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tickerplant_log_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FinspaceKxClusterTickerplantLogConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["FinspaceKxClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster aws_finspace_kx_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param az_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#az_mode FinspaceKxCluster#az_mode}.
        :param environment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#environment_id FinspaceKxCluster#environment_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#name FinspaceKxCluster#name}.
        :param release_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#release_label FinspaceKxCluster#release_label}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#type FinspaceKxCluster#type}.
        :param vpc_configuration: vpc_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#vpc_configuration FinspaceKxCluster#vpc_configuration}
        :param auto_scaling_configuration: auto_scaling_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#auto_scaling_configuration FinspaceKxCluster#auto_scaling_configuration}
        :param availability_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#availability_zone_id FinspaceKxCluster#availability_zone_id}.
        :param cache_storage_configurations: cache_storage_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#cache_storage_configurations FinspaceKxCluster#cache_storage_configurations}
        :param capacity_configuration: capacity_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#capacity_configuration FinspaceKxCluster#capacity_configuration}
        :param code: code block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#code FinspaceKxCluster#code}
        :param command_line_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#command_line_arguments FinspaceKxCluster#command_line_arguments}.
        :param database: database block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#database FinspaceKxCluster#database}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#description FinspaceKxCluster#description}.
        :param execution_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#execution_role FinspaceKxCluster#execution_role}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#id FinspaceKxCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initialization_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#initialization_script FinspaceKxCluster#initialization_script}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#region FinspaceKxCluster#region}
        :param savedown_storage_configuration: savedown_storage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#savedown_storage_configuration FinspaceKxCluster#savedown_storage_configuration}
        :param scaling_group_configuration: scaling_group_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scaling_group_configuration FinspaceKxCluster#scaling_group_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tags FinspaceKxCluster#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tags_all FinspaceKxCluster#tags_all}.
        :param tickerplant_log_configuration: tickerplant_log_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tickerplant_log_configuration FinspaceKxCluster#tickerplant_log_configuration}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#timeouts FinspaceKxCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__084cae885e4940a4b4fdca41ab42e358a87b4499e5eaccdb480e422c5711913f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FinspaceKxClusterConfig(
            az_mode=az_mode,
            environment_id=environment_id,
            name=name,
            release_label=release_label,
            type=type,
            vpc_configuration=vpc_configuration,
            auto_scaling_configuration=auto_scaling_configuration,
            availability_zone_id=availability_zone_id,
            cache_storage_configurations=cache_storage_configurations,
            capacity_configuration=capacity_configuration,
            code=code,
            command_line_arguments=command_line_arguments,
            database=database,
            description=description,
            execution_role=execution_role,
            id=id,
            initialization_script=initialization_script,
            region=region,
            savedown_storage_configuration=savedown_storage_configuration,
            scaling_group_configuration=scaling_group_configuration,
            tags=tags,
            tags_all=tags_all,
            tickerplant_log_configuration=tickerplant_log_configuration,
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
        '''Generates CDKTF code for importing a FinspaceKxCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FinspaceKxCluster to import.
        :param import_from_id: The id of the existing FinspaceKxCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FinspaceKxCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16227c6c992b430d8b868ef44fe6fe78b4cdb73155224efe58d6938764b60005)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoScalingConfiguration")
    def put_auto_scaling_configuration(
        self,
        *,
        auto_scaling_metric: builtins.str,
        max_node_count: jsii.Number,
        metric_target: jsii.Number,
        min_node_count: jsii.Number,
        scale_in_cooldown_seconds: jsii.Number,
        scale_out_cooldown_seconds: jsii.Number,
    ) -> None:
        '''
        :param auto_scaling_metric: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#auto_scaling_metric FinspaceKxCluster#auto_scaling_metric}.
        :param max_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#max_node_count FinspaceKxCluster#max_node_count}.
        :param metric_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#metric_target FinspaceKxCluster#metric_target}.
        :param min_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#min_node_count FinspaceKxCluster#min_node_count}.
        :param scale_in_cooldown_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scale_in_cooldown_seconds FinspaceKxCluster#scale_in_cooldown_seconds}.
        :param scale_out_cooldown_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scale_out_cooldown_seconds FinspaceKxCluster#scale_out_cooldown_seconds}.
        '''
        value = FinspaceKxClusterAutoScalingConfiguration(
            auto_scaling_metric=auto_scaling_metric,
            max_node_count=max_node_count,
            metric_target=metric_target,
            min_node_count=min_node_count,
            scale_in_cooldown_seconds=scale_in_cooldown_seconds,
            scale_out_cooldown_seconds=scale_out_cooldown_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoScalingConfiguration", [value]))

    @jsii.member(jsii_name="putCacheStorageConfigurations")
    def put_cache_storage_configurations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FinspaceKxClusterCacheStorageConfigurations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e9e79b2d5ff2cbf81c59f3ab1b25df7f9db951feb3d80acc8eb7f95932fce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCacheStorageConfigurations", [value]))

    @jsii.member(jsii_name="putCapacityConfiguration")
    def put_capacity_configuration(
        self,
        *,
        node_count: jsii.Number,
        node_type: builtins.str,
    ) -> None:
        '''
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#node_count FinspaceKxCluster#node_count}.
        :param node_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#node_type FinspaceKxCluster#node_type}.
        '''
        value = FinspaceKxClusterCapacityConfiguration(
            node_count=node_count, node_type=node_type
        )

        return typing.cast(None, jsii.invoke(self, "putCapacityConfiguration", [value]))

    @jsii.member(jsii_name="putCode")
    def put_code(
        self,
        *,
        s3_bucket: builtins.str,
        s3_key: builtins.str,
        s3_object_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#s3_bucket FinspaceKxCluster#s3_bucket}.
        :param s3_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#s3_key FinspaceKxCluster#s3_key}.
        :param s3_object_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#s3_object_version FinspaceKxCluster#s3_object_version}.
        '''
        value = FinspaceKxClusterCode(
            s3_bucket=s3_bucket, s3_key=s3_key, s3_object_version=s3_object_version
        )

        return typing.cast(None, jsii.invoke(self, "putCode", [value]))

    @jsii.member(jsii_name="putDatabase")
    def put_database(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FinspaceKxClusterDatabase", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4facbd15e7bf11129099118b9b70b13b0027954704ffb3f745bcdf147ec23ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDatabase", [value]))

    @jsii.member(jsii_name="putSavedownStorageConfiguration")
    def put_savedown_storage_configuration(
        self,
        *,
        size: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        volume_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#size FinspaceKxCluster#size}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#type FinspaceKxCluster#type}.
        :param volume_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#volume_name FinspaceKxCluster#volume_name}.
        '''
        value = FinspaceKxClusterSavedownStorageConfiguration(
            size=size, type=type, volume_name=volume_name
        )

        return typing.cast(None, jsii.invoke(self, "putSavedownStorageConfiguration", [value]))

    @jsii.member(jsii_name="putScalingGroupConfiguration")
    def put_scaling_group_configuration(
        self,
        *,
        memory_reservation: jsii.Number,
        node_count: jsii.Number,
        scaling_group_name: builtins.str,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param memory_reservation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#memory_reservation FinspaceKxCluster#memory_reservation}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#node_count FinspaceKxCluster#node_count}.
        :param scaling_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scaling_group_name FinspaceKxCluster#scaling_group_name}.
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#cpu FinspaceKxCluster#cpu}.
        :param memory_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#memory_limit FinspaceKxCluster#memory_limit}.
        '''
        value = FinspaceKxClusterScalingGroupConfiguration(
            memory_reservation=memory_reservation,
            node_count=node_count,
            scaling_group_name=scaling_group_name,
            cpu=cpu,
            memory_limit=memory_limit,
        )

        return typing.cast(None, jsii.invoke(self, "putScalingGroupConfiguration", [value]))

    @jsii.member(jsii_name="putTickerplantLogConfiguration")
    def put_tickerplant_log_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FinspaceKxClusterTickerplantLogConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c78ca1c764fbed56683e503377fd45a98bb932bed75bc7a13c672e19d9377c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTickerplantLogConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#create FinspaceKxCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#delete FinspaceKxCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#update FinspaceKxCluster#update}.
        '''
        value = FinspaceKxClusterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVpcConfiguration")
    def put_vpc_configuration(
        self,
        *,
        ip_address_type: builtins.str,
        security_group_ids: typing.Sequence[builtins.str],
        subnet_ids: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
    ) -> None:
        '''
        :param ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#ip_address_type FinspaceKxCluster#ip_address_type}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#security_group_ids FinspaceKxCluster#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#subnet_ids FinspaceKxCluster#subnet_ids}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#vpc_id FinspaceKxCluster#vpc_id}.
        '''
        value = FinspaceKxClusterVpcConfiguration(
            ip_address_type=ip_address_type,
            security_group_ids=security_group_ids,
            subnet_ids=subnet_ids,
            vpc_id=vpc_id,
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfiguration", [value]))

    @jsii.member(jsii_name="resetAutoScalingConfiguration")
    def reset_auto_scaling_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoScalingConfiguration", []))

    @jsii.member(jsii_name="resetAvailabilityZoneId")
    def reset_availability_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZoneId", []))

    @jsii.member(jsii_name="resetCacheStorageConfigurations")
    def reset_cache_storage_configurations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheStorageConfigurations", []))

    @jsii.member(jsii_name="resetCapacityConfiguration")
    def reset_capacity_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityConfiguration", []))

    @jsii.member(jsii_name="resetCode")
    def reset_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCode", []))

    @jsii.member(jsii_name="resetCommandLineArguments")
    def reset_command_line_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommandLineArguments", []))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExecutionRole")
    def reset_execution_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionRole", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitializationScript")
    def reset_initialization_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitializationScript", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSavedownStorageConfiguration")
    def reset_savedown_storage_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSavedownStorageConfiguration", []))

    @jsii.member(jsii_name="resetScalingGroupConfiguration")
    def reset_scaling_group_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingGroupConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTickerplantLogConfiguration")
    def reset_tickerplant_log_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTickerplantLogConfiguration", []))

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
    @jsii.member(jsii_name="autoScalingConfiguration")
    def auto_scaling_configuration(
        self,
    ) -> "FinspaceKxClusterAutoScalingConfigurationOutputReference":
        return typing.cast("FinspaceKxClusterAutoScalingConfigurationOutputReference", jsii.get(self, "autoScalingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="cacheStorageConfigurations")
    def cache_storage_configurations(
        self,
    ) -> "FinspaceKxClusterCacheStorageConfigurationsList":
        return typing.cast("FinspaceKxClusterCacheStorageConfigurationsList", jsii.get(self, "cacheStorageConfigurations"))

    @builtins.property
    @jsii.member(jsii_name="capacityConfiguration")
    def capacity_configuration(
        self,
    ) -> "FinspaceKxClusterCapacityConfigurationOutputReference":
        return typing.cast("FinspaceKxClusterCapacityConfigurationOutputReference", jsii.get(self, "capacityConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> "FinspaceKxClusterCodeOutputReference":
        return typing.cast("FinspaceKxClusterCodeOutputReference", jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="createdTimestamp")
    def created_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> "FinspaceKxClusterDatabaseList":
        return typing.cast("FinspaceKxClusterDatabaseList", jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedTimestamp")
    def last_modified_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="savedownStorageConfiguration")
    def savedown_storage_configuration(
        self,
    ) -> "FinspaceKxClusterSavedownStorageConfigurationOutputReference":
        return typing.cast("FinspaceKxClusterSavedownStorageConfigurationOutputReference", jsii.get(self, "savedownStorageConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="scalingGroupConfiguration")
    def scaling_group_configuration(
        self,
    ) -> "FinspaceKxClusterScalingGroupConfigurationOutputReference":
        return typing.cast("FinspaceKxClusterScalingGroupConfigurationOutputReference", jsii.get(self, "scalingGroupConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusReason"))

    @builtins.property
    @jsii.member(jsii_name="tickerplantLogConfiguration")
    def tickerplant_log_configuration(
        self,
    ) -> "FinspaceKxClusterTickerplantLogConfigurationList":
        return typing.cast("FinspaceKxClusterTickerplantLogConfigurationList", jsii.get(self, "tickerplantLogConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FinspaceKxClusterTimeoutsOutputReference":
        return typing.cast("FinspaceKxClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfiguration")
    def vpc_configuration(self) -> "FinspaceKxClusterVpcConfigurationOutputReference":
        return typing.cast("FinspaceKxClusterVpcConfigurationOutputReference", jsii.get(self, "vpcConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationInput")
    def auto_scaling_configuration_input(
        self,
    ) -> typing.Optional["FinspaceKxClusterAutoScalingConfiguration"]:
        return typing.cast(typing.Optional["FinspaceKxClusterAutoScalingConfiguration"], jsii.get(self, "autoScalingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneIdInput")
    def availability_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="azModeInput")
    def az_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azModeInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheStorageConfigurationsInput")
    def cache_storage_configurations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterCacheStorageConfigurations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterCacheStorageConfigurations"]]], jsii.get(self, "cacheStorageConfigurationsInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityConfigurationInput")
    def capacity_configuration_input(
        self,
    ) -> typing.Optional["FinspaceKxClusterCapacityConfiguration"]:
        return typing.cast(typing.Optional["FinspaceKxClusterCapacityConfiguration"], jsii.get(self, "capacityConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="codeInput")
    def code_input(self) -> typing.Optional["FinspaceKxClusterCode"]:
        return typing.cast(typing.Optional["FinspaceKxClusterCode"], jsii.get(self, "codeInput"))

    @builtins.property
    @jsii.member(jsii_name="commandLineArgumentsInput")
    def command_line_arguments_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "commandLineArgumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterDatabase"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterDatabase"]]], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentIdInput")
    def environment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleInput")
    def execution_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initializationScriptInput")
    def initialization_script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initializationScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="releaseLabelInput")
    def release_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releaseLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="savedownStorageConfigurationInput")
    def savedown_storage_configuration_input(
        self,
    ) -> typing.Optional["FinspaceKxClusterSavedownStorageConfiguration"]:
        return typing.cast(typing.Optional["FinspaceKxClusterSavedownStorageConfiguration"], jsii.get(self, "savedownStorageConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingGroupConfigurationInput")
    def scaling_group_configuration_input(
        self,
    ) -> typing.Optional["FinspaceKxClusterScalingGroupConfiguration"]:
        return typing.cast(typing.Optional["FinspaceKxClusterScalingGroupConfiguration"], jsii.get(self, "scalingGroupConfigurationInput"))

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
    @jsii.member(jsii_name="tickerplantLogConfigurationInput")
    def tickerplant_log_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterTickerplantLogConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterTickerplantLogConfiguration"]]], jsii.get(self, "tickerplantLogConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FinspaceKxClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FinspaceKxClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfigurationInput")
    def vpc_configuration_input(
        self,
    ) -> typing.Optional["FinspaceKxClusterVpcConfiguration"]:
        return typing.cast(typing.Optional["FinspaceKxClusterVpcConfiguration"], jsii.get(self, "vpcConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneId")
    def availability_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZoneId"))

    @availability_zone_id.setter
    def availability_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebda6e30717a18e28d27a944d0f45934c7d0546898a94c7a50abe3d8b1c5ad41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azMode")
    def az_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azMode"))

    @az_mode.setter
    def az_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cddbec8daab05828a47e72dc2e860ff649587dfad666a2af77362bf339c18c4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commandLineArguments")
    def command_line_arguments(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "commandLineArguments"))

    @command_line_arguments.setter
    def command_line_arguments(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982723df78e0062351d32d2da6cba0610a6ed4bb612d1adf9dad3eb6c3530a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commandLineArguments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24fd82bdb5332068baba88d711182ded763bf3767c5f5a3a8285a2239589ddd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environmentId"))

    @environment_id.setter
    def environment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5989de11ce6cdf035b274ea15a80eaba32c4e8fd1b9e9dbdede43bee749d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRole"))

    @execution_role.setter
    def execution_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35dda8236f143f370df2ce4a0ae94da4c41183e9793cb42b8ca698524894dafd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489db78b9d89a59b2c62dca56fff18958857f4fe81f4629425362e1e18f4b9ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initializationScript")
    def initialization_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initializationScript"))

    @initialization_script.setter
    def initialization_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d99ef2e58a9bcc53789ac55448976ef4cec34c87db65999d181929421612af1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initializationScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e0113f17674057b8b8601ec4dbcd625ae1dc677d491605c00cea0bd23e4b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14bb725cc7d369b4ee515589a513e2fb87496c879fb82eb521de6d7c97440132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseLabel")
    def release_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseLabel"))

    @release_label.setter
    def release_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cdf46c0f9962f964ddf0eee7abc5a595557bebf9418dbdb3a51782262a45a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967d1f73964f200d8fcde51137f39ddd2dee3af0643150ed8d2ccb289a779914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2402c8a8541069a33cf2e38464a5e3e6a40a27d5982f923cd1c65adec16cbb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9937d00dd9b06dab01816e14e4f17927b86b10f784540fe22d587bcf6cebf1c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterAutoScalingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_metric": "autoScalingMetric",
        "max_node_count": "maxNodeCount",
        "metric_target": "metricTarget",
        "min_node_count": "minNodeCount",
        "scale_in_cooldown_seconds": "scaleInCooldownSeconds",
        "scale_out_cooldown_seconds": "scaleOutCooldownSeconds",
    },
)
class FinspaceKxClusterAutoScalingConfiguration:
    def __init__(
        self,
        *,
        auto_scaling_metric: builtins.str,
        max_node_count: jsii.Number,
        metric_target: jsii.Number,
        min_node_count: jsii.Number,
        scale_in_cooldown_seconds: jsii.Number,
        scale_out_cooldown_seconds: jsii.Number,
    ) -> None:
        '''
        :param auto_scaling_metric: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#auto_scaling_metric FinspaceKxCluster#auto_scaling_metric}.
        :param max_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#max_node_count FinspaceKxCluster#max_node_count}.
        :param metric_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#metric_target FinspaceKxCluster#metric_target}.
        :param min_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#min_node_count FinspaceKxCluster#min_node_count}.
        :param scale_in_cooldown_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scale_in_cooldown_seconds FinspaceKxCluster#scale_in_cooldown_seconds}.
        :param scale_out_cooldown_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scale_out_cooldown_seconds FinspaceKxCluster#scale_out_cooldown_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8a67e1bbdd32b20324c46af9d03bb5219fe2d78f38339f7d77749ce42fddb6)
            check_type(argname="argument auto_scaling_metric", value=auto_scaling_metric, expected_type=type_hints["auto_scaling_metric"])
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument metric_target", value=metric_target, expected_type=type_hints["metric_target"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
            check_type(argname="argument scale_in_cooldown_seconds", value=scale_in_cooldown_seconds, expected_type=type_hints["scale_in_cooldown_seconds"])
            check_type(argname="argument scale_out_cooldown_seconds", value=scale_out_cooldown_seconds, expected_type=type_hints["scale_out_cooldown_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_scaling_metric": auto_scaling_metric,
            "max_node_count": max_node_count,
            "metric_target": metric_target,
            "min_node_count": min_node_count,
            "scale_in_cooldown_seconds": scale_in_cooldown_seconds,
            "scale_out_cooldown_seconds": scale_out_cooldown_seconds,
        }

    @builtins.property
    def auto_scaling_metric(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#auto_scaling_metric FinspaceKxCluster#auto_scaling_metric}.'''
        result = self._values.get("auto_scaling_metric")
        assert result is not None, "Required property 'auto_scaling_metric' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#max_node_count FinspaceKxCluster#max_node_count}.'''
        result = self._values.get("max_node_count")
        assert result is not None, "Required property 'max_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def metric_target(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#metric_target FinspaceKxCluster#metric_target}.'''
        result = self._values.get("metric_target")
        assert result is not None, "Required property 'metric_target' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#min_node_count FinspaceKxCluster#min_node_count}.'''
        result = self._values.get("min_node_count")
        assert result is not None, "Required property 'min_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_in_cooldown_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scale_in_cooldown_seconds FinspaceKxCluster#scale_in_cooldown_seconds}.'''
        result = self._values.get("scale_in_cooldown_seconds")
        assert result is not None, "Required property 'scale_in_cooldown_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out_cooldown_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scale_out_cooldown_seconds FinspaceKxCluster#scale_out_cooldown_seconds}.'''
        result = self._values.get("scale_out_cooldown_seconds")
        assert result is not None, "Required property 'scale_out_cooldown_seconds' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterAutoScalingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FinspaceKxClusterAutoScalingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterAutoScalingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cf0f7dfc21d31873e7f27438e92cadd1cce36989cc880857e86b3bd6503a679)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="autoScalingMetricInput")
    def auto_scaling_metric_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoScalingMetricInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCountInput")
    def max_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="metricTargetInput")
    def metric_target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCountInput")
    def min_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleInCooldownSecondsInput")
    def scale_in_cooldown_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleInCooldownSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutCooldownSecondsInput")
    def scale_out_cooldown_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleOutCooldownSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingMetric")
    def auto_scaling_metric(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoScalingMetric"))

    @auto_scaling_metric.setter
    def auto_scaling_metric(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a4690e94638e3aad305d1e4a5e2d7bd350a936076c3c857ab1a91d5c436a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoScalingMetric", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c9c569e33bcde870460297e82602331873804ce66b9ad176bf5ab285fddc62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricTarget")
    def metric_target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricTarget"))

    @metric_target.setter
    def metric_target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf2aa5f1ede727b42b91d9c81ae12a1436029b515805f182afa530397cfa3fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6a05c1d719c556dbaf224fbc797504c0c9e119d1877360dcbacdd8bd0d57d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleInCooldownSeconds")
    def scale_in_cooldown_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleInCooldownSeconds"))

    @scale_in_cooldown_seconds.setter
    def scale_in_cooldown_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299b183799c2b44339392809fa26b2d46a77dc10e6d5a4c4b0024d38f9055783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleInCooldownSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOutCooldownSeconds")
    def scale_out_cooldown_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOutCooldownSeconds"))

    @scale_out_cooldown_seconds.setter
    def scale_out_cooldown_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040a2b1dd304081dec4cdce28db71819953961e68d1e3cfe3bafcbccafbf1296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOutCooldownSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FinspaceKxClusterAutoScalingConfiguration]:
        return typing.cast(typing.Optional[FinspaceKxClusterAutoScalingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FinspaceKxClusterAutoScalingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600ca473c7de82a3de77cd6560b6c48edcafc3496ffb80e1542acb8d8ed06496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterCacheStorageConfigurations",
    jsii_struct_bases=[],
    name_mapping={"size": "size", "type": "type"},
)
class FinspaceKxClusterCacheStorageConfigurations:
    def __init__(self, *, size: jsii.Number, type: builtins.str) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#size FinspaceKxCluster#size}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#type FinspaceKxCluster#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcdab6cb4fadc56f055cb271614486778fec0150002f694be0f3cf64276c74dc)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size": size,
            "type": type,
        }

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#size FinspaceKxCluster#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#type FinspaceKxCluster#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterCacheStorageConfigurations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FinspaceKxClusterCacheStorageConfigurationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterCacheStorageConfigurationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc58c0379a95e28ab9c9e0f8e3821922b3ec72518d4ce71efa41f9778e2f3260)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FinspaceKxClusterCacheStorageConfigurationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad6a39f2c9871e9a786ec4b92154110614dc83f7a8cc29e45c5dcf6a2980811)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FinspaceKxClusterCacheStorageConfigurationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f995b7e2e90408ac619e6aa6c59e71c1c5d8caaa01e4e2f7de6c0e3f91f2f47d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9f16eb6c9896148fe87d9824b00b158414b56a6e2dec33d1a18c8ce9c5ba978)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14b881fb8af4edca05c1eed8506e29076d6d50644b8f87780d653522eb09c461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterCacheStorageConfigurations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterCacheStorageConfigurations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterCacheStorageConfigurations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0dc1a9787a6a8cb092a23d5b03f4fe80ce7f7c8f313b52e23c3adc65c8b503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FinspaceKxClusterCacheStorageConfigurationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterCacheStorageConfigurationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dce7c8b77f19fcb77a42dc4f545397470f34489541961ec1734e04d645b7f2a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db579e7d50b17aa0ef8887292d8454eb814068de69ee0d7bf952ff4b08f6774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23eb77fa81f5ac19b43295eb7816dff861fd7262f3b0b91a9fc61f48887375c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterCacheStorageConfigurations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterCacheStorageConfigurations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterCacheStorageConfigurations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef21ac054bc4aa228deb0bef1e77886db7ff6ed2b0764336a7b30e6d06660ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterCapacityConfiguration",
    jsii_struct_bases=[],
    name_mapping={"node_count": "nodeCount", "node_type": "nodeType"},
)
class FinspaceKxClusterCapacityConfiguration:
    def __init__(self, *, node_count: jsii.Number, node_type: builtins.str) -> None:
        '''
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#node_count FinspaceKxCluster#node_count}.
        :param node_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#node_type FinspaceKxCluster#node_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6551a11dc554c8c44048a40778cecfa5d40ea2a41a0ca55dce64ba67a8815c41)
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_count": node_count,
            "node_type": node_type,
        }

    @builtins.property
    def node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#node_count FinspaceKxCluster#node_count}.'''
        result = self._values.get("node_count")
        assert result is not None, "Required property 'node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def node_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#node_type FinspaceKxCluster#node_type}.'''
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterCapacityConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FinspaceKxClusterCapacityConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterCapacityConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6516a3a8cc8ce03ebdbe1149b778b282d5bbdf358cd08567019a12e507da6ffa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44a4943d57ce57e383a77d80fe7fa749fb9003e4f9fa91f7186f1fc44b19d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf805a3ccf4df6036d1a6c37925b40db67dd4237e9c27773ab31401dfafa1151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FinspaceKxClusterCapacityConfiguration]:
        return typing.cast(typing.Optional[FinspaceKxClusterCapacityConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FinspaceKxClusterCapacityConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc40c8a49ebb2922427493eccc8272770a217ce5384ee78f21999b01553b2fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterCode",
    jsii_struct_bases=[],
    name_mapping={
        "s3_bucket": "s3Bucket",
        "s3_key": "s3Key",
        "s3_object_version": "s3ObjectVersion",
    },
)
class FinspaceKxClusterCode:
    def __init__(
        self,
        *,
        s3_bucket: builtins.str,
        s3_key: builtins.str,
        s3_object_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#s3_bucket FinspaceKxCluster#s3_bucket}.
        :param s3_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#s3_key FinspaceKxCluster#s3_key}.
        :param s3_object_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#s3_object_version FinspaceKxCluster#s3_object_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0227828dfe63d49d5d7b72772fbc28dbc6dbdbe6ed6b718e954a967823ef5a72)
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_bucket": s3_bucket,
            "s3_key": s3_key,
        }
        if s3_object_version is not None:
            self._values["s3_object_version"] = s3_object_version

    @builtins.property
    def s3_bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#s3_bucket FinspaceKxCluster#s3_bucket}.'''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#s3_key FinspaceKxCluster#s3_key}.'''
        result = self._values.get("s3_key")
        assert result is not None, "Required property 's3_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_object_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#s3_object_version FinspaceKxCluster#s3_object_version}.'''
        result = self._values.get("s3_object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterCode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FinspaceKxClusterCodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterCodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f48f226739656cc7493a7c3bb38024e9e34c2d4d92688e98b34830163d899e75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3ObjectVersion")
    def reset_s3_object_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3ObjectVersion", []))

    @builtins.property
    @jsii.member(jsii_name="s3BucketInput")
    def s3_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketInput"))

    @builtins.property
    @jsii.member(jsii_name="s3KeyInput")
    def s3_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3KeyInput"))

    @builtins.property
    @jsii.member(jsii_name="s3ObjectVersionInput")
    def s3_object_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3ObjectVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f34fdc3439428669f617d1c0c5b145214fc948436a9e427599af9eda24037f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Key")
    def s3_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Key"))

    @s3_key.setter
    def s3_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6318a200f8e01b0c2803ab5bd576cdfa3be7754e208b181c0d4ff4a796d774a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3ObjectVersion")
    def s3_object_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3ObjectVersion"))

    @s3_object_version.setter
    def s3_object_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c493801dd45d94e424c39cecdca162bd5f71097aeae0ac9f31d3fdb2dc0b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3ObjectVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FinspaceKxClusterCode]:
        return typing.cast(typing.Optional[FinspaceKxClusterCode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FinspaceKxClusterCode]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5579c3226f440acd98f7eb61c1f90cbd41ba19b1cbc8602ce9aaaa457328e656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "az_mode": "azMode",
        "environment_id": "environmentId",
        "name": "name",
        "release_label": "releaseLabel",
        "type": "type",
        "vpc_configuration": "vpcConfiguration",
        "auto_scaling_configuration": "autoScalingConfiguration",
        "availability_zone_id": "availabilityZoneId",
        "cache_storage_configurations": "cacheStorageConfigurations",
        "capacity_configuration": "capacityConfiguration",
        "code": "code",
        "command_line_arguments": "commandLineArguments",
        "database": "database",
        "description": "description",
        "execution_role": "executionRole",
        "id": "id",
        "initialization_script": "initializationScript",
        "region": "region",
        "savedown_storage_configuration": "savedownStorageConfiguration",
        "scaling_group_configuration": "scalingGroupConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tickerplant_log_configuration": "tickerplantLogConfiguration",
        "timeouts": "timeouts",
    },
)
class FinspaceKxClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        az_mode: builtins.str,
        environment_id: builtins.str,
        name: builtins.str,
        release_label: builtins.str,
        type: builtins.str,
        vpc_configuration: typing.Union["FinspaceKxClusterVpcConfiguration", typing.Dict[builtins.str, typing.Any]],
        auto_scaling_configuration: typing.Optional[typing.Union[FinspaceKxClusterAutoScalingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        availability_zone_id: typing.Optional[builtins.str] = None,
        cache_storage_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterCacheStorageConfigurations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        capacity_configuration: typing.Optional[typing.Union[FinspaceKxClusterCapacityConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        code: typing.Optional[typing.Union[FinspaceKxClusterCode, typing.Dict[builtins.str, typing.Any]]] = None,
        command_line_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        database: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FinspaceKxClusterDatabase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initialization_script: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        savedown_storage_configuration: typing.Optional[typing.Union["FinspaceKxClusterSavedownStorageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        scaling_group_configuration: typing.Optional[typing.Union["FinspaceKxClusterScalingGroupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tickerplant_log_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FinspaceKxClusterTickerplantLogConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["FinspaceKxClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param az_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#az_mode FinspaceKxCluster#az_mode}.
        :param environment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#environment_id FinspaceKxCluster#environment_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#name FinspaceKxCluster#name}.
        :param release_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#release_label FinspaceKxCluster#release_label}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#type FinspaceKxCluster#type}.
        :param vpc_configuration: vpc_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#vpc_configuration FinspaceKxCluster#vpc_configuration}
        :param auto_scaling_configuration: auto_scaling_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#auto_scaling_configuration FinspaceKxCluster#auto_scaling_configuration}
        :param availability_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#availability_zone_id FinspaceKxCluster#availability_zone_id}.
        :param cache_storage_configurations: cache_storage_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#cache_storage_configurations FinspaceKxCluster#cache_storage_configurations}
        :param capacity_configuration: capacity_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#capacity_configuration FinspaceKxCluster#capacity_configuration}
        :param code: code block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#code FinspaceKxCluster#code}
        :param command_line_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#command_line_arguments FinspaceKxCluster#command_line_arguments}.
        :param database: database block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#database FinspaceKxCluster#database}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#description FinspaceKxCluster#description}.
        :param execution_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#execution_role FinspaceKxCluster#execution_role}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#id FinspaceKxCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initialization_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#initialization_script FinspaceKxCluster#initialization_script}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#region FinspaceKxCluster#region}
        :param savedown_storage_configuration: savedown_storage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#savedown_storage_configuration FinspaceKxCluster#savedown_storage_configuration}
        :param scaling_group_configuration: scaling_group_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scaling_group_configuration FinspaceKxCluster#scaling_group_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tags FinspaceKxCluster#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tags_all FinspaceKxCluster#tags_all}.
        :param tickerplant_log_configuration: tickerplant_log_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tickerplant_log_configuration FinspaceKxCluster#tickerplant_log_configuration}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#timeouts FinspaceKxCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(vpc_configuration, dict):
            vpc_configuration = FinspaceKxClusterVpcConfiguration(**vpc_configuration)
        if isinstance(auto_scaling_configuration, dict):
            auto_scaling_configuration = FinspaceKxClusterAutoScalingConfiguration(**auto_scaling_configuration)
        if isinstance(capacity_configuration, dict):
            capacity_configuration = FinspaceKxClusterCapacityConfiguration(**capacity_configuration)
        if isinstance(code, dict):
            code = FinspaceKxClusterCode(**code)
        if isinstance(savedown_storage_configuration, dict):
            savedown_storage_configuration = FinspaceKxClusterSavedownStorageConfiguration(**savedown_storage_configuration)
        if isinstance(scaling_group_configuration, dict):
            scaling_group_configuration = FinspaceKxClusterScalingGroupConfiguration(**scaling_group_configuration)
        if isinstance(timeouts, dict):
            timeouts = FinspaceKxClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d612bf53a57d90d84e893d9340aea36fb94c171d8d8ec714d38a495d606c243f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument az_mode", value=az_mode, expected_type=type_hints["az_mode"])
            check_type(argname="argument environment_id", value=environment_id, expected_type=type_hints["environment_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument release_label", value=release_label, expected_type=type_hints["release_label"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            check_type(argname="argument auto_scaling_configuration", value=auto_scaling_configuration, expected_type=type_hints["auto_scaling_configuration"])
            check_type(argname="argument availability_zone_id", value=availability_zone_id, expected_type=type_hints["availability_zone_id"])
            check_type(argname="argument cache_storage_configurations", value=cache_storage_configurations, expected_type=type_hints["cache_storage_configurations"])
            check_type(argname="argument capacity_configuration", value=capacity_configuration, expected_type=type_hints["capacity_configuration"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument command_line_arguments", value=command_line_arguments, expected_type=type_hints["command_line_arguments"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initialization_script", value=initialization_script, expected_type=type_hints["initialization_script"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument savedown_storage_configuration", value=savedown_storage_configuration, expected_type=type_hints["savedown_storage_configuration"])
            check_type(argname="argument scaling_group_configuration", value=scaling_group_configuration, expected_type=type_hints["scaling_group_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tickerplant_log_configuration", value=tickerplant_log_configuration, expected_type=type_hints["tickerplant_log_configuration"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "az_mode": az_mode,
            "environment_id": environment_id,
            "name": name,
            "release_label": release_label,
            "type": type,
            "vpc_configuration": vpc_configuration,
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
        if auto_scaling_configuration is not None:
            self._values["auto_scaling_configuration"] = auto_scaling_configuration
        if availability_zone_id is not None:
            self._values["availability_zone_id"] = availability_zone_id
        if cache_storage_configurations is not None:
            self._values["cache_storage_configurations"] = cache_storage_configurations
        if capacity_configuration is not None:
            self._values["capacity_configuration"] = capacity_configuration
        if code is not None:
            self._values["code"] = code
        if command_line_arguments is not None:
            self._values["command_line_arguments"] = command_line_arguments
        if database is not None:
            self._values["database"] = database
        if description is not None:
            self._values["description"] = description
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if id is not None:
            self._values["id"] = id
        if initialization_script is not None:
            self._values["initialization_script"] = initialization_script
        if region is not None:
            self._values["region"] = region
        if savedown_storage_configuration is not None:
            self._values["savedown_storage_configuration"] = savedown_storage_configuration
        if scaling_group_configuration is not None:
            self._values["scaling_group_configuration"] = scaling_group_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tickerplant_log_configuration is not None:
            self._values["tickerplant_log_configuration"] = tickerplant_log_configuration
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
    def az_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#az_mode FinspaceKxCluster#az_mode}.'''
        result = self._values.get("az_mode")
        assert result is not None, "Required property 'az_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#environment_id FinspaceKxCluster#environment_id}.'''
        result = self._values.get("environment_id")
        assert result is not None, "Required property 'environment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#name FinspaceKxCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def release_label(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#release_label FinspaceKxCluster#release_label}.'''
        result = self._values.get("release_label")
        assert result is not None, "Required property 'release_label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#type FinspaceKxCluster#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_configuration(self) -> "FinspaceKxClusterVpcConfiguration":
        '''vpc_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#vpc_configuration FinspaceKxCluster#vpc_configuration}
        '''
        result = self._values.get("vpc_configuration")
        assert result is not None, "Required property 'vpc_configuration' is missing"
        return typing.cast("FinspaceKxClusterVpcConfiguration", result)

    @builtins.property
    def auto_scaling_configuration(
        self,
    ) -> typing.Optional[FinspaceKxClusterAutoScalingConfiguration]:
        '''auto_scaling_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#auto_scaling_configuration FinspaceKxCluster#auto_scaling_configuration}
        '''
        result = self._values.get("auto_scaling_configuration")
        return typing.cast(typing.Optional[FinspaceKxClusterAutoScalingConfiguration], result)

    @builtins.property
    def availability_zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#availability_zone_id FinspaceKxCluster#availability_zone_id}.'''
        result = self._values.get("availability_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_storage_configurations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterCacheStorageConfigurations]]]:
        '''cache_storage_configurations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#cache_storage_configurations FinspaceKxCluster#cache_storage_configurations}
        '''
        result = self._values.get("cache_storage_configurations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterCacheStorageConfigurations]]], result)

    @builtins.property
    def capacity_configuration(
        self,
    ) -> typing.Optional[FinspaceKxClusterCapacityConfiguration]:
        '''capacity_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#capacity_configuration FinspaceKxCluster#capacity_configuration}
        '''
        result = self._values.get("capacity_configuration")
        return typing.cast(typing.Optional[FinspaceKxClusterCapacityConfiguration], result)

    @builtins.property
    def code(self) -> typing.Optional[FinspaceKxClusterCode]:
        '''code block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#code FinspaceKxCluster#code}
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[FinspaceKxClusterCode], result)

    @builtins.property
    def command_line_arguments(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#command_line_arguments FinspaceKxCluster#command_line_arguments}.'''
        result = self._values.get("command_line_arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def database(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterDatabase"]]]:
        '''database block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#database FinspaceKxCluster#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterDatabase"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#description FinspaceKxCluster#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#execution_role FinspaceKxCluster#execution_role}.'''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#id FinspaceKxCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initialization_script(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#initialization_script FinspaceKxCluster#initialization_script}.'''
        result = self._values.get("initialization_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#region FinspaceKxCluster#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def savedown_storage_configuration(
        self,
    ) -> typing.Optional["FinspaceKxClusterSavedownStorageConfiguration"]:
        '''savedown_storage_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#savedown_storage_configuration FinspaceKxCluster#savedown_storage_configuration}
        '''
        result = self._values.get("savedown_storage_configuration")
        return typing.cast(typing.Optional["FinspaceKxClusterSavedownStorageConfiguration"], result)

    @builtins.property
    def scaling_group_configuration(
        self,
    ) -> typing.Optional["FinspaceKxClusterScalingGroupConfiguration"]:
        '''scaling_group_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scaling_group_configuration FinspaceKxCluster#scaling_group_configuration}
        '''
        result = self._values.get("scaling_group_configuration")
        return typing.cast(typing.Optional["FinspaceKxClusterScalingGroupConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tags FinspaceKxCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tags_all FinspaceKxCluster#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tickerplant_log_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterTickerplantLogConfiguration"]]]:
        '''tickerplant_log_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tickerplant_log_configuration FinspaceKxCluster#tickerplant_log_configuration}
        '''
        result = self._values.get("tickerplant_log_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterTickerplantLogConfiguration"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FinspaceKxClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#timeouts FinspaceKxCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FinspaceKxClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterDatabase",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "cache_configurations": "cacheConfigurations",
        "changeset_id": "changesetId",
        "dataview_name": "dataviewName",
    },
)
class FinspaceKxClusterDatabase:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        cache_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FinspaceKxClusterDatabaseCacheConfigurations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        changeset_id: typing.Optional[builtins.str] = None,
        dataview_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#database_name FinspaceKxCluster#database_name}.
        :param cache_configurations: cache_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#cache_configurations FinspaceKxCluster#cache_configurations}
        :param changeset_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#changeset_id FinspaceKxCluster#changeset_id}.
        :param dataview_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#dataview_name FinspaceKxCluster#dataview_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32aea2831a6f775bd35f3556c79f4942cca438e537aa3b2ccb2e73778f4e544)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument cache_configurations", value=cache_configurations, expected_type=type_hints["cache_configurations"])
            check_type(argname="argument changeset_id", value=changeset_id, expected_type=type_hints["changeset_id"])
            check_type(argname="argument dataview_name", value=dataview_name, expected_type=type_hints["dataview_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
        }
        if cache_configurations is not None:
            self._values["cache_configurations"] = cache_configurations
        if changeset_id is not None:
            self._values["changeset_id"] = changeset_id
        if dataview_name is not None:
            self._values["dataview_name"] = dataview_name

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#database_name FinspaceKxCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cache_configurations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterDatabaseCacheConfigurations"]]]:
        '''cache_configurations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#cache_configurations FinspaceKxCluster#cache_configurations}
        '''
        result = self._values.get("cache_configurations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FinspaceKxClusterDatabaseCacheConfigurations"]]], result)

    @builtins.property
    def changeset_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#changeset_id FinspaceKxCluster#changeset_id}.'''
        result = self._values.get("changeset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataview_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#dataview_name FinspaceKxCluster#dataview_name}.'''
        result = self._values.get("dataview_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterDatabase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterDatabaseCacheConfigurations",
    jsii_struct_bases=[],
    name_mapping={"cache_type": "cacheType", "db_paths": "dbPaths"},
)
class FinspaceKxClusterDatabaseCacheConfigurations:
    def __init__(
        self,
        *,
        cache_type: builtins.str,
        db_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cache_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#cache_type FinspaceKxCluster#cache_type}.
        :param db_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#db_paths FinspaceKxCluster#db_paths}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebabc600fcf9c1c9fd958c37471212cd6148bb14e94ca1f8ead17dcb89d835b1)
            check_type(argname="argument cache_type", value=cache_type, expected_type=type_hints["cache_type"])
            check_type(argname="argument db_paths", value=db_paths, expected_type=type_hints["db_paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_type": cache_type,
        }
        if db_paths is not None:
            self._values["db_paths"] = db_paths

    @builtins.property
    def cache_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#cache_type FinspaceKxCluster#cache_type}.'''
        result = self._values.get("cache_type")
        assert result is not None, "Required property 'cache_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def db_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#db_paths FinspaceKxCluster#db_paths}.'''
        result = self._values.get("db_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterDatabaseCacheConfigurations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FinspaceKxClusterDatabaseCacheConfigurationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterDatabaseCacheConfigurationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a02a0309b12bfb46f1e5a2ad2f2acbacee5c65d14062ff81fc96d7c813965cf9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FinspaceKxClusterDatabaseCacheConfigurationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1daaf9e77b6f425abfb4e2852cd06f90c58f13fcc2b885a29b86d86f2335e9c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FinspaceKxClusterDatabaseCacheConfigurationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4970b88c1367fa628ce079413c59bb70676c1d7b08be6929124a6cecdb966f0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b41a3234fe5e07884471f6f2503808c4b97c62a62666ced8b8ecb3b7b9037e72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__389d3f347cd4fe7439a35917ef8d1099000adaba6b69779a04d9ab6f3eb243d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterDatabaseCacheConfigurations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterDatabaseCacheConfigurations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterDatabaseCacheConfigurations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd5f13ada619896bb7fe89e1de522ef6ff8cc47d3f4eeea19be257133726fa0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FinspaceKxClusterDatabaseCacheConfigurationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterDatabaseCacheConfigurationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f74c6d8fcce460ae188557550efe30f0185d6cf4afe97002fece2dd6175a1ea4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDbPaths")
    def reset_db_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbPaths", []))

    @builtins.property
    @jsii.member(jsii_name="cacheTypeInput")
    def cache_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="dbPathsInput")
    def db_paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dbPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheType")
    def cache_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheType"))

    @cache_type.setter
    def cache_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839df9d7f18f7b9e21d06de2039d5a2454ea032a61c1d5d71fa3755e8929872d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbPaths")
    def db_paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dbPaths"))

    @db_paths.setter
    def db_paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc707c94fea17d274b29b3ecb63ee40c02f93d014c8ecb3a261d522c63c3eeef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterDatabaseCacheConfigurations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterDatabaseCacheConfigurations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterDatabaseCacheConfigurations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3562e8a5d97faee3008ed7e21136d8e336eb5205f16610cd8cef138c359d18f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FinspaceKxClusterDatabaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterDatabaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aab3134533ac2d6bee68e2bf75418d61f9915c96eb78cfb3da8bfaf092320fbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FinspaceKxClusterDatabaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef31f251c10ec92ef05179d9ecebdee439d304b7ef523c4935d86077b6a7d875)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FinspaceKxClusterDatabaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c210ad84b6e225a91325f9b24a212dc1221a0a6ef17c5e49cd60a4b0f2b234)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee46aea5bc745f5f0b5da68892c27408d69879a0c1d9d5b4cf425d3c20a3d4cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37a7c694bdd51b0d6a0281e5154cbaec3be7d7201fe284263eed5664fd64771f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterDatabase]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterDatabase]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterDatabase]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ac818243db3fee47bd1ada76f903dbe56da9124d800e3b2a66797e2f455e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FinspaceKxClusterDatabaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterDatabaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71ac9f46875c0e66f11ae3646be0d61ce4fb7a5ad3c2e4fc14d988cc9bec4610)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCacheConfigurations")
    def put_cache_configurations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterDatabaseCacheConfigurations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e621292ed3c6f8f451dc29cd146d2d5c249821687e591ceb710b9384f779a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCacheConfigurations", [value]))

    @jsii.member(jsii_name="resetCacheConfigurations")
    def reset_cache_configurations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheConfigurations", []))

    @jsii.member(jsii_name="resetChangesetId")
    def reset_changeset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangesetId", []))

    @jsii.member(jsii_name="resetDataviewName")
    def reset_dataview_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataviewName", []))

    @builtins.property
    @jsii.member(jsii_name="cacheConfigurations")
    def cache_configurations(self) -> FinspaceKxClusterDatabaseCacheConfigurationsList:
        return typing.cast(FinspaceKxClusterDatabaseCacheConfigurationsList, jsii.get(self, "cacheConfigurations"))

    @builtins.property
    @jsii.member(jsii_name="cacheConfigurationsInput")
    def cache_configurations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterDatabaseCacheConfigurations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterDatabaseCacheConfigurations]]], jsii.get(self, "cacheConfigurationsInput"))

    @builtins.property
    @jsii.member(jsii_name="changesetIdInput")
    def changeset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "changesetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dataviewNameInput")
    def dataview_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataviewNameInput"))

    @builtins.property
    @jsii.member(jsii_name="changesetId")
    def changeset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "changesetId"))

    @changeset_id.setter
    def changeset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33b6fb26a4941cdf1c2239dc77b11b98afd5f0726b0980783fde6a4c8873e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changesetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a51ab3b7bde838f480aa76a964d59e2f3db4e1e80423bd9568769581925fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataviewName")
    def dataview_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataviewName"))

    @dataview_name.setter
    def dataview_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1405cefd4d9b2c89cde57dc07f3639aefee60266fc5b4358d7cca6ab460d743b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataviewName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterDatabase]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterDatabase]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterDatabase]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98a94befa8c0bdb19e80091276c57e60b5500ecf5bfa3441f36f87b692ad86e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterSavedownStorageConfiguration",
    jsii_struct_bases=[],
    name_mapping={"size": "size", "type": "type", "volume_name": "volumeName"},
)
class FinspaceKxClusterSavedownStorageConfiguration:
    def __init__(
        self,
        *,
        size: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        volume_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#size FinspaceKxCluster#size}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#type FinspaceKxCluster#type}.
        :param volume_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#volume_name FinspaceKxCluster#volume_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38529cd9aae3e6eec33a0fcdb012bbdf17192c0300fb4c0cdbf9aafb3c20194)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument volume_name", value=volume_name, expected_type=type_hints["volume_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size is not None:
            self._values["size"] = size
        if type is not None:
            self._values["type"] = type
        if volume_name is not None:
            self._values["volume_name"] = volume_name

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#size FinspaceKxCluster#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#type FinspaceKxCluster#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#volume_name FinspaceKxCluster#volume_name}.'''
        result = self._values.get("volume_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterSavedownStorageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FinspaceKxClusterSavedownStorageConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterSavedownStorageConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74a30472dde93da92b260d201a25624ed37c04e9ba0156edb1373493f699316a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetVolumeName")
    def reset_volume_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeName", []))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeNameInput")
    def volume_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84fa4286e56fa6453da5e8072038ed5e0e6426db0e08786e250ca575e81be264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f372d6470cb1888e4fdbe7ad9aaea635f7f140b1f071050a59d86054e2a9de1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeName")
    def volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeName"))

    @volume_name.setter
    def volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d744a89bfff6f2d6180ef7f8601ca0929d2bedefb592b7702b495bbb9afe1b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FinspaceKxClusterSavedownStorageConfiguration]:
        return typing.cast(typing.Optional[FinspaceKxClusterSavedownStorageConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FinspaceKxClusterSavedownStorageConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2346562cc4c68d59c5ed8899e999b3ecc44995bb676c0573dc854ea730e03fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterScalingGroupConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "memory_reservation": "memoryReservation",
        "node_count": "nodeCount",
        "scaling_group_name": "scalingGroupName",
        "cpu": "cpu",
        "memory_limit": "memoryLimit",
    },
)
class FinspaceKxClusterScalingGroupConfiguration:
    def __init__(
        self,
        *,
        memory_reservation: jsii.Number,
        node_count: jsii.Number,
        scaling_group_name: builtins.str,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param memory_reservation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#memory_reservation FinspaceKxCluster#memory_reservation}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#node_count FinspaceKxCluster#node_count}.
        :param scaling_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scaling_group_name FinspaceKxCluster#scaling_group_name}.
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#cpu FinspaceKxCluster#cpu}.
        :param memory_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#memory_limit FinspaceKxCluster#memory_limit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e37e4af18a247adc72f92593c7ed2162f6eddeed26360a8606e741e4bde364c)
            check_type(argname="argument memory_reservation", value=memory_reservation, expected_type=type_hints["memory_reservation"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument scaling_group_name", value=scaling_group_name, expected_type=type_hints["scaling_group_name"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "memory_reservation": memory_reservation,
            "node_count": node_count,
            "scaling_group_name": scaling_group_name,
        }
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit

    @builtins.property
    def memory_reservation(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#memory_reservation FinspaceKxCluster#memory_reservation}.'''
        result = self._values.get("memory_reservation")
        assert result is not None, "Required property 'memory_reservation' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#node_count FinspaceKxCluster#node_count}.'''
        result = self._values.get("node_count")
        assert result is not None, "Required property 'node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scaling_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#scaling_group_name FinspaceKxCluster#scaling_group_name}.'''
        result = self._values.get("scaling_group_name")
        assert result is not None, "Required property 'scaling_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#cpu FinspaceKxCluster#cpu}.'''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#memory_limit FinspaceKxCluster#memory_limit}.'''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterScalingGroupConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FinspaceKxClusterScalingGroupConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterScalingGroupConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e964e253ce894448edd7eaf192769b317d74789ee7a640b7067772159c1cd268)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetMemoryLimit")
    def reset_memory_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryLimit", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryLimitInput")
    def memory_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryReservationInput")
    def memory_reservation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryReservationInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingGroupNameInput")
    def scaling_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a179213d82fe5704b709c078a26eafcd15e5a16c64480d8d4324a54af392a27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryLimit")
    def memory_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryLimit"))

    @memory_limit.setter
    def memory_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf66192454afe3b2392c59642563f99634be3c1f095b6499fb0af7220768c983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryReservation")
    def memory_reservation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryReservation"))

    @memory_reservation.setter
    def memory_reservation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a40b0fc08f2c214694b4e08f68711d9e333001683e45d0f03ee5c78d94ea7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryReservation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2308e2fe154462f596905df9b3ba9fc812f49e1a99d43188393317c82976d0ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingGroupName")
    def scaling_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingGroupName"))

    @scaling_group_name.setter
    def scaling_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35900937ec144d1c20e386506bead4ddf3f13b75851d501a70a713248b55ec2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FinspaceKxClusterScalingGroupConfiguration]:
        return typing.cast(typing.Optional[FinspaceKxClusterScalingGroupConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FinspaceKxClusterScalingGroupConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a0cf0f16a5a8df08934d256935ff91af705be6e1ae3ec71de299b533e7e624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterTickerplantLogConfiguration",
    jsii_struct_bases=[],
    name_mapping={"tickerplant_log_volumes": "tickerplantLogVolumes"},
)
class FinspaceKxClusterTickerplantLogConfiguration:
    def __init__(
        self,
        *,
        tickerplant_log_volumes: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param tickerplant_log_volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tickerplant_log_volumes FinspaceKxCluster#tickerplant_log_volumes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2944d77415fd57a886bb8d1c7ba0c22ed9ebc93fe1d8d8311da21f57f0cfc6fe)
            check_type(argname="argument tickerplant_log_volumes", value=tickerplant_log_volumes, expected_type=type_hints["tickerplant_log_volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tickerplant_log_volumes": tickerplant_log_volumes,
        }

    @builtins.property
    def tickerplant_log_volumes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#tickerplant_log_volumes FinspaceKxCluster#tickerplant_log_volumes}.'''
        result = self._values.get("tickerplant_log_volumes")
        assert result is not None, "Required property 'tickerplant_log_volumes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterTickerplantLogConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FinspaceKxClusterTickerplantLogConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterTickerplantLogConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62460615d83f73307160cce1c8877698f5ef2bae24ef8066030c832fd994d25a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FinspaceKxClusterTickerplantLogConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc7b819642d4298decbcb67ac35b617f6f27b9a21aa8f060eba005f52cd498c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FinspaceKxClusterTickerplantLogConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f010707b56157890ce38a8cb79848c79238edb03eb63d878e47b5bb04d643fc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7687b84cfd833e328d3df8c9877745be0b5b28179debf6d37d1ecdc254a3a526)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcc6c681883163e7e676301f0f9864a3b3b69c0298aaa31e64450f207dff362b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterTickerplantLogConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterTickerplantLogConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterTickerplantLogConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1124aa52b2de29823d13f43c1ff1e11db602334ba4b57509e1da9ed4f7720864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FinspaceKxClusterTickerplantLogConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterTickerplantLogConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__039da2177ee19ed765cf3a36be5e709337aede86c0a24559815a8bf54398a6b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="tickerplantLogVolumesInput")
    def tickerplant_log_volumes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tickerplantLogVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="tickerplantLogVolumes")
    def tickerplant_log_volumes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tickerplantLogVolumes"))

    @tickerplant_log_volumes.setter
    def tickerplant_log_volumes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9837d398cdda600095d7b2049312cb58fc106be0f15588e9d913e65cd306f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tickerplantLogVolumes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterTickerplantLogConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterTickerplantLogConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterTickerplantLogConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b6c6a0a36d5c01013d959c771e638e3c23a4f80b71b76ab1542a1d752b47d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FinspaceKxClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#create FinspaceKxCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#delete FinspaceKxCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#update FinspaceKxCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de51a014256f7614d686e898f65458e728b61113370beaf8bcf750e3556ae3a2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#create FinspaceKxCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#delete FinspaceKxCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#update FinspaceKxCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FinspaceKxClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9760835df83a208ba5419ed6c370ab7c783f0057bc72e11e39724baeceb5b2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e30a4dad736ceb13226ad46fb7e362fcd91766e65bfdf64037031732982e59b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdb45918b4dbe49bc8b034de9a83692dcadf58aef61a4aef73724d5874f0ce4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d2a2e1593229c8176a5904f58caea708224b150dbe1fc530f07a429da3d22a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5021c5fc29f35f96e20bb91a094e900f64526cef876dc58647fda11f3989d3f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterVpcConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address_type": "ipAddressType",
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "vpc_id": "vpcId",
    },
)
class FinspaceKxClusterVpcConfiguration:
    def __init__(
        self,
        *,
        ip_address_type: builtins.str,
        security_group_ids: typing.Sequence[builtins.str],
        subnet_ids: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
    ) -> None:
        '''
        :param ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#ip_address_type FinspaceKxCluster#ip_address_type}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#security_group_ids FinspaceKxCluster#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#subnet_ids FinspaceKxCluster#subnet_ids}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#vpc_id FinspaceKxCluster#vpc_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de626a27a057afe947cf4c3e1e15445bbae869e491d98819a789c51855024666)
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_address_type": ip_address_type,
            "security_group_ids": security_group_ids,
            "subnet_ids": subnet_ids,
            "vpc_id": vpc_id,
        }

    @builtins.property
    def ip_address_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#ip_address_type FinspaceKxCluster#ip_address_type}.'''
        result = self._values.get("ip_address_type")
        assert result is not None, "Required property 'ip_address_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#security_group_ids FinspaceKxCluster#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#subnet_ids FinspaceKxCluster#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/finspace_kx_cluster#vpc_id FinspaceKxCluster#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FinspaceKxClusterVpcConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FinspaceKxClusterVpcConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.finspaceKxCluster.FinspaceKxClusterVpcConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4ea5c67c8598c399641703bd172ed00003ea287cb7405d983ac7118dc9360ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ipAddressTypeInput")
    def ip_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressType"))

    @ip_address_type.setter
    def ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8f0a1f8adda3def068bf6f5686658f529bae98ece8bc7ad9eb511fa85fc8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2aeb2290efcaa6762372894ea14fd0e6e62c3910c2e0cb2bc8462c724c1078c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebcdba74fab2595d710d5705739683e6f9c2d6e122a1c5639caba9caaa3e725c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61de946a4069b986d74679799d07e94dedd675060945ca62b1287ccdb14d0f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FinspaceKxClusterVpcConfiguration]:
        return typing.cast(typing.Optional[FinspaceKxClusterVpcConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FinspaceKxClusterVpcConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32042c3bc89013c52b93f303c7a81c98be79f745b4957db22d31cf0ee918e6b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FinspaceKxCluster",
    "FinspaceKxClusterAutoScalingConfiguration",
    "FinspaceKxClusterAutoScalingConfigurationOutputReference",
    "FinspaceKxClusterCacheStorageConfigurations",
    "FinspaceKxClusterCacheStorageConfigurationsList",
    "FinspaceKxClusterCacheStorageConfigurationsOutputReference",
    "FinspaceKxClusterCapacityConfiguration",
    "FinspaceKxClusterCapacityConfigurationOutputReference",
    "FinspaceKxClusterCode",
    "FinspaceKxClusterCodeOutputReference",
    "FinspaceKxClusterConfig",
    "FinspaceKxClusterDatabase",
    "FinspaceKxClusterDatabaseCacheConfigurations",
    "FinspaceKxClusterDatabaseCacheConfigurationsList",
    "FinspaceKxClusterDatabaseCacheConfigurationsOutputReference",
    "FinspaceKxClusterDatabaseList",
    "FinspaceKxClusterDatabaseOutputReference",
    "FinspaceKxClusterSavedownStorageConfiguration",
    "FinspaceKxClusterSavedownStorageConfigurationOutputReference",
    "FinspaceKxClusterScalingGroupConfiguration",
    "FinspaceKxClusterScalingGroupConfigurationOutputReference",
    "FinspaceKxClusterTickerplantLogConfiguration",
    "FinspaceKxClusterTickerplantLogConfigurationList",
    "FinspaceKxClusterTickerplantLogConfigurationOutputReference",
    "FinspaceKxClusterTimeouts",
    "FinspaceKxClusterTimeoutsOutputReference",
    "FinspaceKxClusterVpcConfiguration",
    "FinspaceKxClusterVpcConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__084cae885e4940a4b4fdca41ab42e358a87b4499e5eaccdb480e422c5711913f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    az_mode: builtins.str,
    environment_id: builtins.str,
    name: builtins.str,
    release_label: builtins.str,
    type: builtins.str,
    vpc_configuration: typing.Union[FinspaceKxClusterVpcConfiguration, typing.Dict[builtins.str, typing.Any]],
    auto_scaling_configuration: typing.Optional[typing.Union[FinspaceKxClusterAutoScalingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    availability_zone_id: typing.Optional[builtins.str] = None,
    cache_storage_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterCacheStorageConfigurations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity_configuration: typing.Optional[typing.Union[FinspaceKxClusterCapacityConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    code: typing.Optional[typing.Union[FinspaceKxClusterCode, typing.Dict[builtins.str, typing.Any]]] = None,
    command_line_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    database: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterDatabase, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_role: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initialization_script: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    savedown_storage_configuration: typing.Optional[typing.Union[FinspaceKxClusterSavedownStorageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    scaling_group_configuration: typing.Optional[typing.Union[FinspaceKxClusterScalingGroupConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tickerplant_log_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterTickerplantLogConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[FinspaceKxClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__16227c6c992b430d8b868ef44fe6fe78b4cdb73155224efe58d6938764b60005(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e9e79b2d5ff2cbf81c59f3ab1b25df7f9db951feb3d80acc8eb7f95932fce3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterCacheStorageConfigurations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4facbd15e7bf11129099118b9b70b13b0027954704ffb3f745bcdf147ec23ae0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterDatabase, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c78ca1c764fbed56683e503377fd45a98bb932bed75bc7a13c672e19d9377c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterTickerplantLogConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebda6e30717a18e28d27a944d0f45934c7d0546898a94c7a50abe3d8b1c5ad41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cddbec8daab05828a47e72dc2e860ff649587dfad666a2af77362bf339c18c4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982723df78e0062351d32d2da6cba0610a6ed4bb612d1adf9dad3eb6c3530a29(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fd82bdb5332068baba88d711182ded763bf3767c5f5a3a8285a2239589ddd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5989de11ce6cdf035b274ea15a80eaba32c4e8fd1b9e9dbdede43bee749d0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35dda8236f143f370df2ce4a0ae94da4c41183e9793cb42b8ca698524894dafd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489db78b9d89a59b2c62dca56fff18958857f4fe81f4629425362e1e18f4b9ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99ef2e58a9bcc53789ac55448976ef4cec34c87db65999d181929421612af1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e0113f17674057b8b8601ec4dbcd625ae1dc677d491605c00cea0bd23e4b76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14bb725cc7d369b4ee515589a513e2fb87496c879fb82eb521de6d7c97440132(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdf46c0f9962f964ddf0eee7abc5a595557bebf9418dbdb3a51782262a45a23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967d1f73964f200d8fcde51137f39ddd2dee3af0643150ed8d2ccb289a779914(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2402c8a8541069a33cf2e38464a5e3e6a40a27d5982f923cd1c65adec16cbb7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9937d00dd9b06dab01816e14e4f17927b86b10f784540fe22d587bcf6cebf1c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8a67e1bbdd32b20324c46af9d03bb5219fe2d78f38339f7d77749ce42fddb6(
    *,
    auto_scaling_metric: builtins.str,
    max_node_count: jsii.Number,
    metric_target: jsii.Number,
    min_node_count: jsii.Number,
    scale_in_cooldown_seconds: jsii.Number,
    scale_out_cooldown_seconds: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf0f7dfc21d31873e7f27438e92cadd1cce36989cc880857e86b3bd6503a679(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a4690e94638e3aad305d1e4a5e2d7bd350a936076c3c857ab1a91d5c436a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c9c569e33bcde870460297e82602331873804ce66b9ad176bf5ab285fddc62(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf2aa5f1ede727b42b91d9c81ae12a1436029b515805f182afa530397cfa3fe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a05c1d719c556dbaf224fbc797504c0c9e119d1877360dcbacdd8bd0d57d3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299b183799c2b44339392809fa26b2d46a77dc10e6d5a4c4b0024d38f9055783(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040a2b1dd304081dec4cdce28db71819953961e68d1e3cfe3bafcbccafbf1296(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600ca473c7de82a3de77cd6560b6c48edcafc3496ffb80e1542acb8d8ed06496(
    value: typing.Optional[FinspaceKxClusterAutoScalingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcdab6cb4fadc56f055cb271614486778fec0150002f694be0f3cf64276c74dc(
    *,
    size: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc58c0379a95e28ab9c9e0f8e3821922b3ec72518d4ce71efa41f9778e2f3260(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad6a39f2c9871e9a786ec4b92154110614dc83f7a8cc29e45c5dcf6a2980811(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f995b7e2e90408ac619e6aa6c59e71c1c5d8caaa01e4e2f7de6c0e3f91f2f47d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f16eb6c9896148fe87d9824b00b158414b56a6e2dec33d1a18c8ce9c5ba978(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b881fb8af4edca05c1eed8506e29076d6d50644b8f87780d653522eb09c461(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0dc1a9787a6a8cb092a23d5b03f4fe80ce7f7c8f313b52e23c3adc65c8b503(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterCacheStorageConfigurations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce7c8b77f19fcb77a42dc4f545397470f34489541961ec1734e04d645b7f2a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db579e7d50b17aa0ef8887292d8454eb814068de69ee0d7bf952ff4b08f6774(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23eb77fa81f5ac19b43295eb7816dff861fd7262f3b0b91a9fc61f48887375c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef21ac054bc4aa228deb0bef1e77886db7ff6ed2b0764336a7b30e6d06660ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterCacheStorageConfigurations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6551a11dc554c8c44048a40778cecfa5d40ea2a41a0ca55dce64ba67a8815c41(
    *,
    node_count: jsii.Number,
    node_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6516a3a8cc8ce03ebdbe1149b778b282d5bbdf358cd08567019a12e507da6ffa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44a4943d57ce57e383a77d80fe7fa749fb9003e4f9fa91f7186f1fc44b19d0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf805a3ccf4df6036d1a6c37925b40db67dd4237e9c27773ab31401dfafa1151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc40c8a49ebb2922427493eccc8272770a217ce5384ee78f21999b01553b2fc(
    value: typing.Optional[FinspaceKxClusterCapacityConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0227828dfe63d49d5d7b72772fbc28dbc6dbdbe6ed6b718e954a967823ef5a72(
    *,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
    s3_object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48f226739656cc7493a7c3bb38024e9e34c2d4d92688e98b34830163d899e75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f34fdc3439428669f617d1c0c5b145214fc948436a9e427599af9eda24037f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6318a200f8e01b0c2803ab5bd576cdfa3be7754e208b181c0d4ff4a796d774a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c493801dd45d94e424c39cecdca162bd5f71097aeae0ac9f31d3fdb2dc0b21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5579c3226f440acd98f7eb61c1f90cbd41ba19b1cbc8602ce9aaaa457328e656(
    value: typing.Optional[FinspaceKxClusterCode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d612bf53a57d90d84e893d9340aea36fb94c171d8d8ec714d38a495d606c243f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    az_mode: builtins.str,
    environment_id: builtins.str,
    name: builtins.str,
    release_label: builtins.str,
    type: builtins.str,
    vpc_configuration: typing.Union[FinspaceKxClusterVpcConfiguration, typing.Dict[builtins.str, typing.Any]],
    auto_scaling_configuration: typing.Optional[typing.Union[FinspaceKxClusterAutoScalingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    availability_zone_id: typing.Optional[builtins.str] = None,
    cache_storage_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterCacheStorageConfigurations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity_configuration: typing.Optional[typing.Union[FinspaceKxClusterCapacityConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    code: typing.Optional[typing.Union[FinspaceKxClusterCode, typing.Dict[builtins.str, typing.Any]]] = None,
    command_line_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    database: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterDatabase, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_role: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initialization_script: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    savedown_storage_configuration: typing.Optional[typing.Union[FinspaceKxClusterSavedownStorageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    scaling_group_configuration: typing.Optional[typing.Union[FinspaceKxClusterScalingGroupConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tickerplant_log_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterTickerplantLogConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[FinspaceKxClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32aea2831a6f775bd35f3556c79f4942cca438e537aa3b2ccb2e73778f4e544(
    *,
    database_name: builtins.str,
    cache_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterDatabaseCacheConfigurations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    changeset_id: typing.Optional[builtins.str] = None,
    dataview_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebabc600fcf9c1c9fd958c37471212cd6148bb14e94ca1f8ead17dcb89d835b1(
    *,
    cache_type: builtins.str,
    db_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02a0309b12bfb46f1e5a2ad2f2acbacee5c65d14062ff81fc96d7c813965cf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1daaf9e77b6f425abfb4e2852cd06f90c58f13fcc2b885a29b86d86f2335e9c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4970b88c1367fa628ce079413c59bb70676c1d7b08be6929124a6cecdb966f0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41a3234fe5e07884471f6f2503808c4b97c62a62666ced8b8ecb3b7b9037e72(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389d3f347cd4fe7439a35917ef8d1099000adaba6b69779a04d9ab6f3eb243d3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5f13ada619896bb7fe89e1de522ef6ff8cc47d3f4eeea19be257133726fa0d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterDatabaseCacheConfigurations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74c6d8fcce460ae188557550efe30f0185d6cf4afe97002fece2dd6175a1ea4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839df9d7f18f7b9e21d06de2039d5a2454ea032a61c1d5d71fa3755e8929872d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc707c94fea17d274b29b3ecb63ee40c02f93d014c8ecb3a261d522c63c3eeef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3562e8a5d97faee3008ed7e21136d8e336eb5205f16610cd8cef138c359d18f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterDatabaseCacheConfigurations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab3134533ac2d6bee68e2bf75418d61f9915c96eb78cfb3da8bfaf092320fbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef31f251c10ec92ef05179d9ecebdee439d304b7ef523c4935d86077b6a7d875(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c210ad84b6e225a91325f9b24a212dc1221a0a6ef17c5e49cd60a4b0f2b234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee46aea5bc745f5f0b5da68892c27408d69879a0c1d9d5b4cf425d3c20a3d4cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a7c694bdd51b0d6a0281e5154cbaec3be7d7201fe284263eed5664fd64771f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ac818243db3fee47bd1ada76f903dbe56da9124d800e3b2a66797e2f455e21(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterDatabase]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ac9f46875c0e66f11ae3646be0d61ce4fb7a5ad3c2e4fc14d988cc9bec4610(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e621292ed3c6f8f451dc29cd146d2d5c249821687e591ceb710b9384f779a5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FinspaceKxClusterDatabaseCacheConfigurations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33b6fb26a4941cdf1c2239dc77b11b98afd5f0726b0980783fde6a4c8873e47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a51ab3b7bde838f480aa76a964d59e2f3db4e1e80423bd9568769581925fc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1405cefd4d9b2c89cde57dc07f3639aefee60266fc5b4358d7cca6ab460d743b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98a94befa8c0bdb19e80091276c57e60b5500ecf5bfa3441f36f87b692ad86e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterDatabase]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38529cd9aae3e6eec33a0fcdb012bbdf17192c0300fb4c0cdbf9aafb3c20194(
    *,
    size: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    volume_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a30472dde93da92b260d201a25624ed37c04e9ba0156edb1373493f699316a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84fa4286e56fa6453da5e8072038ed5e0e6426db0e08786e250ca575e81be264(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f372d6470cb1888e4fdbe7ad9aaea635f7f140b1f071050a59d86054e2a9de1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d744a89bfff6f2d6180ef7f8601ca0929d2bedefb592b7702b495bbb9afe1b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2346562cc4c68d59c5ed8899e999b3ecc44995bb676c0573dc854ea730e03fe2(
    value: typing.Optional[FinspaceKxClusterSavedownStorageConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e37e4af18a247adc72f92593c7ed2162f6eddeed26360a8606e741e4bde364c(
    *,
    memory_reservation: jsii.Number,
    node_count: jsii.Number,
    scaling_group_name: builtins.str,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e964e253ce894448edd7eaf192769b317d74789ee7a640b7067772159c1cd268(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a179213d82fe5704b709c078a26eafcd15e5a16c64480d8d4324a54af392a27c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf66192454afe3b2392c59642563f99634be3c1f095b6499fb0af7220768c983(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a40b0fc08f2c214694b4e08f68711d9e333001683e45d0f03ee5c78d94ea7f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2308e2fe154462f596905df9b3ba9fc812f49e1a99d43188393317c82976d0ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35900937ec144d1c20e386506bead4ddf3f13b75851d501a70a713248b55ec2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a0cf0f16a5a8df08934d256935ff91af705be6e1ae3ec71de299b533e7e624(
    value: typing.Optional[FinspaceKxClusterScalingGroupConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2944d77415fd57a886bb8d1c7ba0c22ed9ebc93fe1d8d8311da21f57f0cfc6fe(
    *,
    tickerplant_log_volumes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62460615d83f73307160cce1c8877698f5ef2bae24ef8066030c832fd994d25a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc7b819642d4298decbcb67ac35b617f6f27b9a21aa8f060eba005f52cd498c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f010707b56157890ce38a8cb79848c79238edb03eb63d878e47b5bb04d643fc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7687b84cfd833e328d3df8c9877745be0b5b28179debf6d37d1ecdc254a3a526(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc6c681883163e7e676301f0f9864a3b3b69c0298aaa31e64450f207dff362b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1124aa52b2de29823d13f43c1ff1e11db602334ba4b57509e1da9ed4f7720864(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FinspaceKxClusterTickerplantLogConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039da2177ee19ed765cf3a36be5e709337aede86c0a24559815a8bf54398a6b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9837d398cdda600095d7b2049312cb58fc106be0f15588e9d913e65cd306f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b6c6a0a36d5c01013d959c771e638e3c23a4f80b71b76ab1542a1d752b47d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterTickerplantLogConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de51a014256f7614d686e898f65458e728b61113370beaf8bcf750e3556ae3a2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9760835df83a208ba5419ed6c370ab7c783f0057bc72e11e39724baeceb5b2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e30a4dad736ceb13226ad46fb7e362fcd91766e65bfdf64037031732982e59b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdb45918b4dbe49bc8b034de9a83692dcadf58aef61a4aef73724d5874f0ce4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d2a2e1593229c8176a5904f58caea708224b150dbe1fc530f07a429da3d22a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5021c5fc29f35f96e20bb91a094e900f64526cef876dc58647fda11f3989d3f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FinspaceKxClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de626a27a057afe947cf4c3e1e15445bbae869e491d98819a789c51855024666(
    *,
    ip_address_type: builtins.str,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_ids: typing.Sequence[builtins.str],
    vpc_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ea5c67c8598c399641703bd172ed00003ea287cb7405d983ac7118dc9360ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8f0a1f8adda3def068bf6f5686658f529bae98ece8bc7ad9eb511fa85fc8f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2aeb2290efcaa6762372894ea14fd0e6e62c3910c2e0cb2bc8462c724c1078c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebcdba74fab2595d710d5705739683e6f9c2d6e122a1c5639caba9caaa3e725c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61de946a4069b986d74679799d07e94dedd675060945ca62b1287ccdb14d0f09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32042c3bc89013c52b93f303c7a81c98be79f745b4957db22d31cf0ee918e6b2(
    value: typing.Optional[FinspaceKxClusterVpcConfiguration],
) -> None:
    """Type checking stubs"""
    pass
