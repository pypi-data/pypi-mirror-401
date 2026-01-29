r'''
# `aws_mwaa_environment`

Refer to the Terraform Registry for docs: [`aws_mwaa_environment`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment).
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


class MwaaEnvironment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment aws_mwaa_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dag_s3_path: builtins.str,
        execution_role_arn: builtins.str,
        name: builtins.str,
        network_configuration: typing.Union["MwaaEnvironmentNetworkConfiguration", typing.Dict[builtins.str, typing.Any]],
        source_bucket_arn: builtins.str,
        airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        airflow_version: typing.Optional[builtins.str] = None,
        endpoint_management: typing.Optional[builtins.str] = None,
        environment_class: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        max_webservers: typing.Optional[jsii.Number] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        min_webservers: typing.Optional[jsii.Number] = None,
        min_workers: typing.Optional[jsii.Number] = None,
        plugins_s3_object_version: typing.Optional[builtins.str] = None,
        plugins_s3_path: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        requirements_s3_object_version: typing.Optional[builtins.str] = None,
        requirements_s3_path: typing.Optional[builtins.str] = None,
        schedulers: typing.Optional[jsii.Number] = None,
        startup_script_s3_object_version: typing.Optional[builtins.str] = None,
        startup_script_s3_path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MwaaEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        webserver_access_mode: typing.Optional[builtins.str] = None,
        weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
        worker_replacement_strategy: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment aws_mwaa_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dag_s3_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#dag_s3_path MwaaEnvironment#dag_s3_path}.
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#execution_role_arn MwaaEnvironment#execution_role_arn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#name MwaaEnvironment#name}.
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#network_configuration MwaaEnvironment#network_configuration}
        :param source_bucket_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#source_bucket_arn MwaaEnvironment#source_bucket_arn}.
        :param airflow_configuration_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#airflow_configuration_options MwaaEnvironment#airflow_configuration_options}.
        :param airflow_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#airflow_version MwaaEnvironment#airflow_version}.
        :param endpoint_management: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#endpoint_management MwaaEnvironment#endpoint_management}.
        :param environment_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#environment_class MwaaEnvironment#environment_class}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#id MwaaEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#kms_key MwaaEnvironment#kms_key}.
        :param logging_configuration: logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#logging_configuration MwaaEnvironment#logging_configuration}
        :param max_webservers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#max_webservers MwaaEnvironment#max_webservers}.
        :param max_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#max_workers MwaaEnvironment#max_workers}.
        :param min_webservers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#min_webservers MwaaEnvironment#min_webservers}.
        :param min_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#min_workers MwaaEnvironment#min_workers}.
        :param plugins_s3_object_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#plugins_s3_object_version MwaaEnvironment#plugins_s3_object_version}.
        :param plugins_s3_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#plugins_s3_path MwaaEnvironment#plugins_s3_path}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#region MwaaEnvironment#region}
        :param requirements_s3_object_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#requirements_s3_object_version MwaaEnvironment#requirements_s3_object_version}.
        :param requirements_s3_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#requirements_s3_path MwaaEnvironment#requirements_s3_path}.
        :param schedulers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#schedulers MwaaEnvironment#schedulers}.
        :param startup_script_s3_object_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#startup_script_s3_object_version MwaaEnvironment#startup_script_s3_object_version}.
        :param startup_script_s3_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#startup_script_s3_path MwaaEnvironment#startup_script_s3_path}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#tags MwaaEnvironment#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#tags_all MwaaEnvironment#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#timeouts MwaaEnvironment#timeouts}
        :param webserver_access_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#webserver_access_mode MwaaEnvironment#webserver_access_mode}.
        :param weekly_maintenance_window_start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#weekly_maintenance_window_start MwaaEnvironment#weekly_maintenance_window_start}.
        :param worker_replacement_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#worker_replacement_strategy MwaaEnvironment#worker_replacement_strategy}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5977ee21128ce1c6b8693e4395e52b56a25f95b63da99088043cd4144b23d2a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MwaaEnvironmentConfig(
            dag_s3_path=dag_s3_path,
            execution_role_arn=execution_role_arn,
            name=name,
            network_configuration=network_configuration,
            source_bucket_arn=source_bucket_arn,
            airflow_configuration_options=airflow_configuration_options,
            airflow_version=airflow_version,
            endpoint_management=endpoint_management,
            environment_class=environment_class,
            id=id,
            kms_key=kms_key,
            logging_configuration=logging_configuration,
            max_webservers=max_webservers,
            max_workers=max_workers,
            min_webservers=min_webservers,
            min_workers=min_workers,
            plugins_s3_object_version=plugins_s3_object_version,
            plugins_s3_path=plugins_s3_path,
            region=region,
            requirements_s3_object_version=requirements_s3_object_version,
            requirements_s3_path=requirements_s3_path,
            schedulers=schedulers,
            startup_script_s3_object_version=startup_script_s3_object_version,
            startup_script_s3_path=startup_script_s3_path,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            webserver_access_mode=webserver_access_mode,
            weekly_maintenance_window_start=weekly_maintenance_window_start,
            worker_replacement_strategy=worker_replacement_strategy,
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
        '''Generates CDKTF code for importing a MwaaEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MwaaEnvironment to import.
        :param import_from_id: The id of the existing MwaaEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MwaaEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c212e84767f4426e0edf68bbbd0f0153e7ed90ccc4caa24a2a5690d3155d57)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLoggingConfiguration")
    def put_logging_configuration(
        self,
        *,
        dag_processing_logs: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfigurationDagProcessingLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler_logs: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfigurationSchedulerLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        task_logs: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfigurationTaskLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        webserver_logs: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfigurationWebserverLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_logs: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfigurationWorkerLogs", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dag_processing_logs: dag_processing_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#dag_processing_logs MwaaEnvironment#dag_processing_logs}
        :param scheduler_logs: scheduler_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#scheduler_logs MwaaEnvironment#scheduler_logs}
        :param task_logs: task_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#task_logs MwaaEnvironment#task_logs}
        :param webserver_logs: webserver_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#webserver_logs MwaaEnvironment#webserver_logs}
        :param worker_logs: worker_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#worker_logs MwaaEnvironment#worker_logs}
        '''
        value = MwaaEnvironmentLoggingConfiguration(
            dag_processing_logs=dag_processing_logs,
            scheduler_logs=scheduler_logs,
            task_logs=task_logs,
            webserver_logs=webserver_logs,
            worker_logs=worker_logs,
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfiguration", [value]))

    @jsii.member(jsii_name="putNetworkConfiguration")
    def put_network_configuration(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnet_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#security_group_ids MwaaEnvironment#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#subnet_ids MwaaEnvironment#subnet_ids}.
        '''
        value = MwaaEnvironmentNetworkConfiguration(
            security_group_ids=security_group_ids, subnet_ids=subnet_ids
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#create MwaaEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#delete MwaaEnvironment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#update MwaaEnvironment#update}.
        '''
        value = MwaaEnvironmentTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAirflowConfigurationOptions")
    def reset_airflow_configuration_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAirflowConfigurationOptions", []))

    @jsii.member(jsii_name="resetAirflowVersion")
    def reset_airflow_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAirflowVersion", []))

    @jsii.member(jsii_name="resetEndpointManagement")
    def reset_endpoint_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointManagement", []))

    @jsii.member(jsii_name="resetEnvironmentClass")
    def reset_environment_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentClass", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetLoggingConfiguration")
    def reset_logging_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfiguration", []))

    @jsii.member(jsii_name="resetMaxWebservers")
    def reset_max_webservers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxWebservers", []))

    @jsii.member(jsii_name="resetMaxWorkers")
    def reset_max_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxWorkers", []))

    @jsii.member(jsii_name="resetMinWebservers")
    def reset_min_webservers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinWebservers", []))

    @jsii.member(jsii_name="resetMinWorkers")
    def reset_min_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinWorkers", []))

    @jsii.member(jsii_name="resetPluginsS3ObjectVersion")
    def reset_plugins_s3_object_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginsS3ObjectVersion", []))

    @jsii.member(jsii_name="resetPluginsS3Path")
    def reset_plugins_s3_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginsS3Path", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRequirementsS3ObjectVersion")
    def reset_requirements_s3_object_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequirementsS3ObjectVersion", []))

    @jsii.member(jsii_name="resetRequirementsS3Path")
    def reset_requirements_s3_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequirementsS3Path", []))

    @jsii.member(jsii_name="resetSchedulers")
    def reset_schedulers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulers", []))

    @jsii.member(jsii_name="resetStartupScriptS3ObjectVersion")
    def reset_startup_script_s3_object_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartupScriptS3ObjectVersion", []))

    @jsii.member(jsii_name="resetStartupScriptS3Path")
    def reset_startup_script_s3_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartupScriptS3Path", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWebserverAccessMode")
    def reset_webserver_access_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebserverAccessMode", []))

    @jsii.member(jsii_name="resetWeeklyMaintenanceWindowStart")
    def reset_weekly_maintenance_window_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklyMaintenanceWindowStart", []))

    @jsii.member(jsii_name="resetWorkerReplacementStrategy")
    def reset_worker_replacement_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerReplacementStrategy", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="databaseVpcEndpointService")
    def database_vpc_endpoint_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseVpcEndpointService"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    def last_updated(self) -> "MwaaEnvironmentLastUpdatedList":
        return typing.cast("MwaaEnvironmentLastUpdatedList", jsii.get(self, "lastUpdated"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(
        self,
    ) -> "MwaaEnvironmentLoggingConfigurationOutputReference":
        return typing.cast("MwaaEnvironmentLoggingConfigurationOutputReference", jsii.get(self, "loggingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> "MwaaEnvironmentNetworkConfigurationOutputReference":
        return typing.cast("MwaaEnvironmentNetworkConfigurationOutputReference", jsii.get(self, "networkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRoleArn"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MwaaEnvironmentTimeoutsOutputReference":
        return typing.cast("MwaaEnvironmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="webserverUrl")
    def webserver_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webserverUrl"))

    @builtins.property
    @jsii.member(jsii_name="webserverVpcEndpointService")
    def webserver_vpc_endpoint_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webserverVpcEndpointService"))

    @builtins.property
    @jsii.member(jsii_name="airflowConfigurationOptionsInput")
    def airflow_configuration_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "airflowConfigurationOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="airflowVersionInput")
    def airflow_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "airflowVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="dagS3PathInput")
    def dag_s3_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dagS3PathInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointManagementInput")
    def endpoint_management_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointManagementInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentClassInput")
    def environment_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentClassInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArnInput")
    def execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigurationInput")
    def logging_configuration_input(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfiguration"]:
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfiguration"], jsii.get(self, "loggingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWebserversInput")
    def max_webservers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxWebserversInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWorkersInput")
    def max_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="minWebserversInput")
    def min_webservers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minWebserversInput"))

    @builtins.property
    @jsii.member(jsii_name="minWorkersInput")
    def min_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationInput")
    def network_configuration_input(
        self,
    ) -> typing.Optional["MwaaEnvironmentNetworkConfiguration"]:
        return typing.cast(typing.Optional["MwaaEnvironmentNetworkConfiguration"], jsii.get(self, "networkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginsS3ObjectVersionInput")
    def plugins_s3_object_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginsS3ObjectVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginsS3PathInput")
    def plugins_s3_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginsS3PathInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="requirementsS3ObjectVersionInput")
    def requirements_s3_object_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requirementsS3ObjectVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="requirementsS3PathInput")
    def requirements_s3_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requirementsS3PathInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulersInput")
    def schedulers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "schedulersInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceBucketArnInput")
    def source_bucket_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceBucketArnInput"))

    @builtins.property
    @jsii.member(jsii_name="startupScriptS3ObjectVersionInput")
    def startup_script_s3_object_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startupScriptS3ObjectVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="startupScriptS3PathInput")
    def startup_script_s3_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startupScriptS3PathInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MwaaEnvironmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MwaaEnvironmentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="webserverAccessModeInput")
    def webserver_access_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webserverAccessModeInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyMaintenanceWindowStartInput")
    def weekly_maintenance_window_start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "weeklyMaintenanceWindowStartInput"))

    @builtins.property
    @jsii.member(jsii_name="workerReplacementStrategyInput")
    def worker_replacement_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerReplacementStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="airflowConfigurationOptions")
    def airflow_configuration_options(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "airflowConfigurationOptions"))

    @airflow_configuration_options.setter
    def airflow_configuration_options(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf0b92ce8e52093ceb8d67068476c63600ea8f6746a9a0c1eed0159001c79a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "airflowConfigurationOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="airflowVersion")
    def airflow_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "airflowVersion"))

    @airflow_version.setter
    def airflow_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8961b4ff24e3b20af367ad652c55fe4afa695dcbeaf7ad647df97e13499f8c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "airflowVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dagS3Path")
    def dag_s3_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dagS3Path"))

    @dag_s3_path.setter
    def dag_s3_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f94baadd25fdadd343fcae253e833acd024ab6e6eedbaf03d35a27f4527ef08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dagS3Path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointManagement")
    def endpoint_management(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointManagement"))

    @endpoint_management.setter
    def endpoint_management(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75dee3f9c773dcc9370fc14ce23652bb54d30f24f4d66016c4de6f9fa1bbd29c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointManagement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentClass")
    def environment_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environmentClass"))

    @environment_class.setter
    def environment_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d006fab2672f9535241d7fb7e69b0a9a77a09d954d82714f32a3aebcba8034cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc09ad9d7c9ca631aa7860263fc7ae599fcb2a1dcf889455a35646dc47cd01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8b3c9f3bae29452fd9933af0aab8eceaebff87ba706d96960b9a0b4161f44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0615d2e5763dab97e8ba855cc429c154f03ef578703170809b582facb52adee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWebservers")
    def max_webservers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWebservers"))

    @max_webservers.setter
    def max_webservers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b09914e9411f888b6338466f65db0512f9db67d56e2a92cbf9151a976cbe46d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWebservers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWorkers")
    def max_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWorkers"))

    @max_workers.setter
    def max_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba892308444bf77d7fde1ca6ba507462bc071b5ea2edeb8e96fbe2040b2eace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minWebservers")
    def min_webservers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minWebservers"))

    @min_webservers.setter
    def min_webservers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7358e639e648dce1713c0405aa93868e8ae994c8447c9746aa09a3d3b569fa96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWebservers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minWorkers")
    def min_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minWorkers"))

    @min_workers.setter
    def min_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac496990078376adc537e49b4852d3fd38aa9e01064d1350d8284be90e887f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7682d526881568777ea9b8ae82d8fa3a1c860377f194c8c94abcf7fa300d982d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginsS3ObjectVersion")
    def plugins_s3_object_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginsS3ObjectVersion"))

    @plugins_s3_object_version.setter
    def plugins_s3_object_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c09869d09aa333ea2ae7ea75eb8048a0ce87f193cb339ba48aea74e1be0188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginsS3ObjectVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginsS3Path")
    def plugins_s3_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginsS3Path"))

    @plugins_s3_path.setter
    def plugins_s3_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c929d8d1860d28dde67b27c26b922d5fa9aa866935082c6a55cb5c1f10e2213e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginsS3Path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cdc639397c0b561fcecdcda9d47abf0cf4630d30fa83ec3f648ee6acbba3fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requirementsS3ObjectVersion")
    def requirements_s3_object_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requirementsS3ObjectVersion"))

    @requirements_s3_object_version.setter
    def requirements_s3_object_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f8d40eca981e138dbad607d83fe68be29fefbb556cc2e9972e0a8201369114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirementsS3ObjectVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requirementsS3Path")
    def requirements_s3_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requirementsS3Path"))

    @requirements_s3_path.setter
    def requirements_s3_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae024c5d27370f40859f50f7ff26c36a8521ed0172ee2dce215a8af6ca96504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirementsS3Path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedulers")
    def schedulers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "schedulers"))

    @schedulers.setter
    def schedulers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb03ec1163459190b548a2a6b2741e29199b8caebebbc7b1cb1c741010b86af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedulers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceBucketArn")
    def source_bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceBucketArn"))

    @source_bucket_arn.setter
    def source_bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6241f871a3ebec429735ca05f3a5ec15936a56f82dd9972f91d1658ffa34c4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceBucketArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startupScriptS3ObjectVersion")
    def startup_script_s3_object_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startupScriptS3ObjectVersion"))

    @startup_script_s3_object_version.setter
    def startup_script_s3_object_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce14fe3e69234023a2a39f11b21fa354106138b1eb2e9a8b1728cffa8ae4b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startupScriptS3ObjectVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startupScriptS3Path")
    def startup_script_s3_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startupScriptS3Path"))

    @startup_script_s3_path.setter
    def startup_script_s3_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486c54ae0b9bf5099727c699d89c937071e8a15bfe35103ec0fb6ff46079c251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startupScriptS3Path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df6eb689ee6ef2b33384cde675d5d60a6142c9b812a8039e452db96d614dc53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84504449e771fc2d9c764576af5d14096c377fd80b35d6431571e71739008e08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webserverAccessMode")
    def webserver_access_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webserverAccessMode"))

    @webserver_access_mode.setter
    def webserver_access_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fbb0c31b87e86fa81f05cdd7628a368c4f75ae6285df2b7fb566b7ea12849e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webserverAccessMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeklyMaintenanceWindowStart")
    def weekly_maintenance_window_start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "weeklyMaintenanceWindowStart"))

    @weekly_maintenance_window_start.setter
    def weekly_maintenance_window_start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442454a8475c63fe68dcc560ba0fe1f690489842301348dd72752b2cd9c6461f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeklyMaintenanceWindowStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerReplacementStrategy")
    def worker_replacement_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerReplacementStrategy"))

    @worker_replacement_strategy.setter
    def worker_replacement_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5fbaa8509990d92406197d20f95adf725ada54467cd56c00a28bda6d695fb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerReplacementStrategy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dag_s3_path": "dagS3Path",
        "execution_role_arn": "executionRoleArn",
        "name": "name",
        "network_configuration": "networkConfiguration",
        "source_bucket_arn": "sourceBucketArn",
        "airflow_configuration_options": "airflowConfigurationOptions",
        "airflow_version": "airflowVersion",
        "endpoint_management": "endpointManagement",
        "environment_class": "environmentClass",
        "id": "id",
        "kms_key": "kmsKey",
        "logging_configuration": "loggingConfiguration",
        "max_webservers": "maxWebservers",
        "max_workers": "maxWorkers",
        "min_webservers": "minWebservers",
        "min_workers": "minWorkers",
        "plugins_s3_object_version": "pluginsS3ObjectVersion",
        "plugins_s3_path": "pluginsS3Path",
        "region": "region",
        "requirements_s3_object_version": "requirementsS3ObjectVersion",
        "requirements_s3_path": "requirementsS3Path",
        "schedulers": "schedulers",
        "startup_script_s3_object_version": "startupScriptS3ObjectVersion",
        "startup_script_s3_path": "startupScriptS3Path",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "webserver_access_mode": "webserverAccessMode",
        "weekly_maintenance_window_start": "weeklyMaintenanceWindowStart",
        "worker_replacement_strategy": "workerReplacementStrategy",
    },
)
class MwaaEnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dag_s3_path: builtins.str,
        execution_role_arn: builtins.str,
        name: builtins.str,
        network_configuration: typing.Union["MwaaEnvironmentNetworkConfiguration", typing.Dict[builtins.str, typing.Any]],
        source_bucket_arn: builtins.str,
        airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        airflow_version: typing.Optional[builtins.str] = None,
        endpoint_management: typing.Optional[builtins.str] = None,
        environment_class: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        max_webservers: typing.Optional[jsii.Number] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        min_webservers: typing.Optional[jsii.Number] = None,
        min_workers: typing.Optional[jsii.Number] = None,
        plugins_s3_object_version: typing.Optional[builtins.str] = None,
        plugins_s3_path: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        requirements_s3_object_version: typing.Optional[builtins.str] = None,
        requirements_s3_path: typing.Optional[builtins.str] = None,
        schedulers: typing.Optional[jsii.Number] = None,
        startup_script_s3_object_version: typing.Optional[builtins.str] = None,
        startup_script_s3_path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MwaaEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        webserver_access_mode: typing.Optional[builtins.str] = None,
        weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
        worker_replacement_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dag_s3_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#dag_s3_path MwaaEnvironment#dag_s3_path}.
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#execution_role_arn MwaaEnvironment#execution_role_arn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#name MwaaEnvironment#name}.
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#network_configuration MwaaEnvironment#network_configuration}
        :param source_bucket_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#source_bucket_arn MwaaEnvironment#source_bucket_arn}.
        :param airflow_configuration_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#airflow_configuration_options MwaaEnvironment#airflow_configuration_options}.
        :param airflow_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#airflow_version MwaaEnvironment#airflow_version}.
        :param endpoint_management: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#endpoint_management MwaaEnvironment#endpoint_management}.
        :param environment_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#environment_class MwaaEnvironment#environment_class}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#id MwaaEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#kms_key MwaaEnvironment#kms_key}.
        :param logging_configuration: logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#logging_configuration MwaaEnvironment#logging_configuration}
        :param max_webservers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#max_webservers MwaaEnvironment#max_webservers}.
        :param max_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#max_workers MwaaEnvironment#max_workers}.
        :param min_webservers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#min_webservers MwaaEnvironment#min_webservers}.
        :param min_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#min_workers MwaaEnvironment#min_workers}.
        :param plugins_s3_object_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#plugins_s3_object_version MwaaEnvironment#plugins_s3_object_version}.
        :param plugins_s3_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#plugins_s3_path MwaaEnvironment#plugins_s3_path}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#region MwaaEnvironment#region}
        :param requirements_s3_object_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#requirements_s3_object_version MwaaEnvironment#requirements_s3_object_version}.
        :param requirements_s3_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#requirements_s3_path MwaaEnvironment#requirements_s3_path}.
        :param schedulers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#schedulers MwaaEnvironment#schedulers}.
        :param startup_script_s3_object_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#startup_script_s3_object_version MwaaEnvironment#startup_script_s3_object_version}.
        :param startup_script_s3_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#startup_script_s3_path MwaaEnvironment#startup_script_s3_path}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#tags MwaaEnvironment#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#tags_all MwaaEnvironment#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#timeouts MwaaEnvironment#timeouts}
        :param webserver_access_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#webserver_access_mode MwaaEnvironment#webserver_access_mode}.
        :param weekly_maintenance_window_start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#weekly_maintenance_window_start MwaaEnvironment#weekly_maintenance_window_start}.
        :param worker_replacement_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#worker_replacement_strategy MwaaEnvironment#worker_replacement_strategy}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network_configuration, dict):
            network_configuration = MwaaEnvironmentNetworkConfiguration(**network_configuration)
        if isinstance(logging_configuration, dict):
            logging_configuration = MwaaEnvironmentLoggingConfiguration(**logging_configuration)
        if isinstance(timeouts, dict):
            timeouts = MwaaEnvironmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da1ce7470be0488135d3d60cabfa4a13a4cc7fae58a70ab1903d425868ab974)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dag_s3_path", value=dag_s3_path, expected_type=type_hints["dag_s3_path"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument source_bucket_arn", value=source_bucket_arn, expected_type=type_hints["source_bucket_arn"])
            check_type(argname="argument airflow_configuration_options", value=airflow_configuration_options, expected_type=type_hints["airflow_configuration_options"])
            check_type(argname="argument airflow_version", value=airflow_version, expected_type=type_hints["airflow_version"])
            check_type(argname="argument endpoint_management", value=endpoint_management, expected_type=type_hints["endpoint_management"])
            check_type(argname="argument environment_class", value=environment_class, expected_type=type_hints["environment_class"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument max_webservers", value=max_webservers, expected_type=type_hints["max_webservers"])
            check_type(argname="argument max_workers", value=max_workers, expected_type=type_hints["max_workers"])
            check_type(argname="argument min_webservers", value=min_webservers, expected_type=type_hints["min_webservers"])
            check_type(argname="argument min_workers", value=min_workers, expected_type=type_hints["min_workers"])
            check_type(argname="argument plugins_s3_object_version", value=plugins_s3_object_version, expected_type=type_hints["plugins_s3_object_version"])
            check_type(argname="argument plugins_s3_path", value=plugins_s3_path, expected_type=type_hints["plugins_s3_path"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument requirements_s3_object_version", value=requirements_s3_object_version, expected_type=type_hints["requirements_s3_object_version"])
            check_type(argname="argument requirements_s3_path", value=requirements_s3_path, expected_type=type_hints["requirements_s3_path"])
            check_type(argname="argument schedulers", value=schedulers, expected_type=type_hints["schedulers"])
            check_type(argname="argument startup_script_s3_object_version", value=startup_script_s3_object_version, expected_type=type_hints["startup_script_s3_object_version"])
            check_type(argname="argument startup_script_s3_path", value=startup_script_s3_path, expected_type=type_hints["startup_script_s3_path"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument webserver_access_mode", value=webserver_access_mode, expected_type=type_hints["webserver_access_mode"])
            check_type(argname="argument weekly_maintenance_window_start", value=weekly_maintenance_window_start, expected_type=type_hints["weekly_maintenance_window_start"])
            check_type(argname="argument worker_replacement_strategy", value=worker_replacement_strategy, expected_type=type_hints["worker_replacement_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dag_s3_path": dag_s3_path,
            "execution_role_arn": execution_role_arn,
            "name": name,
            "network_configuration": network_configuration,
            "source_bucket_arn": source_bucket_arn,
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
        if airflow_configuration_options is not None:
            self._values["airflow_configuration_options"] = airflow_configuration_options
        if airflow_version is not None:
            self._values["airflow_version"] = airflow_version
        if endpoint_management is not None:
            self._values["endpoint_management"] = endpoint_management
        if environment_class is not None:
            self._values["environment_class"] = environment_class
        if id is not None:
            self._values["id"] = id
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if max_webservers is not None:
            self._values["max_webservers"] = max_webservers
        if max_workers is not None:
            self._values["max_workers"] = max_workers
        if min_webservers is not None:
            self._values["min_webservers"] = min_webservers
        if min_workers is not None:
            self._values["min_workers"] = min_workers
        if plugins_s3_object_version is not None:
            self._values["plugins_s3_object_version"] = plugins_s3_object_version
        if plugins_s3_path is not None:
            self._values["plugins_s3_path"] = plugins_s3_path
        if region is not None:
            self._values["region"] = region
        if requirements_s3_object_version is not None:
            self._values["requirements_s3_object_version"] = requirements_s3_object_version
        if requirements_s3_path is not None:
            self._values["requirements_s3_path"] = requirements_s3_path
        if schedulers is not None:
            self._values["schedulers"] = schedulers
        if startup_script_s3_object_version is not None:
            self._values["startup_script_s3_object_version"] = startup_script_s3_object_version
        if startup_script_s3_path is not None:
            self._values["startup_script_s3_path"] = startup_script_s3_path
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if webserver_access_mode is not None:
            self._values["webserver_access_mode"] = webserver_access_mode
        if weekly_maintenance_window_start is not None:
            self._values["weekly_maintenance_window_start"] = weekly_maintenance_window_start
        if worker_replacement_strategy is not None:
            self._values["worker_replacement_strategy"] = worker_replacement_strategy

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
    def dag_s3_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#dag_s3_path MwaaEnvironment#dag_s3_path}.'''
        result = self._values.get("dag_s3_path")
        assert result is not None, "Required property 'dag_s3_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#execution_role_arn MwaaEnvironment#execution_role_arn}.'''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#name MwaaEnvironment#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_configuration(self) -> "MwaaEnvironmentNetworkConfiguration":
        '''network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#network_configuration MwaaEnvironment#network_configuration}
        '''
        result = self._values.get("network_configuration")
        assert result is not None, "Required property 'network_configuration' is missing"
        return typing.cast("MwaaEnvironmentNetworkConfiguration", result)

    @builtins.property
    def source_bucket_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#source_bucket_arn MwaaEnvironment#source_bucket_arn}.'''
        result = self._values.get("source_bucket_arn")
        assert result is not None, "Required property 'source_bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def airflow_configuration_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#airflow_configuration_options MwaaEnvironment#airflow_configuration_options}.'''
        result = self._values.get("airflow_configuration_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def airflow_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#airflow_version MwaaEnvironment#airflow_version}.'''
        result = self._values.get("airflow_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_management(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#endpoint_management MwaaEnvironment#endpoint_management}.'''
        result = self._values.get("endpoint_management")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_class(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#environment_class MwaaEnvironment#environment_class}.'''
        result = self._values.get("environment_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#id MwaaEnvironment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#kms_key MwaaEnvironment#kms_key}.'''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfiguration"]:
        '''logging_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#logging_configuration MwaaEnvironment#logging_configuration}
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfiguration"], result)

    @builtins.property
    def max_webservers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#max_webservers MwaaEnvironment#max_webservers}.'''
        result = self._values.get("max_webservers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#max_workers MwaaEnvironment#max_workers}.'''
        result = self._values.get("max_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_webservers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#min_webservers MwaaEnvironment#min_webservers}.'''
        result = self._values.get("min_webservers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#min_workers MwaaEnvironment#min_workers}.'''
        result = self._values.get("min_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def plugins_s3_object_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#plugins_s3_object_version MwaaEnvironment#plugins_s3_object_version}.'''
        result = self._values.get("plugins_s3_object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugins_s3_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#plugins_s3_path MwaaEnvironment#plugins_s3_path}.'''
        result = self._values.get("plugins_s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#region MwaaEnvironment#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requirements_s3_object_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#requirements_s3_object_version MwaaEnvironment#requirements_s3_object_version}.'''
        result = self._values.get("requirements_s3_object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requirements_s3_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#requirements_s3_path MwaaEnvironment#requirements_s3_path}.'''
        result = self._values.get("requirements_s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedulers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#schedulers MwaaEnvironment#schedulers}.'''
        result = self._values.get("schedulers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def startup_script_s3_object_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#startup_script_s3_object_version MwaaEnvironment#startup_script_s3_object_version}.'''
        result = self._values.get("startup_script_s3_object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def startup_script_s3_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#startup_script_s3_path MwaaEnvironment#startup_script_s3_path}.'''
        result = self._values.get("startup_script_s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#tags MwaaEnvironment#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#tags_all MwaaEnvironment#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MwaaEnvironmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#timeouts MwaaEnvironment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MwaaEnvironmentTimeouts"], result)

    @builtins.property
    def webserver_access_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#webserver_access_mode MwaaEnvironment#webserver_access_mode}.'''
        result = self._values.get("webserver_access_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekly_maintenance_window_start(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#weekly_maintenance_window_start MwaaEnvironment#weekly_maintenance_window_start}.'''
        result = self._values.get("weekly_maintenance_window_start")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_replacement_strategy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#worker_replacement_strategy MwaaEnvironment#worker_replacement_strategy}.'''
        result = self._values.get("worker_replacement_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLastUpdated",
    jsii_struct_bases=[],
    name_mapping={},
)
class MwaaEnvironmentLastUpdated:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentLastUpdated(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLastUpdatedError",
    jsii_struct_bases=[],
    name_mapping={},
)
class MwaaEnvironmentLastUpdatedError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentLastUpdatedError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MwaaEnvironmentLastUpdatedErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLastUpdatedErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49226e51dffd71f265ec8e219d601a835d9ccf7ed61193da84f635df0e7e0752)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MwaaEnvironmentLastUpdatedErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e96f5c9e03c31e762aad1c2511dc4b7c93bc6fa78e8814d10eeded56c4cfc2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MwaaEnvironmentLastUpdatedErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f963ca15eb3d00b43d1bc342cec77761d8ce583f78396aa5e40cc16c13d0876b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5508c4f3b91452287f0d044b9924a4d583f3b0b60eba5304e3c9cc78f085c01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f83d8c5b5a35f12566b04dfe9e5d1f748fe4f89adea4be4c272eb0186690675c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MwaaEnvironmentLastUpdatedErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLastUpdatedErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f9405b98941dbc11d38df0f2c8ab4bf27a6c175af50bca073249c29fc811c16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="errorCode")
    def error_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorCode"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MwaaEnvironmentLastUpdatedError]:
        return typing.cast(typing.Optional[MwaaEnvironmentLastUpdatedError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MwaaEnvironmentLastUpdatedError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bddbd587aa5f0b6a00430ef6a854fb54f910d514ef3055675c56ac0fdcc1d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MwaaEnvironmentLastUpdatedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLastUpdatedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e88711214769fec655cc9f301c89f0c727af762193072ee1be676adf1364fb28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MwaaEnvironmentLastUpdatedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6327323ec342c550c7b51dc0140cbe3216283bedfb099c5ddd7fe8bc3f1affa6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MwaaEnvironmentLastUpdatedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed0a0a8f5c29b214891e7cfecd5d73fd42b79d232001b7749cc5383da157360)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd114c844c9d9d80a706f8d106bd436386db5fd3c1671562eaf82495edc605a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dde90f6d0f075ce852400c023882a748f5d992b3d80241c56a6499d2b53bbd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MwaaEnvironmentLastUpdatedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLastUpdatedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6658a3c33595ff0004d7bf35b5af5725144740e8ab8bd64156ff34b8d2816d91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(self) -> MwaaEnvironmentLastUpdatedErrorList:
        return typing.cast(MwaaEnvironmentLastUpdatedErrorList, jsii.get(self, "error"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MwaaEnvironmentLastUpdated]:
        return typing.cast(typing.Optional[MwaaEnvironmentLastUpdated], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MwaaEnvironmentLastUpdated],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd73cf6056e30edaa7f877641d464e975db84d450cf9fdbabc533df177b5037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "dag_processing_logs": "dagProcessingLogs",
        "scheduler_logs": "schedulerLogs",
        "task_logs": "taskLogs",
        "webserver_logs": "webserverLogs",
        "worker_logs": "workerLogs",
    },
)
class MwaaEnvironmentLoggingConfiguration:
    def __init__(
        self,
        *,
        dag_processing_logs: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfigurationDagProcessingLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler_logs: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfigurationSchedulerLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        task_logs: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfigurationTaskLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        webserver_logs: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfigurationWebserverLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_logs: typing.Optional[typing.Union["MwaaEnvironmentLoggingConfigurationWorkerLogs", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dag_processing_logs: dag_processing_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#dag_processing_logs MwaaEnvironment#dag_processing_logs}
        :param scheduler_logs: scheduler_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#scheduler_logs MwaaEnvironment#scheduler_logs}
        :param task_logs: task_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#task_logs MwaaEnvironment#task_logs}
        :param webserver_logs: webserver_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#webserver_logs MwaaEnvironment#webserver_logs}
        :param worker_logs: worker_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#worker_logs MwaaEnvironment#worker_logs}
        '''
        if isinstance(dag_processing_logs, dict):
            dag_processing_logs = MwaaEnvironmentLoggingConfigurationDagProcessingLogs(**dag_processing_logs)
        if isinstance(scheduler_logs, dict):
            scheduler_logs = MwaaEnvironmentLoggingConfigurationSchedulerLogs(**scheduler_logs)
        if isinstance(task_logs, dict):
            task_logs = MwaaEnvironmentLoggingConfigurationTaskLogs(**task_logs)
        if isinstance(webserver_logs, dict):
            webserver_logs = MwaaEnvironmentLoggingConfigurationWebserverLogs(**webserver_logs)
        if isinstance(worker_logs, dict):
            worker_logs = MwaaEnvironmentLoggingConfigurationWorkerLogs(**worker_logs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f1db60d7184a6424d45acbc4a932936c84a6d86e473b391fe4a30ce87bd845)
            check_type(argname="argument dag_processing_logs", value=dag_processing_logs, expected_type=type_hints["dag_processing_logs"])
            check_type(argname="argument scheduler_logs", value=scheduler_logs, expected_type=type_hints["scheduler_logs"])
            check_type(argname="argument task_logs", value=task_logs, expected_type=type_hints["task_logs"])
            check_type(argname="argument webserver_logs", value=webserver_logs, expected_type=type_hints["webserver_logs"])
            check_type(argname="argument worker_logs", value=worker_logs, expected_type=type_hints["worker_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dag_processing_logs is not None:
            self._values["dag_processing_logs"] = dag_processing_logs
        if scheduler_logs is not None:
            self._values["scheduler_logs"] = scheduler_logs
        if task_logs is not None:
            self._values["task_logs"] = task_logs
        if webserver_logs is not None:
            self._values["webserver_logs"] = webserver_logs
        if worker_logs is not None:
            self._values["worker_logs"] = worker_logs

    @builtins.property
    def dag_processing_logs(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfigurationDagProcessingLogs"]:
        '''dag_processing_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#dag_processing_logs MwaaEnvironment#dag_processing_logs}
        '''
        result = self._values.get("dag_processing_logs")
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfigurationDagProcessingLogs"], result)

    @builtins.property
    def scheduler_logs(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfigurationSchedulerLogs"]:
        '''scheduler_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#scheduler_logs MwaaEnvironment#scheduler_logs}
        '''
        result = self._values.get("scheduler_logs")
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfigurationSchedulerLogs"], result)

    @builtins.property
    def task_logs(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfigurationTaskLogs"]:
        '''task_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#task_logs MwaaEnvironment#task_logs}
        '''
        result = self._values.get("task_logs")
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfigurationTaskLogs"], result)

    @builtins.property
    def webserver_logs(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfigurationWebserverLogs"]:
        '''webserver_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#webserver_logs MwaaEnvironment#webserver_logs}
        '''
        result = self._values.get("webserver_logs")
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfigurationWebserverLogs"], result)

    @builtins.property
    def worker_logs(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfigurationWorkerLogs"]:
        '''worker_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#worker_logs MwaaEnvironment#worker_logs}
        '''
        result = self._values.get("worker_logs")
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfigurationWorkerLogs"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentLoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationDagProcessingLogs",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "log_level": "logLevel"},
)
class MwaaEnvironmentLoggingConfigurationDagProcessingLogs:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a9b7d8d9377785f789f20ff4833862b07e8bc2e5c9305a63c3981b62eb20cd)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_level is not None:
            self._values["log_level"] = log_level

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.'''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentLoggingConfigurationDagProcessingLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MwaaEnvironmentLoggingConfigurationDagProcessingLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationDagProcessingLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a69dcedbf51c342a0939aa845b848da284aeb349f326267e947d383999ccd20a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudWatchLogGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__78b2e75bc581442f8fd4e08c7a0aac90fff0afc1ce1cec1e91842388f4da4b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd95abd4ba13cffdb99cece961ec4d68d984bc40eb531e17f049c57d19717c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MwaaEnvironmentLoggingConfigurationDagProcessingLogs]:
        return typing.cast(typing.Optional[MwaaEnvironmentLoggingConfigurationDagProcessingLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MwaaEnvironmentLoggingConfigurationDagProcessingLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75c51b28a34cdb5bf65bb487f46201b9dc8b54e022071b611c94e8667385d92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MwaaEnvironmentLoggingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f4840cddb4d3dce405380aabe22fc6bede4e0e207eb745379f5031fa7f3c847)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDagProcessingLogs")
    def put_dag_processing_logs(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.
        '''
        value = MwaaEnvironmentLoggingConfigurationDagProcessingLogs(
            enabled=enabled, log_level=log_level
        )

        return typing.cast(None, jsii.invoke(self, "putDagProcessingLogs", [value]))

    @jsii.member(jsii_name="putSchedulerLogs")
    def put_scheduler_logs(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.
        '''
        value = MwaaEnvironmentLoggingConfigurationSchedulerLogs(
            enabled=enabled, log_level=log_level
        )

        return typing.cast(None, jsii.invoke(self, "putSchedulerLogs", [value]))

    @jsii.member(jsii_name="putTaskLogs")
    def put_task_logs(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.
        '''
        value = MwaaEnvironmentLoggingConfigurationTaskLogs(
            enabled=enabled, log_level=log_level
        )

        return typing.cast(None, jsii.invoke(self, "putTaskLogs", [value]))

    @jsii.member(jsii_name="putWebserverLogs")
    def put_webserver_logs(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.
        '''
        value = MwaaEnvironmentLoggingConfigurationWebserverLogs(
            enabled=enabled, log_level=log_level
        )

        return typing.cast(None, jsii.invoke(self, "putWebserverLogs", [value]))

    @jsii.member(jsii_name="putWorkerLogs")
    def put_worker_logs(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.
        '''
        value = MwaaEnvironmentLoggingConfigurationWorkerLogs(
            enabled=enabled, log_level=log_level
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerLogs", [value]))

    @jsii.member(jsii_name="resetDagProcessingLogs")
    def reset_dag_processing_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDagProcessingLogs", []))

    @jsii.member(jsii_name="resetSchedulerLogs")
    def reset_scheduler_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulerLogs", []))

    @jsii.member(jsii_name="resetTaskLogs")
    def reset_task_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskLogs", []))

    @jsii.member(jsii_name="resetWebserverLogs")
    def reset_webserver_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebserverLogs", []))

    @jsii.member(jsii_name="resetWorkerLogs")
    def reset_worker_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerLogs", []))

    @builtins.property
    @jsii.member(jsii_name="dagProcessingLogs")
    def dag_processing_logs(
        self,
    ) -> MwaaEnvironmentLoggingConfigurationDagProcessingLogsOutputReference:
        return typing.cast(MwaaEnvironmentLoggingConfigurationDagProcessingLogsOutputReference, jsii.get(self, "dagProcessingLogs"))

    @builtins.property
    @jsii.member(jsii_name="schedulerLogs")
    def scheduler_logs(
        self,
    ) -> "MwaaEnvironmentLoggingConfigurationSchedulerLogsOutputReference":
        return typing.cast("MwaaEnvironmentLoggingConfigurationSchedulerLogsOutputReference", jsii.get(self, "schedulerLogs"))

    @builtins.property
    @jsii.member(jsii_name="taskLogs")
    def task_logs(self) -> "MwaaEnvironmentLoggingConfigurationTaskLogsOutputReference":
        return typing.cast("MwaaEnvironmentLoggingConfigurationTaskLogsOutputReference", jsii.get(self, "taskLogs"))

    @builtins.property
    @jsii.member(jsii_name="webserverLogs")
    def webserver_logs(
        self,
    ) -> "MwaaEnvironmentLoggingConfigurationWebserverLogsOutputReference":
        return typing.cast("MwaaEnvironmentLoggingConfigurationWebserverLogsOutputReference", jsii.get(self, "webserverLogs"))

    @builtins.property
    @jsii.member(jsii_name="workerLogs")
    def worker_logs(
        self,
    ) -> "MwaaEnvironmentLoggingConfigurationWorkerLogsOutputReference":
        return typing.cast("MwaaEnvironmentLoggingConfigurationWorkerLogsOutputReference", jsii.get(self, "workerLogs"))

    @builtins.property
    @jsii.member(jsii_name="dagProcessingLogsInput")
    def dag_processing_logs_input(
        self,
    ) -> typing.Optional[MwaaEnvironmentLoggingConfigurationDagProcessingLogs]:
        return typing.cast(typing.Optional[MwaaEnvironmentLoggingConfigurationDagProcessingLogs], jsii.get(self, "dagProcessingLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulerLogsInput")
    def scheduler_logs_input(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfigurationSchedulerLogs"]:
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfigurationSchedulerLogs"], jsii.get(self, "schedulerLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="taskLogsInput")
    def task_logs_input(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfigurationTaskLogs"]:
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfigurationTaskLogs"], jsii.get(self, "taskLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="webserverLogsInput")
    def webserver_logs_input(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfigurationWebserverLogs"]:
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfigurationWebserverLogs"], jsii.get(self, "webserverLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="workerLogsInput")
    def worker_logs_input(
        self,
    ) -> typing.Optional["MwaaEnvironmentLoggingConfigurationWorkerLogs"]:
        return typing.cast(typing.Optional["MwaaEnvironmentLoggingConfigurationWorkerLogs"], jsii.get(self, "workerLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MwaaEnvironmentLoggingConfiguration]:
        return typing.cast(typing.Optional[MwaaEnvironmentLoggingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MwaaEnvironmentLoggingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00487ed45f9424d3bac9b036339a841f0417f3877b952607f031e807ef093cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationSchedulerLogs",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "log_level": "logLevel"},
)
class MwaaEnvironmentLoggingConfigurationSchedulerLogs:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4604e60cc0c04dd367277969f59c70c00cf43bf0da9da984df386a731ed765e8)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_level is not None:
            self._values["log_level"] = log_level

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.'''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentLoggingConfigurationSchedulerLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MwaaEnvironmentLoggingConfigurationSchedulerLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationSchedulerLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__890199f2c7ed4634490c42ec17b209602dfa9b2e8a3d866fe01dba0bf1f0f8cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudWatchLogGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__52830e543af4ac26e9c07ae310fe306b6b7cc567adf6ef9cd66ad1a730bedd00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e55aacea128fbd2202f72c00600e081ac920553d28580d6dcd398683b1a1804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MwaaEnvironmentLoggingConfigurationSchedulerLogs]:
        return typing.cast(typing.Optional[MwaaEnvironmentLoggingConfigurationSchedulerLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MwaaEnvironmentLoggingConfigurationSchedulerLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80f9faba0157dc22a27c43664d912cf024001ad9363b8693d49f6a08a63b380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationTaskLogs",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "log_level": "logLevel"},
)
class MwaaEnvironmentLoggingConfigurationTaskLogs:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078a2dd053d20963e2c3c34edf77a0db8632d19f8d7186392fbe4d50dd52bc41)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_level is not None:
            self._values["log_level"] = log_level

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.'''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentLoggingConfigurationTaskLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MwaaEnvironmentLoggingConfigurationTaskLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationTaskLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53cd14faca700f7e799059840a82f66fb0dcbde818b5db88a941600ae4ed8f11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudWatchLogGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__16874b9c9e52249c0ddffcdd841fdb8c1feb03be8fe5770c3310351b054e9c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1ccd444989ea083db3f9fed8ecf1e162407c0e22a30de16f2ea02f7102903c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MwaaEnvironmentLoggingConfigurationTaskLogs]:
        return typing.cast(typing.Optional[MwaaEnvironmentLoggingConfigurationTaskLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MwaaEnvironmentLoggingConfigurationTaskLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7f75410a2e256b88ea0b2f1779118edd4463a6a4147295afbbcccd69240edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationWebserverLogs",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "log_level": "logLevel"},
)
class MwaaEnvironmentLoggingConfigurationWebserverLogs:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f80a613ddf0d1bbf30f76b4e8ac8a455cd15ea6da652b9dca923dbb41a7797)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_level is not None:
            self._values["log_level"] = log_level

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.'''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentLoggingConfigurationWebserverLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MwaaEnvironmentLoggingConfigurationWebserverLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationWebserverLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27fbbb9fe47fa170eab03b0f9ae7db9e50a7044d7329eb90b0a343c3f017ce18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudWatchLogGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c7f81c3af08fc52d6009188dfcb7351c8e6e70a1bd26e9543352f8c70fc1f04a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7ce1cce1033c48b51eb3d8a68402ae93000fbc2a9acebb476871e27667528b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MwaaEnvironmentLoggingConfigurationWebserverLogs]:
        return typing.cast(typing.Optional[MwaaEnvironmentLoggingConfigurationWebserverLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MwaaEnvironmentLoggingConfigurationWebserverLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173b0bb4646bd10f2974925af55a7839c0bb9fbb9c650d350ff9a704074b7170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationWorkerLogs",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "log_level": "logLevel"},
)
class MwaaEnvironmentLoggingConfigurationWorkerLogs:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2154f661c47ba17d5118aff2de3386026433859186ac70a2bfa3f3308871734)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_level is not None:
            self._values["log_level"] = log_level

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#enabled MwaaEnvironment#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#log_level MwaaEnvironment#log_level}.'''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentLoggingConfigurationWorkerLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MwaaEnvironmentLoggingConfigurationWorkerLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentLoggingConfigurationWorkerLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__229a32de621984434d5b1768ca30a3d7d28e620c767958b2307fec0a7a81045a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudWatchLogGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2d7e45de2745547420564847c024e7bc166c8fd7e8f91f85754e5c13fe025cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754022f404fd86a501254eea0d5c9abc9b6e51b8045a4a9c24c26951743c3fba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MwaaEnvironmentLoggingConfigurationWorkerLogs]:
        return typing.cast(typing.Optional[MwaaEnvironmentLoggingConfigurationWorkerLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MwaaEnvironmentLoggingConfigurationWorkerLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6458981fcf2be9acb8406305f4ab181a5c0ea013e34f0a8c7a1c9bd28bb6190e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"security_group_ids": "securityGroupIds", "subnet_ids": "subnetIds"},
)
class MwaaEnvironmentNetworkConfiguration:
    def __init__(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnet_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#security_group_ids MwaaEnvironment#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#subnet_ids MwaaEnvironment#subnet_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9674372fc697f0cb6ae9ffa1126f2f209ea41d62fd0d7bcb0b40eccbb69b3c13)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_ids": security_group_ids,
            "subnet_ids": subnet_ids,
        }

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#security_group_ids MwaaEnvironment#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#subnet_ids MwaaEnvironment#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MwaaEnvironmentNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentNetworkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb48948b4862899db45f315b5f1c329d83a2c7d8de3fce4ce02345a2240c38b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f545b485aa998abbd59baa5605f406bb3c0cd6d47d681c278c7bec5cbd805a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00fc3cdccd6b63e10fd54b8f71588f5ec5a48978b1a73db2dc2281c270bf3891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MwaaEnvironmentNetworkConfiguration]:
        return typing.cast(typing.Optional[MwaaEnvironmentNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MwaaEnvironmentNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__473c2f73c1d02a455a8bd979ddb92155c0a5a17aedf759cb8d7d06b68900b66d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MwaaEnvironmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#create MwaaEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#delete MwaaEnvironment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#update MwaaEnvironment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27409c43b3ce697e81468fedb92d6a5b553d781e22f9386efb1d9e656d45ec4e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#create MwaaEnvironment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#delete MwaaEnvironment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mwaa_environment#update MwaaEnvironment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwaaEnvironmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MwaaEnvironmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mwaaEnvironment.MwaaEnvironmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63d79a9945caa4861f422955d684276dfcffdbe4d0e1905ac37b2b23adf89ea0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6610dcfff5f33b57b18f06f930302f493ede67ba963d1af73748c39394e54fae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c3e436e734526815cf64a77d90a1e2050a8324a511e3b5ce485bef74bf8f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9943b8225436fb160812423c5c70a650c3efec788af765c2b599d47b519db02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MwaaEnvironmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MwaaEnvironmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MwaaEnvironmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498b87a8de8f27092cff96df0f38a6e7aee64815aa3056014e151e5336adbc91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MwaaEnvironment",
    "MwaaEnvironmentConfig",
    "MwaaEnvironmentLastUpdated",
    "MwaaEnvironmentLastUpdatedError",
    "MwaaEnvironmentLastUpdatedErrorList",
    "MwaaEnvironmentLastUpdatedErrorOutputReference",
    "MwaaEnvironmentLastUpdatedList",
    "MwaaEnvironmentLastUpdatedOutputReference",
    "MwaaEnvironmentLoggingConfiguration",
    "MwaaEnvironmentLoggingConfigurationDagProcessingLogs",
    "MwaaEnvironmentLoggingConfigurationDagProcessingLogsOutputReference",
    "MwaaEnvironmentLoggingConfigurationOutputReference",
    "MwaaEnvironmentLoggingConfigurationSchedulerLogs",
    "MwaaEnvironmentLoggingConfigurationSchedulerLogsOutputReference",
    "MwaaEnvironmentLoggingConfigurationTaskLogs",
    "MwaaEnvironmentLoggingConfigurationTaskLogsOutputReference",
    "MwaaEnvironmentLoggingConfigurationWebserverLogs",
    "MwaaEnvironmentLoggingConfigurationWebserverLogsOutputReference",
    "MwaaEnvironmentLoggingConfigurationWorkerLogs",
    "MwaaEnvironmentLoggingConfigurationWorkerLogsOutputReference",
    "MwaaEnvironmentNetworkConfiguration",
    "MwaaEnvironmentNetworkConfigurationOutputReference",
    "MwaaEnvironmentTimeouts",
    "MwaaEnvironmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5977ee21128ce1c6b8693e4395e52b56a25f95b63da99088043cd4144b23d2a8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dag_s3_path: builtins.str,
    execution_role_arn: builtins.str,
    name: builtins.str,
    network_configuration: typing.Union[MwaaEnvironmentNetworkConfiguration, typing.Dict[builtins.str, typing.Any]],
    source_bucket_arn: builtins.str,
    airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    airflow_version: typing.Optional[builtins.str] = None,
    endpoint_management: typing.Optional[builtins.str] = None,
    environment_class: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[MwaaEnvironmentLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    max_webservers: typing.Optional[jsii.Number] = None,
    max_workers: typing.Optional[jsii.Number] = None,
    min_webservers: typing.Optional[jsii.Number] = None,
    min_workers: typing.Optional[jsii.Number] = None,
    plugins_s3_object_version: typing.Optional[builtins.str] = None,
    plugins_s3_path: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    requirements_s3_object_version: typing.Optional[builtins.str] = None,
    requirements_s3_path: typing.Optional[builtins.str] = None,
    schedulers: typing.Optional[jsii.Number] = None,
    startup_script_s3_object_version: typing.Optional[builtins.str] = None,
    startup_script_s3_path: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MwaaEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    webserver_access_mode: typing.Optional[builtins.str] = None,
    weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
    worker_replacement_strategy: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__68c212e84767f4426e0edf68bbbd0f0153e7ed90ccc4caa24a2a5690d3155d57(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf0b92ce8e52093ceb8d67068476c63600ea8f6746a9a0c1eed0159001c79a5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8961b4ff24e3b20af367ad652c55fe4afa695dcbeaf7ad647df97e13499f8c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f94baadd25fdadd343fcae253e833acd024ab6e6eedbaf03d35a27f4527ef08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75dee3f9c773dcc9370fc14ce23652bb54d30f24f4d66016c4de6f9fa1bbd29c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d006fab2672f9535241d7fb7e69b0a9a77a09d954d82714f32a3aebcba8034cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc09ad9d7c9ca631aa7860263fc7ae599fcb2a1dcf889455a35646dc47cd01a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8b3c9f3bae29452fd9933af0aab8eceaebff87ba706d96960b9a0b4161f44e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0615d2e5763dab97e8ba855cc429c154f03ef578703170809b582facb52adee1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b09914e9411f888b6338466f65db0512f9db67d56e2a92cbf9151a976cbe46d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba892308444bf77d7fde1ca6ba507462bc071b5ea2edeb8e96fbe2040b2eace(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7358e639e648dce1713c0405aa93868e8ae994c8447c9746aa09a3d3b569fa96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac496990078376adc537e49b4852d3fd38aa9e01064d1350d8284be90e887f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7682d526881568777ea9b8ae82d8fa3a1c860377f194c8c94abcf7fa300d982d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c09869d09aa333ea2ae7ea75eb8048a0ce87f193cb339ba48aea74e1be0188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c929d8d1860d28dde67b27c26b922d5fa9aa866935082c6a55cb5c1f10e2213e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdc639397c0b561fcecdcda9d47abf0cf4630d30fa83ec3f648ee6acbba3fc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f8d40eca981e138dbad607d83fe68be29fefbb556cc2e9972e0a8201369114(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae024c5d27370f40859f50f7ff26c36a8521ed0172ee2dce215a8af6ca96504(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb03ec1163459190b548a2a6b2741e29199b8caebebbc7b1cb1c741010b86af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6241f871a3ebec429735ca05f3a5ec15936a56f82dd9972f91d1658ffa34c4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce14fe3e69234023a2a39f11b21fa354106138b1eb2e9a8b1728cffa8ae4b4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486c54ae0b9bf5099727c699d89c937071e8a15bfe35103ec0fb6ff46079c251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df6eb689ee6ef2b33384cde675d5d60a6142c9b812a8039e452db96d614dc53(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84504449e771fc2d9c764576af5d14096c377fd80b35d6431571e71739008e08(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fbb0c31b87e86fa81f05cdd7628a368c4f75ae6285df2b7fb566b7ea12849e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442454a8475c63fe68dcc560ba0fe1f690489842301348dd72752b2cd9c6461f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5fbaa8509990d92406197d20f95adf725ada54467cd56c00a28bda6d695fb17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da1ce7470be0488135d3d60cabfa4a13a4cc7fae58a70ab1903d425868ab974(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dag_s3_path: builtins.str,
    execution_role_arn: builtins.str,
    name: builtins.str,
    network_configuration: typing.Union[MwaaEnvironmentNetworkConfiguration, typing.Dict[builtins.str, typing.Any]],
    source_bucket_arn: builtins.str,
    airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    airflow_version: typing.Optional[builtins.str] = None,
    endpoint_management: typing.Optional[builtins.str] = None,
    environment_class: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[MwaaEnvironmentLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    max_webservers: typing.Optional[jsii.Number] = None,
    max_workers: typing.Optional[jsii.Number] = None,
    min_webservers: typing.Optional[jsii.Number] = None,
    min_workers: typing.Optional[jsii.Number] = None,
    plugins_s3_object_version: typing.Optional[builtins.str] = None,
    plugins_s3_path: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    requirements_s3_object_version: typing.Optional[builtins.str] = None,
    requirements_s3_path: typing.Optional[builtins.str] = None,
    schedulers: typing.Optional[jsii.Number] = None,
    startup_script_s3_object_version: typing.Optional[builtins.str] = None,
    startup_script_s3_path: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MwaaEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    webserver_access_mode: typing.Optional[builtins.str] = None,
    weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
    worker_replacement_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49226e51dffd71f265ec8e219d601a835d9ccf7ed61193da84f635df0e7e0752(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e96f5c9e03c31e762aad1c2511dc4b7c93bc6fa78e8814d10eeded56c4cfc2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f963ca15eb3d00b43d1bc342cec77761d8ce583f78396aa5e40cc16c13d0876b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5508c4f3b91452287f0d044b9924a4d583f3b0b60eba5304e3c9cc78f085c01(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83d8c5b5a35f12566b04dfe9e5d1f748fe4f89adea4be4c272eb0186690675c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9405b98941dbc11d38df0f2c8ab4bf27a6c175af50bca073249c29fc811c16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bddbd587aa5f0b6a00430ef6a854fb54f910d514ef3055675c56ac0fdcc1d6c(
    value: typing.Optional[MwaaEnvironmentLastUpdatedError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88711214769fec655cc9f301c89f0c727af762193072ee1be676adf1364fb28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6327323ec342c550c7b51dc0140cbe3216283bedfb099c5ddd7fe8bc3f1affa6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed0a0a8f5c29b214891e7cfecd5d73fd42b79d232001b7749cc5383da157360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd114c844c9d9d80a706f8d106bd436386db5fd3c1671562eaf82495edc605a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dde90f6d0f075ce852400c023882a748f5d992b3d80241c56a6499d2b53bbd1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6658a3c33595ff0004d7bf35b5af5725144740e8ab8bd64156ff34b8d2816d91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd73cf6056e30edaa7f877641d464e975db84d450cf9fdbabc533df177b5037(
    value: typing.Optional[MwaaEnvironmentLastUpdated],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f1db60d7184a6424d45acbc4a932936c84a6d86e473b391fe4a30ce87bd845(
    *,
    dag_processing_logs: typing.Optional[typing.Union[MwaaEnvironmentLoggingConfigurationDagProcessingLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduler_logs: typing.Optional[typing.Union[MwaaEnvironmentLoggingConfigurationSchedulerLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    task_logs: typing.Optional[typing.Union[MwaaEnvironmentLoggingConfigurationTaskLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    webserver_logs: typing.Optional[typing.Union[MwaaEnvironmentLoggingConfigurationWebserverLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_logs: typing.Optional[typing.Union[MwaaEnvironmentLoggingConfigurationWorkerLogs, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a9b7d8d9377785f789f20ff4833862b07e8bc2e5c9305a63c3981b62eb20cd(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69dcedbf51c342a0939aa845b848da284aeb349f326267e947d383999ccd20a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b2e75bc581442f8fd4e08c7a0aac90fff0afc1ce1cec1e91842388f4da4b29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd95abd4ba13cffdb99cece961ec4d68d984bc40eb531e17f049c57d19717c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75c51b28a34cdb5bf65bb487f46201b9dc8b54e022071b611c94e8667385d92(
    value: typing.Optional[MwaaEnvironmentLoggingConfigurationDagProcessingLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4840cddb4d3dce405380aabe22fc6bede4e0e207eb745379f5031fa7f3c847(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00487ed45f9424d3bac9b036339a841f0417f3877b952607f031e807ef093cf5(
    value: typing.Optional[MwaaEnvironmentLoggingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4604e60cc0c04dd367277969f59c70c00cf43bf0da9da984df386a731ed765e8(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__890199f2c7ed4634490c42ec17b209602dfa9b2e8a3d866fe01dba0bf1f0f8cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52830e543af4ac26e9c07ae310fe306b6b7cc567adf6ef9cd66ad1a730bedd00(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e55aacea128fbd2202f72c00600e081ac920553d28580d6dcd398683b1a1804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80f9faba0157dc22a27c43664d912cf024001ad9363b8693d49f6a08a63b380(
    value: typing.Optional[MwaaEnvironmentLoggingConfigurationSchedulerLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078a2dd053d20963e2c3c34edf77a0db8632d19f8d7186392fbe4d50dd52bc41(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53cd14faca700f7e799059840a82f66fb0dcbde818b5db88a941600ae4ed8f11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16874b9c9e52249c0ddffcdd841fdb8c1feb03be8fe5770c3310351b054e9c86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1ccd444989ea083db3f9fed8ecf1e162407c0e22a30de16f2ea02f7102903c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7f75410a2e256b88ea0b2f1779118edd4463a6a4147295afbbcccd69240edb(
    value: typing.Optional[MwaaEnvironmentLoggingConfigurationTaskLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f80a613ddf0d1bbf30f76b4e8ac8a455cd15ea6da652b9dca923dbb41a7797(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27fbbb9fe47fa170eab03b0f9ae7db9e50a7044d7329eb90b0a343c3f017ce18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f81c3af08fc52d6009188dfcb7351c8e6e70a1bd26e9543352f8c70fc1f04a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7ce1cce1033c48b51eb3d8a68402ae93000fbc2a9acebb476871e27667528b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173b0bb4646bd10f2974925af55a7839c0bb9fbb9c650d350ff9a704074b7170(
    value: typing.Optional[MwaaEnvironmentLoggingConfigurationWebserverLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2154f661c47ba17d5118aff2de3386026433859186ac70a2bfa3f3308871734(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229a32de621984434d5b1768ca30a3d7d28e620c767958b2307fec0a7a81045a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7e45de2745547420564847c024e7bc166c8fd7e8f91f85754e5c13fe025cd3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754022f404fd86a501254eea0d5c9abc9b6e51b8045a4a9c24c26951743c3fba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6458981fcf2be9acb8406305f4ab181a5c0ea013e34f0a8c7a1c9bd28bb6190e(
    value: typing.Optional[MwaaEnvironmentLoggingConfigurationWorkerLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9674372fc697f0cb6ae9ffa1126f2f209ea41d62fd0d7bcb0b40eccbb69b3c13(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb48948b4862899db45f315b5f1c329d83a2c7d8de3fce4ce02345a2240c38b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f545b485aa998abbd59baa5605f406bb3c0cd6d47d681c278c7bec5cbd805a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00fc3cdccd6b63e10fd54b8f71588f5ec5a48978b1a73db2dc2281c270bf3891(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473c2f73c1d02a455a8bd979ddb92155c0a5a17aedf759cb8d7d06b68900b66d(
    value: typing.Optional[MwaaEnvironmentNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27409c43b3ce697e81468fedb92d6a5b553d781e22f9386efb1d9e656d45ec4e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d79a9945caa4861f422955d684276dfcffdbe4d0e1905ac37b2b23adf89ea0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6610dcfff5f33b57b18f06f930302f493ede67ba963d1af73748c39394e54fae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c3e436e734526815cf64a77d90a1e2050a8324a511e3b5ce485bef74bf8f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9943b8225436fb160812423c5c70a650c3efec788af765c2b599d47b519db02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498b87a8de8f27092cff96df0f38a6e7aee64815aa3056014e151e5336adbc91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MwaaEnvironmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
