r'''
# `aws_emrserverless_application`

Refer to the Terraform Registry for docs: [`aws_emrserverless_application`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application).
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


class EmrserverlessApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application aws_emrserverless_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        release_label: builtins.str,
        type: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        auto_start_configuration: typing.Optional[typing.Union["EmrserverlessApplicationAutoStartConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_stop_configuration: typing.Optional[typing.Union["EmrserverlessApplicationAutoStopConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        image_configuration: typing.Optional[typing.Union["EmrserverlessApplicationImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_capacity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationInitialCapacity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        interactive_configuration: typing.Optional[typing.Union["EmrserverlessApplicationInteractiveConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_capacity: typing.Optional[typing.Union["EmrserverlessApplicationMaximumCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        network_configuration: typing.Optional[typing.Union["EmrserverlessApplicationNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        runtime_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationRuntimeConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheduler_configuration: typing.Optional[typing.Union["EmrserverlessApplicationSchedulerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application aws_emrserverless_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#name EmrserverlessApplication#name}.
        :param release_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#release_label EmrserverlessApplication#release_label}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#type EmrserverlessApplication#type}.
        :param architecture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#architecture EmrserverlessApplication#architecture}.
        :param auto_start_configuration: auto_start_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#auto_start_configuration EmrserverlessApplication#auto_start_configuration}
        :param auto_stop_configuration: auto_stop_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#auto_stop_configuration EmrserverlessApplication#auto_stop_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#id EmrserverlessApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_configuration: image_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#image_configuration EmrserverlessApplication#image_configuration}
        :param initial_capacity: initial_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#initial_capacity EmrserverlessApplication#initial_capacity}
        :param interactive_configuration: interactive_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#interactive_configuration EmrserverlessApplication#interactive_configuration}
        :param maximum_capacity: maximum_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#maximum_capacity EmrserverlessApplication#maximum_capacity}
        :param monitoring_configuration: monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#monitoring_configuration EmrserverlessApplication#monitoring_configuration}
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#network_configuration EmrserverlessApplication#network_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#region EmrserverlessApplication#region}
        :param runtime_configuration: runtime_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#runtime_configuration EmrserverlessApplication#runtime_configuration}
        :param scheduler_configuration: scheduler_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#scheduler_configuration EmrserverlessApplication#scheduler_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#tags EmrserverlessApplication#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#tags_all EmrserverlessApplication#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b5b9c8ec14985f323d8d84a4fc86d9f9b13fa6501669045bceab598e68ad8a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EmrserverlessApplicationConfig(
            name=name,
            release_label=release_label,
            type=type,
            architecture=architecture,
            auto_start_configuration=auto_start_configuration,
            auto_stop_configuration=auto_stop_configuration,
            id=id,
            image_configuration=image_configuration,
            initial_capacity=initial_capacity,
            interactive_configuration=interactive_configuration,
            maximum_capacity=maximum_capacity,
            monitoring_configuration=monitoring_configuration,
            network_configuration=network_configuration,
            region=region,
            runtime_configuration=runtime_configuration,
            scheduler_configuration=scheduler_configuration,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a EmrserverlessApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EmrserverlessApplication to import.
        :param import_from_id: The id of the existing EmrserverlessApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EmrserverlessApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3479eff2d1ddc3bd355a8ade8b7a36cf3eb4a26b6360845b65c7dd0ef0f3893c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoStartConfiguration")
    def put_auto_start_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        '''
        value = EmrserverlessApplicationAutoStartConfiguration(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAutoStartConfiguration", [value]))

    @jsii.member(jsii_name="putAutoStopConfiguration")
    def put_auto_stop_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param idle_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#idle_timeout_minutes EmrserverlessApplication#idle_timeout_minutes}.
        '''
        value = EmrserverlessApplicationAutoStopConfiguration(
            enabled=enabled, idle_timeout_minutes=idle_timeout_minutes
        )

        return typing.cast(None, jsii.invoke(self, "putAutoStopConfiguration", [value]))

    @jsii.member(jsii_name="putImageConfiguration")
    def put_image_configuration(self, *, image_uri: builtins.str) -> None:
        '''
        :param image_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#image_uri EmrserverlessApplication#image_uri}.
        '''
        value = EmrserverlessApplicationImageConfiguration(image_uri=image_uri)

        return typing.cast(None, jsii.invoke(self, "putImageConfiguration", [value]))

    @jsii.member(jsii_name="putInitialCapacity")
    def put_initial_capacity(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationInitialCapacity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ed908b238c50d71e3d7f76b68026b3520a0104e64117a5631b178abc0f4b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInitialCapacity", [value]))

    @jsii.member(jsii_name="putInteractiveConfiguration")
    def put_interactive_configuration(
        self,
        *,
        livy_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        studio_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param livy_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#livy_endpoint_enabled EmrserverlessApplication#livy_endpoint_enabled}.
        :param studio_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#studio_enabled EmrserverlessApplication#studio_enabled}.
        '''
        value = EmrserverlessApplicationInteractiveConfiguration(
            livy_endpoint_enabled=livy_endpoint_enabled, studio_enabled=studio_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putInteractiveConfiguration", [value]))

    @jsii.member(jsii_name="putMaximumCapacity")
    def put_maximum_capacity(
        self,
        *,
        cpu: builtins.str,
        memory: builtins.str,
        disk: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.
        '''
        value = EmrserverlessApplicationMaximumCapacity(
            cpu=cpu, memory=memory, disk=disk
        )

        return typing.cast(None, jsii.invoke(self, "putMaximumCapacity", [value]))

    @jsii.member(jsii_name="putMonitoringConfiguration")
    def put_monitoring_configuration(
        self,
        *,
        cloudwatch_logging_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_persistence_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        prometheus_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_logging_configuration: cloudwatch_logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#cloudwatch_logging_configuration EmrserverlessApplication#cloudwatch_logging_configuration}
        :param managed_persistence_monitoring_configuration: managed_persistence_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#managed_persistence_monitoring_configuration EmrserverlessApplication#managed_persistence_monitoring_configuration}
        :param prometheus_monitoring_configuration: prometheus_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#prometheus_monitoring_configuration EmrserverlessApplication#prometheus_monitoring_configuration}
        :param s3_monitoring_configuration: s3_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#s3_monitoring_configuration EmrserverlessApplication#s3_monitoring_configuration}
        '''
        value = EmrserverlessApplicationMonitoringConfiguration(
            cloudwatch_logging_configuration=cloudwatch_logging_configuration,
            managed_persistence_monitoring_configuration=managed_persistence_monitoring_configuration,
            prometheus_monitoring_configuration=prometheus_monitoring_configuration,
            s3_monitoring_configuration=s3_monitoring_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoringConfiguration", [value]))

    @jsii.member(jsii_name="putNetworkConfiguration")
    def put_network_configuration(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#security_group_ids EmrserverlessApplication#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#subnet_ids EmrserverlessApplication#subnet_ids}.
        '''
        value = EmrserverlessApplicationNetworkConfiguration(
            security_group_ids=security_group_ids, subnet_ids=subnet_ids
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfiguration", [value]))

    @jsii.member(jsii_name="putRuntimeConfiguration")
    def put_runtime_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationRuntimeConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ce2a08281f836fa3d13a69f87fbcb4367416068c958d94cc0d922778f9b9b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRuntimeConfiguration", [value]))

    @jsii.member(jsii_name="putSchedulerConfiguration")
    def put_scheduler_configuration(
        self,
        *,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        queue_timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_runs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#max_concurrent_runs EmrserverlessApplication#max_concurrent_runs}.
        :param queue_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#queue_timeout_minutes EmrserverlessApplication#queue_timeout_minutes}.
        '''
        value = EmrserverlessApplicationSchedulerConfiguration(
            max_concurrent_runs=max_concurrent_runs,
            queue_timeout_minutes=queue_timeout_minutes,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedulerConfiguration", [value]))

    @jsii.member(jsii_name="resetArchitecture")
    def reset_architecture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitecture", []))

    @jsii.member(jsii_name="resetAutoStartConfiguration")
    def reset_auto_start_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoStartConfiguration", []))

    @jsii.member(jsii_name="resetAutoStopConfiguration")
    def reset_auto_stop_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoStopConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageConfiguration")
    def reset_image_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageConfiguration", []))

    @jsii.member(jsii_name="resetInitialCapacity")
    def reset_initial_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialCapacity", []))

    @jsii.member(jsii_name="resetInteractiveConfiguration")
    def reset_interactive_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInteractiveConfiguration", []))

    @jsii.member(jsii_name="resetMaximumCapacity")
    def reset_maximum_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumCapacity", []))

    @jsii.member(jsii_name="resetMonitoringConfiguration")
    def reset_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringConfiguration", []))

    @jsii.member(jsii_name="resetNetworkConfiguration")
    def reset_network_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfiguration", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRuntimeConfiguration")
    def reset_runtime_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeConfiguration", []))

    @jsii.member(jsii_name="resetSchedulerConfiguration")
    def reset_scheduler_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulerConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="autoStartConfiguration")
    def auto_start_configuration(
        self,
    ) -> "EmrserverlessApplicationAutoStartConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationAutoStartConfigurationOutputReference", jsii.get(self, "autoStartConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="autoStopConfiguration")
    def auto_stop_configuration(
        self,
    ) -> "EmrserverlessApplicationAutoStopConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationAutoStopConfigurationOutputReference", jsii.get(self, "autoStopConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="imageConfiguration")
    def image_configuration(
        self,
    ) -> "EmrserverlessApplicationImageConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationImageConfigurationOutputReference", jsii.get(self, "imageConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="initialCapacity")
    def initial_capacity(self) -> "EmrserverlessApplicationInitialCapacityList":
        return typing.cast("EmrserverlessApplicationInitialCapacityList", jsii.get(self, "initialCapacity"))

    @builtins.property
    @jsii.member(jsii_name="interactiveConfiguration")
    def interactive_configuration(
        self,
    ) -> "EmrserverlessApplicationInteractiveConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationInteractiveConfigurationOutputReference", jsii.get(self, "interactiveConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="maximumCapacity")
    def maximum_capacity(
        self,
    ) -> "EmrserverlessApplicationMaximumCapacityOutputReference":
        return typing.cast("EmrserverlessApplicationMaximumCapacityOutputReference", jsii.get(self, "maximumCapacity"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfiguration")
    def monitoring_configuration(
        self,
    ) -> "EmrserverlessApplicationMonitoringConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationMonitoringConfigurationOutputReference", jsii.get(self, "monitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> "EmrserverlessApplicationNetworkConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationNetworkConfigurationOutputReference", jsii.get(self, "networkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfiguration")
    def runtime_configuration(
        self,
    ) -> "EmrserverlessApplicationRuntimeConfigurationList":
        return typing.cast("EmrserverlessApplicationRuntimeConfigurationList", jsii.get(self, "runtimeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="schedulerConfiguration")
    def scheduler_configuration(
        self,
    ) -> "EmrserverlessApplicationSchedulerConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationSchedulerConfigurationOutputReference", jsii.get(self, "schedulerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="autoStartConfigurationInput")
    def auto_start_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationAutoStartConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationAutoStartConfiguration"], jsii.get(self, "autoStartConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoStopConfigurationInput")
    def auto_stop_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationAutoStopConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationAutoStopConfiguration"], jsii.get(self, "autoStopConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageConfigurationInput")
    def image_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationImageConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationImageConfiguration"], jsii.get(self, "imageConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="initialCapacityInput")
    def initial_capacity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationInitialCapacity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationInitialCapacity"]]], jsii.get(self, "initialCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="interactiveConfigurationInput")
    def interactive_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationInteractiveConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationInteractiveConfiguration"], jsii.get(self, "interactiveConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumCapacityInput")
    def maximum_capacity_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMaximumCapacity"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationMaximumCapacity"], jsii.get(self, "maximumCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfigurationInput")
    def monitoring_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfiguration"], jsii.get(self, "monitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationInput")
    def network_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationNetworkConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationNetworkConfiguration"], jsii.get(self, "networkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="releaseLabelInput")
    def release_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releaseLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfigurationInput")
    def runtime_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationRuntimeConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationRuntimeConfiguration"]]], jsii.get(self, "runtimeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulerConfigurationInput")
    def scheduler_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationSchedulerConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationSchedulerConfiguration"], jsii.get(self, "schedulerConfigurationInput"))

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
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5fbc19c465453ff1745b393e7f1b2c08cec62c62098dc03eafd5ef4e216143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c693568f0e90018bcaf2eb05e62830df5d435727acdad72d1492dde6fa21142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b237a0eb5de5058bb900ff4db7f1a363a147398df0ae28352427f50adaf187bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e6e1dc1470c68d9326a44af86372ac18101daf3e6b76984cfb770b3f2b1fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseLabel")
    def release_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseLabel"))

    @release_label.setter
    def release_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faef4d692384d84496bb119613c092063a3094d42de565fd8fb39cd7eb4e774a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943a467dca40b6765941fce09c92405da021c3c4b0f8ca9e0668c5eb081c0141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670943c05a5b47f71bc19c6d39bee1b32cf257b9b4a7dab9c719ba3b20422414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__252bb2bf0dc45941ba7e21417e4f58150d7dbd33b7c42088efd1fdc017436691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationAutoStartConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class EmrserverlessApplicationAutoStartConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb519e9a7a2ec3eae031d6cc23974206caf4378ce3491f3809107d1a12a0dc68)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationAutoStartConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationAutoStartConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationAutoStartConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc2921c144078f5b63610a72c2ce42235fb157bbd8e11120d5871015584c4beb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__609559afc4b3864d1c59fa58210e3c9596fed95c5a5c5a58fc9eecdf0db88268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationAutoStartConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationAutoStartConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationAutoStartConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de02b9fa03e802b2361426596616d2f8ec4ed59d1cbecd9d6e7d5cfbeea1e6f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationAutoStopConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "idle_timeout_minutes": "idleTimeoutMinutes"},
)
class EmrserverlessApplicationAutoStopConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param idle_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#idle_timeout_minutes EmrserverlessApplication#idle_timeout_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d5efe5d055cbcebdbcf40b4203baedde2e7b3e88d29495b91ea2631036c8a8)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument idle_timeout_minutes", value=idle_timeout_minutes, expected_type=type_hints["idle_timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if idle_timeout_minutes is not None:
            self._values["idle_timeout_minutes"] = idle_timeout_minutes

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def idle_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#idle_timeout_minutes EmrserverlessApplication#idle_timeout_minutes}.'''
        result = self._values.get("idle_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationAutoStopConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationAutoStopConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationAutoStopConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__691b5a3d577d176f1c6a0fbdf1c45b312e2e92690ec4a1085d83c3f3f3b807fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetIdleTimeoutMinutes")
    def reset_idle_timeout_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleTimeoutMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutMinutesInput")
    def idle_timeout_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleTimeoutMinutesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0b0ba3ca61209fabbeccd7e9f26b7f3c040b243dc14035ad03810341b160916a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutMinutes")
    def idle_timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleTimeoutMinutes"))

    @idle_timeout_minutes.setter
    def idle_timeout_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30fac42d8b1b40418252550bc709db48c2ccf8998bddb1d85a574ad15585e3de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeoutMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationAutoStopConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationAutoStopConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationAutoStopConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75bf5dd947d56efd2383a2ff1dea7ea89260cd5f3d0f0abba3923dadd30395e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationConfig",
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
        "release_label": "releaseLabel",
        "type": "type",
        "architecture": "architecture",
        "auto_start_configuration": "autoStartConfiguration",
        "auto_stop_configuration": "autoStopConfiguration",
        "id": "id",
        "image_configuration": "imageConfiguration",
        "initial_capacity": "initialCapacity",
        "interactive_configuration": "interactiveConfiguration",
        "maximum_capacity": "maximumCapacity",
        "monitoring_configuration": "monitoringConfiguration",
        "network_configuration": "networkConfiguration",
        "region": "region",
        "runtime_configuration": "runtimeConfiguration",
        "scheduler_configuration": "schedulerConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class EmrserverlessApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        release_label: builtins.str,
        type: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        auto_start_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStartConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_stop_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStopConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        image_configuration: typing.Optional[typing.Union["EmrserverlessApplicationImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_capacity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationInitialCapacity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        interactive_configuration: typing.Optional[typing.Union["EmrserverlessApplicationInteractiveConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_capacity: typing.Optional[typing.Union["EmrserverlessApplicationMaximumCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        network_configuration: typing.Optional[typing.Union["EmrserverlessApplicationNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        runtime_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationRuntimeConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheduler_configuration: typing.Optional[typing.Union["EmrserverlessApplicationSchedulerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#name EmrserverlessApplication#name}.
        :param release_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#release_label EmrserverlessApplication#release_label}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#type EmrserverlessApplication#type}.
        :param architecture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#architecture EmrserverlessApplication#architecture}.
        :param auto_start_configuration: auto_start_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#auto_start_configuration EmrserverlessApplication#auto_start_configuration}
        :param auto_stop_configuration: auto_stop_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#auto_stop_configuration EmrserverlessApplication#auto_stop_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#id EmrserverlessApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_configuration: image_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#image_configuration EmrserverlessApplication#image_configuration}
        :param initial_capacity: initial_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#initial_capacity EmrserverlessApplication#initial_capacity}
        :param interactive_configuration: interactive_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#interactive_configuration EmrserverlessApplication#interactive_configuration}
        :param maximum_capacity: maximum_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#maximum_capacity EmrserverlessApplication#maximum_capacity}
        :param monitoring_configuration: monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#monitoring_configuration EmrserverlessApplication#monitoring_configuration}
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#network_configuration EmrserverlessApplication#network_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#region EmrserverlessApplication#region}
        :param runtime_configuration: runtime_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#runtime_configuration EmrserverlessApplication#runtime_configuration}
        :param scheduler_configuration: scheduler_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#scheduler_configuration EmrserverlessApplication#scheduler_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#tags EmrserverlessApplication#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#tags_all EmrserverlessApplication#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auto_start_configuration, dict):
            auto_start_configuration = EmrserverlessApplicationAutoStartConfiguration(**auto_start_configuration)
        if isinstance(auto_stop_configuration, dict):
            auto_stop_configuration = EmrserverlessApplicationAutoStopConfiguration(**auto_stop_configuration)
        if isinstance(image_configuration, dict):
            image_configuration = EmrserverlessApplicationImageConfiguration(**image_configuration)
        if isinstance(interactive_configuration, dict):
            interactive_configuration = EmrserverlessApplicationInteractiveConfiguration(**interactive_configuration)
        if isinstance(maximum_capacity, dict):
            maximum_capacity = EmrserverlessApplicationMaximumCapacity(**maximum_capacity)
        if isinstance(monitoring_configuration, dict):
            monitoring_configuration = EmrserverlessApplicationMonitoringConfiguration(**monitoring_configuration)
        if isinstance(network_configuration, dict):
            network_configuration = EmrserverlessApplicationNetworkConfiguration(**network_configuration)
        if isinstance(scheduler_configuration, dict):
            scheduler_configuration = EmrserverlessApplicationSchedulerConfiguration(**scheduler_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32760dfe39c0dab9e07ddd983057dc7398096711e8610c08bf5ea10a5d0ac847)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument release_label", value=release_label, expected_type=type_hints["release_label"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument auto_start_configuration", value=auto_start_configuration, expected_type=type_hints["auto_start_configuration"])
            check_type(argname="argument auto_stop_configuration", value=auto_stop_configuration, expected_type=type_hints["auto_stop_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
            check_type(argname="argument initial_capacity", value=initial_capacity, expected_type=type_hints["initial_capacity"])
            check_type(argname="argument interactive_configuration", value=interactive_configuration, expected_type=type_hints["interactive_configuration"])
            check_type(argname="argument maximum_capacity", value=maximum_capacity, expected_type=type_hints["maximum_capacity"])
            check_type(argname="argument monitoring_configuration", value=monitoring_configuration, expected_type=type_hints["monitoring_configuration"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument runtime_configuration", value=runtime_configuration, expected_type=type_hints["runtime_configuration"])
            check_type(argname="argument scheduler_configuration", value=scheduler_configuration, expected_type=type_hints["scheduler_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "release_label": release_label,
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
        if architecture is not None:
            self._values["architecture"] = architecture
        if auto_start_configuration is not None:
            self._values["auto_start_configuration"] = auto_start_configuration
        if auto_stop_configuration is not None:
            self._values["auto_stop_configuration"] = auto_stop_configuration
        if id is not None:
            self._values["id"] = id
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration
        if initial_capacity is not None:
            self._values["initial_capacity"] = initial_capacity
        if interactive_configuration is not None:
            self._values["interactive_configuration"] = interactive_configuration
        if maximum_capacity is not None:
            self._values["maximum_capacity"] = maximum_capacity
        if monitoring_configuration is not None:
            self._values["monitoring_configuration"] = monitoring_configuration
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if region is not None:
            self._values["region"] = region
        if runtime_configuration is not None:
            self._values["runtime_configuration"] = runtime_configuration
        if scheduler_configuration is not None:
            self._values["scheduler_configuration"] = scheduler_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#name EmrserverlessApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def release_label(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#release_label EmrserverlessApplication#release_label}.'''
        result = self._values.get("release_label")
        assert result is not None, "Required property 'release_label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#type EmrserverlessApplication#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#architecture EmrserverlessApplication#architecture}.'''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_start_configuration(
        self,
    ) -> typing.Optional[EmrserverlessApplicationAutoStartConfiguration]:
        '''auto_start_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#auto_start_configuration EmrserverlessApplication#auto_start_configuration}
        '''
        result = self._values.get("auto_start_configuration")
        return typing.cast(typing.Optional[EmrserverlessApplicationAutoStartConfiguration], result)

    @builtins.property
    def auto_stop_configuration(
        self,
    ) -> typing.Optional[EmrserverlessApplicationAutoStopConfiguration]:
        '''auto_stop_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#auto_stop_configuration EmrserverlessApplication#auto_stop_configuration}
        '''
        result = self._values.get("auto_stop_configuration")
        return typing.cast(typing.Optional[EmrserverlessApplicationAutoStopConfiguration], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#id EmrserverlessApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationImageConfiguration"]:
        '''image_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#image_configuration EmrserverlessApplication#image_configuration}
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationImageConfiguration"], result)

    @builtins.property
    def initial_capacity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationInitialCapacity"]]]:
        '''initial_capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#initial_capacity EmrserverlessApplication#initial_capacity}
        '''
        result = self._values.get("initial_capacity")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationInitialCapacity"]]], result)

    @builtins.property
    def interactive_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationInteractiveConfiguration"]:
        '''interactive_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#interactive_configuration EmrserverlessApplication#interactive_configuration}
        '''
        result = self._values.get("interactive_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationInteractiveConfiguration"], result)

    @builtins.property
    def maximum_capacity(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMaximumCapacity"]:
        '''maximum_capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#maximum_capacity EmrserverlessApplication#maximum_capacity}
        '''
        result = self._values.get("maximum_capacity")
        return typing.cast(typing.Optional["EmrserverlessApplicationMaximumCapacity"], result)

    @builtins.property
    def monitoring_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfiguration"]:
        '''monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#monitoring_configuration EmrserverlessApplication#monitoring_configuration}
        '''
        result = self._values.get("monitoring_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfiguration"], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationNetworkConfiguration"]:
        '''network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#network_configuration EmrserverlessApplication#network_configuration}
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationNetworkConfiguration"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#region EmrserverlessApplication#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationRuntimeConfiguration"]]]:
        '''runtime_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#runtime_configuration EmrserverlessApplication#runtime_configuration}
        '''
        result = self._values.get("runtime_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationRuntimeConfiguration"]]], result)

    @builtins.property
    def scheduler_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationSchedulerConfiguration"]:
        '''scheduler_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#scheduler_configuration EmrserverlessApplication#scheduler_configuration}
        '''
        result = self._values.get("scheduler_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationSchedulerConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#tags EmrserverlessApplication#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#tags_all EmrserverlessApplication#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationImageConfiguration",
    jsii_struct_bases=[],
    name_mapping={"image_uri": "imageUri"},
)
class EmrserverlessApplicationImageConfiguration:
    def __init__(self, *, image_uri: builtins.str) -> None:
        '''
        :param image_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#image_uri EmrserverlessApplication#image_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8109f1f74e26c5be4b1abc28dbbe4a206ff9071256f92fa6430a2978e2d1525c)
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_uri": image_uri,
        }

    @builtins.property
    def image_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#image_uri EmrserverlessApplication#image_uri}.'''
        result = self._values.get("image_uri")
        assert result is not None, "Required property 'image_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationImageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationImageConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationImageConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__179d8f145366e5dceb5994632426f33740b8a9aec6b69fb68a9f8d3d6c2a1410)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc23cd604eeb563e5e549bb82a1b946d5b8c9ae2e6fe39bbe98a80036de3fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationImageConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationImageConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationImageConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e16277b861c2da37d1fa42d455d9798d148016f26b5762f3f4a45c4616ab7eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacity",
    jsii_struct_bases=[],
    name_mapping={
        "initial_capacity_type": "initialCapacityType",
        "initial_capacity_config": "initialCapacityConfig",
    },
)
class EmrserverlessApplicationInitialCapacity:
    def __init__(
        self,
        *,
        initial_capacity_type: builtins.str,
        initial_capacity_config: typing.Optional[typing.Union["EmrserverlessApplicationInitialCapacityInitialCapacityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param initial_capacity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#initial_capacity_type EmrserverlessApplication#initial_capacity_type}.
        :param initial_capacity_config: initial_capacity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#initial_capacity_config EmrserverlessApplication#initial_capacity_config}
        '''
        if isinstance(initial_capacity_config, dict):
            initial_capacity_config = EmrserverlessApplicationInitialCapacityInitialCapacityConfig(**initial_capacity_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377e685c269118f040da4c8306a71b392d3730182afcb03b9dbe5e96b1f07764)
            check_type(argname="argument initial_capacity_type", value=initial_capacity_type, expected_type=type_hints["initial_capacity_type"])
            check_type(argname="argument initial_capacity_config", value=initial_capacity_config, expected_type=type_hints["initial_capacity_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "initial_capacity_type": initial_capacity_type,
        }
        if initial_capacity_config is not None:
            self._values["initial_capacity_config"] = initial_capacity_config

    @builtins.property
    def initial_capacity_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#initial_capacity_type EmrserverlessApplication#initial_capacity_type}.'''
        result = self._values.get("initial_capacity_type")
        assert result is not None, "Required property 'initial_capacity_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_capacity_config(
        self,
    ) -> typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfig"]:
        '''initial_capacity_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#initial_capacity_config EmrserverlessApplication#initial_capacity_config}
        '''
        result = self._values.get("initial_capacity_config")
        return typing.cast(typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationInitialCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityInitialCapacityConfig",
    jsii_struct_bases=[],
    name_mapping={
        "worker_count": "workerCount",
        "worker_configuration": "workerConfiguration",
    },
)
class EmrserverlessApplicationInitialCapacityInitialCapacityConfig:
    def __init__(
        self,
        *,
        worker_count: jsii.Number,
        worker_configuration: typing.Optional[typing.Union["EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param worker_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#worker_count EmrserverlessApplication#worker_count}.
        :param worker_configuration: worker_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#worker_configuration EmrserverlessApplication#worker_configuration}
        '''
        if isinstance(worker_configuration, dict):
            worker_configuration = EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration(**worker_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33380cad1a9c928e43e6b4ebaa900c013da7f61c6807efa2399b2885d68137cb)
            check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
            check_type(argname="argument worker_configuration", value=worker_configuration, expected_type=type_hints["worker_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "worker_count": worker_count,
        }
        if worker_configuration is not None:
            self._values["worker_configuration"] = worker_configuration

    @builtins.property
    def worker_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#worker_count EmrserverlessApplication#worker_count}.'''
        result = self._values.get("worker_count")
        assert result is not None, "Required property 'worker_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def worker_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration"]:
        '''worker_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#worker_configuration EmrserverlessApplication#worker_configuration}
        '''
        result = self._values.get("worker_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationInitialCapacityInitialCapacityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationInitialCapacityInitialCapacityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityInitialCapacityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf9737963ebba48a8b64ab3a47802ae37246d006b5c4822bfef60933612bd0ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWorkerConfiguration")
    def put_worker_configuration(
        self,
        *,
        cpu: builtins.str,
        memory: builtins.str,
        disk: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.
        '''
        value = EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration(
            cpu=cpu, memory=memory, disk=disk
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerConfiguration", [value]))

    @jsii.member(jsii_name="resetWorkerConfiguration")
    def reset_worker_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="workerConfiguration")
    def worker_configuration(
        self,
    ) -> "EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfigurationOutputReference", jsii.get(self, "workerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="workerConfigurationInput")
    def worker_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration"], jsii.get(self, "workerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="workerCountInput")
    def worker_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "workerCountInput"))

    @builtins.property
    @jsii.member(jsii_name="workerCount")
    def worker_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "workerCount"))

    @worker_count.setter
    def worker_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a25c569060367751d61f89decc140e4fecb16c9d40df8a85e52acb540dcb414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig]:
        return typing.cast(typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc78676651977edea4b72caa1a63c91f5edf5748a57cde6c72a914b743b2678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory", "disk": "disk"},
)
class EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration:
    def __init__(
        self,
        *,
        cpu: builtins.str,
        memory: builtins.str,
        disk: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307a965e64cc6b665cb828181bdc249ca3552b13b2c9f1c4d6bc5e48c8323730)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
            "memory": memory,
        }
        if disk is not None:
            self._values["disk"] = disk

    @builtins.property
    def cpu(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.'''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def memory(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.'''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.'''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32b85203790b2d264929469ed1046d6a531adc9cc050c4be1da72fd175e064a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisk")
    def reset_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisk", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebfe75a937be2093bcf9ab51e8c9950f746bee0584d453ef4c217b1779f7bccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disk"))

    @disk.setter
    def disk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9afe601db63e5630af378967fc3174fe9a10ee70399bfc24abac63847825931b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a263e34f400075b2b4d4cacb193cc78a390e66b68a30eba9e1fd91293ed9e3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee390f005cbcc6c0b356fcd9073a86d4823efb32f5946d468ace6846810aaf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationInitialCapacityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a52e9f578d5b77c8c2213847a07d275499d905bf3d02137faa70e9fbdc4c45f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EmrserverlessApplicationInitialCapacityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f780694a420491be1867fd92e3d02ca3e69c71982505a3e1c034641def063dc6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EmrserverlessApplicationInitialCapacityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36dea75bf0b67a305838c8eca048ed8db9185fe8e991ef1e7a53cf562452f4b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa3e1a3a5fbaa2a574d2ce09196a796005174526b1ed33573030cda7827cfa4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80bd9e39d97bf9ec7c28b19de746f137412810c5dc710f4eb933e1840c0e3e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationInitialCapacity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationInitialCapacity]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationInitialCapacity]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__226c22281df0a35c6b2f3c8182905953ec2dcf1187a95c3b32eb56b4e48c4e42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationInitialCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d847f506627ba83fb14e54bcf891bd0f29186231a0f48090b4069783d16abe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInitialCapacityConfig")
    def put_initial_capacity_config(
        self,
        *,
        worker_count: jsii.Number,
        worker_configuration: typing.Optional[typing.Union[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param worker_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#worker_count EmrserverlessApplication#worker_count}.
        :param worker_configuration: worker_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#worker_configuration EmrserverlessApplication#worker_configuration}
        '''
        value = EmrserverlessApplicationInitialCapacityInitialCapacityConfig(
            worker_count=worker_count, worker_configuration=worker_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putInitialCapacityConfig", [value]))

    @jsii.member(jsii_name="resetInitialCapacityConfig")
    def reset_initial_capacity_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialCapacityConfig", []))

    @builtins.property
    @jsii.member(jsii_name="initialCapacityConfig")
    def initial_capacity_config(
        self,
    ) -> EmrserverlessApplicationInitialCapacityInitialCapacityConfigOutputReference:
        return typing.cast(EmrserverlessApplicationInitialCapacityInitialCapacityConfigOutputReference, jsii.get(self, "initialCapacityConfig"))

    @builtins.property
    @jsii.member(jsii_name="initialCapacityConfigInput")
    def initial_capacity_config_input(
        self,
    ) -> typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig]:
        return typing.cast(typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig], jsii.get(self, "initialCapacityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="initialCapacityTypeInput")
    def initial_capacity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initialCapacityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="initialCapacityType")
    def initial_capacity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initialCapacityType"))

    @initial_capacity_type.setter
    def initial_capacity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05d2b925023b6da3f1ad1ec033813c851dfc3b6c7f2b1f052e6bc4af023785e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialCapacityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationInitialCapacity]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationInitialCapacity]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationInitialCapacity]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55635adc8b9d30764273b4901c7c9888838210c91d63ff9cd697b3edb7d02134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationInteractiveConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "livy_endpoint_enabled": "livyEndpointEnabled",
        "studio_enabled": "studioEnabled",
    },
)
class EmrserverlessApplicationInteractiveConfiguration:
    def __init__(
        self,
        *,
        livy_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        studio_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param livy_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#livy_endpoint_enabled EmrserverlessApplication#livy_endpoint_enabled}.
        :param studio_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#studio_enabled EmrserverlessApplication#studio_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f0fe5b32d58a28556cc468d988191ab84fac77226724e489073ef08b6f9f74)
            check_type(argname="argument livy_endpoint_enabled", value=livy_endpoint_enabled, expected_type=type_hints["livy_endpoint_enabled"])
            check_type(argname="argument studio_enabled", value=studio_enabled, expected_type=type_hints["studio_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if livy_endpoint_enabled is not None:
            self._values["livy_endpoint_enabled"] = livy_endpoint_enabled
        if studio_enabled is not None:
            self._values["studio_enabled"] = studio_enabled

    @builtins.property
    def livy_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#livy_endpoint_enabled EmrserverlessApplication#livy_endpoint_enabled}.'''
        result = self._values.get("livy_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def studio_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#studio_enabled EmrserverlessApplication#studio_enabled}.'''
        result = self._values.get("studio_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationInteractiveConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationInteractiveConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationInteractiveConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c00632cf20e95d303142058a03ffc39028988fe469a10833b86096200f360520)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLivyEndpointEnabled")
    def reset_livy_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLivyEndpointEnabled", []))

    @jsii.member(jsii_name="resetStudioEnabled")
    def reset_studio_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStudioEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="livyEndpointEnabledInput")
    def livy_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "livyEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="studioEnabledInput")
    def studio_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "studioEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="livyEndpointEnabled")
    def livy_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "livyEndpointEnabled"))

    @livy_endpoint_enabled.setter
    def livy_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1852e7a5d0d20976086d370b4e549ed7d3d0d61a174af4cdd1ee8fe85202729d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "livyEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="studioEnabled")
    def studio_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "studioEnabled"))

    @studio_enabled.setter
    def studio_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0044f9135f75838e3016e19d931596bc6bb51987e5f71975d00c9d7fdea465f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "studioEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationInteractiveConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationInteractiveConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationInteractiveConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d5d41ad2ea15408946a8f6cfd360bd0d348b4e13d8c116266e757a3d4d5ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMaximumCapacity",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory", "disk": "disk"},
)
class EmrserverlessApplicationMaximumCapacity:
    def __init__(
        self,
        *,
        cpu: builtins.str,
        memory: builtins.str,
        disk: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0444b98bf1f077817a389d0fc72edce3610588df5508bb49fe50fc764b18ca83)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
            "memory": memory,
        }
        if disk is not None:
            self._values["disk"] = disk

    @builtins.property
    def cpu(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.'''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def memory(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.'''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.'''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMaximumCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationMaximumCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMaximumCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e59ab9f22198d4bf3a5bee0a65e3ff935cfa3aa57de1479c4183c3d3d99a245)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisk")
    def reset_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisk", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d21c9633ba9ed78e77a8f24cb8c1608fc4a56718189d6dc7a7d3731966b72cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disk"))

    @disk.setter
    def disk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efe7f6f0516984f9d03ff2e64dfb804c184d89be566a1d4a72ce7f85619e130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9638ad5b0e9e86f09957d869dc1682a5bbff14fd392e12ad47f948cde584f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMaximumCapacity]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMaximumCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMaximumCapacity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3891fef2a55e3fae459f2ceb4063f6402c8679f7f20bbdaf69f689f22e83c2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_logging_configuration": "cloudwatchLoggingConfiguration",
        "managed_persistence_monitoring_configuration": "managedPersistenceMonitoringConfiguration",
        "prometheus_monitoring_configuration": "prometheusMonitoringConfiguration",
        "s3_monitoring_configuration": "s3MonitoringConfiguration",
    },
)
class EmrserverlessApplicationMonitoringConfiguration:
    def __init__(
        self,
        *,
        cloudwatch_logging_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_persistence_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        prometheus_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_logging_configuration: cloudwatch_logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#cloudwatch_logging_configuration EmrserverlessApplication#cloudwatch_logging_configuration}
        :param managed_persistence_monitoring_configuration: managed_persistence_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#managed_persistence_monitoring_configuration EmrserverlessApplication#managed_persistence_monitoring_configuration}
        :param prometheus_monitoring_configuration: prometheus_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#prometheus_monitoring_configuration EmrserverlessApplication#prometheus_monitoring_configuration}
        :param s3_monitoring_configuration: s3_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#s3_monitoring_configuration EmrserverlessApplication#s3_monitoring_configuration}
        '''
        if isinstance(cloudwatch_logging_configuration, dict):
            cloudwatch_logging_configuration = EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration(**cloudwatch_logging_configuration)
        if isinstance(managed_persistence_monitoring_configuration, dict):
            managed_persistence_monitoring_configuration = EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration(**managed_persistence_monitoring_configuration)
        if isinstance(prometheus_monitoring_configuration, dict):
            prometheus_monitoring_configuration = EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration(**prometheus_monitoring_configuration)
        if isinstance(s3_monitoring_configuration, dict):
            s3_monitoring_configuration = EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration(**s3_monitoring_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19a84b16abefd8bb502dbfd2acdd085afc3d8a8626b2cf393d1f01f1ef36d9a)
            check_type(argname="argument cloudwatch_logging_configuration", value=cloudwatch_logging_configuration, expected_type=type_hints["cloudwatch_logging_configuration"])
            check_type(argname="argument managed_persistence_monitoring_configuration", value=managed_persistence_monitoring_configuration, expected_type=type_hints["managed_persistence_monitoring_configuration"])
            check_type(argname="argument prometheus_monitoring_configuration", value=prometheus_monitoring_configuration, expected_type=type_hints["prometheus_monitoring_configuration"])
            check_type(argname="argument s3_monitoring_configuration", value=s3_monitoring_configuration, expected_type=type_hints["s3_monitoring_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_logging_configuration is not None:
            self._values["cloudwatch_logging_configuration"] = cloudwatch_logging_configuration
        if managed_persistence_monitoring_configuration is not None:
            self._values["managed_persistence_monitoring_configuration"] = managed_persistence_monitoring_configuration
        if prometheus_monitoring_configuration is not None:
            self._values["prometheus_monitoring_configuration"] = prometheus_monitoring_configuration
        if s3_monitoring_configuration is not None:
            self._values["s3_monitoring_configuration"] = s3_monitoring_configuration

    @builtins.property
    def cloudwatch_logging_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration"]:
        '''cloudwatch_logging_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#cloudwatch_logging_configuration EmrserverlessApplication#cloudwatch_logging_configuration}
        '''
        result = self._values.get("cloudwatch_logging_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration"], result)

    @builtins.property
    def managed_persistence_monitoring_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration"]:
        '''managed_persistence_monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#managed_persistence_monitoring_configuration EmrserverlessApplication#managed_persistence_monitoring_configuration}
        '''
        result = self._values.get("managed_persistence_monitoring_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration"], result)

    @builtins.property
    def prometheus_monitoring_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration"]:
        '''prometheus_monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#prometheus_monitoring_configuration EmrserverlessApplication#prometheus_monitoring_configuration}
        '''
        result = self._values.get("prometheus_monitoring_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration"], result)

    @builtins.property
    def s3_monitoring_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration"]:
        '''s3_monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#s3_monitoring_configuration EmrserverlessApplication#s3_monitoring_configuration}
        '''
        result = self._values.get("s3_monitoring_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "encryption_key_arn": "encryptionKeyArn",
        "log_group_name": "logGroupName",
        "log_stream_name_prefix": "logStreamNamePrefix",
        "log_types": "logTypes",
    },
)
class EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        encryption_key_arn: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name_prefix: typing.Optional[builtins.str] = None,
        log_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_group_name EmrserverlessApplication#log_group_name}.
        :param log_stream_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_stream_name_prefix EmrserverlessApplication#log_stream_name_prefix}.
        :param log_types: log_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_types EmrserverlessApplication#log_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5447184df8e677c3d516e0f5aa1ba516507bf514fe7ec0126c2788de14abffc)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name_prefix", value=log_stream_name_prefix, expected_type=type_hints["log_stream_name_prefix"])
            check_type(argname="argument log_types", value=log_types, expected_type=type_hints["log_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name_prefix is not None:
            self._values["log_stream_name_prefix"] = log_stream_name_prefix
        if log_types is not None:
            self._values["log_types"] = log_types

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.'''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_group_name EmrserverlessApplication#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_stream_name_prefix EmrserverlessApplication#log_stream_name_prefix}.'''
        result = self._values.get("log_stream_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes"]]]:
        '''log_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_types EmrserverlessApplication#log_types}
        '''
        result = self._values.get("log_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#name EmrserverlessApplication#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#values EmrserverlessApplication#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746c695579bcec43d4e262d02f7f3cdfd74c61f1ca2331f79ca503e550634f6f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#name EmrserverlessApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#values EmrserverlessApplication#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29af38c789f0f355a2b75de563c94bcc9a8c80fbe0f44c3aa3c5867ce6c60e9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557ba5b9bef9e18862be5a142ea150d4b7d723c53b510192af2a452d52b39416)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d49879628c74d79f1ac8b3e0309f01beb56780bea6e42facf9c3a34a1d9d546)
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
            type_hints = typing.get_type_hints(_typecheckingstub__255ee46611571fc3d7a11321a0b32e12b595ddb71f87b7c4cd4277f5edc17cf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a10b619ee8784c1a8846cec00ea8f99a04a3ee69527e043b7e5c1bd4fa2cbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e973759d1d77127199c413cc7cf464261a582256208d11f0a5c85423ebe5667b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73429b8b14a30a5b796c34d8974807ed9153fdfe63ef20df528edf04c9666e50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0f619889305cbb865e27b54a6b7e433bb5436a7167ccfb819d318025a8d0c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65bebb7f4a39f9a500aaa69168d295d08e7c773b943ab1398a2f00ea18dd90e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9416325aed76904ecbed3b0bea55f57e3541504a127f57969bb5fe6434dd90a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a6d9bb3685d41fbd5ec33ad7c06b40fdd39fead9ca657ab3cab0c2c3015322d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLogTypes")
    def put_log_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45271b0286c457b9459ec587c84b7bec30a7b439ec4bda7a2267caacb65e99ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogTypes", [value]))

    @jsii.member(jsii_name="resetEncryptionKeyArn")
    def reset_encryption_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyArn", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogStreamNamePrefix")
    def reset_log_stream_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamNamePrefix", []))

    @jsii.member(jsii_name="resetLogTypes")
    def reset_log_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogTypes", []))

    @builtins.property
    @jsii.member(jsii_name="logTypes")
    def log_types(
        self,
    ) -> EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesList:
        return typing.cast(EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesList, jsii.get(self, "logTypes"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArnInput")
    def encryption_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNamePrefixInput")
    def log_stream_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="logTypesInput")
    def log_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]], jsii.get(self, "logTypesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fa0fc93ccc74691a0ca16c206be9bf543ba9aadea7f4be53839f7617426e69ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArn")
    def encryption_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeyArn"))

    @encryption_key_arn.setter
    def encryption_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860a9ff367289bfa5070826a22ca0fd290e663c0aaa8c0350e1d15e2f04ae9ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03979a183dedf6c46b75d8528a73df6636171c9f10f11ea91a74f4cb53e09221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamNamePrefix")
    def log_stream_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamNamePrefix"))

    @log_stream_name_prefix.setter
    def log_stream_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaae3efa0b67b9559ef2fbc022c9b39885682571b62e42b52e093d64c7d3bdb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1acef40f9632d839c00f4cc569bf48ec30dd8ce4c0a3fad22689d0ee807a6f9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "encryption_key_arn": "encryptionKeyArn"},
)
class EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a71f1a18994543e60a3ec867416725089bb19763a3fb23f6b5f9a8a287750bb)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.'''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d06586e58cb4b83f46a898bfeabfb9ad9ddc23443b35caa6daee0efb320ea1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEncryptionKeyArn")
    def reset_encryption_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyArn", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArnInput")
    def encryption_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyArnInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__75ec72e54d8afc0d5bf4a85d91bc0267b12d7022b6af29691d764d7264d4f05f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArn")
    def encryption_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeyArn"))

    @encryption_key_arn.setter
    def encryption_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da9462fbadad2818cfc8a7c751219219a52149834fbeba7fc64f1007dfbe011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9cd95c37acc4cc4a24afbf43e28b4d38835e920c4b8682ef104a731c21d434b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationMonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__648d1ffd1b0f036805322173defeaad9a6f72ee559cd60339d5a9d22527afc52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLoggingConfiguration")
    def put_cloudwatch_logging_configuration(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        encryption_key_arn: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name_prefix: typing.Optional[builtins.str] = None,
        log_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_group_name EmrserverlessApplication#log_group_name}.
        :param log_stream_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_stream_name_prefix EmrserverlessApplication#log_stream_name_prefix}.
        :param log_types: log_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_types EmrserverlessApplication#log_types}
        '''
        value = EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration(
            enabled=enabled,
            encryption_key_arn=encryption_key_arn,
            log_group_name=log_group_name,
            log_stream_name_prefix=log_stream_name_prefix,
            log_types=log_types,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingConfiguration", [value]))

    @jsii.member(jsii_name="putManagedPersistenceMonitoringConfiguration")
    def put_managed_persistence_monitoring_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        '''
        value = EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration(
            enabled=enabled, encryption_key_arn=encryption_key_arn
        )

        return typing.cast(None, jsii.invoke(self, "putManagedPersistenceMonitoringConfiguration", [value]))

    @jsii.member(jsii_name="putPrometheusMonitoringConfiguration")
    def put_prometheus_monitoring_configuration(
        self,
        *,
        remote_write_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param remote_write_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#remote_write_url EmrserverlessApplication#remote_write_url}.
        '''
        value = EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration(
            remote_write_url=remote_write_url
        )

        return typing.cast(None, jsii.invoke(self, "putPrometheusMonitoringConfiguration", [value]))

    @jsii.member(jsii_name="putS3MonitoringConfiguration")
    def put_s3_monitoring_configuration(
        self,
        *,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        log_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        :param log_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_uri EmrserverlessApplication#log_uri}.
        '''
        value = EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration(
            encryption_key_arn=encryption_key_arn, log_uri=log_uri
        )

        return typing.cast(None, jsii.invoke(self, "putS3MonitoringConfiguration", [value]))

    @jsii.member(jsii_name="resetCloudwatchLoggingConfiguration")
    def reset_cloudwatch_logging_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingConfiguration", []))

    @jsii.member(jsii_name="resetManagedPersistenceMonitoringConfiguration")
    def reset_managed_persistence_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedPersistenceMonitoringConfiguration", []))

    @jsii.member(jsii_name="resetPrometheusMonitoringConfiguration")
    def reset_prometheus_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrometheusMonitoringConfiguration", []))

    @jsii.member(jsii_name="resetS3MonitoringConfiguration")
    def reset_s3_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3MonitoringConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingConfiguration")
    def cloudwatch_logging_configuration(
        self,
    ) -> EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationOutputReference:
        return typing.cast(EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationOutputReference, jsii.get(self, "cloudwatchLoggingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="managedPersistenceMonitoringConfiguration")
    def managed_persistence_monitoring_configuration(
        self,
    ) -> EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfigurationOutputReference:
        return typing.cast(EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfigurationOutputReference, jsii.get(self, "managedPersistenceMonitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="prometheusMonitoringConfiguration")
    def prometheus_monitoring_configuration(
        self,
    ) -> "EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfigurationOutputReference", jsii.get(self, "prometheusMonitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3MonitoringConfiguration")
    def s3_monitoring_configuration(
        self,
    ) -> "EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfigurationOutputReference", jsii.get(self, "s3MonitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingConfigurationInput")
    def cloudwatch_logging_configuration_input(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration], jsii.get(self, "cloudwatchLoggingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedPersistenceMonitoringConfigurationInput")
    def managed_persistence_monitoring_configuration_input(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration], jsii.get(self, "managedPersistenceMonitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="prometheusMonitoringConfigurationInput")
    def prometheus_monitoring_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration"], jsii.get(self, "prometheusMonitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3MonitoringConfigurationInput")
    def s3_monitoring_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration"], jsii.get(self, "s3MonitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04ab25af99f4abae51bd3dc5cea3f04f0419c607ee0c1adb4c4084746a5dd30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={"remote_write_url": "remoteWriteUrl"},
)
class EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration:
    def __init__(
        self,
        *,
        remote_write_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param remote_write_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#remote_write_url EmrserverlessApplication#remote_write_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524ffd04ed6df35c74fbee0e6deec5820ac2a84b8f416fb12daa3429df4c153a)
            check_type(argname="argument remote_write_url", value=remote_write_url, expected_type=type_hints["remote_write_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if remote_write_url is not None:
            self._values["remote_write_url"] = remote_write_url

    @builtins.property
    def remote_write_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#remote_write_url EmrserverlessApplication#remote_write_url}.'''
        result = self._values.get("remote_write_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9993d278aa7c3832f7129321c3a224da7031dea74a17a1abcdf845cfc02968c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRemoteWriteUrl")
    def reset_remote_write_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteWriteUrl", []))

    @builtins.property
    @jsii.member(jsii_name="remoteWriteUrlInput")
    def remote_write_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteWriteUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteWriteUrl")
    def remote_write_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteWriteUrl"))

    @remote_write_url.setter
    def remote_write_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb43b97bbe5da69dcb09149f6f543a0a0738cc95b0ecd4893adfa992b91b4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteWriteUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bbdeb42090ca6edc22df2cc2558b285b809cafe7eedfd08ed24e505ba7920e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={"encryption_key_arn": "encryptionKeyArn", "log_uri": "logUri"},
)
class EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration:
    def __init__(
        self,
        *,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        log_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        :param log_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_uri EmrserverlessApplication#log_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ed16045dafbdbf6fe26be1dd6980ab723f77e3784fd6f16a301899290fae0b)
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            check_type(argname="argument log_uri", value=log_uri, expected_type=type_hints["log_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if log_uri is not None:
            self._values["log_uri"] = log_uri

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.'''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#log_uri EmrserverlessApplication#log_uri}.'''
        result = self._values.get("log_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccc30a19253aa08f5d1295b6c1e214c4522bd29f643b0619352becc6737859f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncryptionKeyArn")
    def reset_encryption_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyArn", []))

    @jsii.member(jsii_name="resetLogUri")
    def reset_log_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogUri", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArnInput")
    def encryption_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logUriInput")
    def log_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logUriInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArn")
    def encryption_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeyArn"))

    @encryption_key_arn.setter
    def encryption_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9cbb011be911962f1e1957f3f27dab66fad024e88e31e0a1c8495707fa99e5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logUri")
    def log_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logUri"))

    @log_uri.setter
    def log_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e09aec9f2c95427e177e6880530a2555715d287a1348115284c7f0b095c5bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3275f38fbdc95012f2cabeb5c159ea937aa17be8564ee5497eabc36edf5e4b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"security_group_ids": "securityGroupIds", "subnet_ids": "subnetIds"},
)
class EmrserverlessApplicationNetworkConfiguration:
    def __init__(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#security_group_ids EmrserverlessApplication#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#subnet_ids EmrserverlessApplication#subnet_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b1ee93c58dc515c6b68f571f4c6cad18fab2d0c2e4a6fd40641796baa5f5be)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#security_group_ids EmrserverlessApplication#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#subnet_ids EmrserverlessApplication#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationNetworkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c7260c22301ea3786c5b9a9c167f1248b58d1319dc550076ceeb6db044c456)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSubnetIds")
    def reset_subnet_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetIds", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6ffe86ef29d607cc736e02f8fa71b4986b6834ccca9594c29642bc20008b9e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6bdade834ebe1a4044957d685809bbc7c925f5e0e4a240d628bf9fe128e82d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationNetworkConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce8357129d43e437454ab4b463bbb1f3e834cef91f4e420af1a3647439ac13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationRuntimeConfiguration",
    jsii_struct_bases=[],
    name_mapping={"classification": "classification", "properties": "properties"},
)
class EmrserverlessApplicationRuntimeConfiguration:
    def __init__(
        self,
        *,
        classification: builtins.str,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#classification EmrserverlessApplication#classification}.
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#properties EmrserverlessApplication#properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__befef0f5d39e80d84a71317152c4d6773e7d5ed919869e99800df436bb858ff6)
            check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "classification": classification,
        }
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def classification(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#classification EmrserverlessApplication#classification}.'''
        result = self._values.get("classification")
        assert result is not None, "Required property 'classification' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#properties EmrserverlessApplication#properties}.'''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationRuntimeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationRuntimeConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationRuntimeConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c1b62185e31ee503a18e7f227e711aa15a538707bb2c9355d01533a5b70ae00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EmrserverlessApplicationRuntimeConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b961330990bcc7e1e5c4f3a385259fb7f33cb2d804a3767ae92cdb568018fb2f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EmrserverlessApplicationRuntimeConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787b2521b49ed1520229b7aaefd8776262a67a011674f854e8afa40fe4749c5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61c3f82e15a557fc7ef480931ea7a7242a8bb41b9b125da2f29c109add402602)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39c021baa85e1a842f1387592985f15225a55e00ae5050cff5eb8ad0efbaeb5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationRuntimeConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationRuntimeConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationRuntimeConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a913ec1f9ec9d59bda26a23db113c6c057d8d94f22666ba0665810ccd580c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationRuntimeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationRuntimeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ab8ad1c339370acb1cf80717143fd2083e3893420c2a3db50575677cfbb5c73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="classificationInput")
    def classification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "classificationInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="classification")
    def classification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classification"))

    @classification.setter
    def classification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ec23c0b66ecfb2331402a0ada04a980209ef299f27d0eea2bd94557ec0877d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e89821bea5db17e269d9f549edf55b1d7a902d0c8bc96055966ac057bf10e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationRuntimeConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationRuntimeConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationRuntimeConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304a7edc177618acb99d97a25bb60b247b9ce12a61b271571dda802fe90b0ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationSchedulerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrent_runs": "maxConcurrentRuns",
        "queue_timeout_minutes": "queueTimeoutMinutes",
    },
)
class EmrserverlessApplicationSchedulerConfiguration:
    def __init__(
        self,
        *,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        queue_timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_runs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#max_concurrent_runs EmrserverlessApplication#max_concurrent_runs}.
        :param queue_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#queue_timeout_minutes EmrserverlessApplication#queue_timeout_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__717cf337bfe0e59006383e6f90422ed7659e03d6be959eeec811ca9efda93894)
            check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
            check_type(argname="argument queue_timeout_minutes", value=queue_timeout_minutes, expected_type=type_hints["queue_timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_concurrent_runs is not None:
            self._values["max_concurrent_runs"] = max_concurrent_runs
        if queue_timeout_minutes is not None:
            self._values["queue_timeout_minutes"] = queue_timeout_minutes

    @builtins.property
    def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#max_concurrent_runs EmrserverlessApplication#max_concurrent_runs}.'''
        result = self._values.get("max_concurrent_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrserverless_application#queue_timeout_minutes EmrserverlessApplication#queue_timeout_minutes}.'''
        result = self._values.get("queue_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationSchedulerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationSchedulerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrserverlessApplication.EmrserverlessApplicationSchedulerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dc3111bc83f6b5a708ac550edc320d3bf8de356157574a8daa5b6882946663f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxConcurrentRuns")
    def reset_max_concurrent_runs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentRuns", []))

    @jsii.member(jsii_name="resetQueueTimeoutMinutes")
    def reset_queue_timeout_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueTimeoutMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRunsInput")
    def max_concurrent_runs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentRunsInput"))

    @builtins.property
    @jsii.member(jsii_name="queueTimeoutMinutesInput")
    def queue_timeout_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queueTimeoutMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRuns")
    def max_concurrent_runs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentRuns"))

    @max_concurrent_runs.setter
    def max_concurrent_runs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ded36201847cf0bd3806db9df49336a4ce7e55804fbad9801712e4b6eb1970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentRuns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueTimeoutMinutes")
    def queue_timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queueTimeoutMinutes"))

    @queue_timeout_minutes.setter
    def queue_timeout_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020ac8f1067324a603ed26d0456087929c79c288f147e47d77c1aa106e8e91b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueTimeoutMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationSchedulerConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationSchedulerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationSchedulerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e2d5517ea04fe3006984fe07fcd92bdd8e2b32f5d383990a04f1413fc0544fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EmrserverlessApplication",
    "EmrserverlessApplicationAutoStartConfiguration",
    "EmrserverlessApplicationAutoStartConfigurationOutputReference",
    "EmrserverlessApplicationAutoStopConfiguration",
    "EmrserverlessApplicationAutoStopConfigurationOutputReference",
    "EmrserverlessApplicationConfig",
    "EmrserverlessApplicationImageConfiguration",
    "EmrserverlessApplicationImageConfigurationOutputReference",
    "EmrserverlessApplicationInitialCapacity",
    "EmrserverlessApplicationInitialCapacityInitialCapacityConfig",
    "EmrserverlessApplicationInitialCapacityInitialCapacityConfigOutputReference",
    "EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration",
    "EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfigurationOutputReference",
    "EmrserverlessApplicationInitialCapacityList",
    "EmrserverlessApplicationInitialCapacityOutputReference",
    "EmrserverlessApplicationInteractiveConfiguration",
    "EmrserverlessApplicationInteractiveConfigurationOutputReference",
    "EmrserverlessApplicationMaximumCapacity",
    "EmrserverlessApplicationMaximumCapacityOutputReference",
    "EmrserverlessApplicationMonitoringConfiguration",
    "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration",
    "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes",
    "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesList",
    "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesOutputReference",
    "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationOutputReference",
    "EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration",
    "EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfigurationOutputReference",
    "EmrserverlessApplicationMonitoringConfigurationOutputReference",
    "EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration",
    "EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfigurationOutputReference",
    "EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration",
    "EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfigurationOutputReference",
    "EmrserverlessApplicationNetworkConfiguration",
    "EmrserverlessApplicationNetworkConfigurationOutputReference",
    "EmrserverlessApplicationRuntimeConfiguration",
    "EmrserverlessApplicationRuntimeConfigurationList",
    "EmrserverlessApplicationRuntimeConfigurationOutputReference",
    "EmrserverlessApplicationSchedulerConfiguration",
    "EmrserverlessApplicationSchedulerConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__a6b5b9c8ec14985f323d8d84a4fc86d9f9b13fa6501669045bceab598e68ad8a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    release_label: builtins.str,
    type: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    auto_start_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStartConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_stop_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStopConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    image_configuration: typing.Optional[typing.Union[EmrserverlessApplicationImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_capacity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationInitialCapacity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    interactive_configuration: typing.Optional[typing.Union[EmrserverlessApplicationInteractiveConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_capacity: typing.Optional[typing.Union[EmrserverlessApplicationMaximumCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    network_configuration: typing.Optional[typing.Union[EmrserverlessApplicationNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    runtime_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationRuntimeConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scheduler_configuration: typing.Optional[typing.Union[EmrserverlessApplicationSchedulerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__3479eff2d1ddc3bd355a8ade8b7a36cf3eb4a26b6360845b65c7dd0ef0f3893c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ed908b238c50d71e3d7f76b68026b3520a0104e64117a5631b178abc0f4b65(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationInitialCapacity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ce2a08281f836fa3d13a69f87fbcb4367416068c958d94cc0d922778f9b9b4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationRuntimeConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5fbc19c465453ff1745b393e7f1b2c08cec62c62098dc03eafd5ef4e216143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c693568f0e90018bcaf2eb05e62830df5d435727acdad72d1492dde6fa21142(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b237a0eb5de5058bb900ff4db7f1a363a147398df0ae28352427f50adaf187bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e6e1dc1470c68d9326a44af86372ac18101daf3e6b76984cfb770b3f2b1fe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faef4d692384d84496bb119613c092063a3094d42de565fd8fb39cd7eb4e774a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943a467dca40b6765941fce09c92405da021c3c4b0f8ca9e0668c5eb081c0141(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670943c05a5b47f71bc19c6d39bee1b32cf257b9b4a7dab9c719ba3b20422414(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252bb2bf0dc45941ba7e21417e4f58150d7dbd33b7c42088efd1fdc017436691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb519e9a7a2ec3eae031d6cc23974206caf4378ce3491f3809107d1a12a0dc68(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2921c144078f5b63610a72c2ce42235fb157bbd8e11120d5871015584c4beb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609559afc4b3864d1c59fa58210e3c9596fed95c5a5c5a58fc9eecdf0db88268(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de02b9fa03e802b2361426596616d2f8ec4ed59d1cbecd9d6e7d5cfbeea1e6f7(
    value: typing.Optional[EmrserverlessApplicationAutoStartConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d5efe5d055cbcebdbcf40b4203baedde2e7b3e88d29495b91ea2631036c8a8(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    idle_timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691b5a3d577d176f1c6a0fbdf1c45b312e2e92690ec4a1085d83c3f3f3b807fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0ba3ca61209fabbeccd7e9f26b7f3c040b243dc14035ad03810341b160916a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fac42d8b1b40418252550bc709db48c2ccf8998bddb1d85a574ad15585e3de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bf5dd947d56efd2383a2ff1dea7ea89260cd5f3d0f0abba3923dadd30395e6(
    value: typing.Optional[EmrserverlessApplicationAutoStopConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32760dfe39c0dab9e07ddd983057dc7398096711e8610c08bf5ea10a5d0ac847(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    release_label: builtins.str,
    type: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    auto_start_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStartConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_stop_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStopConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    image_configuration: typing.Optional[typing.Union[EmrserverlessApplicationImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_capacity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationInitialCapacity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    interactive_configuration: typing.Optional[typing.Union[EmrserverlessApplicationInteractiveConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_capacity: typing.Optional[typing.Union[EmrserverlessApplicationMaximumCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    network_configuration: typing.Optional[typing.Union[EmrserverlessApplicationNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    runtime_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationRuntimeConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scheduler_configuration: typing.Optional[typing.Union[EmrserverlessApplicationSchedulerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8109f1f74e26c5be4b1abc28dbbe4a206ff9071256f92fa6430a2978e2d1525c(
    *,
    image_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179d8f145366e5dceb5994632426f33740b8a9aec6b69fb68a9f8d3d6c2a1410(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc23cd604eeb563e5e549bb82a1b946d5b8c9ae2e6fe39bbe98a80036de3fdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16277b861c2da37d1fa42d455d9798d148016f26b5762f3f4a45c4616ab7eaf(
    value: typing.Optional[EmrserverlessApplicationImageConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377e685c269118f040da4c8306a71b392d3730182afcb03b9dbe5e96b1f07764(
    *,
    initial_capacity_type: builtins.str,
    initial_capacity_config: typing.Optional[typing.Union[EmrserverlessApplicationInitialCapacityInitialCapacityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33380cad1a9c928e43e6b4ebaa900c013da7f61c6807efa2399b2885d68137cb(
    *,
    worker_count: jsii.Number,
    worker_configuration: typing.Optional[typing.Union[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9737963ebba48a8b64ab3a47802ae37246d006b5c4822bfef60933612bd0ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a25c569060367751d61f89decc140e4fecb16c9d40df8a85e52acb540dcb414(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc78676651977edea4b72caa1a63c91f5edf5748a57cde6c72a914b743b2678(
    value: typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307a965e64cc6b665cb828181bdc249ca3552b13b2c9f1c4d6bc5e48c8323730(
    *,
    cpu: builtins.str,
    memory: builtins.str,
    disk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b85203790b2d264929469ed1046d6a531adc9cc050c4be1da72fd175e064a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebfe75a937be2093bcf9ab51e8c9950f746bee0584d453ef4c217b1779f7bccb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9afe601db63e5630af378967fc3174fe9a10ee70399bfc24abac63847825931b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a263e34f400075b2b4d4cacb193cc78a390e66b68a30eba9e1fd91293ed9e3e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee390f005cbcc6c0b356fcd9073a86d4823efb32f5946d468ace6846810aaf4(
    value: typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a52e9f578d5b77c8c2213847a07d275499d905bf3d02137faa70e9fbdc4c45f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f780694a420491be1867fd92e3d02ca3e69c71982505a3e1c034641def063dc6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36dea75bf0b67a305838c8eca048ed8db9185fe8e991ef1e7a53cf562452f4b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3e1a3a5fbaa2a574d2ce09196a796005174526b1ed33573030cda7827cfa4e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80bd9e39d97bf9ec7c28b19de746f137412810c5dc710f4eb933e1840c0e3e98(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226c22281df0a35c6b2f3c8182905953ec2dcf1187a95c3b32eb56b4e48c4e42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationInitialCapacity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d847f506627ba83fb14e54bcf891bd0f29186231a0f48090b4069783d16abe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05d2b925023b6da3f1ad1ec033813c851dfc3b6c7f2b1f052e6bc4af023785e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55635adc8b9d30764273b4901c7c9888838210c91d63ff9cd697b3edb7d02134(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationInitialCapacity]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f0fe5b32d58a28556cc468d988191ab84fac77226724e489073ef08b6f9f74(
    *,
    livy_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    studio_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00632cf20e95d303142058a03ffc39028988fe469a10833b86096200f360520(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1852e7a5d0d20976086d370b4e549ed7d3d0d61a174af4cdd1ee8fe85202729d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0044f9135f75838e3016e19d931596bc6bb51987e5f71975d00c9d7fdea465f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d5d41ad2ea15408946a8f6cfd360bd0d348b4e13d8c116266e757a3d4d5ecf(
    value: typing.Optional[EmrserverlessApplicationInteractiveConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0444b98bf1f077817a389d0fc72edce3610588df5508bb49fe50fc764b18ca83(
    *,
    cpu: builtins.str,
    memory: builtins.str,
    disk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e59ab9f22198d4bf3a5bee0a65e3ff935cfa3aa57de1479c4183c3d3d99a245(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d21c9633ba9ed78e77a8f24cb8c1608fc4a56718189d6dc7a7d3731966b72cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efe7f6f0516984f9d03ff2e64dfb804c184d89be566a1d4a72ce7f85619e130(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9638ad5b0e9e86f09957d869dc1682a5bbff14fd392e12ad47f948cde584f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3891fef2a55e3fae459f2ceb4063f6402c8679f7f20bbdaf69f689f22e83c2ce(
    value: typing.Optional[EmrserverlessApplicationMaximumCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19a84b16abefd8bb502dbfd2acdd085afc3d8a8626b2cf393d1f01f1ef36d9a(
    *,
    cloudwatch_logging_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_persistence_monitoring_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    prometheus_monitoring_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_monitoring_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5447184df8e677c3d516e0f5aa1ba516507bf514fe7ec0126c2788de14abffc(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    encryption_key_arn: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name_prefix: typing.Optional[builtins.str] = None,
    log_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746c695579bcec43d4e262d02f7f3cdfd74c61f1ca2331f79ca503e550634f6f(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29af38c789f0f355a2b75de563c94bcc9a8c80fbe0f44c3aa3c5867ce6c60e9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557ba5b9bef9e18862be5a142ea150d4b7d723c53b510192af2a452d52b39416(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d49879628c74d79f1ac8b3e0309f01beb56780bea6e42facf9c3a34a1d9d546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255ee46611571fc3d7a11321a0b32e12b595ddb71f87b7c4cd4277f5edc17cf0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a10b619ee8784c1a8846cec00ea8f99a04a3ee69527e043b7e5c1bd4fa2cbd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e973759d1d77127199c413cc7cf464261a582256208d11f0a5c85423ebe5667b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73429b8b14a30a5b796c34d8974807ed9153fdfe63ef20df528edf04c9666e50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f619889305cbb865e27b54a6b7e433bb5436a7167ccfb819d318025a8d0c8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65bebb7f4a39f9a500aaa69168d295d08e7c773b943ab1398a2f00ea18dd90e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9416325aed76904ecbed3b0bea55f57e3541504a127f57969bb5fe6434dd90a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6d9bb3685d41fbd5ec33ad7c06b40fdd39fead9ca657ab3cab0c2c3015322d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45271b0286c457b9459ec587c84b7bec30a7b439ec4bda7a2267caacb65e99ed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0fc93ccc74691a0ca16c206be9bf543ba9aadea7f4be53839f7617426e69ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860a9ff367289bfa5070826a22ca0fd290e663c0aaa8c0350e1d15e2f04ae9ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03979a183dedf6c46b75d8528a73df6636171c9f10f11ea91a74f4cb53e09221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaae3efa0b67b9559ef2fbc022c9b39885682571b62e42b52e093d64c7d3bdb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acef40f9632d839c00f4cc569bf48ec30dd8ce4c0a3fad22689d0ee807a6f9b(
    value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a71f1a18994543e60a3ec867416725089bb19763a3fb23f6b5f9a8a287750bb(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d06586e58cb4b83f46a898bfeabfb9ad9ddc23443b35caa6daee0efb320ea1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ec72e54d8afc0d5bf4a85d91bc0267b12d7022b6af29691d764d7264d4f05f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da9462fbadad2818cfc8a7c751219219a52149834fbeba7fc64f1007dfbe011(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9cd95c37acc4cc4a24afbf43e28b4d38835e920c4b8682ef104a731c21d434b(
    value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648d1ffd1b0f036805322173defeaad9a6f72ee559cd60339d5a9d22527afc52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04ab25af99f4abae51bd3dc5cea3f04f0419c607ee0c1adb4c4084746a5dd30(
    value: typing.Optional[EmrserverlessApplicationMonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524ffd04ed6df35c74fbee0e6deec5820ac2a84b8f416fb12daa3429df4c153a(
    *,
    remote_write_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9993d278aa7c3832f7129321c3a224da7031dea74a17a1abcdf845cfc02968c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb43b97bbe5da69dcb09149f6f543a0a0738cc95b0ecd4893adfa992b91b4b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbdeb42090ca6edc22df2cc2558b285b809cafe7eedfd08ed24e505ba7920e5(
    value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ed16045dafbdbf6fe26be1dd6980ab723f77e3784fd6f16a301899290fae0b(
    *,
    encryption_key_arn: typing.Optional[builtins.str] = None,
    log_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc30a19253aa08f5d1295b6c1e214c4522bd29f643b0619352becc6737859f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9cbb011be911962f1e1957f3f27dab66fad024e88e31e0a1c8495707fa99e5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e09aec9f2c95427e177e6880530a2555715d287a1348115284c7f0b095c5bc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3275f38fbdc95012f2cabeb5c159ea937aa17be8564ee5497eabc36edf5e4b9a(
    value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b1ee93c58dc515c6b68f571f4c6cad18fab2d0c2e4a6fd40641796baa5f5be(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c7260c22301ea3786c5b9a9c167f1248b58d1319dc550076ceeb6db044c456(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ffe86ef29d607cc736e02f8fa71b4986b6834ccca9594c29642bc20008b9e30(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6bdade834ebe1a4044957d685809bbc7c925f5e0e4a240d628bf9fe128e82d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce8357129d43e437454ab4b463bbb1f3e834cef91f4e420af1a3647439ac13a(
    value: typing.Optional[EmrserverlessApplicationNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befef0f5d39e80d84a71317152c4d6773e7d5ed919869e99800df436bb858ff6(
    *,
    classification: builtins.str,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1b62185e31ee503a18e7f227e711aa15a538707bb2c9355d01533a5b70ae00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b961330990bcc7e1e5c4f3a385259fb7f33cb2d804a3767ae92cdb568018fb2f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787b2521b49ed1520229b7aaefd8776262a67a011674f854e8afa40fe4749c5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c3f82e15a557fc7ef480931ea7a7242a8bb41b9b125da2f29c109add402602(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c021baa85e1a842f1387592985f15225a55e00ae5050cff5eb8ad0efbaeb5a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a913ec1f9ec9d59bda26a23db113c6c057d8d94f22666ba0665810ccd580c83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationRuntimeConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab8ad1c339370acb1cf80717143fd2083e3893420c2a3db50575677cfbb5c73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ec23c0b66ecfb2331402a0ada04a980209ef299f27d0eea2bd94557ec0877d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e89821bea5db17e269d9f549edf55b1d7a902d0c8bc96055966ac057bf10e9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304a7edc177618acb99d97a25bb60b247b9ce12a61b271571dda802fe90b0ff3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationRuntimeConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717cf337bfe0e59006383e6f90422ed7659e03d6be959eeec811ca9efda93894(
    *,
    max_concurrent_runs: typing.Optional[jsii.Number] = None,
    queue_timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc3111bc83f6b5a708ac550edc320d3bf8de356157574a8daa5b6882946663f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ded36201847cf0bd3806db9df49336a4ce7e55804fbad9801712e4b6eb1970(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020ac8f1067324a603ed26d0456087929c79c288f147e47d77c1aa106e8e91b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2d5517ea04fe3006984fe07fcd92bdd8e2b32f5d383990a04f1413fc0544fe(
    value: typing.Optional[EmrserverlessApplicationSchedulerConfiguration],
) -> None:
    """Type checking stubs"""
    pass
