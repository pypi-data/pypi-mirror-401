r'''
# `aws_apprunner_service`

Refer to the Terraform Registry for docs: [`aws_apprunner_service`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service).
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


class ApprunnerService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service aws_apprunner_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        service_name: builtins.str,
        source_configuration: typing.Union["ApprunnerServiceSourceConfiguration", typing.Dict[builtins.str, typing.Any]],
        auto_scaling_configuration_arn: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union["ApprunnerServiceEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        health_check_configuration: typing.Optional[typing.Union["ApprunnerServiceHealthCheckConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_configuration: typing.Optional[typing.Union["ApprunnerServiceInstanceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        network_configuration: typing.Optional[typing.Union["ApprunnerServiceNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        observability_configuration: typing.Optional[typing.Union["ApprunnerServiceObservabilityConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service aws_apprunner_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#service_name ApprunnerService#service_name}.
        :param source_configuration: source_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#source_configuration ApprunnerService#source_configuration}
        :param auto_scaling_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#auto_scaling_configuration_arn ApprunnerService#auto_scaling_configuration_arn}.
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#encryption_configuration ApprunnerService#encryption_configuration}
        :param health_check_configuration: health_check_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#health_check_configuration ApprunnerService#health_check_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#id ApprunnerService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_configuration: instance_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#instance_configuration ApprunnerService#instance_configuration}
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#network_configuration ApprunnerService#network_configuration}
        :param observability_configuration: observability_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#observability_configuration ApprunnerService#observability_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#region ApprunnerService#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#tags ApprunnerService#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#tags_all ApprunnerService#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151db1605640873f5f95ba4c8e37ee1b83a3cb47260b335f0ea20a37438691c8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApprunnerServiceConfig(
            service_name=service_name,
            source_configuration=source_configuration,
            auto_scaling_configuration_arn=auto_scaling_configuration_arn,
            encryption_configuration=encryption_configuration,
            health_check_configuration=health_check_configuration,
            id=id,
            instance_configuration=instance_configuration,
            network_configuration=network_configuration,
            observability_configuration=observability_configuration,
            region=region,
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
        '''Generates CDKTF code for importing a ApprunnerService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApprunnerService to import.
        :param import_from_id: The id of the existing ApprunnerService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApprunnerService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0007aee4f3db63680742afec4a93757ea8adb11a6694e25b4f1daaa92f63cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(self, *, kms_key: builtins.str) -> None:
        '''
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#kms_key ApprunnerService#kms_key}.
        '''
        value = ApprunnerServiceEncryptionConfiguration(kms_key=kms_key)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putHealthCheckConfiguration")
    def put_health_check_configuration(
        self,
        *,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param healthy_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#healthy_threshold ApprunnerService#healthy_threshold}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#interval ApprunnerService#interval}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#path ApprunnerService#path}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#protocol ApprunnerService#protocol}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#timeout ApprunnerService#timeout}.
        :param unhealthy_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#unhealthy_threshold ApprunnerService#unhealthy_threshold}.
        '''
        value = ApprunnerServiceHealthCheckConfiguration(
            healthy_threshold=healthy_threshold,
            interval=interval,
            path=path,
            protocol=protocol,
            timeout=timeout,
            unhealthy_threshold=unhealthy_threshold,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthCheckConfiguration", [value]))

    @jsii.member(jsii_name="putInstanceConfiguration")
    def put_instance_configuration(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        instance_role_arn: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#cpu ApprunnerService#cpu}.
        :param instance_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#instance_role_arn ApprunnerService#instance_role_arn}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#memory ApprunnerService#memory}.
        '''
        value = ApprunnerServiceInstanceConfiguration(
            cpu=cpu, instance_role_arn=instance_role_arn, memory=memory
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceConfiguration", [value]))

    @jsii.member(jsii_name="putNetworkConfiguration")
    def put_network_configuration(
        self,
        *,
        egress_configuration: typing.Optional[typing.Union["ApprunnerServiceNetworkConfigurationEgressConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_configuration: typing.Optional[typing.Union["ApprunnerServiceNetworkConfigurationIngressConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param egress_configuration: egress_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#egress_configuration ApprunnerService#egress_configuration}
        :param ingress_configuration: ingress_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#ingress_configuration ApprunnerService#ingress_configuration}
        :param ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#ip_address_type ApprunnerService#ip_address_type}.
        '''
        value = ApprunnerServiceNetworkConfiguration(
            egress_configuration=egress_configuration,
            ingress_configuration=ingress_configuration,
            ip_address_type=ip_address_type,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfiguration", [value]))

    @jsii.member(jsii_name="putObservabilityConfiguration")
    def put_observability_configuration(
        self,
        *,
        observability_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        observability_configuration_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param observability_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#observability_enabled ApprunnerService#observability_enabled}.
        :param observability_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#observability_configuration_arn ApprunnerService#observability_configuration_arn}.
        '''
        value = ApprunnerServiceObservabilityConfiguration(
            observability_enabled=observability_enabled,
            observability_configuration_arn=observability_configuration_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putObservabilityConfiguration", [value]))

    @jsii.member(jsii_name="putSourceConfiguration")
    def put_source_configuration(
        self,
        *,
        authentication_configuration: typing.Optional[typing.Union["ApprunnerServiceSourceConfigurationAuthenticationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_deployments_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        code_repository: typing.Optional[typing.Union["ApprunnerServiceSourceConfigurationCodeRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        image_repository: typing.Optional[typing.Union["ApprunnerServiceSourceConfigurationImageRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authentication_configuration: authentication_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#authentication_configuration ApprunnerService#authentication_configuration}
        :param auto_deployments_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#auto_deployments_enabled ApprunnerService#auto_deployments_enabled}.
        :param code_repository: code_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#code_repository ApprunnerService#code_repository}
        :param image_repository: image_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_repository ApprunnerService#image_repository}
        '''
        value = ApprunnerServiceSourceConfiguration(
            authentication_configuration=authentication_configuration,
            auto_deployments_enabled=auto_deployments_enabled,
            code_repository=code_repository,
            image_repository=image_repository,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceConfiguration", [value]))

    @jsii.member(jsii_name="resetAutoScalingConfigurationArn")
    def reset_auto_scaling_configuration_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoScalingConfigurationArn", []))

    @jsii.member(jsii_name="resetEncryptionConfiguration")
    def reset_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetHealthCheckConfiguration")
    def reset_health_check_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceConfiguration")
    def reset_instance_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceConfiguration", []))

    @jsii.member(jsii_name="resetNetworkConfiguration")
    def reset_network_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfiguration", []))

    @jsii.member(jsii_name="resetObservabilityConfiguration")
    def reset_observability_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObservabilityConfiguration", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> "ApprunnerServiceEncryptionConfigurationOutputReference":
        return typing.cast("ApprunnerServiceEncryptionConfigurationOutputReference", jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckConfiguration")
    def health_check_configuration(
        self,
    ) -> "ApprunnerServiceHealthCheckConfigurationOutputReference":
        return typing.cast("ApprunnerServiceHealthCheckConfigurationOutputReference", jsii.get(self, "healthCheckConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="instanceConfiguration")
    def instance_configuration(
        self,
    ) -> "ApprunnerServiceInstanceConfigurationOutputReference":
        return typing.cast("ApprunnerServiceInstanceConfigurationOutputReference", jsii.get(self, "instanceConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> "ApprunnerServiceNetworkConfigurationOutputReference":
        return typing.cast("ApprunnerServiceNetworkConfigurationOutputReference", jsii.get(self, "networkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfiguration")
    def observability_configuration(
        self,
    ) -> "ApprunnerServiceObservabilityConfigurationOutputReference":
        return typing.cast("ApprunnerServiceObservabilityConfigurationOutputReference", jsii.get(self, "observabilityConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @builtins.property
    @jsii.member(jsii_name="serviceUrl")
    def service_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceUrl"))

    @builtins.property
    @jsii.member(jsii_name="sourceConfiguration")
    def source_configuration(
        self,
    ) -> "ApprunnerServiceSourceConfigurationOutputReference":
        return typing.cast("ApprunnerServiceSourceConfigurationOutputReference", jsii.get(self, "sourceConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationArnInput")
    def auto_scaling_configuration_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoScalingConfigurationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional["ApprunnerServiceEncryptionConfiguration"]:
        return typing.cast(typing.Optional["ApprunnerServiceEncryptionConfiguration"], jsii.get(self, "encryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckConfigurationInput")
    def health_check_configuration_input(
        self,
    ) -> typing.Optional["ApprunnerServiceHealthCheckConfiguration"]:
        return typing.cast(typing.Optional["ApprunnerServiceHealthCheckConfiguration"], jsii.get(self, "healthCheckConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceConfigurationInput")
    def instance_configuration_input(
        self,
    ) -> typing.Optional["ApprunnerServiceInstanceConfiguration"]:
        return typing.cast(typing.Optional["ApprunnerServiceInstanceConfiguration"], jsii.get(self, "instanceConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationInput")
    def network_configuration_input(
        self,
    ) -> typing.Optional["ApprunnerServiceNetworkConfiguration"]:
        return typing.cast(typing.Optional["ApprunnerServiceNetworkConfiguration"], jsii.get(self, "networkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationInput")
    def observability_configuration_input(
        self,
    ) -> typing.Optional["ApprunnerServiceObservabilityConfiguration"]:
        return typing.cast(typing.Optional["ApprunnerServiceObservabilityConfiguration"], jsii.get(self, "observabilityConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceConfigurationInput")
    def source_configuration_input(
        self,
    ) -> typing.Optional["ApprunnerServiceSourceConfiguration"]:
        return typing.cast(typing.Optional["ApprunnerServiceSourceConfiguration"], jsii.get(self, "sourceConfigurationInput"))

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
    @jsii.member(jsii_name="autoScalingConfigurationArn")
    def auto_scaling_configuration_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoScalingConfigurationArn"))

    @auto_scaling_configuration_arn.setter
    def auto_scaling_configuration_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f191837d16d585a0a586e36c9f06f40bac3850e54321b3f02d1cd3887f943e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoScalingConfigurationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abeaf402e709e01def8cb5eccfe704ddd017b26fcb93e8cdc592356db0448470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd8656f657bd3db20078bca985dc382e9ff57a8254c7b118039678eb138eb01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99c8c8c0f51a7f555a4c52ae36039ece4fbed9d63ba0cb1bfe0ef35d08f7b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb56158ac146089b62066f8c178cc9406b97be3855a685cad056d36ae54ccd5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8ff997019525beb72a2b642e0eecc0c4285d0ade48dce1eb45a66cbc691ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "service_name": "serviceName",
        "source_configuration": "sourceConfiguration",
        "auto_scaling_configuration_arn": "autoScalingConfigurationArn",
        "encryption_configuration": "encryptionConfiguration",
        "health_check_configuration": "healthCheckConfiguration",
        "id": "id",
        "instance_configuration": "instanceConfiguration",
        "network_configuration": "networkConfiguration",
        "observability_configuration": "observabilityConfiguration",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class ApprunnerServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        service_name: builtins.str,
        source_configuration: typing.Union["ApprunnerServiceSourceConfiguration", typing.Dict[builtins.str, typing.Any]],
        auto_scaling_configuration_arn: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union["ApprunnerServiceEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        health_check_configuration: typing.Optional[typing.Union["ApprunnerServiceHealthCheckConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_configuration: typing.Optional[typing.Union["ApprunnerServiceInstanceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        network_configuration: typing.Optional[typing.Union["ApprunnerServiceNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        observability_configuration: typing.Optional[typing.Union["ApprunnerServiceObservabilityConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
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
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#service_name ApprunnerService#service_name}.
        :param source_configuration: source_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#source_configuration ApprunnerService#source_configuration}
        :param auto_scaling_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#auto_scaling_configuration_arn ApprunnerService#auto_scaling_configuration_arn}.
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#encryption_configuration ApprunnerService#encryption_configuration}
        :param health_check_configuration: health_check_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#health_check_configuration ApprunnerService#health_check_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#id ApprunnerService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_configuration: instance_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#instance_configuration ApprunnerService#instance_configuration}
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#network_configuration ApprunnerService#network_configuration}
        :param observability_configuration: observability_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#observability_configuration ApprunnerService#observability_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#region ApprunnerService#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#tags ApprunnerService#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#tags_all ApprunnerService#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(source_configuration, dict):
            source_configuration = ApprunnerServiceSourceConfiguration(**source_configuration)
        if isinstance(encryption_configuration, dict):
            encryption_configuration = ApprunnerServiceEncryptionConfiguration(**encryption_configuration)
        if isinstance(health_check_configuration, dict):
            health_check_configuration = ApprunnerServiceHealthCheckConfiguration(**health_check_configuration)
        if isinstance(instance_configuration, dict):
            instance_configuration = ApprunnerServiceInstanceConfiguration(**instance_configuration)
        if isinstance(network_configuration, dict):
            network_configuration = ApprunnerServiceNetworkConfiguration(**network_configuration)
        if isinstance(observability_configuration, dict):
            observability_configuration = ApprunnerServiceObservabilityConfiguration(**observability_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8677de2af13e11b6d0b22f45684bc5030ec440ade76d8dad4e22fe04160808b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument source_configuration", value=source_configuration, expected_type=type_hints["source_configuration"])
            check_type(argname="argument auto_scaling_configuration_arn", value=auto_scaling_configuration_arn, expected_type=type_hints["auto_scaling_configuration_arn"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument health_check_configuration", value=health_check_configuration, expected_type=type_hints["health_check_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_configuration", value=instance_configuration, expected_type=type_hints["instance_configuration"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument observability_configuration", value=observability_configuration, expected_type=type_hints["observability_configuration"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_name": service_name,
            "source_configuration": source_configuration,
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
        if auto_scaling_configuration_arn is not None:
            self._values["auto_scaling_configuration_arn"] = auto_scaling_configuration_arn
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if health_check_configuration is not None:
            self._values["health_check_configuration"] = health_check_configuration
        if id is not None:
            self._values["id"] = id
        if instance_configuration is not None:
            self._values["instance_configuration"] = instance_configuration
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if observability_configuration is not None:
            self._values["observability_configuration"] = observability_configuration
        if region is not None:
            self._values["region"] = region
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
    def service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#service_name ApprunnerService#service_name}.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_configuration(self) -> "ApprunnerServiceSourceConfiguration":
        '''source_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#source_configuration ApprunnerService#source_configuration}
        '''
        result = self._values.get("source_configuration")
        assert result is not None, "Required property 'source_configuration' is missing"
        return typing.cast("ApprunnerServiceSourceConfiguration", result)

    @builtins.property
    def auto_scaling_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#auto_scaling_configuration_arn ApprunnerService#auto_scaling_configuration_arn}.'''
        result = self._values.get("auto_scaling_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional["ApprunnerServiceEncryptionConfiguration"]:
        '''encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#encryption_configuration ApprunnerService#encryption_configuration}
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional["ApprunnerServiceEncryptionConfiguration"], result)

    @builtins.property
    def health_check_configuration(
        self,
    ) -> typing.Optional["ApprunnerServiceHealthCheckConfiguration"]:
        '''health_check_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#health_check_configuration ApprunnerService#health_check_configuration}
        '''
        result = self._values.get("health_check_configuration")
        return typing.cast(typing.Optional["ApprunnerServiceHealthCheckConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#id ApprunnerService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_configuration(
        self,
    ) -> typing.Optional["ApprunnerServiceInstanceConfiguration"]:
        '''instance_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#instance_configuration ApprunnerService#instance_configuration}
        '''
        result = self._values.get("instance_configuration")
        return typing.cast(typing.Optional["ApprunnerServiceInstanceConfiguration"], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional["ApprunnerServiceNetworkConfiguration"]:
        '''network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#network_configuration ApprunnerService#network_configuration}
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional["ApprunnerServiceNetworkConfiguration"], result)

    @builtins.property
    def observability_configuration(
        self,
    ) -> typing.Optional["ApprunnerServiceObservabilityConfiguration"]:
        '''observability_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#observability_configuration ApprunnerService#observability_configuration}
        '''
        result = self._values.get("observability_configuration")
        return typing.cast(typing.Optional["ApprunnerServiceObservabilityConfiguration"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#region ApprunnerService#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#tags ApprunnerService#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#tags_all ApprunnerService#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class ApprunnerServiceEncryptionConfiguration:
    def __init__(self, *, kms_key: builtins.str) -> None:
        '''
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#kms_key ApprunnerService#kms_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bba09ae72cb41b697cec4c25c7a55e3d9d10b6b3b7bacba5dc24bf73bfa883b)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key": kms_key,
        }

    @builtins.property
    def kms_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#kms_key ApprunnerService#kms_key}.'''
        result = self._values.get("kms_key")
        assert result is not None, "Required property 'kms_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApprunnerServiceEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b3f0b5520b085d7c0f2ec263011d9ab25304960937aaf7eb9aa1caf62b43c21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ef54ce7cbb08c9a5d4d614f3bbcb481e921eab01fe31b65a9f4568bc334d38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceEncryptionConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea995c20f0029cf247acde4a61eb34503855fb048fc9029cfcb8be17556d186e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceHealthCheckConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "healthy_threshold": "healthyThreshold",
        "interval": "interval",
        "path": "path",
        "protocol": "protocol",
        "timeout": "timeout",
        "unhealthy_threshold": "unhealthyThreshold",
    },
)
class ApprunnerServiceHealthCheckConfiguration:
    def __init__(
        self,
        *,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param healthy_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#healthy_threshold ApprunnerService#healthy_threshold}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#interval ApprunnerService#interval}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#path ApprunnerService#path}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#protocol ApprunnerService#protocol}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#timeout ApprunnerService#timeout}.
        :param unhealthy_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#unhealthy_threshold ApprunnerService#unhealthy_threshold}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e00885dcc11ebc1f3f8ece7b82fe3254d700d38e3280d7eb2028db2b2e0f52)
            check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if healthy_threshold is not None:
            self._values["healthy_threshold"] = healthy_threshold
        if interval is not None:
            self._values["interval"] = interval
        if path is not None:
            self._values["path"] = path
        if protocol is not None:
            self._values["protocol"] = protocol
        if timeout is not None:
            self._values["timeout"] = timeout
        if unhealthy_threshold is not None:
            self._values["unhealthy_threshold"] = unhealthy_threshold

    @builtins.property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#healthy_threshold ApprunnerService#healthy_threshold}.'''
        result = self._values.get("healthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#interval ApprunnerService#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#path ApprunnerService#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#protocol ApprunnerService#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#timeout ApprunnerService#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#unhealthy_threshold ApprunnerService#unhealthy_threshold}.'''
        result = self._values.get("unhealthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceHealthCheckConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApprunnerServiceHealthCheckConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceHealthCheckConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a99695328b0693df41173ccc4f7a6218f06e3b7370f403b3adcbac020149e02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHealthyThreshold")
    def reset_healthy_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthyThreshold", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetUnhealthyThreshold")
    def reset_unhealthy_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnhealthyThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="healthyThresholdInput")
    def healthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="unhealthyThresholdInput")
    def unhealthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unhealthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="healthyThreshold")
    def healthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthyThreshold"))

    @healthy_threshold.setter
    def healthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f97175fa9a5f6eafbdc2c18f0ad139063eb4e6ed08abf36d8706a974068ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthyThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb967d3a6cd17e672fe59202ef10b945b8f0fa15fac816d97ae6fbb2622d5b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7383e6e9d8ec0daa860a4caf67ea96af4da500d6bf6ca945dff9b3c0568eb85d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588824a1c52557afae1cfe85bfbd12aeb37656f3aab05c6002548a8cae8ce068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da0a25773763ca75013a94298dbe8aae41fe9248983382f9c6059ab6326e4fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unhealthyThreshold")
    def unhealthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unhealthyThreshold"))

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c0feed558a50c66baa96afe37e130db78c6472a4b82dd52d0c2c8c7bd804279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unhealthyThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceHealthCheckConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceHealthCheckConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceHealthCheckConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf1549ff200b5f8e1bc098ce57f365db5bfc882b98af98104a2ca2ef811e5b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceInstanceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "instance_role_arn": "instanceRoleArn",
        "memory": "memory",
    },
)
class ApprunnerServiceInstanceConfiguration:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        instance_role_arn: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#cpu ApprunnerService#cpu}.
        :param instance_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#instance_role_arn ApprunnerService#instance_role_arn}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#memory ApprunnerService#memory}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9b9e7c19ffad8390936753bcc3f03cd4551b1219dd3c5b58c632265a52e96a)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument instance_role_arn", value=instance_role_arn, expected_type=type_hints["instance_role_arn"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if instance_role_arn is not None:
            self._values["instance_role_arn"] = instance_role_arn
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpu(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#cpu ApprunnerService#cpu}.'''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#instance_role_arn ApprunnerService#instance_role_arn}.'''
        result = self._values.get("instance_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#memory ApprunnerService#memory}.'''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceInstanceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApprunnerServiceInstanceConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceInstanceConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9bf47d52eb12631e17d0025270721fc659d3b673784d1fce7a5657205db5f61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetInstanceRoleArn")
    def reset_instance_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceRoleArn", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceRoleArnInput")
    def instance_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceRoleArnInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e779fe68aacf88d24b85afd3f670efced1814dba9ccdef59fe8f787b14e3800a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceRoleArn")
    def instance_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceRoleArn"))

    @instance_role_arn.setter
    def instance_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5045f6290c2bd9c0ebfe04eced35cfef5bf29ba75199b1804079b6c566abca67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74a67123535f0b00f4d67844b9e6701c4a75461c161cceed6afbc2d7bc8ca2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApprunnerServiceInstanceConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceInstanceConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceInstanceConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ca7a72d5f78293867e2d0a1ff31090f681fd45557ebf0f98704b34b6625792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "egress_configuration": "egressConfiguration",
        "ingress_configuration": "ingressConfiguration",
        "ip_address_type": "ipAddressType",
    },
)
class ApprunnerServiceNetworkConfiguration:
    def __init__(
        self,
        *,
        egress_configuration: typing.Optional[typing.Union["ApprunnerServiceNetworkConfigurationEgressConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_configuration: typing.Optional[typing.Union["ApprunnerServiceNetworkConfigurationIngressConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param egress_configuration: egress_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#egress_configuration ApprunnerService#egress_configuration}
        :param ingress_configuration: ingress_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#ingress_configuration ApprunnerService#ingress_configuration}
        :param ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#ip_address_type ApprunnerService#ip_address_type}.
        '''
        if isinstance(egress_configuration, dict):
            egress_configuration = ApprunnerServiceNetworkConfigurationEgressConfiguration(**egress_configuration)
        if isinstance(ingress_configuration, dict):
            ingress_configuration = ApprunnerServiceNetworkConfigurationIngressConfiguration(**ingress_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8ccb693be6e72622967764e1917535be2a943b68cb4437fda4b5a42b4711db)
            check_type(argname="argument egress_configuration", value=egress_configuration, expected_type=type_hints["egress_configuration"])
            check_type(argname="argument ingress_configuration", value=ingress_configuration, expected_type=type_hints["ingress_configuration"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress_configuration is not None:
            self._values["egress_configuration"] = egress_configuration
        if ingress_configuration is not None:
            self._values["ingress_configuration"] = ingress_configuration
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type

    @builtins.property
    def egress_configuration(
        self,
    ) -> typing.Optional["ApprunnerServiceNetworkConfigurationEgressConfiguration"]:
        '''egress_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#egress_configuration ApprunnerService#egress_configuration}
        '''
        result = self._values.get("egress_configuration")
        return typing.cast(typing.Optional["ApprunnerServiceNetworkConfigurationEgressConfiguration"], result)

    @builtins.property
    def ingress_configuration(
        self,
    ) -> typing.Optional["ApprunnerServiceNetworkConfigurationIngressConfiguration"]:
        '''ingress_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#ingress_configuration ApprunnerService#ingress_configuration}
        '''
        result = self._values.get("ingress_configuration")
        return typing.cast(typing.Optional["ApprunnerServiceNetworkConfigurationIngressConfiguration"], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#ip_address_type ApprunnerService#ip_address_type}.'''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceNetworkConfigurationEgressConfiguration",
    jsii_struct_bases=[],
    name_mapping={"egress_type": "egressType", "vpc_connector_arn": "vpcConnectorArn"},
)
class ApprunnerServiceNetworkConfigurationEgressConfiguration:
    def __init__(
        self,
        *,
        egress_type: typing.Optional[builtins.str] = None,
        vpc_connector_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param egress_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#egress_type ApprunnerService#egress_type}.
        :param vpc_connector_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#vpc_connector_arn ApprunnerService#vpc_connector_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4de99a2e793cd247db9ddf43ae2937ad0f0dda6259ba5ec75086d1fabff5d7)
            check_type(argname="argument egress_type", value=egress_type, expected_type=type_hints["egress_type"])
            check_type(argname="argument vpc_connector_arn", value=vpc_connector_arn, expected_type=type_hints["vpc_connector_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress_type is not None:
            self._values["egress_type"] = egress_type
        if vpc_connector_arn is not None:
            self._values["vpc_connector_arn"] = vpc_connector_arn

    @builtins.property
    def egress_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#egress_type ApprunnerService#egress_type}.'''
        result = self._values.get("egress_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_connector_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#vpc_connector_arn ApprunnerService#vpc_connector_arn}.'''
        result = self._values.get("vpc_connector_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceNetworkConfigurationEgressConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApprunnerServiceNetworkConfigurationEgressConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceNetworkConfigurationEgressConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2279568f32ce6034d6411fe1bd2b07df9ebe9fd476fd4fc369689d9257fa349)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEgressType")
    def reset_egress_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressType", []))

    @jsii.member(jsii_name="resetVpcConnectorArn")
    def reset_vpc_connector_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConnectorArn", []))

    @builtins.property
    @jsii.member(jsii_name="egressTypeInput")
    def egress_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "egressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorArnInput")
    def vpc_connector_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcConnectorArnInput"))

    @builtins.property
    @jsii.member(jsii_name="egressType")
    def egress_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "egressType"))

    @egress_type.setter
    def egress_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1034513dcfda8f708df3e9cafd246ff312a1ffd23e63a0dc533e8d6d8e9ca658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorArn")
    def vpc_connector_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorArn"))

    @vpc_connector_arn.setter
    def vpc_connector_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2417732ca7e76cc5a41cc6a83ed7254782d4b92cc68ed5f0aeae704132b4d5a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnectorArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceNetworkConfigurationEgressConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceNetworkConfigurationEgressConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceNetworkConfigurationEgressConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02cf58f8a9ced8bd6cba37b9b05be74ef3ade96fa2ec54417fe0e02c8f412060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceNetworkConfigurationIngressConfiguration",
    jsii_struct_bases=[],
    name_mapping={"is_publicly_accessible": "isPubliclyAccessible"},
)
class ApprunnerServiceNetworkConfigurationIngressConfiguration:
    def __init__(
        self,
        *,
        is_publicly_accessible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_publicly_accessible: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#is_publicly_accessible ApprunnerService#is_publicly_accessible}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3a08b50cba93bc93fca1b234368197d0dcfe39ae7925ab9840a12ed621b670)
            check_type(argname="argument is_publicly_accessible", value=is_publicly_accessible, expected_type=type_hints["is_publicly_accessible"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_publicly_accessible is not None:
            self._values["is_publicly_accessible"] = is_publicly_accessible

    @builtins.property
    def is_publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#is_publicly_accessible ApprunnerService#is_publicly_accessible}.'''
        result = self._values.get("is_publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceNetworkConfigurationIngressConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApprunnerServiceNetworkConfigurationIngressConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceNetworkConfigurationIngressConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6d8cbe4ea07e3bc6e38df4e426f14586d95d07e8abe0e33268b005bea01f071)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsPubliclyAccessible")
    def reset_is_publicly_accessible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsPubliclyAccessible", []))

    @builtins.property
    @jsii.member(jsii_name="isPubliclyAccessibleInput")
    def is_publicly_accessible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isPubliclyAccessibleInput"))

    @builtins.property
    @jsii.member(jsii_name="isPubliclyAccessible")
    def is_publicly_accessible(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isPubliclyAccessible"))

    @is_publicly_accessible.setter
    def is_publicly_accessible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e995c926a469429d2381f74552201a77939ccd49e1643a573286bfb146d26d71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPubliclyAccessible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceNetworkConfigurationIngressConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceNetworkConfigurationIngressConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceNetworkConfigurationIngressConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d74a48150f6524c16308a41c3814e062c9c0a14ae8e33c0806cdfb1b6f19f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApprunnerServiceNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceNetworkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c17d8426cc9107cf2ecd4ee4b9809c552f2002160d183ab67fadcac3457eece)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEgressConfiguration")
    def put_egress_configuration(
        self,
        *,
        egress_type: typing.Optional[builtins.str] = None,
        vpc_connector_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param egress_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#egress_type ApprunnerService#egress_type}.
        :param vpc_connector_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#vpc_connector_arn ApprunnerService#vpc_connector_arn}.
        '''
        value = ApprunnerServiceNetworkConfigurationEgressConfiguration(
            egress_type=egress_type, vpc_connector_arn=vpc_connector_arn
        )

        return typing.cast(None, jsii.invoke(self, "putEgressConfiguration", [value]))

    @jsii.member(jsii_name="putIngressConfiguration")
    def put_ingress_configuration(
        self,
        *,
        is_publicly_accessible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_publicly_accessible: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#is_publicly_accessible ApprunnerService#is_publicly_accessible}.
        '''
        value = ApprunnerServiceNetworkConfigurationIngressConfiguration(
            is_publicly_accessible=is_publicly_accessible
        )

        return typing.cast(None, jsii.invoke(self, "putIngressConfiguration", [value]))

    @jsii.member(jsii_name="resetEgressConfiguration")
    def reset_egress_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressConfiguration", []))

    @jsii.member(jsii_name="resetIngressConfiguration")
    def reset_ingress_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressConfiguration", []))

    @jsii.member(jsii_name="resetIpAddressType")
    def reset_ip_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddressType", []))

    @builtins.property
    @jsii.member(jsii_name="egressConfiguration")
    def egress_configuration(
        self,
    ) -> ApprunnerServiceNetworkConfigurationEgressConfigurationOutputReference:
        return typing.cast(ApprunnerServiceNetworkConfigurationEgressConfigurationOutputReference, jsii.get(self, "egressConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="ingressConfiguration")
    def ingress_configuration(
        self,
    ) -> ApprunnerServiceNetworkConfigurationIngressConfigurationOutputReference:
        return typing.cast(ApprunnerServiceNetworkConfigurationIngressConfigurationOutputReference, jsii.get(self, "ingressConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="egressConfigurationInput")
    def egress_configuration_input(
        self,
    ) -> typing.Optional[ApprunnerServiceNetworkConfigurationEgressConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceNetworkConfigurationEgressConfiguration], jsii.get(self, "egressConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressConfigurationInput")
    def ingress_configuration_input(
        self,
    ) -> typing.Optional[ApprunnerServiceNetworkConfigurationIngressConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceNetworkConfigurationIngressConfiguration], jsii.get(self, "ingressConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressTypeInput")
    def ip_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressType"))

    @ip_address_type.setter
    def ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c0f555843a68972b859182aaefe09c9271ece891b2a1dbcfaa6c36e6275cf7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApprunnerServiceNetworkConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f222c01525dde90194e37ab12a46856f2d4a3a3a751bf1383d977325152e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceObservabilityConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "observability_enabled": "observabilityEnabled",
        "observability_configuration_arn": "observabilityConfigurationArn",
    },
)
class ApprunnerServiceObservabilityConfiguration:
    def __init__(
        self,
        *,
        observability_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        observability_configuration_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param observability_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#observability_enabled ApprunnerService#observability_enabled}.
        :param observability_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#observability_configuration_arn ApprunnerService#observability_configuration_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dec349316c737ff840768a656046578a58212b40982d1e053fc08891dce9a30)
            check_type(argname="argument observability_enabled", value=observability_enabled, expected_type=type_hints["observability_enabled"])
            check_type(argname="argument observability_configuration_arn", value=observability_configuration_arn, expected_type=type_hints["observability_configuration_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "observability_enabled": observability_enabled,
        }
        if observability_configuration_arn is not None:
            self._values["observability_configuration_arn"] = observability_configuration_arn

    @builtins.property
    def observability_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#observability_enabled ApprunnerService#observability_enabled}.'''
        result = self._values.get("observability_enabled")
        assert result is not None, "Required property 'observability_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def observability_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#observability_configuration_arn ApprunnerService#observability_configuration_arn}.'''
        result = self._values.get("observability_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceObservabilityConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApprunnerServiceObservabilityConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceObservabilityConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de01d98cbf88b922993632ede3969ef49c9785102cba7eb23fa3acea5f21ac72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetObservabilityConfigurationArn")
    def reset_observability_configuration_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObservabilityConfigurationArn", []))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationArnInput")
    def observability_configuration_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "observabilityConfigurationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="observabilityEnabledInput")
    def observability_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "observabilityEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationArn")
    def observability_configuration_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "observabilityConfigurationArn"))

    @observability_configuration_arn.setter
    def observability_configuration_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a4295d9217b9c1ca03c27bee805caf9c5d831d02c2e0bd447480278e00cf92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "observabilityConfigurationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="observabilityEnabled")
    def observability_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "observabilityEnabled"))

    @observability_enabled.setter
    def observability_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a5328b156379b33362e44711a5130e310b6b2c947859f3ae19be772f864407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "observabilityEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceObservabilityConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceObservabilityConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceObservabilityConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1001793e2330745933a70727773513faea4e85a24269af2f7492cb0fbc6aa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_configuration": "authenticationConfiguration",
        "auto_deployments_enabled": "autoDeploymentsEnabled",
        "code_repository": "codeRepository",
        "image_repository": "imageRepository",
    },
)
class ApprunnerServiceSourceConfiguration:
    def __init__(
        self,
        *,
        authentication_configuration: typing.Optional[typing.Union["ApprunnerServiceSourceConfigurationAuthenticationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_deployments_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        code_repository: typing.Optional[typing.Union["ApprunnerServiceSourceConfigurationCodeRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        image_repository: typing.Optional[typing.Union["ApprunnerServiceSourceConfigurationImageRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authentication_configuration: authentication_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#authentication_configuration ApprunnerService#authentication_configuration}
        :param auto_deployments_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#auto_deployments_enabled ApprunnerService#auto_deployments_enabled}.
        :param code_repository: code_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#code_repository ApprunnerService#code_repository}
        :param image_repository: image_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_repository ApprunnerService#image_repository}
        '''
        if isinstance(authentication_configuration, dict):
            authentication_configuration = ApprunnerServiceSourceConfigurationAuthenticationConfiguration(**authentication_configuration)
        if isinstance(code_repository, dict):
            code_repository = ApprunnerServiceSourceConfigurationCodeRepository(**code_repository)
        if isinstance(image_repository, dict):
            image_repository = ApprunnerServiceSourceConfigurationImageRepository(**image_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b66bf5a977e30300e523b2ad3fc13fcee260045caaacf2b0eeafad9cdd107b1)
            check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
            check_type(argname="argument auto_deployments_enabled", value=auto_deployments_enabled, expected_type=type_hints["auto_deployments_enabled"])
            check_type(argname="argument code_repository", value=code_repository, expected_type=type_hints["code_repository"])
            check_type(argname="argument image_repository", value=image_repository, expected_type=type_hints["image_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_configuration is not None:
            self._values["authentication_configuration"] = authentication_configuration
        if auto_deployments_enabled is not None:
            self._values["auto_deployments_enabled"] = auto_deployments_enabled
        if code_repository is not None:
            self._values["code_repository"] = code_repository
        if image_repository is not None:
            self._values["image_repository"] = image_repository

    @builtins.property
    def authentication_configuration(
        self,
    ) -> typing.Optional["ApprunnerServiceSourceConfigurationAuthenticationConfiguration"]:
        '''authentication_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#authentication_configuration ApprunnerService#authentication_configuration}
        '''
        result = self._values.get("authentication_configuration")
        return typing.cast(typing.Optional["ApprunnerServiceSourceConfigurationAuthenticationConfiguration"], result)

    @builtins.property
    def auto_deployments_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#auto_deployments_enabled ApprunnerService#auto_deployments_enabled}.'''
        result = self._values.get("auto_deployments_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def code_repository(
        self,
    ) -> typing.Optional["ApprunnerServiceSourceConfigurationCodeRepository"]:
        '''code_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#code_repository ApprunnerService#code_repository}
        '''
        result = self._values.get("code_repository")
        return typing.cast(typing.Optional["ApprunnerServiceSourceConfigurationCodeRepository"], result)

    @builtins.property
    def image_repository(
        self,
    ) -> typing.Optional["ApprunnerServiceSourceConfigurationImageRepository"]:
        '''image_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_repository ApprunnerService#image_repository}
        '''
        result = self._values.get("image_repository")
        return typing.cast(typing.Optional["ApprunnerServiceSourceConfigurationImageRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceSourceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationAuthenticationConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "access_role_arn": "accessRoleArn",
        "connection_arn": "connectionArn",
    },
)
class ApprunnerServiceSourceConfigurationAuthenticationConfiguration:
    def __init__(
        self,
        *,
        access_role_arn: typing.Optional[builtins.str] = None,
        connection_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#access_role_arn ApprunnerService#access_role_arn}.
        :param connection_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#connection_arn ApprunnerService#connection_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45e17899938632ac3bb7ea8f33989f85d3151a1e9703fdf672bb48a4f644721)
            check_type(argname="argument access_role_arn", value=access_role_arn, expected_type=type_hints["access_role_arn"])
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_role_arn is not None:
            self._values["access_role_arn"] = access_role_arn
        if connection_arn is not None:
            self._values["connection_arn"] = connection_arn

    @builtins.property
    def access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#access_role_arn ApprunnerService#access_role_arn}.'''
        result = self._values.get("access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#connection_arn ApprunnerService#connection_arn}.'''
        result = self._values.get("connection_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceSourceConfigurationAuthenticationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApprunnerServiceSourceConfigurationAuthenticationConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationAuthenticationConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59f8db6cdaeb148235e6640a2673c4b1ce7a2e7fc55f69c35557de5f3b62683a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessRoleArn")
    def reset_access_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessRoleArn", []))

    @jsii.member(jsii_name="resetConnectionArn")
    def reset_connection_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionArn", []))

    @builtins.property
    @jsii.member(jsii_name="accessRoleArnInput")
    def access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionArnInput")
    def connection_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="accessRoleArn")
    def access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessRoleArn"))

    @access_role_arn.setter
    def access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca511f56537fd3ab91c99441e030292a665fb9f87e2b07ed0006ac9a60c879db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @connection_arn.setter
    def connection_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8951e3aff3d01a5c4fc7bb2aac6a73b433aa51f116e1518d89babb95c28870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationAuthenticationConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationAuthenticationConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceSourceConfigurationAuthenticationConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeaf3a0c271b0602711f14b28e29bfd8f166fdd577c63a2dc3aef2825e3f59de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationCodeRepository",
    jsii_struct_bases=[],
    name_mapping={
        "repository_url": "repositoryUrl",
        "source_code_version": "sourceCodeVersion",
        "code_configuration": "codeConfiguration",
        "source_directory": "sourceDirectory",
    },
)
class ApprunnerServiceSourceConfigurationCodeRepository:
    def __init__(
        self,
        *,
        repository_url: builtins.str,
        source_code_version: typing.Union["ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion", typing.Dict[builtins.str, typing.Any]],
        code_configuration: typing.Optional[typing.Union["ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        source_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#repository_url ApprunnerService#repository_url}.
        :param source_code_version: source_code_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#source_code_version ApprunnerService#source_code_version}
        :param code_configuration: code_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#code_configuration ApprunnerService#code_configuration}
        :param source_directory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#source_directory ApprunnerService#source_directory}.
        '''
        if isinstance(source_code_version, dict):
            source_code_version = ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion(**source_code_version)
        if isinstance(code_configuration, dict):
            code_configuration = ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration(**code_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd736118280a4378e2cf94ebac3cfac9b0bb0e024bac33f6149ccb9bc5432a44)
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
            check_type(argname="argument source_code_version", value=source_code_version, expected_type=type_hints["source_code_version"])
            check_type(argname="argument code_configuration", value=code_configuration, expected_type=type_hints["code_configuration"])
            check_type(argname="argument source_directory", value=source_directory, expected_type=type_hints["source_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_url": repository_url,
            "source_code_version": source_code_version,
        }
        if code_configuration is not None:
            self._values["code_configuration"] = code_configuration
        if source_directory is not None:
            self._values["source_directory"] = source_directory

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#repository_url ApprunnerService#repository_url}.'''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_code_version(
        self,
    ) -> "ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion":
        '''source_code_version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#source_code_version ApprunnerService#source_code_version}
        '''
        result = self._values.get("source_code_version")
        assert result is not None, "Required property 'source_code_version' is missing"
        return typing.cast("ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion", result)

    @builtins.property
    def code_configuration(
        self,
    ) -> typing.Optional["ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration"]:
        '''code_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#code_configuration ApprunnerService#code_configuration}
        '''
        result = self._values.get("code_configuration")
        return typing.cast(typing.Optional["ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration"], result)

    @builtins.property
    def source_directory(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#source_directory ApprunnerService#source_directory}.'''
        result = self._values.get("source_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceSourceConfigurationCodeRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_source": "configurationSource",
        "code_configuration_values": "codeConfigurationValues",
    },
)
class ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration:
    def __init__(
        self,
        *,
        configuration_source: builtins.str,
        code_configuration_values: typing.Optional[typing.Union["ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configuration_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#configuration_source ApprunnerService#configuration_source}.
        :param code_configuration_values: code_configuration_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#code_configuration_values ApprunnerService#code_configuration_values}
        '''
        if isinstance(code_configuration_values, dict):
            code_configuration_values = ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues(**code_configuration_values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c7f6c12f3de45877b3456991e07e075c43c3ce556fad75c2db6a2bbe5f1aaf)
            check_type(argname="argument configuration_source", value=configuration_source, expected_type=type_hints["configuration_source"])
            check_type(argname="argument code_configuration_values", value=code_configuration_values, expected_type=type_hints["code_configuration_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_source": configuration_source,
        }
        if code_configuration_values is not None:
            self._values["code_configuration_values"] = code_configuration_values

    @builtins.property
    def configuration_source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#configuration_source ApprunnerService#configuration_source}.'''
        result = self._values.get("configuration_source")
        assert result is not None, "Required property 'configuration_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code_configuration_values(
        self,
    ) -> typing.Optional["ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues"]:
        '''code_configuration_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#code_configuration_values ApprunnerService#code_configuration_values}
        '''
        result = self._values.get("code_configuration_values")
        return typing.cast(typing.Optional["ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues",
    jsii_struct_bases=[],
    name_mapping={
        "runtime": "runtime",
        "build_command": "buildCommand",
        "port": "port",
        "runtime_environment_secrets": "runtimeEnvironmentSecrets",
        "runtime_environment_variables": "runtimeEnvironmentVariables",
        "start_command": "startCommand",
    },
)
class ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues:
    def __init__(
        self,
        *,
        runtime: builtins.str,
        build_command: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        runtime_environment_secrets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        runtime_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        start_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime ApprunnerService#runtime}.
        :param build_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#build_command ApprunnerService#build_command}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#port ApprunnerService#port}.
        :param runtime_environment_secrets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_secrets ApprunnerService#runtime_environment_secrets}.
        :param runtime_environment_variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_variables ApprunnerService#runtime_environment_variables}.
        :param start_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#start_command ApprunnerService#start_command}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c1f90b06912a16fe4af736ac45ec58c1ad167fb22ca44eb412af5111157443)
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument runtime_environment_secrets", value=runtime_environment_secrets, expected_type=type_hints["runtime_environment_secrets"])
            check_type(argname="argument runtime_environment_variables", value=runtime_environment_variables, expected_type=type_hints["runtime_environment_variables"])
            check_type(argname="argument start_command", value=start_command, expected_type=type_hints["start_command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "runtime": runtime,
        }
        if build_command is not None:
            self._values["build_command"] = build_command
        if port is not None:
            self._values["port"] = port
        if runtime_environment_secrets is not None:
            self._values["runtime_environment_secrets"] = runtime_environment_secrets
        if runtime_environment_variables is not None:
            self._values["runtime_environment_variables"] = runtime_environment_variables
        if start_command is not None:
            self._values["start_command"] = start_command

    @builtins.property
    def runtime(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime ApprunnerService#runtime}.'''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#build_command ApprunnerService#build_command}.'''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#port ApprunnerService#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_environment_secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_secrets ApprunnerService#runtime_environment_secrets}.'''
        result = self._values.get("runtime_environment_secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def runtime_environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_variables ApprunnerService#runtime_environment_variables}.'''
        result = self._values.get("runtime_environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def start_command(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#start_command ApprunnerService#start_command}.'''
        result = self._values.get("start_command")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afe15dbc1fb43612bf40412d0224240a3a5fca6153868d8b0a4d1b72c2006b24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBuildCommand")
    def reset_build_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildCommand", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetRuntimeEnvironmentSecrets")
    def reset_runtime_environment_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeEnvironmentSecrets", []))

    @jsii.member(jsii_name="resetRuntimeEnvironmentVariables")
    def reset_runtime_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeEnvironmentVariables", []))

    @jsii.member(jsii_name="resetStartCommand")
    def reset_start_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartCommand", []))

    @builtins.property
    @jsii.member(jsii_name="buildCommandInput")
    def build_command_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildCommandInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeEnvironmentSecretsInput")
    def runtime_environment_secrets_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "runtimeEnvironmentSecretsInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeEnvironmentVariablesInput")
    def runtime_environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "runtimeEnvironmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startCommandInput")
    def start_command_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startCommandInput"))

    @builtins.property
    @jsii.member(jsii_name="buildCommand")
    def build_command(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildCommand"))

    @build_command.setter
    def build_command(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec4565e36f538540a9a645ba6a48e05b3ae2aaf86c2be605b1ee5f279153a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildCommand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f828173b6023d515cab77c3a258e894278f95474734e741e9ffc0bc7ea42e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c35d02bf5505df29d3ac79bf155995567a9c5c669a45b45f537cd84b6223c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeEnvironmentSecrets")
    def runtime_environment_secrets(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "runtimeEnvironmentSecrets"))

    @runtime_environment_secrets.setter
    def runtime_environment_secrets(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6384d2e936d429b5e8c261d8437ee327d7f470b62cbc34e9b39d8bc0307bf956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeEnvironmentSecrets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeEnvironmentVariables")
    def runtime_environment_variables(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "runtimeEnvironmentVariables"))

    @runtime_environment_variables.setter
    def runtime_environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0eb69b3513a6a64c4b4626ea376e154a5ca4e7cc75b7e178cb853bf024195b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeEnvironmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startCommand")
    def start_command(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startCommand"))

    @start_command.setter
    def start_command(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a14347daa470ab1a5375521691ed41499cbbc1d794254a4fbbf278da926668f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startCommand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5640abf7750f5926dbd8e74ffc25ce467c19c87d53e1082e53377820096605c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b60a73d853206f16abb03fde0444d5a98fd5480da8696b71c82e54be1bb61c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCodeConfigurationValues")
    def put_code_configuration_values(
        self,
        *,
        runtime: builtins.str,
        build_command: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        runtime_environment_secrets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        runtime_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        start_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime ApprunnerService#runtime}.
        :param build_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#build_command ApprunnerService#build_command}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#port ApprunnerService#port}.
        :param runtime_environment_secrets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_secrets ApprunnerService#runtime_environment_secrets}.
        :param runtime_environment_variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_variables ApprunnerService#runtime_environment_variables}.
        :param start_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#start_command ApprunnerService#start_command}.
        '''
        value = ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues(
            runtime=runtime,
            build_command=build_command,
            port=port,
            runtime_environment_secrets=runtime_environment_secrets,
            runtime_environment_variables=runtime_environment_variables,
            start_command=start_command,
        )

        return typing.cast(None, jsii.invoke(self, "putCodeConfigurationValues", [value]))

    @jsii.member(jsii_name="resetCodeConfigurationValues")
    def reset_code_configuration_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeConfigurationValues", []))

    @builtins.property
    @jsii.member(jsii_name="codeConfigurationValues")
    def code_configuration_values(
        self,
    ) -> ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesOutputReference:
        return typing.cast(ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesOutputReference, jsii.get(self, "codeConfigurationValues"))

    @builtins.property
    @jsii.member(jsii_name="codeConfigurationValuesInput")
    def code_configuration_values_input(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues], jsii.get(self, "codeConfigurationValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationSourceInput")
    def configuration_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationSource")
    def configuration_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configurationSource"))

    @configuration_source.setter
    def configuration_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52f0d2e906ae037c2ba13d92eb8f4f26dbc88b682d8261f0835fc5d57ddac63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e332996fd4ae6d77bc1e95c62b30e1a8fe602230d23764bb9f5f439879b1a869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApprunnerServiceSourceConfigurationCodeRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationCodeRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2af4bdb0eff8b0e221e5e48e48fca75bd30beb6e29ed116da0f0eb93f2baa4c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCodeConfiguration")
    def put_code_configuration(
        self,
        *,
        configuration_source: builtins.str,
        code_configuration_values: typing.Optional[typing.Union[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configuration_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#configuration_source ApprunnerService#configuration_source}.
        :param code_configuration_values: code_configuration_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#code_configuration_values ApprunnerService#code_configuration_values}
        '''
        value = ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration(
            configuration_source=configuration_source,
            code_configuration_values=code_configuration_values,
        )

        return typing.cast(None, jsii.invoke(self, "putCodeConfiguration", [value]))

    @jsii.member(jsii_name="putSourceCodeVersion")
    def put_source_code_version(
        self,
        *,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#type ApprunnerService#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#value ApprunnerService#value}.
        '''
        value_ = ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putSourceCodeVersion", [value_]))

    @jsii.member(jsii_name="resetCodeConfiguration")
    def reset_code_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeConfiguration", []))

    @jsii.member(jsii_name="resetSourceDirectory")
    def reset_source_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceDirectory", []))

    @builtins.property
    @jsii.member(jsii_name="codeConfiguration")
    def code_configuration(
        self,
    ) -> ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationOutputReference:
        return typing.cast(ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationOutputReference, jsii.get(self, "codeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="sourceCodeVersion")
    def source_code_version(
        self,
    ) -> "ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersionOutputReference":
        return typing.cast("ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersionOutputReference", jsii.get(self, "sourceCodeVersion"))

    @builtins.property
    @jsii.member(jsii_name="codeConfigurationInput")
    def code_configuration_input(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration], jsii.get(self, "codeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUrlInput")
    def repository_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceCodeVersionInput")
    def source_code_version_input(
        self,
    ) -> typing.Optional["ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion"]:
        return typing.cast(typing.Optional["ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion"], jsii.get(self, "sourceCodeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDirectoryInput")
    def source_directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUrl")
    def repository_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryUrl"))

    @repository_url.setter
    def repository_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad2f491817436bbc919cbfc2188363c798157350a3d873ddb50fa58df840777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceDirectory")
    def source_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDirectory"))

    @source_directory.setter
    def source_directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2dc0802ade1626983168fbba71bd523be8038073a52ad32916eed6aacfae21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationCodeRepository]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationCodeRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceSourceConfigurationCodeRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468a10f597de73f16bc476d8cccca9c2a8c6aa845797bd14fb5193fbd083d868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion:
    def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#type ApprunnerService#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#value ApprunnerService#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e1eef1bee6dfcdd6b01783bf0de7387ad0dcb7db85b9299152a4a4793547ce2)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#type ApprunnerService#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#value ApprunnerService#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__828bd595397c0a92d7b4e2609cddb996a82822e0fe7b48c86550d1863ee4b370)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1382fb5b7d55ac595148965393e10e83183e4dac04e3d4e65ab8944e8789e57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f83ec7fd7acbdea7f24418f8048cf82d8110313e10e23a3b02ba85a42db8992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56b213a8deaf0eaf7289299f45318690dd7dd02c631d59db6bc217eeab47dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationImageRepository",
    jsii_struct_bases=[],
    name_mapping={
        "image_identifier": "imageIdentifier",
        "image_repository_type": "imageRepositoryType",
        "image_configuration": "imageConfiguration",
    },
)
class ApprunnerServiceSourceConfigurationImageRepository:
    def __init__(
        self,
        *,
        image_identifier: builtins.str,
        image_repository_type: builtins.str,
        image_configuration: typing.Optional[typing.Union["ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param image_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_identifier ApprunnerService#image_identifier}.
        :param image_repository_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_repository_type ApprunnerService#image_repository_type}.
        :param image_configuration: image_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_configuration ApprunnerService#image_configuration}
        '''
        if isinstance(image_configuration, dict):
            image_configuration = ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration(**image_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe556c20e37feebb502bef5a6fe8649ab6d0b1f7bbd17445c75327fe1e0e21a)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
            check_type(argname="argument image_repository_type", value=image_repository_type, expected_type=type_hints["image_repository_type"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_identifier": image_identifier,
            "image_repository_type": image_repository_type,
        }
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration

    @builtins.property
    def image_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_identifier ApprunnerService#image_identifier}.'''
        result = self._values.get("image_identifier")
        assert result is not None, "Required property 'image_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_repository_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_repository_type ApprunnerService#image_repository_type}.'''
        result = self._values.get("image_repository_type")
        assert result is not None, "Required property 'image_repository_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_configuration(
        self,
    ) -> typing.Optional["ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration"]:
        '''image_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_configuration ApprunnerService#image_configuration}
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional["ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceSourceConfigurationImageRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "runtime_environment_secrets": "runtimeEnvironmentSecrets",
        "runtime_environment_variables": "runtimeEnvironmentVariables",
        "start_command": "startCommand",
    },
)
class ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration:
    def __init__(
        self,
        *,
        port: typing.Optional[builtins.str] = None,
        runtime_environment_secrets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        runtime_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        start_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#port ApprunnerService#port}.
        :param runtime_environment_secrets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_secrets ApprunnerService#runtime_environment_secrets}.
        :param runtime_environment_variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_variables ApprunnerService#runtime_environment_variables}.
        :param start_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#start_command ApprunnerService#start_command}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851fa8e57f4bb9f207470d178f6a32ba340cf1a387167799316a28a47e22c34a)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument runtime_environment_secrets", value=runtime_environment_secrets, expected_type=type_hints["runtime_environment_secrets"])
            check_type(argname="argument runtime_environment_variables", value=runtime_environment_variables, expected_type=type_hints["runtime_environment_variables"])
            check_type(argname="argument start_command", value=start_command, expected_type=type_hints["start_command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if runtime_environment_secrets is not None:
            self._values["runtime_environment_secrets"] = runtime_environment_secrets
        if runtime_environment_variables is not None:
            self._values["runtime_environment_variables"] = runtime_environment_variables
        if start_command is not None:
            self._values["start_command"] = start_command

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#port ApprunnerService#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_environment_secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_secrets ApprunnerService#runtime_environment_secrets}.'''
        result = self._values.get("runtime_environment_secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def runtime_environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_variables ApprunnerService#runtime_environment_variables}.'''
        result = self._values.get("runtime_environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def start_command(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#start_command ApprunnerService#start_command}.'''
        result = self._values.get("start_command")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApprunnerServiceSourceConfigurationImageRepositoryImageConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationImageRepositoryImageConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30a1628998c68af9b3dec79847c9955d0ad0e390663f3832c1a9ab2f15347e22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetRuntimeEnvironmentSecrets")
    def reset_runtime_environment_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeEnvironmentSecrets", []))

    @jsii.member(jsii_name="resetRuntimeEnvironmentVariables")
    def reset_runtime_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeEnvironmentVariables", []))

    @jsii.member(jsii_name="resetStartCommand")
    def reset_start_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartCommand", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeEnvironmentSecretsInput")
    def runtime_environment_secrets_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "runtimeEnvironmentSecretsInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeEnvironmentVariablesInput")
    def runtime_environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "runtimeEnvironmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="startCommandInput")
    def start_command_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startCommandInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a015c60de9db7bd1e0d2f3c6071b5468c0f6afd146ae0ca9f31621a073779e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeEnvironmentSecrets")
    def runtime_environment_secrets(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "runtimeEnvironmentSecrets"))

    @runtime_environment_secrets.setter
    def runtime_environment_secrets(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e5f080533fc0774b90c52e4be16d6f2427614025fcc60a5987d8df90c24bd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeEnvironmentSecrets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeEnvironmentVariables")
    def runtime_environment_variables(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "runtimeEnvironmentVariables"))

    @runtime_environment_variables.setter
    def runtime_environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522516a5c5913e81b83d6871944ec261097b6d34045553730d98d229d7a53f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeEnvironmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startCommand")
    def start_command(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startCommand"))

    @start_command.setter
    def start_command(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6ec1edc852776adb6a42dcbcd84e9b74181d2193ad86d9be65e87fc1111a0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startCommand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea01c0bdd5a30cd8067818bc0a2ef708fa422200037051d6f57398908c30b8ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApprunnerServiceSourceConfigurationImageRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationImageRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__265fb325bbca3f18d40fe6d15cd2ebcc1056a8c7e012a8fb651dd08a2bb12a50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putImageConfiguration")
    def put_image_configuration(
        self,
        *,
        port: typing.Optional[builtins.str] = None,
        runtime_environment_secrets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        runtime_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        start_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#port ApprunnerService#port}.
        :param runtime_environment_secrets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_secrets ApprunnerService#runtime_environment_secrets}.
        :param runtime_environment_variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#runtime_environment_variables ApprunnerService#runtime_environment_variables}.
        :param start_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#start_command ApprunnerService#start_command}.
        '''
        value = ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration(
            port=port,
            runtime_environment_secrets=runtime_environment_secrets,
            runtime_environment_variables=runtime_environment_variables,
            start_command=start_command,
        )

        return typing.cast(None, jsii.invoke(self, "putImageConfiguration", [value]))

    @jsii.member(jsii_name="resetImageConfiguration")
    def reset_image_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="imageConfiguration")
    def image_configuration(
        self,
    ) -> ApprunnerServiceSourceConfigurationImageRepositoryImageConfigurationOutputReference:
        return typing.cast(ApprunnerServiceSourceConfigurationImageRepositoryImageConfigurationOutputReference, jsii.get(self, "imageConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="imageConfigurationInput")
    def image_configuration_input(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration], jsii.get(self, "imageConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="imageIdentifierInput")
    def image_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="imageRepositoryTypeInput")
    def image_repository_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageRepositoryTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="imageIdentifier")
    def image_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageIdentifier"))

    @image_identifier.setter
    def image_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e429208622f291a30f3bb7a900cef451e08f0fe9cd4b4c08193222e9318a9bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageRepositoryType")
    def image_repository_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageRepositoryType"))

    @image_repository_type.setter
    def image_repository_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d27d500e6187d908d312fa5d76d513a02ecd1025f2b9e792203b32c9d80ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageRepositoryType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationImageRepository]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationImageRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceSourceConfigurationImageRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af8780cb04110d2e368fa874c110c590c2f6a7e67e8c517da91c88420b3634a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApprunnerServiceSourceConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.apprunnerService.ApprunnerServiceSourceConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89d1068c43f9d1e52768c23cc3ed0b1eab7f38e546bcce32ed9a9a75a54a4684)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthenticationConfiguration")
    def put_authentication_configuration(
        self,
        *,
        access_role_arn: typing.Optional[builtins.str] = None,
        connection_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#access_role_arn ApprunnerService#access_role_arn}.
        :param connection_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#connection_arn ApprunnerService#connection_arn}.
        '''
        value = ApprunnerServiceSourceConfigurationAuthenticationConfiguration(
            access_role_arn=access_role_arn, connection_arn=connection_arn
        )

        return typing.cast(None, jsii.invoke(self, "putAuthenticationConfiguration", [value]))

    @jsii.member(jsii_name="putCodeRepository")
    def put_code_repository(
        self,
        *,
        repository_url: builtins.str,
        source_code_version: typing.Union[ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion, typing.Dict[builtins.str, typing.Any]],
        code_configuration: typing.Optional[typing.Union[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        source_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#repository_url ApprunnerService#repository_url}.
        :param source_code_version: source_code_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#source_code_version ApprunnerService#source_code_version}
        :param code_configuration: code_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#code_configuration ApprunnerService#code_configuration}
        :param source_directory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#source_directory ApprunnerService#source_directory}.
        '''
        value = ApprunnerServiceSourceConfigurationCodeRepository(
            repository_url=repository_url,
            source_code_version=source_code_version,
            code_configuration=code_configuration,
            source_directory=source_directory,
        )

        return typing.cast(None, jsii.invoke(self, "putCodeRepository", [value]))

    @jsii.member(jsii_name="putImageRepository")
    def put_image_repository(
        self,
        *,
        image_identifier: builtins.str,
        image_repository_type: builtins.str,
        image_configuration: typing.Optional[typing.Union[ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param image_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_identifier ApprunnerService#image_identifier}.
        :param image_repository_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_repository_type ApprunnerService#image_repository_type}.
        :param image_configuration: image_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/apprunner_service#image_configuration ApprunnerService#image_configuration}
        '''
        value = ApprunnerServiceSourceConfigurationImageRepository(
            image_identifier=image_identifier,
            image_repository_type=image_repository_type,
            image_configuration=image_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putImageRepository", [value]))

    @jsii.member(jsii_name="resetAuthenticationConfiguration")
    def reset_authentication_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationConfiguration", []))

    @jsii.member(jsii_name="resetAutoDeploymentsEnabled")
    def reset_auto_deployments_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeploymentsEnabled", []))

    @jsii.member(jsii_name="resetCodeRepository")
    def reset_code_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeRepository", []))

    @jsii.member(jsii_name="resetImageRepository")
    def reset_image_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageRepository", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfiguration")
    def authentication_configuration(
        self,
    ) -> ApprunnerServiceSourceConfigurationAuthenticationConfigurationOutputReference:
        return typing.cast(ApprunnerServiceSourceConfigurationAuthenticationConfigurationOutputReference, jsii.get(self, "authenticationConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="codeRepository")
    def code_repository(
        self,
    ) -> ApprunnerServiceSourceConfigurationCodeRepositoryOutputReference:
        return typing.cast(ApprunnerServiceSourceConfigurationCodeRepositoryOutputReference, jsii.get(self, "codeRepository"))

    @builtins.property
    @jsii.member(jsii_name="imageRepository")
    def image_repository(
        self,
    ) -> ApprunnerServiceSourceConfigurationImageRepositoryOutputReference:
        return typing.cast(ApprunnerServiceSourceConfigurationImageRepositoryOutputReference, jsii.get(self, "imageRepository"))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfigurationInput")
    def authentication_configuration_input(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationAuthenticationConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationAuthenticationConfiguration], jsii.get(self, "authenticationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeploymentsEnabledInput")
    def auto_deployments_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoDeploymentsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="codeRepositoryInput")
    def code_repository_input(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationCodeRepository]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationCodeRepository], jsii.get(self, "codeRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="imageRepositoryInput")
    def image_repository_input(
        self,
    ) -> typing.Optional[ApprunnerServiceSourceConfigurationImageRepository]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfigurationImageRepository], jsii.get(self, "imageRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeploymentsEnabled")
    def auto_deployments_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoDeploymentsEnabled"))

    @auto_deployments_enabled.setter
    def auto_deployments_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8cf4a2208a4ec710ab5cc9ba18a08397a11abbe9b5bae50c9c5c01f68e4ba71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeploymentsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApprunnerServiceSourceConfiguration]:
        return typing.cast(typing.Optional[ApprunnerServiceSourceConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApprunnerServiceSourceConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de1b3119e39744a3c965173f6aba6dd79bf5ffde6f953ec46c828430f841b207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApprunnerService",
    "ApprunnerServiceConfig",
    "ApprunnerServiceEncryptionConfiguration",
    "ApprunnerServiceEncryptionConfigurationOutputReference",
    "ApprunnerServiceHealthCheckConfiguration",
    "ApprunnerServiceHealthCheckConfigurationOutputReference",
    "ApprunnerServiceInstanceConfiguration",
    "ApprunnerServiceInstanceConfigurationOutputReference",
    "ApprunnerServiceNetworkConfiguration",
    "ApprunnerServiceNetworkConfigurationEgressConfiguration",
    "ApprunnerServiceNetworkConfigurationEgressConfigurationOutputReference",
    "ApprunnerServiceNetworkConfigurationIngressConfiguration",
    "ApprunnerServiceNetworkConfigurationIngressConfigurationOutputReference",
    "ApprunnerServiceNetworkConfigurationOutputReference",
    "ApprunnerServiceObservabilityConfiguration",
    "ApprunnerServiceObservabilityConfigurationOutputReference",
    "ApprunnerServiceSourceConfiguration",
    "ApprunnerServiceSourceConfigurationAuthenticationConfiguration",
    "ApprunnerServiceSourceConfigurationAuthenticationConfigurationOutputReference",
    "ApprunnerServiceSourceConfigurationCodeRepository",
    "ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration",
    "ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues",
    "ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesOutputReference",
    "ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationOutputReference",
    "ApprunnerServiceSourceConfigurationCodeRepositoryOutputReference",
    "ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion",
    "ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersionOutputReference",
    "ApprunnerServiceSourceConfigurationImageRepository",
    "ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration",
    "ApprunnerServiceSourceConfigurationImageRepositoryImageConfigurationOutputReference",
    "ApprunnerServiceSourceConfigurationImageRepositoryOutputReference",
    "ApprunnerServiceSourceConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__151db1605640873f5f95ba4c8e37ee1b83a3cb47260b335f0ea20a37438691c8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    service_name: builtins.str,
    source_configuration: typing.Union[ApprunnerServiceSourceConfiguration, typing.Dict[builtins.str, typing.Any]],
    auto_scaling_configuration_arn: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[ApprunnerServiceEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    health_check_configuration: typing.Optional[typing.Union[ApprunnerServiceHealthCheckConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_configuration: typing.Optional[typing.Union[ApprunnerServiceInstanceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    network_configuration: typing.Optional[typing.Union[ApprunnerServiceNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    observability_configuration: typing.Optional[typing.Union[ApprunnerServiceObservabilityConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__9d0007aee4f3db63680742afec4a93757ea8adb11a6694e25b4f1daaa92f63cd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f191837d16d585a0a586e36c9f06f40bac3850e54321b3f02d1cd3887f943e55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abeaf402e709e01def8cb5eccfe704ddd017b26fcb93e8cdc592356db0448470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd8656f657bd3db20078bca985dc382e9ff57a8254c7b118039678eb138eb01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99c8c8c0f51a7f555a4c52ae36039ece4fbed9d63ba0cb1bfe0ef35d08f7b61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb56158ac146089b62066f8c178cc9406b97be3855a685cad056d36ae54ccd5b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8ff997019525beb72a2b642e0eecc0c4285d0ade48dce1eb45a66cbc691ebc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8677de2af13e11b6d0b22f45684bc5030ec440ade76d8dad4e22fe04160808b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: builtins.str,
    source_configuration: typing.Union[ApprunnerServiceSourceConfiguration, typing.Dict[builtins.str, typing.Any]],
    auto_scaling_configuration_arn: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[ApprunnerServiceEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    health_check_configuration: typing.Optional[typing.Union[ApprunnerServiceHealthCheckConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_configuration: typing.Optional[typing.Union[ApprunnerServiceInstanceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    network_configuration: typing.Optional[typing.Union[ApprunnerServiceNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    observability_configuration: typing.Optional[typing.Union[ApprunnerServiceObservabilityConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bba09ae72cb41b697cec4c25c7a55e3d9d10b6b3b7bacba5dc24bf73bfa883b(
    *,
    kms_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3f0b5520b085d7c0f2ec263011d9ab25304960937aaf7eb9aa1caf62b43c21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ef54ce7cbb08c9a5d4d614f3bbcb481e921eab01fe31b65a9f4568bc334d38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea995c20f0029cf247acde4a61eb34503855fb048fc9029cfcb8be17556d186e(
    value: typing.Optional[ApprunnerServiceEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e00885dcc11ebc1f3f8ece7b82fe3254d700d38e3280d7eb2028db2b2e0f52(
    *,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a99695328b0693df41173ccc4f7a6218f06e3b7370f403b3adcbac020149e02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f97175fa9a5f6eafbdc2c18f0ad139063eb4e6ed08abf36d8706a974068ff0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb967d3a6cd17e672fe59202ef10b945b8f0fa15fac816d97ae6fbb2622d5b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7383e6e9d8ec0daa860a4caf67ea96af4da500d6bf6ca945dff9b3c0568eb85d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588824a1c52557afae1cfe85bfbd12aeb37656f3aab05c6002548a8cae8ce068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da0a25773763ca75013a94298dbe8aae41fe9248983382f9c6059ab6326e4fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0feed558a50c66baa96afe37e130db78c6472a4b82dd52d0c2c8c7bd804279(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1549ff200b5f8e1bc098ce57f365db5bfc882b98af98104a2ca2ef811e5b6a(
    value: typing.Optional[ApprunnerServiceHealthCheckConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9b9e7c19ffad8390936753bcc3f03cd4551b1219dd3c5b58c632265a52e96a(
    *,
    cpu: typing.Optional[builtins.str] = None,
    instance_role_arn: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bf47d52eb12631e17d0025270721fc659d3b673784d1fce7a5657205db5f61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e779fe68aacf88d24b85afd3f670efced1814dba9ccdef59fe8f787b14e3800a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5045f6290c2bd9c0ebfe04eced35cfef5bf29ba75199b1804079b6c566abca67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74a67123535f0b00f4d67844b9e6701c4a75461c161cceed6afbc2d7bc8ca2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ca7a72d5f78293867e2d0a1ff31090f681fd45557ebf0f98704b34b6625792(
    value: typing.Optional[ApprunnerServiceInstanceConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8ccb693be6e72622967764e1917535be2a943b68cb4437fda4b5a42b4711db(
    *,
    egress_configuration: typing.Optional[typing.Union[ApprunnerServiceNetworkConfigurationEgressConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_configuration: typing.Optional[typing.Union[ApprunnerServiceNetworkConfigurationIngressConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4de99a2e793cd247db9ddf43ae2937ad0f0dda6259ba5ec75086d1fabff5d7(
    *,
    egress_type: typing.Optional[builtins.str] = None,
    vpc_connector_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2279568f32ce6034d6411fe1bd2b07df9ebe9fd476fd4fc369689d9257fa349(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1034513dcfda8f708df3e9cafd246ff312a1ffd23e63a0dc533e8d6d8e9ca658(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2417732ca7e76cc5a41cc6a83ed7254782d4b92cc68ed5f0aeae704132b4d5a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02cf58f8a9ced8bd6cba37b9b05be74ef3ade96fa2ec54417fe0e02c8f412060(
    value: typing.Optional[ApprunnerServiceNetworkConfigurationEgressConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3a08b50cba93bc93fca1b234368197d0dcfe39ae7925ab9840a12ed621b670(
    *,
    is_publicly_accessible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d8cbe4ea07e3bc6e38df4e426f14586d95d07e8abe0e33268b005bea01f071(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e995c926a469429d2381f74552201a77939ccd49e1643a573286bfb146d26d71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d74a48150f6524c16308a41c3814e062c9c0a14ae8e33c0806cdfb1b6f19f96(
    value: typing.Optional[ApprunnerServiceNetworkConfigurationIngressConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c17d8426cc9107cf2ecd4ee4b9809c552f2002160d183ab67fadcac3457eece(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0f555843a68972b859182aaefe09c9271ece891b2a1dbcfaa6c36e6275cf7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f222c01525dde90194e37ab12a46856f2d4a3a3a751bf1383d977325152e15(
    value: typing.Optional[ApprunnerServiceNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dec349316c737ff840768a656046578a58212b40982d1e053fc08891dce9a30(
    *,
    observability_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    observability_configuration_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de01d98cbf88b922993632ede3969ef49c9785102cba7eb23fa3acea5f21ac72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a4295d9217b9c1ca03c27bee805caf9c5d831d02c2e0bd447480278e00cf92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a5328b156379b33362e44711a5130e310b6b2c947859f3ae19be772f864407(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1001793e2330745933a70727773513faea4e85a24269af2f7492cb0fbc6aa9(
    value: typing.Optional[ApprunnerServiceObservabilityConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b66bf5a977e30300e523b2ad3fc13fcee260045caaacf2b0eeafad9cdd107b1(
    *,
    authentication_configuration: typing.Optional[typing.Union[ApprunnerServiceSourceConfigurationAuthenticationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_deployments_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    code_repository: typing.Optional[typing.Union[ApprunnerServiceSourceConfigurationCodeRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    image_repository: typing.Optional[typing.Union[ApprunnerServiceSourceConfigurationImageRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45e17899938632ac3bb7ea8f33989f85d3151a1e9703fdf672bb48a4f644721(
    *,
    access_role_arn: typing.Optional[builtins.str] = None,
    connection_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f8db6cdaeb148235e6640a2673c4b1ce7a2e7fc55f69c35557de5f3b62683a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca511f56537fd3ab91c99441e030292a665fb9f87e2b07ed0006ac9a60c879db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8951e3aff3d01a5c4fc7bb2aac6a73b433aa51f116e1518d89babb95c28870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeaf3a0c271b0602711f14b28e29bfd8f166fdd577c63a2dc3aef2825e3f59de(
    value: typing.Optional[ApprunnerServiceSourceConfigurationAuthenticationConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd736118280a4378e2cf94ebac3cfac9b0bb0e024bac33f6149ccb9bc5432a44(
    *,
    repository_url: builtins.str,
    source_code_version: typing.Union[ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion, typing.Dict[builtins.str, typing.Any]],
    code_configuration: typing.Optional[typing.Union[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    source_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c7f6c12f3de45877b3456991e07e075c43c3ce556fad75c2db6a2bbe5f1aaf(
    *,
    configuration_source: builtins.str,
    code_configuration_values: typing.Optional[typing.Union[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c1f90b06912a16fe4af736ac45ec58c1ad167fb22ca44eb412af5111157443(
    *,
    runtime: builtins.str,
    build_command: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    runtime_environment_secrets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    runtime_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    start_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe15dbc1fb43612bf40412d0224240a3a5fca6153868d8b0a4d1b72c2006b24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec4565e36f538540a9a645ba6a48e05b3ae2aaf86c2be605b1ee5f279153a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f828173b6023d515cab77c3a258e894278f95474734e741e9ffc0bc7ea42e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c35d02bf5505df29d3ac79bf155995567a9c5c669a45b45f537cd84b6223c59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6384d2e936d429b5e8c261d8437ee327d7f470b62cbc34e9b39d8bc0307bf956(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0eb69b3513a6a64c4b4626ea376e154a5ca4e7cc75b7e178cb853bf024195b6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a14347daa470ab1a5375521691ed41499cbbc1d794254a4fbbf278da926668f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5640abf7750f5926dbd8e74ffc25ce467c19c87d53e1082e53377820096605c8(
    value: typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b60a73d853206f16abb03fde0444d5a98fd5480da8696b71c82e54be1bb61c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52f0d2e906ae037c2ba13d92eb8f4f26dbc88b682d8261f0835fc5d57ddac63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e332996fd4ae6d77bc1e95c62b30e1a8fe602230d23764bb9f5f439879b1a869(
    value: typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositoryCodeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af4bdb0eff8b0e221e5e48e48fca75bd30beb6e29ed116da0f0eb93f2baa4c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad2f491817436bbc919cbfc2188363c798157350a3d873ddb50fa58df840777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2dc0802ade1626983168fbba71bd523be8038073a52ad32916eed6aacfae21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468a10f597de73f16bc476d8cccca9c2a8c6aa845797bd14fb5193fbd083d868(
    value: typing.Optional[ApprunnerServiceSourceConfigurationCodeRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1eef1bee6dfcdd6b01783bf0de7387ad0dcb7db85b9299152a4a4793547ce2(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828bd595397c0a92d7b4e2609cddb996a82822e0fe7b48c86550d1863ee4b370(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1382fb5b7d55ac595148965393e10e83183e4dac04e3d4e65ab8944e8789e57e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f83ec7fd7acbdea7f24418f8048cf82d8110313e10e23a3b02ba85a42db8992(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56b213a8deaf0eaf7289299f45318690dd7dd02c631d59db6bc217eeab47dd2(
    value: typing.Optional[ApprunnerServiceSourceConfigurationCodeRepositorySourceCodeVersion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe556c20e37feebb502bef5a6fe8649ab6d0b1f7bbd17445c75327fe1e0e21a(
    *,
    image_identifier: builtins.str,
    image_repository_type: builtins.str,
    image_configuration: typing.Optional[typing.Union[ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851fa8e57f4bb9f207470d178f6a32ba340cf1a387167799316a28a47e22c34a(
    *,
    port: typing.Optional[builtins.str] = None,
    runtime_environment_secrets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    runtime_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    start_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a1628998c68af9b3dec79847c9955d0ad0e390663f3832c1a9ab2f15347e22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a015c60de9db7bd1e0d2f3c6071b5468c0f6afd146ae0ca9f31621a073779e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e5f080533fc0774b90c52e4be16d6f2427614025fcc60a5987d8df90c24bd5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522516a5c5913e81b83d6871944ec261097b6d34045553730d98d229d7a53f38(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6ec1edc852776adb6a42dcbcd84e9b74181d2193ad86d9be65e87fc1111a0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea01c0bdd5a30cd8067818bc0a2ef708fa422200037051d6f57398908c30b8ab(
    value: typing.Optional[ApprunnerServiceSourceConfigurationImageRepositoryImageConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265fb325bbca3f18d40fe6d15cd2ebcc1056a8c7e012a8fb651dd08a2bb12a50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e429208622f291a30f3bb7a900cef451e08f0fe9cd4b4c08193222e9318a9bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d27d500e6187d908d312fa5d76d513a02ecd1025f2b9e792203b32c9d80ab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8780cb04110d2e368fa874c110c590c2f6a7e67e8c517da91c88420b3634a3(
    value: typing.Optional[ApprunnerServiceSourceConfigurationImageRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d1068c43f9d1e52768c23cc3ed0b1eab7f38e546bcce32ed9a9a75a54a4684(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cf4a2208a4ec710ab5cc9ba18a08397a11abbe9b5bae50c9c5c01f68e4ba71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1b3119e39744a3c965173f6aba6dd79bf5ffde6f953ec46c828430f841b207(
    value: typing.Optional[ApprunnerServiceSourceConfiguration],
) -> None:
    """Type checking stubs"""
    pass
