r'''
# `aws_sagemaker_feature_group`

Refer to the Terraform Registry for docs: [`aws_sagemaker_feature_group`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group).
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


class SagemakerFeatureGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group aws_sagemaker_feature_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        event_time_feature_name: builtins.str,
        feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerFeatureGroupFeatureDefinition", typing.Dict[builtins.str, typing.Any]]]],
        feature_group_name: builtins.str,
        record_identifier_feature_name: builtins.str,
        role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        offline_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        online_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        throughput_config: typing.Optional[typing.Union["SagemakerFeatureGroupThroughputConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group aws_sagemaker_feature_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param event_time_feature_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#event_time_feature_name SagemakerFeatureGroup#event_time_feature_name}.
        :param feature_definition: feature_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#feature_definition SagemakerFeatureGroup#feature_definition}
        :param feature_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#feature_group_name SagemakerFeatureGroup#feature_group_name}.
        :param record_identifier_feature_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#record_identifier_feature_name SagemakerFeatureGroup#record_identifier_feature_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#role_arn SagemakerFeatureGroup#role_arn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#description SagemakerFeatureGroup#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#id SagemakerFeatureGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param offline_store_config: offline_store_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#offline_store_config SagemakerFeatureGroup#offline_store_config}
        :param online_store_config: online_store_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#online_store_config SagemakerFeatureGroup#online_store_config}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#region SagemakerFeatureGroup#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#tags SagemakerFeatureGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#tags_all SagemakerFeatureGroup#tags_all}.
        :param throughput_config: throughput_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#throughput_config SagemakerFeatureGroup#throughput_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759ddfac683ad88529cf42b2dd251676ff9dc1aad288d63d18f4c8fa6a579361)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerFeatureGroupConfig(
            event_time_feature_name=event_time_feature_name,
            feature_definition=feature_definition,
            feature_group_name=feature_group_name,
            record_identifier_feature_name=record_identifier_feature_name,
            role_arn=role_arn,
            description=description,
            id=id,
            offline_store_config=offline_store_config,
            online_store_config=online_store_config,
            region=region,
            tags=tags,
            tags_all=tags_all,
            throughput_config=throughput_config,
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
        '''Generates CDKTF code for importing a SagemakerFeatureGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerFeatureGroup to import.
        :param import_from_id: The id of the existing SagemakerFeatureGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerFeatureGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5cec4c6fd37ba445d07a48e1f79975d1f63a3ff47cd46f095ab27f4eac7ca1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFeatureDefinition")
    def put_feature_definition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerFeatureGroupFeatureDefinition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c277fdcf29477d8bab8b4bd83220bf16e4583449926374ebbfe37fb140de14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFeatureDefinition", [value]))

    @jsii.member(jsii_name="putOfflineStoreConfig")
    def put_offline_store_config(
        self,
        *,
        s3_storage_config: typing.Union["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig", typing.Dict[builtins.str, typing.Any]],
        data_catalog_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_glue_table_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        table_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_storage_config: s3_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#s3_storage_config SagemakerFeatureGroup#s3_storage_config}
        :param data_catalog_config: data_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#data_catalog_config SagemakerFeatureGroup#data_catalog_config}
        :param disable_glue_table_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#disable_glue_table_creation SagemakerFeatureGroup#disable_glue_table_creation}.
        :param table_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#table_format SagemakerFeatureGroup#table_format}.
        '''
        value = SagemakerFeatureGroupOfflineStoreConfig(
            s3_storage_config=s3_storage_config,
            data_catalog_config=data_catalog_config,
            disable_glue_table_creation=disable_glue_table_creation,
            table_format=table_format,
        )

        return typing.cast(None, jsii.invoke(self, "putOfflineStoreConfig", [value]))

    @jsii.member(jsii_name="putOnlineStoreConfig")
    def put_online_store_config(
        self,
        *,
        enable_online_store: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        ttl_duration: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfigTtlDuration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_online_store: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#enable_online_store SagemakerFeatureGroup#enable_online_store}.
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#security_config SagemakerFeatureGroup#security_config}
        :param storage_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#storage_type SagemakerFeatureGroup#storage_type}.
        :param ttl_duration: ttl_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#ttl_duration SagemakerFeatureGroup#ttl_duration}
        '''
        value = SagemakerFeatureGroupOnlineStoreConfig(
            enable_online_store=enable_online_store,
            security_config=security_config,
            storage_type=storage_type,
            ttl_duration=ttl_duration,
        )

        return typing.cast(None, jsii.invoke(self, "putOnlineStoreConfig", [value]))

    @jsii.member(jsii_name="putThroughputConfig")
    def put_throughput_config(
        self,
        *,
        provisioned_read_capacity_units: typing.Optional[jsii.Number] = None,
        provisioned_write_capacity_units: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param provisioned_read_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#provisioned_read_capacity_units SagemakerFeatureGroup#provisioned_read_capacity_units}.
        :param provisioned_write_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#provisioned_write_capacity_units SagemakerFeatureGroup#provisioned_write_capacity_units}.
        :param throughput_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#throughput_mode SagemakerFeatureGroup#throughput_mode}.
        '''
        value = SagemakerFeatureGroupThroughputConfig(
            provisioned_read_capacity_units=provisioned_read_capacity_units,
            provisioned_write_capacity_units=provisioned_write_capacity_units,
            throughput_mode=throughput_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putThroughputConfig", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOfflineStoreConfig")
    def reset_offline_store_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOfflineStoreConfig", []))

    @jsii.member(jsii_name="resetOnlineStoreConfig")
    def reset_online_store_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlineStoreConfig", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetThroughputConfig")
    def reset_throughput_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughputConfig", []))

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
    @jsii.member(jsii_name="featureDefinition")
    def feature_definition(self) -> "SagemakerFeatureGroupFeatureDefinitionList":
        return typing.cast("SagemakerFeatureGroupFeatureDefinitionList", jsii.get(self, "featureDefinition"))

    @builtins.property
    @jsii.member(jsii_name="offlineStoreConfig")
    def offline_store_config(
        self,
    ) -> "SagemakerFeatureGroupOfflineStoreConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOfflineStoreConfigOutputReference", jsii.get(self, "offlineStoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="onlineStoreConfig")
    def online_store_config(
        self,
    ) -> "SagemakerFeatureGroupOnlineStoreConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOnlineStoreConfigOutputReference", jsii.get(self, "onlineStoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="throughputConfig")
    def throughput_config(
        self,
    ) -> "SagemakerFeatureGroupThroughputConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupThroughputConfigOutputReference", jsii.get(self, "throughputConfig"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTimeFeatureNameInput")
    def event_time_feature_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTimeFeatureNameInput"))

    @builtins.property
    @jsii.member(jsii_name="featureDefinitionInput")
    def feature_definition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]]], jsii.get(self, "featureDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="featureGroupNameInput")
    def feature_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="offlineStoreConfigInput")
    def offline_store_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"], jsii.get(self, "offlineStoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="onlineStoreConfigInput")
    def online_store_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"], jsii.get(self, "onlineStoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="recordIdentifierFeatureNameInput")
    def record_identifier_feature_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordIdentifierFeatureNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

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
    @jsii.member(jsii_name="throughputConfigInput")
    def throughput_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupThroughputConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupThroughputConfig"], jsii.get(self, "throughputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd4fda9e8aa02afd04c802034eeebfd90869cda61bb8c133dc085ef2d66cab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventTimeFeatureName")
    def event_time_feature_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventTimeFeatureName"))

    @event_time_feature_name.setter
    def event_time_feature_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca0dee55c20199dfbf6ea9bf6c6b03a123d52a8f3799968632fe52f40fce4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventTimeFeatureName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureGroupName")
    def feature_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureGroupName"))

    @feature_group_name.setter
    def feature_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae6dbb2d20a6ed6fb99b835b3fe4ad808e00827a4af4ba28eca987fdd08ab30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd1cc715789c1c5b80f9986154eb2c23dfb0dfc3213b605c443f0d240487103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordIdentifierFeatureName")
    def record_identifier_feature_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordIdentifierFeatureName"))

    @record_identifier_feature_name.setter
    def record_identifier_feature_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10749ad1db76127c48e38f02693df155409beb262e930803e6b72da8a3951591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordIdentifierFeatureName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d68f04e618655f926df2d475d19a299da8bdc94d6cdc4785d03baa5c72bfbff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb49a04c069ffdb2250cf74e089122750dd567533c6cb40a79e4a7d29c713cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9439c73afe56f73ec40cb2d5686d5754b2122c186089632b0b4ccc739895260f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00bebeb9b0a65473f08b985eb4b34aca3c5aeda328933d8eb334f6706c3a150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "event_time_feature_name": "eventTimeFeatureName",
        "feature_definition": "featureDefinition",
        "feature_group_name": "featureGroupName",
        "record_identifier_feature_name": "recordIdentifierFeatureName",
        "role_arn": "roleArn",
        "description": "description",
        "id": "id",
        "offline_store_config": "offlineStoreConfig",
        "online_store_config": "onlineStoreConfig",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "throughput_config": "throughputConfig",
    },
)
class SagemakerFeatureGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        event_time_feature_name: builtins.str,
        feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerFeatureGroupFeatureDefinition", typing.Dict[builtins.str, typing.Any]]]],
        feature_group_name: builtins.str,
        record_identifier_feature_name: builtins.str,
        role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        offline_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        online_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        throughput_config: typing.Optional[typing.Union["SagemakerFeatureGroupThroughputConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param event_time_feature_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#event_time_feature_name SagemakerFeatureGroup#event_time_feature_name}.
        :param feature_definition: feature_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#feature_definition SagemakerFeatureGroup#feature_definition}
        :param feature_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#feature_group_name SagemakerFeatureGroup#feature_group_name}.
        :param record_identifier_feature_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#record_identifier_feature_name SagemakerFeatureGroup#record_identifier_feature_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#role_arn SagemakerFeatureGroup#role_arn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#description SagemakerFeatureGroup#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#id SagemakerFeatureGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param offline_store_config: offline_store_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#offline_store_config SagemakerFeatureGroup#offline_store_config}
        :param online_store_config: online_store_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#online_store_config SagemakerFeatureGroup#online_store_config}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#region SagemakerFeatureGroup#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#tags SagemakerFeatureGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#tags_all SagemakerFeatureGroup#tags_all}.
        :param throughput_config: throughput_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#throughput_config SagemakerFeatureGroup#throughput_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(offline_store_config, dict):
            offline_store_config = SagemakerFeatureGroupOfflineStoreConfig(**offline_store_config)
        if isinstance(online_store_config, dict):
            online_store_config = SagemakerFeatureGroupOnlineStoreConfig(**online_store_config)
        if isinstance(throughput_config, dict):
            throughput_config = SagemakerFeatureGroupThroughputConfig(**throughput_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ecbd19e0189d8e1fad5612b6c765588516fd4c27f462a8387dcfacdda528bdd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument event_time_feature_name", value=event_time_feature_name, expected_type=type_hints["event_time_feature_name"])
            check_type(argname="argument feature_definition", value=feature_definition, expected_type=type_hints["feature_definition"])
            check_type(argname="argument feature_group_name", value=feature_group_name, expected_type=type_hints["feature_group_name"])
            check_type(argname="argument record_identifier_feature_name", value=record_identifier_feature_name, expected_type=type_hints["record_identifier_feature_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument offline_store_config", value=offline_store_config, expected_type=type_hints["offline_store_config"])
            check_type(argname="argument online_store_config", value=online_store_config, expected_type=type_hints["online_store_config"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument throughput_config", value=throughput_config, expected_type=type_hints["throughput_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_time_feature_name": event_time_feature_name,
            "feature_definition": feature_definition,
            "feature_group_name": feature_group_name,
            "record_identifier_feature_name": record_identifier_feature_name,
            "role_arn": role_arn,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if offline_store_config is not None:
            self._values["offline_store_config"] = offline_store_config
        if online_store_config is not None:
            self._values["online_store_config"] = online_store_config
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if throughput_config is not None:
            self._values["throughput_config"] = throughput_config

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
    def event_time_feature_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#event_time_feature_name SagemakerFeatureGroup#event_time_feature_name}.'''
        result = self._values.get("event_time_feature_name")
        assert result is not None, "Required property 'event_time_feature_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def feature_definition(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]]:
        '''feature_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#feature_definition SagemakerFeatureGroup#feature_definition}
        '''
        result = self._values.get("feature_definition")
        assert result is not None, "Required property 'feature_definition' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]], result)

    @builtins.property
    def feature_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#feature_group_name SagemakerFeatureGroup#feature_group_name}.'''
        result = self._values.get("feature_group_name")
        assert result is not None, "Required property 'feature_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def record_identifier_feature_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#record_identifier_feature_name SagemakerFeatureGroup#record_identifier_feature_name}.'''
        result = self._values.get("record_identifier_feature_name")
        assert result is not None, "Required property 'record_identifier_feature_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#role_arn SagemakerFeatureGroup#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#description SagemakerFeatureGroup#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#id SagemakerFeatureGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def offline_store_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"]:
        '''offline_store_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#offline_store_config SagemakerFeatureGroup#offline_store_config}
        '''
        result = self._values.get("offline_store_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"], result)

    @builtins.property
    def online_store_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"]:
        '''online_store_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#online_store_config SagemakerFeatureGroup#online_store_config}
        '''
        result = self._values.get("online_store_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#region SagemakerFeatureGroup#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#tags SagemakerFeatureGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#tags_all SagemakerFeatureGroup#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def throughput_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupThroughputConfig"]:
        '''throughput_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#throughput_config SagemakerFeatureGroup#throughput_config}
        '''
        result = self._values.get("throughput_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupThroughputConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "collection_config": "collectionConfig",
        "collection_type": "collectionType",
        "feature_name": "featureName",
        "feature_type": "featureType",
    },
)
class SagemakerFeatureGroupFeatureDefinition:
    def __init__(
        self,
        *,
        collection_config: typing.Optional[typing.Union["SagemakerFeatureGroupFeatureDefinitionCollectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        collection_type: typing.Optional[builtins.str] = None,
        feature_name: typing.Optional[builtins.str] = None,
        feature_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param collection_config: collection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#collection_config SagemakerFeatureGroup#collection_config}
        :param collection_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#collection_type SagemakerFeatureGroup#collection_type}.
        :param feature_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#feature_name SagemakerFeatureGroup#feature_name}.
        :param feature_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#feature_type SagemakerFeatureGroup#feature_type}.
        '''
        if isinstance(collection_config, dict):
            collection_config = SagemakerFeatureGroupFeatureDefinitionCollectionConfig(**collection_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3708e32aca4025d07faae04c29b96dd85e77743383b4efe91d5c5b9b62618b)
            check_type(argname="argument collection_config", value=collection_config, expected_type=type_hints["collection_config"])
            check_type(argname="argument collection_type", value=collection_type, expected_type=type_hints["collection_type"])
            check_type(argname="argument feature_name", value=feature_name, expected_type=type_hints["feature_name"])
            check_type(argname="argument feature_type", value=feature_type, expected_type=type_hints["feature_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if collection_config is not None:
            self._values["collection_config"] = collection_config
        if collection_type is not None:
            self._values["collection_type"] = collection_type
        if feature_name is not None:
            self._values["feature_name"] = feature_name
        if feature_type is not None:
            self._values["feature_type"] = feature_type

    @builtins.property
    def collection_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfig"]:
        '''collection_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#collection_config SagemakerFeatureGroup#collection_config}
        '''
        result = self._values.get("collection_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfig"], result)

    @builtins.property
    def collection_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#collection_type SagemakerFeatureGroup#collection_type}.'''
        result = self._values.get("collection_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feature_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#feature_name SagemakerFeatureGroup#feature_name}.'''
        result = self._values.get("feature_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feature_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#feature_type SagemakerFeatureGroup#feature_type}.'''
        result = self._values.get("feature_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupFeatureDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionCollectionConfig",
    jsii_struct_bases=[],
    name_mapping={"vector_config": "vectorConfig"},
)
class SagemakerFeatureGroupFeatureDefinitionCollectionConfig:
    def __init__(
        self,
        *,
        vector_config: typing.Optional[typing.Union["SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vector_config: vector_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#vector_config SagemakerFeatureGroup#vector_config}
        '''
        if isinstance(vector_config, dict):
            vector_config = SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig(**vector_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d703cbcc479bbe2c9cc5df52d875149053c222d939b67bb86f5b4385bceac7)
            check_type(argname="argument vector_config", value=vector_config, expected_type=type_hints["vector_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vector_config is not None:
            self._values["vector_config"] = vector_config

    @builtins.property
    def vector_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig"]:
        '''vector_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#vector_config SagemakerFeatureGroup#vector_config}
        '''
        result = self._values.get("vector_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupFeatureDefinitionCollectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupFeatureDefinitionCollectionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionCollectionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bee9865340727c4a36a6b55a6bafef2398120a8d30e6039f4954f057946c1f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVectorConfig")
    def put_vector_config(
        self,
        *,
        dimension: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dimension: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#dimension SagemakerFeatureGroup#dimension}.
        '''
        value = SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig(
            dimension=dimension
        )

        return typing.cast(None, jsii.invoke(self, "putVectorConfig", [value]))

    @jsii.member(jsii_name="resetVectorConfig")
    def reset_vector_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVectorConfig", []))

    @builtins.property
    @jsii.member(jsii_name="vectorConfig")
    def vector_config(
        self,
    ) -> "SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfigOutputReference", jsii.get(self, "vectorConfig"))

    @builtins.property
    @jsii.member(jsii_name="vectorConfigInput")
    def vector_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig"], jsii.get(self, "vectorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d8975976eee919a11e67f1c55a17a927a56103a35223aa0fee32b6d76afade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig",
    jsii_struct_bases=[],
    name_mapping={"dimension": "dimension"},
)
class SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig:
    def __init__(self, *, dimension: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param dimension: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#dimension SagemakerFeatureGroup#dimension}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b573759d0e098c90c95e53cc73fb67259dc1caf92222000f75cb853ffabe0c54)
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dimension is not None:
            self._values["dimension"] = dimension

    @builtins.property
    def dimension(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#dimension SagemakerFeatureGroup#dimension}.'''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc6d39db2e71a3998d598457a4583582a851065517355d9206e45dff28d51eeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dimension"))

    @dimension.setter
    def dimension(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ff8929d28dbb5b96dbc0cc32208c098df2765828696488f4702f4d0cf5ff2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a486ea8650133dd2ea45268154e10c2936e659b661b7fc4fe9f53c6c90c2ce96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerFeatureGroupFeatureDefinitionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9761776edb35a303d6c9836d564190b2af5cd61d51f9c286327542bc25b9e787)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerFeatureGroupFeatureDefinitionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca517822789a782cfa287cf0376d8860aa8c2ae39e58d0899fcd3ad16a09984c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerFeatureGroupFeatureDefinitionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e779636b285a2e09c197df36222b8648b2373b4c6d05c6b91d4a6eebd917f18e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e5aefff722d940497bda3b30e071cbfc485edb1fd258dec31cdff5d7c23f9cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdcd2c3427d9bac6fc06fb6841304033bbb3d88dba688c2233ca83b14e75eda4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c4e6cb79d783a437de0505de6d9bc7e1103a3e5b2440eaf75d209f03890cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerFeatureGroupFeatureDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed13379807b6b96fb4c01dbb9e4dd4f2d5c0ebb89334be2f8c084eff8ad6bab1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCollectionConfig")
    def put_collection_config(
        self,
        *,
        vector_config: typing.Optional[typing.Union[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vector_config: vector_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#vector_config SagemakerFeatureGroup#vector_config}
        '''
        value = SagemakerFeatureGroupFeatureDefinitionCollectionConfig(
            vector_config=vector_config
        )

        return typing.cast(None, jsii.invoke(self, "putCollectionConfig", [value]))

    @jsii.member(jsii_name="resetCollectionConfig")
    def reset_collection_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectionConfig", []))

    @jsii.member(jsii_name="resetCollectionType")
    def reset_collection_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectionType", []))

    @jsii.member(jsii_name="resetFeatureName")
    def reset_feature_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureName", []))

    @jsii.member(jsii_name="resetFeatureType")
    def reset_feature_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureType", []))

    @builtins.property
    @jsii.member(jsii_name="collectionConfig")
    def collection_config(
        self,
    ) -> SagemakerFeatureGroupFeatureDefinitionCollectionConfigOutputReference:
        return typing.cast(SagemakerFeatureGroupFeatureDefinitionCollectionConfigOutputReference, jsii.get(self, "collectionConfig"))

    @builtins.property
    @jsii.member(jsii_name="collectionConfigInput")
    def collection_config_input(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig], jsii.get(self, "collectionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionTypeInput")
    def collection_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="featureNameInput")
    def feature_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureNameInput"))

    @builtins.property
    @jsii.member(jsii_name="featureTypeInput")
    def feature_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionType")
    def collection_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionType"))

    @collection_type.setter
    def collection_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f962251925549135744acc060aaedb30f7e767f6ccc9237a4740a5e839787b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureName")
    def feature_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureName"))

    @feature_name.setter
    def feature_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff0ee318a1c29493cd5c689bb857df50d1c88fee2d89af24d7aff084e86a189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureType")
    def feature_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureType"))

    @feature_type.setter
    def feature_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04548be8271dc2a85d7b896b0f66080950cb05436dc69003ea6bb217b4eaea70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerFeatureGroupFeatureDefinition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerFeatureGroupFeatureDefinition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerFeatureGroupFeatureDefinition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bfebb351b4a9576ea03a98b44caf73d3bf0a9ade89da393b636c782221f9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfig",
    jsii_struct_bases=[],
    name_mapping={
        "s3_storage_config": "s3StorageConfig",
        "data_catalog_config": "dataCatalogConfig",
        "disable_glue_table_creation": "disableGlueTableCreation",
        "table_format": "tableFormat",
    },
)
class SagemakerFeatureGroupOfflineStoreConfig:
    def __init__(
        self,
        *,
        s3_storage_config: typing.Union["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig", typing.Dict[builtins.str, typing.Any]],
        data_catalog_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_glue_table_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        table_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_storage_config: s3_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#s3_storage_config SagemakerFeatureGroup#s3_storage_config}
        :param data_catalog_config: data_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#data_catalog_config SagemakerFeatureGroup#data_catalog_config}
        :param disable_glue_table_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#disable_glue_table_creation SagemakerFeatureGroup#disable_glue_table_creation}.
        :param table_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#table_format SagemakerFeatureGroup#table_format}.
        '''
        if isinstance(s3_storage_config, dict):
            s3_storage_config = SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig(**s3_storage_config)
        if isinstance(data_catalog_config, dict):
            data_catalog_config = SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig(**data_catalog_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fcb64be6078c25fa3924d7db7f5324019c6ee8a8453b8b67f4d65702ff5db53)
            check_type(argname="argument s3_storage_config", value=s3_storage_config, expected_type=type_hints["s3_storage_config"])
            check_type(argname="argument data_catalog_config", value=data_catalog_config, expected_type=type_hints["data_catalog_config"])
            check_type(argname="argument disable_glue_table_creation", value=disable_glue_table_creation, expected_type=type_hints["disable_glue_table_creation"])
            check_type(argname="argument table_format", value=table_format, expected_type=type_hints["table_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_storage_config": s3_storage_config,
        }
        if data_catalog_config is not None:
            self._values["data_catalog_config"] = data_catalog_config
        if disable_glue_table_creation is not None:
            self._values["disable_glue_table_creation"] = disable_glue_table_creation
        if table_format is not None:
            self._values["table_format"] = table_format

    @builtins.property
    def s3_storage_config(
        self,
    ) -> "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig":
        '''s3_storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#s3_storage_config SagemakerFeatureGroup#s3_storage_config}
        '''
        result = self._values.get("s3_storage_config")
        assert result is not None, "Required property 's3_storage_config' is missing"
        return typing.cast("SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig", result)

    @builtins.property
    def data_catalog_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig"]:
        '''data_catalog_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#data_catalog_config SagemakerFeatureGroup#data_catalog_config}
        '''
        result = self._values.get("data_catalog_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig"], result)

    @builtins.property
    def disable_glue_table_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#disable_glue_table_creation SagemakerFeatureGroup#disable_glue_table_creation}.'''
        result = self._values.get("disable_glue_table_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def table_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#table_format SagemakerFeatureGroup#table_format}.'''
        result = self._values.get("table_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOfflineStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "catalog": "catalog",
        "database": "database",
        "table_name": "tableName",
    },
)
class SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig:
    def __init__(
        self,
        *,
        catalog: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#catalog SagemakerFeatureGroup#catalog}.
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#database SagemakerFeatureGroup#database}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#table_name SagemakerFeatureGroup#table_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bb3478f873c65b7587e4c05c1fea1bbd8d5633b88c6d8e6787739b69a91680)
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog is not None:
            self._values["catalog"] = catalog
        if database is not None:
            self._values["database"] = database
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#catalog SagemakerFeatureGroup#catalog}.'''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#database SagemakerFeatureGroup#database}.'''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#table_name SagemakerFeatureGroup#table_name}.'''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79d82d0d50ed1b35cc8dad76fa46205d2afff501f44b2d452138c73326e55c3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCatalog")
    def reset_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalog", []))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetTableName")
    def reset_table_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableName", []))

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f072f85a14fc33aeaa0d6aa97ce70fe94b87e7499a5e827e5c67ceb138019e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6804a3de6124a067f957bdf2cf3104400cab32dc9122bacb8f8d7e29fd830999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2bd5d801b57f9dbd5c5f10dbacb43ceaeeec9aebf4b3c05075f2ea87b8c5e24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2881b2fa67b2a4a68266f0216dfdbdcf6fdb6868760c75d499e6320029e1fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerFeatureGroupOfflineStoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7f486f82877c8a70d1bd1d7c422b2c62d9157263d5eebef7a157106b2d82465)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataCatalogConfig")
    def put_data_catalog_config(
        self,
        *,
        catalog: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#catalog SagemakerFeatureGroup#catalog}.
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#database SagemakerFeatureGroup#database}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#table_name SagemakerFeatureGroup#table_name}.
        '''
        value = SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig(
            catalog=catalog, database=database, table_name=table_name
        )

        return typing.cast(None, jsii.invoke(self, "putDataCatalogConfig", [value]))

    @jsii.member(jsii_name="putS3StorageConfig")
    def put_s3_storage_config(
        self,
        *,
        s3_uri: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
        resolved_output_s3_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#s3_uri SagemakerFeatureGroup#s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        :param resolved_output_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#resolved_output_s3_uri SagemakerFeatureGroup#resolved_output_s3_uri}.
        '''
        value = SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig(
            s3_uri=s3_uri,
            kms_key_id=kms_key_id,
            resolved_output_s3_uri=resolved_output_s3_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putS3StorageConfig", [value]))

    @jsii.member(jsii_name="resetDataCatalogConfig")
    def reset_data_catalog_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCatalogConfig", []))

    @jsii.member(jsii_name="resetDisableGlueTableCreation")
    def reset_disable_glue_table_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableGlueTableCreation", []))

    @jsii.member(jsii_name="resetTableFormat")
    def reset_table_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableFormat", []))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogConfig")
    def data_catalog_config(
        self,
    ) -> SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference:
        return typing.cast(SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference, jsii.get(self, "dataCatalogConfig"))

    @builtins.property
    @jsii.member(jsii_name="s3StorageConfig")
    def s3_storage_config(
        self,
    ) -> "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference", jsii.get(self, "s3StorageConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogConfigInput")
    def data_catalog_config_input(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig], jsii.get(self, "dataCatalogConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="disableGlueTableCreationInput")
    def disable_glue_table_creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableGlueTableCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3StorageConfigInput")
    def s3_storage_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig"], jsii.get(self, "s3StorageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tableFormatInput")
    def table_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="disableGlueTableCreation")
    def disable_glue_table_creation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableGlueTableCreation"))

    @disable_glue_table_creation.setter
    def disable_glue_table_creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a6461f940a4263796277d7d7e9183d6c85b35637aecaa1cb9156e4501e0954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableGlueTableCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableFormat")
    def table_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableFormat"))

    @table_format.setter
    def table_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ef31dff67ac5d283fdd850a2eb58a2618d77a0b1951cc8535bbc096f80cbec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7f2749e8354058996a4bb0b732a573870b8dc2ca7ec903172c185681358059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "s3_uri": "s3Uri",
        "kms_key_id": "kmsKeyId",
        "resolved_output_s3_uri": "resolvedOutputS3Uri",
    },
)
class SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig:
    def __init__(
        self,
        *,
        s3_uri: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
        resolved_output_s3_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#s3_uri SagemakerFeatureGroup#s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        :param resolved_output_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#resolved_output_s3_uri SagemakerFeatureGroup#resolved_output_s3_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2059def252f2990cd3f65274a7ad352297d02e50b4bde053567a32b5bd44cf38)
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument resolved_output_s3_uri", value=resolved_output_s3_uri, expected_type=type_hints["resolved_output_s3_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_uri": s3_uri,
        }
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if resolved_output_s3_uri is not None:
            self._values["resolved_output_s3_uri"] = resolved_output_s3_uri

    @builtins.property
    def s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#s3_uri SagemakerFeatureGroup#s3_uri}.'''
        result = self._values.get("s3_uri")
        assert result is not None, "Required property 's3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolved_output_s3_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#resolved_output_s3_uri SagemakerFeatureGroup#resolved_output_s3_uri}.'''
        result = self._values.get("resolved_output_s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cbbedfa9a3ef84fd4b76566af3da7011d01ed696a425249dd63c508012bacd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetResolvedOutputS3Uri")
    def reset_resolved_output_s3_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResolvedOutputS3Uri", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resolvedOutputS3UriInput")
    def resolved_output_s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resolvedOutputS3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd32e6361cc3ee19b987cee580d2066f0d26f116e68a332a4afe6b04764ff95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resolvedOutputS3Uri")
    def resolved_output_s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resolvedOutputS3Uri"))

    @resolved_output_s3_uri.setter
    def resolved_output_s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ceda7ab130b2f7d00e2913b569c3a3ae429c61ac3c38391415d3aeef1a21549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolvedOutputS3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38da8d3eff6a966ffa9d00eaf1be8252d6eee981293e97199033399009e93ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dcde056264ef584e2be6e528aa4456031f67eb256d65a365228a8ae37d70a13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_online_store": "enableOnlineStore",
        "security_config": "securityConfig",
        "storage_type": "storageType",
        "ttl_duration": "ttlDuration",
    },
)
class SagemakerFeatureGroupOnlineStoreConfig:
    def __init__(
        self,
        *,
        enable_online_store: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        ttl_duration: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfigTtlDuration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_online_store: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#enable_online_store SagemakerFeatureGroup#enable_online_store}.
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#security_config SagemakerFeatureGroup#security_config}
        :param storage_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#storage_type SagemakerFeatureGroup#storage_type}.
        :param ttl_duration: ttl_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#ttl_duration SagemakerFeatureGroup#ttl_duration}
        '''
        if isinstance(security_config, dict):
            security_config = SagemakerFeatureGroupOnlineStoreConfigSecurityConfig(**security_config)
        if isinstance(ttl_duration, dict):
            ttl_duration = SagemakerFeatureGroupOnlineStoreConfigTtlDuration(**ttl_duration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e4bd99a317a34fa83db350b8d5e5806f250e21e78105b206de5c0a4f9271dc)
            check_type(argname="argument enable_online_store", value=enable_online_store, expected_type=type_hints["enable_online_store"])
            check_type(argname="argument security_config", value=security_config, expected_type=type_hints["security_config"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument ttl_duration", value=ttl_duration, expected_type=type_hints["ttl_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_online_store is not None:
            self._values["enable_online_store"] = enable_online_store
        if security_config is not None:
            self._values["security_config"] = security_config
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if ttl_duration is not None:
            self._values["ttl_duration"] = ttl_duration

    @builtins.property
    def enable_online_store(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#enable_online_store SagemakerFeatureGroup#enable_online_store}.'''
        result = self._values.get("enable_online_store")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"]:
        '''security_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#security_config SagemakerFeatureGroup#security_config}
        '''
        result = self._values.get("security_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#storage_type SagemakerFeatureGroup#storage_type}.'''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl_duration(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfigTtlDuration"]:
        '''ttl_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#ttl_duration SagemakerFeatureGroup#ttl_duration}
        '''
        result = self._values.get("ttl_duration")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfigTtlDuration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOnlineStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOnlineStoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d3c8668077f298f58c64325e56f1e8f2d56bfec4b36e835ed606f7c6e1aacce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecurityConfig")
    def put_security_config(
        self,
        *,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        '''
        value = SagemakerFeatureGroupOnlineStoreConfigSecurityConfig(
            kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityConfig", [value]))

    @jsii.member(jsii_name="putTtlDuration")
    def put_ttl_duration(
        self,
        *,
        unit: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#unit SagemakerFeatureGroup#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#value SagemakerFeatureGroup#value}.
        '''
        value_ = SagemakerFeatureGroupOnlineStoreConfigTtlDuration(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putTtlDuration", [value_]))

    @jsii.member(jsii_name="resetEnableOnlineStore")
    def reset_enable_online_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableOnlineStore", []))

    @jsii.member(jsii_name="resetSecurityConfig")
    def reset_security_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfig", []))

    @jsii.member(jsii_name="resetStorageType")
    def reset_storage_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageType", []))

    @jsii.member(jsii_name="resetTtlDuration")
    def reset_ttl_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtlDuration", []))

    @builtins.property
    @jsii.member(jsii_name="securityConfig")
    def security_config(
        self,
    ) -> "SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference", jsii.get(self, "securityConfig"))

    @builtins.property
    @jsii.member(jsii_name="ttlDuration")
    def ttl_duration(
        self,
    ) -> "SagemakerFeatureGroupOnlineStoreConfigTtlDurationOutputReference":
        return typing.cast("SagemakerFeatureGroupOnlineStoreConfigTtlDurationOutputReference", jsii.get(self, "ttlDuration"))

    @builtins.property
    @jsii.member(jsii_name="enableOnlineStoreInput")
    def enable_online_store_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableOnlineStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigInput")
    def security_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"], jsii.get(self, "securityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="storageTypeInput")
    def storage_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlDurationInput")
    def ttl_duration_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfigTtlDuration"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfigTtlDuration"], jsii.get(self, "ttlDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableOnlineStore")
    def enable_online_store(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableOnlineStore"))

    @enable_online_store.setter
    def enable_online_store(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e193b9479e7033ba0fdedc775f16b8d683df2b5b2ce497824ae1f088dcbe4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableOnlineStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageType"))

    @storage_type.setter
    def storage_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1190dbe1f06a759e83742803dc50f6bc2aa267a7bb7df004ee1f1c28ef01fb5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerFeatureGroupOnlineStoreConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOnlineStoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d28383673829dabb920f57060406bedd4c4e4afd4019075496dcde611ec847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_id": "kmsKeyId"},
)
class SagemakerFeatureGroupOnlineStoreConfigSecurityConfig:
    def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece1f7c98528119ec91f699893743623e167a0424657a792973b1ebd685f4ba1)
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOnlineStoreConfigSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__920fde1e08d773f7fa404e1b413af5a1d7b13d46c6d0f45994ca4c6f07317e36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd86c04b0f79f6840f96f5bffff68564e3c8dc39f62095787a623b051e1c42c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb163269a8d968a8bf03e3577bee650ff3ed47ff6a300df257498967ace7d5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigTtlDuration",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class SagemakerFeatureGroupOnlineStoreConfigTtlDuration:
    def __init__(
        self,
        *,
        unit: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#unit SagemakerFeatureGroup#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#value SagemakerFeatureGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e1dbd704d9a6a636264504a0323850b678f22ac52dfdaf21868c8049c8e1c5)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if unit is not None:
            self._values["unit"] = unit
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#unit SagemakerFeatureGroup#unit}.'''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#value SagemakerFeatureGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOnlineStoreConfigTtlDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOnlineStoreConfigTtlDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigTtlDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e747608e1ffe4352391808f673f9f1637370b7025b43419b64fa3ff635a6fd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUnit")
    def reset_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnit", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59389dcdc51272d7be70697aa9dcb1b0f7410d1992879295522e9942ab9e1563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e520e6ff115e18d8db0cbdeea1318538d70a093065f89d2a7993cbf00aeebc60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOnlineStoreConfigTtlDuration]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOnlineStoreConfigTtlDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfigTtlDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963ee5d3d567dc8157cd068ef77f5adb790a2a48088fb0bae123dcb8fa91676a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupThroughputConfig",
    jsii_struct_bases=[],
    name_mapping={
        "provisioned_read_capacity_units": "provisionedReadCapacityUnits",
        "provisioned_write_capacity_units": "provisionedWriteCapacityUnits",
        "throughput_mode": "throughputMode",
    },
)
class SagemakerFeatureGroupThroughputConfig:
    def __init__(
        self,
        *,
        provisioned_read_capacity_units: typing.Optional[jsii.Number] = None,
        provisioned_write_capacity_units: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param provisioned_read_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#provisioned_read_capacity_units SagemakerFeatureGroup#provisioned_read_capacity_units}.
        :param provisioned_write_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#provisioned_write_capacity_units SagemakerFeatureGroup#provisioned_write_capacity_units}.
        :param throughput_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#throughput_mode SagemakerFeatureGroup#throughput_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4267760411c034d06ef033cb631561087ce6b2be4e15245f60b69ff61b732492)
            check_type(argname="argument provisioned_read_capacity_units", value=provisioned_read_capacity_units, expected_type=type_hints["provisioned_read_capacity_units"])
            check_type(argname="argument provisioned_write_capacity_units", value=provisioned_write_capacity_units, expected_type=type_hints["provisioned_write_capacity_units"])
            check_type(argname="argument throughput_mode", value=throughput_mode, expected_type=type_hints["throughput_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if provisioned_read_capacity_units is not None:
            self._values["provisioned_read_capacity_units"] = provisioned_read_capacity_units
        if provisioned_write_capacity_units is not None:
            self._values["provisioned_write_capacity_units"] = provisioned_write_capacity_units
        if throughput_mode is not None:
            self._values["throughput_mode"] = throughput_mode

    @builtins.property
    def provisioned_read_capacity_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#provisioned_read_capacity_units SagemakerFeatureGroup#provisioned_read_capacity_units}.'''
        result = self._values.get("provisioned_read_capacity_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_write_capacity_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#provisioned_write_capacity_units SagemakerFeatureGroup#provisioned_write_capacity_units}.'''
        result = self._values.get("provisioned_write_capacity_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_feature_group#throughput_mode SagemakerFeatureGroup#throughput_mode}.'''
        result = self._values.get("throughput_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupThroughputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupThroughputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupThroughputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae663b8f1f2c9d04263aa7f676f7e3439974316b0903a22456d7cd4defd08612)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProvisionedReadCapacityUnits")
    def reset_provisioned_read_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedReadCapacityUnits", []))

    @jsii.member(jsii_name="resetProvisionedWriteCapacityUnits")
    def reset_provisioned_write_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedWriteCapacityUnits", []))

    @jsii.member(jsii_name="resetThroughputMode")
    def reset_throughput_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughputMode", []))

    @builtins.property
    @jsii.member(jsii_name="provisionedReadCapacityUnitsInput")
    def provisioned_read_capacity_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedReadCapacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedWriteCapacityUnitsInput")
    def provisioned_write_capacity_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedWriteCapacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputModeInput")
    def throughput_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "throughputModeInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedReadCapacityUnits")
    def provisioned_read_capacity_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedReadCapacityUnits"))

    @provisioned_read_capacity_units.setter
    def provisioned_read_capacity_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276a82d4550aa57accf24261020aca791ad31a3f760e2a5ec5b1b985adb6c0e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedReadCapacityUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedWriteCapacityUnits")
    def provisioned_write_capacity_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedWriteCapacityUnits"))

    @provisioned_write_capacity_units.setter
    def provisioned_write_capacity_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958ca9f974e8bb6b38a2cc1228c6e7e48ae0269b896a4d040e7d4d866c8438e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedWriteCapacityUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughputMode")
    def throughput_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "throughputMode"))

    @throughput_mode.setter
    def throughput_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470bf183862df0b8b1b09b78ad2bdc73c25fbd4c991d18c83959a88009ba2105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughputMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerFeatureGroupThroughputConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupThroughputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupThroughputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c0bc0c31d86a5b1c331e53e18a6683639982ee2679464ad35eb1a6c9e1f991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SagemakerFeatureGroup",
    "SagemakerFeatureGroupConfig",
    "SagemakerFeatureGroupFeatureDefinition",
    "SagemakerFeatureGroupFeatureDefinitionCollectionConfig",
    "SagemakerFeatureGroupFeatureDefinitionCollectionConfigOutputReference",
    "SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig",
    "SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfigOutputReference",
    "SagemakerFeatureGroupFeatureDefinitionList",
    "SagemakerFeatureGroupFeatureDefinitionOutputReference",
    "SagemakerFeatureGroupOfflineStoreConfig",
    "SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig",
    "SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference",
    "SagemakerFeatureGroupOfflineStoreConfigOutputReference",
    "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig",
    "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference",
    "SagemakerFeatureGroupOnlineStoreConfig",
    "SagemakerFeatureGroupOnlineStoreConfigOutputReference",
    "SagemakerFeatureGroupOnlineStoreConfigSecurityConfig",
    "SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference",
    "SagemakerFeatureGroupOnlineStoreConfigTtlDuration",
    "SagemakerFeatureGroupOnlineStoreConfigTtlDurationOutputReference",
    "SagemakerFeatureGroupThroughputConfig",
    "SagemakerFeatureGroupThroughputConfigOutputReference",
]

publication.publish()

def _typecheckingstub__759ddfac683ad88529cf42b2dd251676ff9dc1aad288d63d18f4c8fa6a579361(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    event_time_feature_name: builtins.str,
    feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerFeatureGroupFeatureDefinition, typing.Dict[builtins.str, typing.Any]]]],
    feature_group_name: builtins.str,
    record_identifier_feature_name: builtins.str,
    role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    offline_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOfflineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    online_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    throughput_config: typing.Optional[typing.Union[SagemakerFeatureGroupThroughputConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fe5cec4c6fd37ba445d07a48e1f79975d1f63a3ff47cd46f095ab27f4eac7ca1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c277fdcf29477d8bab8b4bd83220bf16e4583449926374ebbfe37fb140de14(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerFeatureGroupFeatureDefinition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd4fda9e8aa02afd04c802034eeebfd90869cda61bb8c133dc085ef2d66cab3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca0dee55c20199dfbf6ea9bf6c6b03a123d52a8f3799968632fe52f40fce4be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae6dbb2d20a6ed6fb99b835b3fe4ad808e00827a4af4ba28eca987fdd08ab30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd1cc715789c1c5b80f9986154eb2c23dfb0dfc3213b605c443f0d240487103(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10749ad1db76127c48e38f02693df155409beb262e930803e6b72da8a3951591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d68f04e618655f926df2d475d19a299da8bdc94d6cdc4785d03baa5c72bfbff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb49a04c069ffdb2250cf74e089122750dd567533c6cb40a79e4a7d29c713cb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9439c73afe56f73ec40cb2d5686d5754b2122c186089632b0b4ccc739895260f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00bebeb9b0a65473f08b985eb4b34aca3c5aeda328933d8eb334f6706c3a150(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ecbd19e0189d8e1fad5612b6c765588516fd4c27f462a8387dcfacdda528bdd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_time_feature_name: builtins.str,
    feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerFeatureGroupFeatureDefinition, typing.Dict[builtins.str, typing.Any]]]],
    feature_group_name: builtins.str,
    record_identifier_feature_name: builtins.str,
    role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    offline_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOfflineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    online_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    throughput_config: typing.Optional[typing.Union[SagemakerFeatureGroupThroughputConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3708e32aca4025d07faae04c29b96dd85e77743383b4efe91d5c5b9b62618b(
    *,
    collection_config: typing.Optional[typing.Union[SagemakerFeatureGroupFeatureDefinitionCollectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    collection_type: typing.Optional[builtins.str] = None,
    feature_name: typing.Optional[builtins.str] = None,
    feature_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d703cbcc479bbe2c9cc5df52d875149053c222d939b67bb86f5b4385bceac7(
    *,
    vector_config: typing.Optional[typing.Union[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bee9865340727c4a36a6b55a6bafef2398120a8d30e6039f4954f057946c1f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d8975976eee919a11e67f1c55a17a927a56103a35223aa0fee32b6d76afade(
    value: typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b573759d0e098c90c95e53cc73fb67259dc1caf92222000f75cb853ffabe0c54(
    *,
    dimension: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6d39db2e71a3998d598457a4583582a851065517355d9206e45dff28d51eeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ff8929d28dbb5b96dbc0cc32208c098df2765828696488f4702f4d0cf5ff2c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a486ea8650133dd2ea45268154e10c2936e659b661b7fc4fe9f53c6c90c2ce96(
    value: typing.Optional[SagemakerFeatureGroupFeatureDefinitionCollectionConfigVectorConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9761776edb35a303d6c9836d564190b2af5cd61d51f9c286327542bc25b9e787(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca517822789a782cfa287cf0376d8860aa8c2ae39e58d0899fcd3ad16a09984c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e779636b285a2e09c197df36222b8648b2373b4c6d05c6b91d4a6eebd917f18e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5aefff722d940497bda3b30e071cbfc485edb1fd258dec31cdff5d7c23f9cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdcd2c3427d9bac6fc06fb6841304033bbb3d88dba688c2233ca83b14e75eda4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c4e6cb79d783a437de0505de6d9bc7e1103a3e5b2440eaf75d209f03890cc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed13379807b6b96fb4c01dbb9e4dd4f2d5c0ebb89334be2f8c084eff8ad6bab1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f962251925549135744acc060aaedb30f7e767f6ccc9237a4740a5e839787b0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff0ee318a1c29493cd5c689bb857df50d1c88fee2d89af24d7aff084e86a189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04548be8271dc2a85d7b896b0f66080950cb05436dc69003ea6bb217b4eaea70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bfebb351b4a9576ea03a98b44caf73d3bf0a9ade89da393b636c782221f9fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerFeatureGroupFeatureDefinition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fcb64be6078c25fa3924d7db7f5324019c6ee8a8453b8b67f4d65702ff5db53(
    *,
    s3_storage_config: typing.Union[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig, typing.Dict[builtins.str, typing.Any]],
    data_catalog_config: typing.Optional[typing.Union[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_glue_table_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    table_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bb3478f873c65b7587e4c05c1fea1bbd8d5633b88c6d8e6787739b69a91680(
    *,
    catalog: typing.Optional[builtins.str] = None,
    database: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d82d0d50ed1b35cc8dad76fa46205d2afff501f44b2d452138c73326e55c3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f072f85a14fc33aeaa0d6aa97ce70fe94b87e7499a5e827e5c67ceb138019e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6804a3de6124a067f957bdf2cf3104400cab32dc9122bacb8f8d7e29fd830999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bd5d801b57f9dbd5c5f10dbacb43ceaeeec9aebf4b3c05075f2ea87b8c5e24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2881b2fa67b2a4a68266f0216dfdbdcf6fdb6868760c75d499e6320029e1fe(
    value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f486f82877c8a70d1bd1d7c422b2c62d9157263d5eebef7a157106b2d82465(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a6461f940a4263796277d7d7e9183d6c85b35637aecaa1cb9156e4501e0954(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ef31dff67ac5d283fdd850a2eb58a2618d77a0b1951cc8535bbc096f80cbec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7f2749e8354058996a4bb0b732a573870b8dc2ca7ec903172c185681358059(
    value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2059def252f2990cd3f65274a7ad352297d02e50b4bde053567a32b5bd44cf38(
    *,
    s3_uri: builtins.str,
    kms_key_id: typing.Optional[builtins.str] = None,
    resolved_output_s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbbedfa9a3ef84fd4b76566af3da7011d01ed696a425249dd63c508012bacd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd32e6361cc3ee19b987cee580d2066f0d26f116e68a332a4afe6b04764ff95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ceda7ab130b2f7d00e2913b569c3a3ae429c61ac3c38391415d3aeef1a21549(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38da8d3eff6a966ffa9d00eaf1be8252d6eee981293e97199033399009e93ddc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dcde056264ef584e2be6e528aa4456031f67eb256d65a365228a8ae37d70a13(
    value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e4bd99a317a34fa83db350b8d5e5806f250e21e78105b206de5c0a4f9271dc(
    *,
    enable_online_store: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_config: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_type: typing.Optional[builtins.str] = None,
    ttl_duration: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfigTtlDuration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3c8668077f298f58c64325e56f1e8f2d56bfec4b36e835ed606f7c6e1aacce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e193b9479e7033ba0fdedc775f16b8d683df2b5b2ce497824ae1f088dcbe4c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1190dbe1f06a759e83742803dc50f6bc2aa267a7bb7df004ee1f1c28ef01fb5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d28383673829dabb920f57060406bedd4c4e4afd4019075496dcde611ec847(
    value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece1f7c98528119ec91f699893743623e167a0424657a792973b1ebd685f4ba1(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920fde1e08d773f7fa404e1b413af5a1d7b13d46c6d0f45994ca4c6f07317e36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd86c04b0f79f6840f96f5bffff68564e3c8dc39f62095787a623b051e1c42c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb163269a8d968a8bf03e3577bee650ff3ed47ff6a300df257498967ace7d5ed(
    value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e1dbd704d9a6a636264504a0323850b678f22ac52dfdaf21868c8049c8e1c5(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e747608e1ffe4352391808f673f9f1637370b7025b43419b64fa3ff635a6fd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59389dcdc51272d7be70697aa9dcb1b0f7410d1992879295522e9942ab9e1563(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e520e6ff115e18d8db0cbdeea1318538d70a093065f89d2a7993cbf00aeebc60(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963ee5d3d567dc8157cd068ef77f5adb790a2a48088fb0bae123dcb8fa91676a(
    value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfigTtlDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4267760411c034d06ef033cb631561087ce6b2be4e15245f60b69ff61b732492(
    *,
    provisioned_read_capacity_units: typing.Optional[jsii.Number] = None,
    provisioned_write_capacity_units: typing.Optional[jsii.Number] = None,
    throughput_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae663b8f1f2c9d04263aa7f676f7e3439974316b0903a22456d7cd4defd08612(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276a82d4550aa57accf24261020aca791ad31a3f760e2a5ec5b1b985adb6c0e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958ca9f974e8bb6b38a2cc1228c6e7e48ae0269b896a4d040e7d4d866c8438e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470bf183862df0b8b1b09b78ad2bdc73c25fbd4c991d18c83959a88009ba2105(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c0bc0c31d86a5b1c331e53e18a6683639982ee2679464ad35eb1a6c9e1f991(
    value: typing.Optional[SagemakerFeatureGroupThroughputConfig],
) -> None:
    """Type checking stubs"""
    pass
